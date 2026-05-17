DAMAGE_TYPE_KEYWORDS = {
    # ── Kinetic ────────────────────────────────────────────────────
    "Kinetic": [
        # Hybrid ammo
        "antimatter", "tungsten", "iron", "lead", "iridium",
        "null", "spike", "void",
        # Kinetic missile ammo
        "scourge", "javelin", "precision", "bloodclaw",
        # Hybrid turret type names (appear when ammo not logged separately)
        "electron blaster", "ion blaster", "neutron blaster",
        "blaster", "railgun", "rail gun", "gauss",
        # Kinetic drones
        "hammerhead", "wasp", "infiltrator",
        # Generic
        "kinetic",
    ],

    # ── Thermal ────────────────────────────────────────────────────
    "Thermal": [
        # Laser crystals (Thermal-leaning)
        "conflagration",
        # Thermal missile ammo
        "inferno", "piranha",
        # Thermal drones
        "vespa", "hobgoblin", "praetor",
        # Generic
        "thermal",
    ],

    # ── EM ─────────────────────────────────────────────────────────
    "EM": [
        # Laser crystals
        "multifrequency", "standard", "gamma", "x-ray", "radio",
        "microwave", "infrared", "ultraviolet",
        "gleam",    # T2 pulse (59% EM)
        "aurora",   # T2 beam  (75% EM)
        "scorch",   # faction pulse (~52% EM)
        # Laser turret type names
        "pulse laser", "beam laser", "laser",
        "megapulse", "tachyon", "pulse", "beam",
        # EM missile ammo
        "mjolnir",      # EM torpedo / heavy missile
        "thunderbolt",  # Minmatar EM light missile
        # EM drones
        "hornet", "acolyte", "warrior", "ogre",
        "bouncer", "curator", "garde",

        # ── NPC-specific energy weapon names ──────────────────────
        # Sansha's Nation NPCs use "particle cannon" turrets instead of
        # standard laser names. Examples seen in combat logs:
        #   "Anode Light Neutron Particle Cannon"   (Centii frigates)
        #   "Meson Assault Particle Cannon"          (Centum cruisers)
        #   "Baryon Proximity Assault Cannon"        (Centus battleships)
        #   "Gluon Scoped Assault Buster"            (various)
        #   "Mega Modulated Pulse Energy Cannon"     (battleships)
        "particle cannon", "energy cannon", "modulated pulse",
        "anode", "meson", "baryon", "gluon",
        # Other NPC energy weapon patterns
        "energy turret", "laser cannon", "energy beam",
        # Amarr / Blood Raiders NPC turrets use standard laser names
        # (matched by "laser", "pulse", "beam" above)

        # Generic fallback (space-padded to avoid partial matches in words)
        " em ",

        # ── NPC entity name prefixes (turrets don't log weapon names) ─────────
        # When a turret NPC hits you, EVE logs "Entity - Hits" with no weapon.
        # log_parser falls back to the entity name, so we match on NPC class prefixes.

        # Sansha's Nation (all ship classes deal primarily EM)
        "centii",       # frigates: Ravener, Scavenger, Slavehunter, Savage, Minion…
        "centior",      # destroyers: Devourer, Abomination, Horror, Monster…
        "centum",       # cruisers: Ravisher, Fiend, Mutant, Execrator…
        "centus",       # battleships: Plague, Beast, Savage, Tyrant…
        "centatis",     # officer spawns
        "sansha",       # covers Sansha Sentry Gun, Tower Sentry Sansha, etc.

        # Blood Raiders (energy weapons, EM/Thermal — EM dominant)
        "corpii",       # frigates: Raider, Diviner, Worshiper, Engraver…
        "corpior",      # destroyers: Devoter, Converter, Templar…
        "corpus",       # cruisers: Monsignor, Pope, Patriarch, Archbishop…
        "corpatis",     # officer spawns
        "dark blood",   # officer/faction prefix
    ],

    # ── Explosive ──────────────────────────────────────────────────
    "Explosive": [
        # Projectile ammo
        "depleted uranium", "emp", "proton", "carbonized lead",
        "titanium sabot", "barrage", "hail", "quake", "tremor",
        # Explosive missile ammo
        "nova",       # Nova = Explosive (was wrongly Kinetic before)
        "sabretooth", # Minmatar explosive light missile
        # Projectile turret type names
        "autocannon", "auto cannon", "artillery",
        # Explosive drones
        "valkyrie", "berserker",
        # Triglavian
        "entropic disintegrator", "disintegrator",
        # Generic
        "explosive",

        # ── NPC entity name prefixes (turrets, no weapon logged) ──────────────
        # Angel Cartel (autocannons, primarily Explosive)
        "gistii",       # frigates: Smasher, Trasher, Arrogator…
        "gistior",      # destroyers: Haunter, Defiler, Seeker…
        "gistum",       # cruisers: Breaker, Marauder, Mutilator…
        "gistatis",     # officer spawns
        "arch gistii", "arch gistior", "arch gistum",   # arch-class
    ],
}

# Build a flat list sorted by keyword length descending so longer phrases match first.
# WARNING: Do NOT add generic missile TYPE names (torpedo, cruise missile, heavy missile,
# rocket, etc.) — they are longer than specific ammo-prefix names and shadow them.
# Example: "cruise missile" (14 chars) would beat "nova" (4 chars) for "Nova Cruise Missile".
# EVE combat logs always include the specific ammo name, so the prefix alone is sufficient.
_SORTED_KEYWORDS = sorted(
    ((kw.lower(), dtype) for dtype, kws in DAMAGE_TYPE_KEYWORDS.items() for kw in kws),
    key=lambda x: -len(x[0]),
)


def get_damage_type(weapon: str) -> str:
    """Return damage type string for a given weapon/ammo name."""
    lower = weapon.lower()
    for kw, dtype in _SORTED_KEYWORDS:
        if kw in lower:
            return dtype
    return "Unknown"
