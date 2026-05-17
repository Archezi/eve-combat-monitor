import re
from datetime import datetime
from dataclasses import dataclass
from typing import Optional

from damage_types import get_damage_type

_HTML_RE = re.compile(r"<[^>]+>")

# Timestamp + combat prefix (matched after HTML stripping)
_PREFIX_RE = re.compile(
    r"\[\s*(\d{4}\.\d{2}\.\d{2}\s+\d{2}:\d{2}:\d{2})\s*\]\s*\(combat\)\s+(\d+)\s+(to|from)\s+(.+)$",
    re.IGNORECASE,
)

# Entity portion: "Name[CORP](Full Name)" or "Name[CORP]" or plain "Name"
_ENTITY_RE = re.compile(
    r"^(.*?)(?:\[.*?\])?(?:\(.*?\))?\s*-\s*(.*)$"
)


@dataclass
class CombatEvent:
    timestamp: datetime
    damage: int
    direction: str      # "to" or "from"
    entity: str
    weapon: str
    damage_type: str
    is_critical: bool


def _parse_tail(tail: str):
    """
    Parse everything after 'to|from '.
    Returns (entity, weapon, result_word) or None.

    Formats:
      Guristas Kyoukan[GURI](Guristas Kyoukan) - Antimatter Charge M - Hits
      Guristas Ratter[GURI](Guristas Ratter) - hits you
      Some Target - Weapon - Critical
    """
    # Split on ' - ' keeping at most 3 parts
    parts = [p.strip() for p in tail.split(' - ')]
    if len(parts) < 2:
        return None

    # Strip entity corporation/alliance brackets
    raw_entity = parts[0]
    entity_clean = re.sub(r'\[.*?\]', '', raw_entity)   # remove [CORP]
    entity_clean = re.sub(r'\(.*?\)', '', entity_clean)  # remove (Full Name)
    entity_clean = entity_clean.strip()

    if len(parts) == 2:
        # Could be "weapon - result" or "result you" (no weapon)
        weapon = parts[1]
        result = parts[1]
    else:
        weapon = parts[1]
        result = parts[-1]

    return entity_clean, weapon, result


def parse_line(line: str) -> Optional[CombatEvent]:
    """Parse a single log line. Returns CombatEvent or None."""
    if "(combat)" not in line:
        return None

    # EVE wraps log content in HTML color/font tags — strip them first
    line = _HTML_RE.sub("", line)

    m = _PREFIX_RE.search(line)
    if not m:
        return None

    ts_str   = m.group(1).strip()
    dmg_str  = m.group(2)
    direction = m.group(3).lower()
    tail     = m.group(4)

    parsed = _parse_tail(tail)
    if not parsed:
        return None

    entity, weapon, result = parsed

    try:
        ts = datetime.strptime(ts_str, "%Y.%m.%d %H:%M:%S")
    except ValueError:
        return None

    return CombatEvent(
        timestamp=ts,
        damage=int(dmg_str),
        direction=direction,
        entity=entity,
        weapon=weapon,
        damage_type=get_damage_type(weapon),
        is_critical="critical" in result.lower(),
    )
