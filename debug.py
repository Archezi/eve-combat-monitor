"""Run this to diagnose why combat events aren't showing up."""
import sys
from pathlib import Path

print("=== EVE Combat Monitor Diagnostics ===\n")

# 1. Find log directory
candidates = [
    Path.home() / "Documents" / "EVE" / "logs" / "Gamelogs",
    Path.home() / "OneDrive" / "Documents" / "EVE" / "logs" / "Gamelogs",
    Path.home() / "Documents" / "EVE" / "logs" / "Combatlogs",
    Path.home() / "OneDrive" / "Documents" / "EVE" / "logs" / "Combatlogs",
]

found_dir = None
for c in candidates:
    exists = c.exists()
    print(f"{'[FOUND]' if exists else '[    ]'} {c}")
    if exists and not found_dir:
        found_dir = c

print()

if not found_dir:
    print("ERROR: No EVE log directory found. Is EVE installed?")
    sys.exit(1)

# 2. List files in found dir
files = sorted(found_dir.glob("*.txt"), key=lambda p: p.stat().st_mtime, reverse=True)
print(f"Log files in {found_dir} ({len(files)} total):")
for f in files[:5]:
    size = f.stat().st_size
    print(f"  {f.name}  ({size} bytes)")

print()

if not files:
    print("ERROR: No .txt log files found. Start EVE and enter space.")
    sys.exit(1)

latest = files[0]
print(f"Monitoring: {latest.name}\n")

# 3. Try to read last 30 lines and parse
print("=== Last 30 lines of log file ===")
for enc in ["utf-8", "utf-16", "latin-1"]:
    try:
        with open(latest, "r", encoding=enc, errors="replace") as f:
            all_lines = f.readlines()
        print(f"(encoding works: {enc}, total lines: {len(all_lines)})")
        for line in all_lines[-30:]:
            print(repr(line[:120]))
        break
    except Exception as e:
        print(f"  {enc} failed: {e}")

print()

# 4. Try parser on those lines
print("=== Parsed combat events (last 30 lines) ===")
sys.path.insert(0, str(Path(__file__).parent))
try:
    from log_parser import parse_line
    combat_count = 0
    for line in all_lines[-30:]:
        ev = parse_line(line)
        if ev:
            combat_count += 1
            print(f"  OK  {ev.direction:4s} | {ev.damage:6d} | {ev.entity[:25]:25s} | {ev.weapon[:20]:20s} | {ev.damage_type} | crit={ev.is_critical}")
    if combat_count == 0:
        print("  No combat lines found in last 30 lines.")
        print("  (Are you currently in combat? Check if any lines contain '(combat)')")
        combat_lines = [l for l in all_lines if "(combat)" in l]
        print(f"\n  Total lines with '(combat)' in entire file: {len(combat_lines)}")
        if combat_lines:
            print("  Sample combat line:")
            print("  " + repr(combat_lines[-1][:150]))
except Exception as e:
    print(f"  Parser error: {e}")
    import traceback; traceback.print_exc()

input("\nPress Enter to exit...")
