"""Match EVE NPC entity names to faction intelligence entries."""

from npc_data import NPC_FACTIONS, RARE_SPAWN_KEYWORDS

# Pre-sort ship-name entries by key length descending for greedy (longest) match first
_SHIP_LOOKUP: list = []
for _fn, _fd in NPC_FACTIONS.items():
    for _sn, _sd in _fd.get("ship_names", {}).items():
        _SHIP_LOOKUP.append((_sn.lower(), _fn, _fd, _sd))
_SHIP_LOOKUP.sort(key=lambda x: -len(x[0]))

_RARE_LOWER = [k.lower() for k in RARE_SPAWN_KEYWORDS]


def match_npc(entity_name: str):
    """
    Match entity_name against faction and ship databases.
    Returns (faction_name, faction_data, ship_data) — ship_data may be None.
    Returns (None, None, None) if no match.
    """
    name_lower = entity_name.lower()

    # 1. Specific ship names (longest match wins)
    for ship_lower, faction_name, faction_data, ship_data in _SHIP_LOOKUP:
        if ship_lower in name_lower:
            return faction_name, faction_data, ship_data

    # 2. Faction keyword matching
    for faction_name, faction_data in NPC_FACTIONS.items():
        for kw in faction_data.get("name_keywords", []):
            if kw.lower() in name_lower:
                return faction_name, faction_data, None

    return None, None, None
