"""NPC entity name → primary damage type lookup.

Used as a fallback when EVE combat logs omit the weapon name (turret NPCs
log 'Entity - Hits' with no weapon; missile NPCs log the missile name).

Sources:
  wiki.eveuniversity.org/NPC_damage_types
  wiki.eveuniversity.org/NPC_naming_conventions

Each faction has a standard naming convention by ship class:
  Frigate / Destroyer / Cruiser / Battlecruiser / Battleship / Elite / Officer

We check entity names for these substrings (longest match first) to infer
the primary damage type without needing the weapon name in the log.
"""

# (substring, primary_damage_type)
# Listed grouped by faction for readability; sorted at module load time.
_ENTRIES = [

    # ── Angel Cartel ─────────────────────────────────────────────────────────
    # Damage: Explosive 62% / Kinetic 22%   Source: wiki.eveuniversity.org
    # Naming: Gistii (frig) / Gistior (dest) / Gistum (cru) / Gistatis (BC) / Gist (BS)
    # Elite: Arch Gistii / Arch Gistior / Arch Gistum / Arch Gist
    # Officer/Faction: Domination
    ("arch gistior",     "Explosive"),
    ("arch gistum",      "Explosive"),
    ("arch gistii",      "Explosive"),
    ("arch gist",        "Explosive"),
    ("domination",       "Explosive"),
    ("gistatis",         "Explosive"),
    ("gistior",          "Explosive"),
    ("gistum",           "Explosive"),
    ("gistii",           "Explosive"),
    ("gist",             "Explosive"),   # battleships: Gist Thunder, Gist Warlord…

    # ── Sansha's Nation ───────────────────────────────────────────────────────
    # Damage: EM 53% / Thermal 47%   Source: wiki.eveuniversity.org
    # Naming: Centii (frig) / Centior (dest) / Centum (cru) / Centatis (BC) / Centus (BS)
    # Elite: Loyal Centii / Loyal Centior…
    # Officer/Faction: True Sansha
    # Structures: Sansha Sentry Gun, Tower Sentry Sansha
    ("true sansha",      "EM"),
    ("centatis",         "EM"),
    ("centior",          "EM"),
    ("centum",           "EM"),
    ("centus",           "EM"),
    ("centii",           "EM"),
    ("loyal",            "EM"),    # elite prefix: Loyal Centii…
    ("sansha",           "EM"),    # sentry guns, structures, general fallback

    # ── Blood Raiders ─────────────────────────────────────────────────────────
    # Damage: EM 50% / Thermal 48%   Source: wiki.eveuniversity.org
    # Naming: Corpii (frig) / Corpior (dest) / Corpum (cru) / Corpatis (BC) / Corpus (BS)
    # Elite: Elder Corpii / Elder Corpus…
    # Officer/Faction: Dark Blood
    ("dark blood",       "EM"),
    ("corpatis",         "EM"),
    ("corpior",          "EM"),
    ("corpus",           "EM"),
    ("corpum",           "EM"),
    ("corpii",           "EM"),
    ("elder",            "EM"),    # elite prefix: Elder Corpii…

    # ── Guristas Pirates ──────────────────────────────────────────────────────
    # Damage: Kinetic 79% / Thermal 18%   Source: wiki.eveuniversity.org
    # Naming: Pithi (frig) / Pithior (dest) / Pithum (cru) / Pithatis (BC) / Pith (BS)
    # Elite: Dire Pithi / Dire Pithum…
    # Officer/Faction: Dread Guristas
    ("dread guristas",   "Kinetic"),
    ("pithatis",         "Kinetic"),
    ("pithior",          "Kinetic"),
    ("pithum",           "Kinetic"),
    ("pithi",            "Kinetic"),
    ("dire",             "Kinetic"),   # elite prefix: Dire Pithi…
    ("pith",             "Kinetic"),   # battleships: Pith Exterminator, Pith Eliminator…

    # ── Serpentis ─────────────────────────────────────────────────────────────
    # Damage: Thermal 55% / Kinetic 45%   Source: wiki.eveuniversity.org
    # Naming: Coreli (frig) / Corelior (dest) / Corelum (cru) / Corelatis (BC) / Core (BS)
    # Elite: Guardian Serpentis
    # Officer/Faction: Shadow Serpentis
    ("shadow serpentis", "Thermal"),
    ("guardian serpentis","Thermal"),
    ("corelatis",        "Thermal"),
    ("corelior",         "Thermal"),
    ("corelum",          "Thermal"),
    ("coreli",           "Thermal"),
    ("core",             "Thermal"),   # battleships: Core Admiral, Core Grand Admiral…

    # ── Rogue Drones ──────────────────────────────────────────────────────────
    # Damage: Kinetic / Thermal primarily (varies; some EM/Explosive)
    # Source: wiki.eveuniversity.org — "deal the damage of railgun ammunition"
    # Naming: Alvi (frig) / Alvior (dest) / Alvum (cru) / Alvatis (BC) / Alvus (BS)
    # Elite: Strain   Officer: Sentient
    ("sentient",         "Kinetic"),   # officer rogue drone
    ("alvatis",          "Kinetic"),
    ("alvior",           "Kinetic"),
    ("strain",           "Kinetic"),   # elite rogue drone prefix
    ("alvum",            "Kinetic"),
    ("alvus",            "Kinetic"),
    ("alvi",             "Kinetic"),

    # ── Triglavian Collective ──────────────────────────────────────────────────
    # Damage: Thermal 60% / Explosive 40%   Source: wiki.eveuniversity.org
    # Ship names: Damavik (frig) / Kikimora (dest) / Vedmak (cru) / Leshak (BS)
    # Modifiers: Starving / Liminal / Emerging / Anchoring / Renewing / Striking
    ("anchoring",        "Thermal"),
    ("renewing",         "Thermal"),
    ("striking",         "Thermal"),
    ("emerging",         "Thermal"),
    ("starving",         "Thermal"),
    ("liminal",          "Thermal"),
    ("kikimora",         "Thermal"),
    ("damavik",          "Thermal"),
    ("vedmak",           "Thermal"),
    ("leshak",           "Thermal"),

    # ── Empire / CONCORD mission NPCs ─────────────────────────────────────────
    ("caldari navy",     "Kinetic"),
    ("caldari state",    "Kinetic"),
    ("gallente",         "Kinetic"),
    ("minmatar",         "Explosive"),
    ("amarr",            "EM"),        # Amarr mission rats deal EM/Thermal

    # ── Mordu's Legion ────────────────────────────────────────────────────────
    # Damage: Kinetic 70% / Thermal 30%
    ("mordu",            "Kinetic"),
]

# Sort longest substring first so more specific names win over short prefixes
_ENTRIES.sort(key=lambda x: -len(x[0]))


def lookup(entity_name: str) -> str | None:
    """Return primary damage type for an NPC entity name, or None if not known."""
    lower = entity_name.lower()
    for substring, dtype in _ENTRIES:
        if substring in lower:
            return dtype
    return None
