DAMAGE_TYPE_KEYWORDS = {
    "Kinetic": [
        "antimatter", "tungsten", "iron", "lead", "iridium", "mjolnir",
        "caldari navy antimatter", "nova", "scourge", "javelin", "spike", "null",
        "titanium sabot",
    ],
    "Thermal": [
        "plutonium", "helium", "hydrogen", "inferno", "conflagration",
        "gleam", "aurora", "phased plasma",
    ],
    "EM": [
        "multifrequency", "standard", "gamma", "x-ray", "radio", "microwave",
        "infrared", "ultraviolet", "megapulse", "tachyon", "pulse", "beam",
    ],
    "Explosive": [
        "depleted uranium", "emp", "proton", "carbonized lead",
        "quake", "tremor", "barrage", "hail",
    ],
}

# Build a flat list sorted by keyword length descending so longer phrases match first
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
