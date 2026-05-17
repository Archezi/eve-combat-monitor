import os
import sys
import time
import threading
import glob as glob_mod
from collections import deque
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import webview
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from log_parser import parse_line, CombatEvent
from npc_matcher import match_npc

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _get_log_dir() -> Optional[Path]:
    candidates = [
        Path.home() / "OneDrive" / "Documents" / "EVE" / "logs" / "Gamelogs",
        Path.home() / "Documents" / "EVE" / "logs" / "Gamelogs",
    ]
    # Also check OneDrive variants with org suffixes (e.g. "OneDrive - Corp")
    for p in Path.home().iterdir() if Path.home().exists() else []:
        if p.is_dir() and p.name.lower().startswith("onedrive"):
            candidates.append(p / "Documents" / "EVE" / "logs" / "Gamelogs")
    for c in candidates:
        if c.exists():
            return c
    return None


def _latest_log(log_dir: Path) -> Optional[Path]:
    files = list(log_dir.glob("*.txt"))
    if not files:
        return None
    return max(files, key=lambda p: p.stat().st_mtime)


# ---------------------------------------------------------------------------
# State / API
# ---------------------------------------------------------------------------

DAMAGE_TYPES = ["EM", "Thermal", "Kinetic", "Explosive", "Unknown"]
DPS_WINDOW = 10.0       # seconds
CONSISTENCY_WINDOW = 60  # last N hits
AUTO_RESET_IDLE = 60.0  # seconds of no combat before auto-reset


class SessionState:
    def __init__(self):
        self._lock = threading.Lock()
        self.reset()

    def reset(self):
        with self._lock if hasattr(self, "_lock") else _nullctx():
            self._out_hits: deque = deque()         # (timestamp, damage, dtype, is_crit) — 10s window
            self._in_hits: deque = deque()          # same
            self._out_all_dmg: list = []            # all-time damage values for consistency calc
            self._out_type_totals: dict = {t: 0 for t in DAMAGE_TYPES}  # all-time
            self._in_type_totals: dict = {t: 0 for t in DAMAGE_TYPES}   # all-time
            self._recent_crits: deque = deque(maxlen=20)
            self._targets: dict = {}          # name → {out, in_}
            self._start = time.time()
            self._last_event_ts: Optional[float] = None  # wall-clock time of most recent event
            self._paper_dps: Optional[float] = None
            # NPC intel
            self._faction_hits: dict = {}     # faction_name → hit count
            self._faction_data: dict = {}     # faction_name → faction_data dict
            self._faction_last: dict = {}     # faction_name → last seen timestamp
            self._rare_alerts: dict = {}      # entity_name → alert dict (deduped)

    def add_event(self, ev: CombatEvent):
        # Use wall-clock time, not the EVE log timestamp (EVE logs UTC,
        # but datetime.timestamp() assumes local time — causes immediate pruning).
        ts = time.time()
        with self._lock:
            self._last_event_ts = ts
            bucket = self._out_hits if ev.direction == "to" else self._in_hits
            bucket.append((ts, ev.damage, ev.damage_type, ev.is_critical))
            type_totals = self._out_type_totals if ev.direction == "to" else self._in_type_totals
            key = ev.damage_type if ev.damage_type in type_totals else "Unknown"
            type_totals[key] += ev.damage
            if ev.direction == "to":
                self._out_all_dmg.append(ev.damage)

            if ev.is_critical:
                self._recent_crits.append({
                    "amount": ev.damage,
                    "direction": ev.direction,
                    "timestamp": ts,
                })

            # NPC intel — match entities from both directions (attacker or target)
            faction_name, faction_data, ship_data = match_npc(ev.entity)
            if faction_name:
                self._faction_hits[faction_name] = self._faction_hits.get(faction_name, 0) + 1
                self._faction_data[faction_name] = faction_data
                self._faction_last[faction_name] = ts
            if ship_data and ship_data.get("threat") in ("rare", "elite", "boss"):
                if ev.entity not in self._rare_alerts:
                    self._rare_alerts[ev.entity] = {
                        "name": ev.entity,
                        "threat": ship_data["threat"],
                        "notes": ship_data.get("notes", ""),
                        "ts": ts,
                    }

            t = self._targets.setdefault(ev.entity, {"out": 0, "in_": 0})
            if ev.direction == "to":
                t["out"] += ev.damage
            else:
                t["in_"] += ev.damage

    def set_paper_dps(self, value: float):
        with self._lock:
            self._paper_dps = float(value)

    def clear_paper_dps(self):
        with self._lock:
            self._paper_dps = None

    def check_auto_reset(self):
        """Reset the session if no combat event has been seen for AUTO_RESET_IDLE seconds."""
        with self._lock:
            if self._last_event_ts is None:
                return
            if time.time() - self._last_event_ts <= AUTO_RESET_IDLE:
                return
            has_data = bool(self._targets)
        if has_data:
            self.reset()

    def get_state(self) -> dict:
        now = time.time()
        cutoff = now - DPS_WINDOW

        with self._lock:
            # Prune old entries
            while self._out_hits and self._out_hits[0][0] < cutoff:
                self._out_hits.popleft()
            while self._in_hits and self._in_hits[0][0] < cutoff:
                self._in_hits.popleft()

            out_dps = sum(h[1] for h in self._out_hits) / DPS_WINDOW
            in_dps = sum(h[1] for h in self._in_hits) / DPS_WINDOW
            # Per-type incoming DPS from the live window
            _in_type_raw: dict = {}
            for _, dmg, dtype, _ in self._in_hits:
                _in_type_raw[dtype] = _in_type_raw.get(dtype, 0) + dmg
            in_dps_by_type = {k: round(v / DPS_WINDOW, 1) for k, v in _in_type_raw.items()}
            out_type_snap = dict(self._out_type_totals)
            in_type_snap = dict(self._in_type_totals)
            paper = self._paper_dps

        def type_pcts(totals):
            grand = sum(totals.values()) or 1
            return {k: round(v / grand * 100, 1) for k, v in totals.items()}

        out_by_type = type_pcts(out_type_snap)
        in_by_type = type_pcts(in_type_snap)

        # Application
        if paper and paper > 0:
            app_pct = min(out_dps / paper * 100, 150.0)
            app_mode = "paper"
        else:
            # Consistency mode: use all-time outgoing hits
            with self._lock:
                consistency_hits = list(self._out_all_dmg)
            if len(consistency_hits) >= 2:
                top_n = max(1, len(consistency_hits) // 20)  # top 5%
                sorted_hits = sorted(consistency_hits, reverse=True)
                top_mean = sum(sorted_hits[:top_n]) / top_n
                mean_all = sum(consistency_hits) / len(consistency_hits)
                app_pct = min(mean_all / top_mean * 100, 100.0) if top_mean else 0.0
            else:
                app_pct = 0.0
            app_mode = "consistency"

        with self._lock:
            crits = list(self._recent_crits)
            targets_snap = dict(self._targets)
            session_sec = int(now - self._start)
            total_out = sum(v["out"] for v in self._targets.values())
            total_in = sum(v["in_"] for v in self._targets.values())
            paper_snap = self._paper_dps
            # NPC intel snapshot — most recently seen faction is "current"
            faction_hits_snap = dict(self._faction_hits)
            faction_data_snap = dict(self._faction_data)
            faction_last_snap = dict(self._faction_last)
            rare_snap = list(self._rare_alerts.values())

        if faction_last_snap:
            current_faction = max(faction_last_snap, key=faction_last_snap.get)
            faction_info = faction_data_snap.get(current_faction)
            if faction_info:
                faction_info = {k: v for k, v in faction_info.items() if k != "ship_names"}
        else:
            current_faction = None
            faction_info = None

        rare_snap.sort(key=lambda x: -x["ts"])

        return {
            "outgoing_dps": round(out_dps, 1),
            "incoming_dps": round(in_dps, 1),
            "paper_dps": paper_snap,
            "application_pct": round(app_pct, 1),
            "application_mode": app_mode,
            "outgoing_by_type": out_by_type,
            "incoming_by_type": in_by_type,
            "session_seconds": session_sec,
            "total_outgoing": int(total_out),
            "total_incoming": int(total_in),
            "incoming_dps_by_type": in_dps_by_type,
            "recent_crits": crits[-5:],
            "current_faction": current_faction,
            "faction_info": faction_info,
            "rare_alerts": rare_snap[:6],
        }


class _nullctx:
    def __enter__(self): return self
    def __exit__(self, *a): pass


# ---------------------------------------------------------------------------
# API exposed to JS
# ---------------------------------------------------------------------------

class Api:
    def __init__(self, state: SessionState, window_ref, tailer_ref):
        self._state = state
        self._win = window_ref      # list so we can set later
        self._tailer = tailer_ref   # list so we can set later

    def get_state(self):
        s = self._state.get_state()
        tailer = self._tailer[0] if self._tailer else None
        s["monitored_file"] = tailer._file.name if (tailer and tailer._file) else None
        return s

    def set_paper_dps(self, value):
        try:
            self._state.set_paper_dps(float(value))
        except (ValueError, TypeError):
            pass

    def clear_paper_dps(self):
        self._state.clear_paper_dps()

    def reset_session(self):
        self._state.reset()

    def _hwnd(self):
        import ctypes
        hwnd = ctypes.windll.user32.FindWindowW(None, "EVE Combat Monitor")
        return hwnd

    def set_always_on_top(self, value: bool):
        try:
            import ctypes
            u32 = ctypes.windll.user32
            hwnd = self._hwnd()
            if not hwnd:
                return
            GWL_EXSTYLE   = -20
            WS_EX_LAYERED = 0x00080000
            LWA_ALPHA     = 0x00000002
            HWND_TOPMOST   = -1
            HWND_NOTOPMOST = -2
            SWP_NOMOVE     = 0x0002
            SWP_NOSIZE     = 0x0001
            ex = u32.GetWindowLongW(hwnd, GWL_EXSTYLE)
            if value:
                u32.SetWindowLongW(hwnd, GWL_EXSTYLE, ex | WS_EX_LAYERED)
                u32.SetLayeredWindowAttributes(hwnd, 0, 217, LWA_ALPHA)
                u32.SetWindowPos(hwnd, HWND_TOPMOST, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE)
            else:
                u32.SetWindowLongW(hwnd, GWL_EXSTYLE, ex & ~WS_EX_LAYERED)
                u32.SetWindowPos(hwnd, HWND_NOTOPMOST, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE)
        except Exception:
            pass

    def set_window_alpha(self, alpha):
        try:
            import ctypes
            u32 = ctypes.windll.user32
            hwnd = self._hwnd()
            if not hwnd:
                return
            GWL_EXSTYLE   = -20
            WS_EX_LAYERED = 0x00080000
            LWA_ALPHA     = 0x00000002
            ex = u32.GetWindowLongW(hwnd, GWL_EXSTYLE)
            if not (ex & WS_EX_LAYERED):
                u32.SetWindowLongW(hwnd, GWL_EXSTYLE, ex | WS_EX_LAYERED)
            u32.SetLayeredWindowAttributes(hwnd, 0, int(max(0, min(255, alpha))), LWA_ALPHA)
        except Exception:
            pass

    def pick_log_dir(self):
        wins = self._win
        if wins:
            result = wins[0].create_file_dialog(
                webview.FOLDER_DIALOG, directory=str(Path.home())
            )
            if result:
                return result[0]
        return None


# ---------------------------------------------------------------------------
# Log file tailer / watcher
# ---------------------------------------------------------------------------

class LogTailer:
    def __init__(self, state: SessionState):
        self._state = state
        self._file: Optional[Path] = None
        self._pos = 0
        self._lock = threading.Lock()

    def set_file(self, path: Path):
        with self._lock:
            self._file = path
            try:
                self._pos = path.stat().st_size  # tail from current end
            except OSError:
                self._pos = 0

    def tail(self):
        with self._lock:
            f = self._file
            pos = self._pos
        if not f:
            return
        try:
            size = f.stat().st_size
        except OSError:
            return
        if size < pos:
            pos = 0  # file was truncated/rotated
        if size == pos:
            return
        try:
            with open(f, "r", encoding="utf-8", errors="replace") as fh:
                fh.seek(pos)
                for line in fh:
                    ev = parse_line(line)
                    if ev:
                        self._state.add_event(ev)
                pos = fh.tell()
        except OSError:
            return
        with self._lock:
            self._pos = pos


class LogDirWatcher(FileSystemEventHandler):
    """Watchdog handler — switches to newest log file when one is created."""
    def __init__(self, tailer: LogTailer, log_dir: Path):
        super().__init__()
        self._tailer = tailer
        self._log_dir = log_dir

    def on_created(self, event):
        if event.is_directory:
            return
        p = Path(event.src_path)
        if p.suffix.lower() == ".txt" and p.parent == self._log_dir:
            time.sleep(0.5)
            self._tailer.set_file(p)


# ---------------------------------------------------------------------------
# Load UI HTML
# ---------------------------------------------------------------------------

def _load_html() -> str:
    here = Path(__file__).parent
    html_path = here / "ui" / "index.html"
    with open(html_path, "r", encoding="utf-8") as f:
        return f.read()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    state = SessionState()
    window_holder = []  # filled after window creation
    tailer_holder = []  # filled below

    log_dir = _get_log_dir()
    tailer = LogTailer(state)
    tailer_holder.append(tailer)

    api = Api(state, window_holder, tailer_holder)

    no_log_dir = log_dir is None

    if log_dir:
        latest = _latest_log(log_dir)
        if latest:
            tailer.set_file(latest)

    def poll_loop():
        while True:
            tailer.tail()
            state.check_auto_reset()
            time.sleep(0.25)

    t = threading.Thread(target=poll_loop, daemon=True)
    t.start()

    # Set up watchdog if we have a log dir
    observer = None
    if log_dir:
        handler = LogDirWatcher(tailer, log_dir)
        observer = Observer()
        observer.schedule(handler, str(log_dir), recursive=False)
        observer.start()

    html = _load_html()

    # Inject runtime config into the page
    config_script = f"<script>window._CFG = {{ noLogDir: {'true' if no_log_dir else 'false'} }};</script>"
    html = html.replace("</head>", config_script + "</head>", 1)

    window = webview.create_window(
        "EVE Combat Monitor",
        html=html,
        js_api=api,
        width=620,
        height=860,
        resizable=True,
        background_color='#0d0d0f',
        on_top=True,
    )
    window_holder.append(window)

    webview.start(debug=False)

    if observer:
        observer.stop()
        observer.join()


if __name__ == "__main__":
    main()
