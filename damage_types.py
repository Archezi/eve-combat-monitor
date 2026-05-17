DAMAGE_TYPE_KEYWORDS = {
    # ── Kinetic ────────────────────────────────────────────────────
    "Kinetic": [
        # Hybrid ammo (specific names)
        "antimatter", "tungsten", "iron", "lead", "iridium",
        "null", "spike", "void",
        # Kinetic missile ammo
        "scourge", "javelin", "precision", "bloodclaw",
        # Hybrid turret TYPE names (turret name in log, not ammo)
        "electron blaster", "ion blaster", "neutron blaster",
        "blaster", "railgun", "rail gun", "gauss",
        # Kinetic drones (by name)
        "hammerhead", "wasp", "infiltrator",
        # Generic fallback
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
        # Generic fallback
        "thermal",
    ],
    # ── EM ─────────────────────────────────────────────────────────
    "EM": [
        # Laser crystals
        "multifrequency", "standard", "gamma", "x-ray", "radio",
        "microwave", "infrared", "ultraviolet",
        "gleam",    # T2 pulse (59% EM)  — was incorrectly Thermal
        "aurora",   # T2 beam  (75% EM)  — was incorrectly Thermal
        "scorch",   # faction pulse (~52% EM)
        # Laser turret type names
        "pulse laser", "beam laser", "laser",
        "megapulse", "tachyon", "pulse", "beam",
        # EM missile ammo
        "mjolnir",      # EM torpedo/cruise — was incorrectly Kinetic
        "thunderbolt",  # Minmatar EM light missile
        # EM drones
        "hornet", "acolyte", "warrior", "ogre",
        "bouncer", "curator", "garde",  # sentry drones
        # Generic fallback (space-padded to avoid matching "rem", "item" etc.)
        " em ",
    ],
    # ── Explosive ──────────────────────────────────────────────────
    "Explosive": [
        # Projectile ammo
        "depleted uranium", "emp", "proton", "carbonized lead",
        "titanium sabot", "barrage", "hail", "quake", "tremor",
        # Explosive missile ammo
        "nova",       # was incorrectly Kinetic — Nova = Explosive
        "sabretooth", # Minmatar explosive light missile
        # Projectile turret type names
        "autocannon", "auto cannon", "artillery",
        # Explosive drones
        "valkyrie", "berserker",
        # Triglavian (Thermal/Explosive; Explosive is secondary, Thermal primary)
        "entropic disintegrator", "disintegrator",
        # Generic fallback
        "explosive",
    ],
}

# Build a flat list sorted by keyword length descending so longer phrases match first.
# NOTE: Do NOT add generic missile TYPE names here (torpedo, cruise missile, heavy missile,
# rocket, etc.) — they are longer than specific ammo names and would wrongly shadow them.
# e.g. "cruise missile" (14 chars) would beat "nova" (4 chars) for "Nova Cruise Missile".
# In EVE combat logs the specific ammo name always appears (Nova, Scourge, Mjolnir, Inferno).
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
