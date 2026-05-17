"""EVE Online NPC faction intelligence database."""

THREAT_COLORS = {
    "normal": "#888780",
    "elite":  "#EF9F27",
    "rare":   "#7F77DD",
    "boss":   "#D85A30",
}

NPC_FACTIONS = {

    # ── KNOWN SPACE ─────────────────────────────────────────────────

    "Angel Cartel": {
        "weak_to": ["Explosive", "Kinetic"],
        "deals":   ["Explosive", "Kinetic"],
        "ew":      ["Target Painters"],
        "tank":    "shield",
        "name_keywords": ["Angel", "Gist", "Arch Gist", "Gistii", "Gistum", "Gisti",
                          "Domination", "Cartel"],
        "notes": "Shield tank. TP increases your sig radius. Explosive primary.",
        "ship_names": {
            "Cynabal":    {"threat": "rare",  "notes": "Fast, web, neut. Faction cruiser."},
            "Machariel":  {"threat": "rare",  "notes": "Faction battleship. High alpha. Very fast."},
            "Dramiel":    {"threat": "rare",  "notes": "Faction frigate. Web + scram."},
            "Daredevil":  {"threat": "rare",  "notes": "Faction frigate. High DPS web."},
            "Vangel":     {"threat": "rare",  "notes": "Faction cruiser. Rare escalation."},
            "Domination": {"threat": "elite", "notes": "Commander. Higher HP/DPS. Faction loot."},
            "Arch Gist":  {"threat": "elite", "notes": "Elite battleship. Higher DPS."},
        },
    },

    "Blood Raiders": {
        "weak_to": ["EM", "Thermal"],
        "deals":   ["EM", "Thermal"],
        "ew":      ["Energy Neutralizers", "Tracking Disruptors"],
        "tank":    "armor",
        "name_keywords": ["Corpii", "Corpum", "Corpus", "Corp", "Elder", "Blood Raider", "Covenant"],
        "notes": "Armor tank. Neuts drain cap — watch active tank. TDs hurt turrets.",
        "ship_names": {
            "Cruor":     {"threat": "rare",  "notes": "Heavy neuts + web. Kills cap-reliant ships."},
            "Ashimmu":   {"threat": "rare",  "notes": "Faction cruiser. Heavy neuts and web."},
            "Bhaalgorn": {"threat": "rare",  "notes": "Faction battleship. Extreme neuts."},
            "Elder":     {"threat": "elite", "notes": "Commander spawn. Higher EHP. Faction loot."},
        },
    },

    "Guristas Pirates": {
        "weak_to": ["Kinetic", "Thermal"],
        "deals":   ["Kinetic", "Thermal"],
        "ew":      ["ECM"],
        "tank":    "shield",
        "name_keywords": ["Guristas", "Pith", "Pithi", "Pithum", "Pithatis", "Pithior"],
        "notes": "Shield tank. Kinetic primary. ECM breaks target locks.",
        "ship_names": {
            "Dread Guristas":        {"threat": "rare",  "notes": "Commander. Drops faction loot."},
            "Worm":                  {"threat": "rare",  "notes": "Faction frigate. Drone boat."},
            "Gila":                  {"threat": "rare",  "notes": "Faction cruiser. High drone DPS."},
            "Rattlesnake":           {"threat": "rare",  "notes": "Faction battleship. Very high EHP."},
            "Pith Exterminator":     {"threat": "elite", "notes": "Elite battleship. High missile DPS."},
            "Pith Obliterator":      {"threat": "elite", "notes": "Elite battleship. High missile DPS."},
        },
    },

    "Sansha's Nation": {
        "weak_to": ["EM", "Thermal"],
        "deals":   ["EM", "Thermal"],
        "ew":      ["Tracking Disruptors", "Warp Scramblers"],
        "tank":    "armor",
        "name_keywords": ["Sansha", "Centii", "Centum", "Centus", "True Sansha", "Slave", "Devoted"],
        "notes": "Armor tank. TDs reduce turret effectiveness. EM primary.",
        "ship_names": {
            "True Sansha": {"threat": "rare",  "notes": "Commander variant. Faction loot."},
            "Phantasm":    {"threat": "rare",  "notes": "Faction cruiser. Fast. EM/Thermal."},
            "Nightmare":   {"threat": "rare",  "notes": "Faction battleship. High laser DPS."},
            "Succubus":    {"threat": "rare",  "notes": "Faction frigate. Fast tackle."},
        },
    },

    "Serpentis": {
        "weak_to": ["Kinetic", "Thermal"],
        "deals":   ["Thermal", "Kinetic"],
        "ew":      ["Sensor Dampeners"],
        "tank":    "armor",
        "name_keywords": ["Serpentis", "Corelii", "Corelum", "Core", "Guardian", "Coreli"],
        "notes": "Armor tank. Sensor Damps reduce lock range — get close.",
        "ship_names": {
            "Shadow Serpentis": {"threat": "rare",  "notes": "Commander. Drops faction loot."},
            "Vigilant":         {"threat": "rare",  "notes": "90% web. Devastating at close range."},
            "Vindicator":       {"threat": "rare",  "notes": "Faction battleship. 90% web. Extreme DPS."},
            "Daredevil":        {"threat": "rare",  "notes": "Faction frigate. 90% web."},
            "Guardian Vexor":   {"threat": "elite", "notes": "Elite cruiser. High drone DPS."},
        },
    },

    "Rogue Drones": {
        "weak_to": ["EM", "Thermal"],
        "deals":   ["varies"],
        "ew":      [],
        "tank":    "varies",
        "name_keywords": ["Drone", "Strain", "Decimator", "Render", "Dismantler",
                          "Destructor", "Ripper", "Hunter", "Sentry", "Infester",
                          "Termite", "Splinter", "Bomber", "Swarm", "Overmind",
                          "Fieldweaver", "Plateforger", "Snarecaster"],
        "notes": "EM/Thermal generally best. Resists vary by hull class.",
        "ship_names": {
            "Overmind":        {"threat": "boss",   "notes": "Drone BS. Extreme HP. Weak to Explosive."},
            "Alvus":           {"threat": "elite",  "notes": "Drone battleship. High EHP."},
            "Fieldweaver":     {"threat": "normal", "notes": "Repair drone — kill to stop reps."},
            "Plateforger":     {"threat": "normal", "notes": "Repair drone — kill to stop reps."},
            "Snarecaster":     {"threat": "normal", "notes": "Webifier drone — prioritize."},
            "Strain Splinter": {"threat": "normal", "notes": "Fast tackle drone."},
        },
    },

    "Mordu's Legion": {
        "weak_to": ["Kinetic", "EM"],
        "deals":   ["Kinetic", "Thermal"],
        "ew":      [],
        "tank":    "shield",
        "name_keywords": ["Mordu", "Legion"],
        "notes": "Active shield tank. Kinetic primary. Long point kiters.",
        "ship_names": {
            "Orthrus":  {"threat": "rare", "notes": "Faction cruiser. Long point, fast."},
            "Barghest": {"threat": "rare", "notes": "Faction battleship. High missile DPS."},
            "Garmur":   {"threat": "rare", "notes": "Faction frigate. Long point kiter."},
        },
    },

    "Sleepers": {
        "weak_to": ["omni"],
        "deals":   ["omni"],
        "ew":      ["Energy Neutralizers", "Warp Scramblers", "Stasis Webifiers"],
        "tank":    "omni",
        "name_keywords": ["Sleeper", "Awakened", "Emergent", "Circadian", "Seeker",
                          "Upholder", "Lancer", "Preserver", "Ephialtes", "Lucid",
                          "Warped", "Ancient"],
        "notes": "Omni resists — no hole. Kill logi first. All damage types equal.",
        "ship_names": {
            "Sleepless Guardian": {"threat": "boss",  "notes": "Sleeper battleship. Extreme HP/DPS."},
            "Sleepless Escort":   {"threat": "elite", "notes": "Sleeper cruiser. High DPS."},
            "Awakened Escort":    {"threat": "elite", "notes": "Cruiser. Webs and neuts."},
            "Emergent Escort":    {"threat": "normal","notes": "Sleeper frigate. Fast tackle."},
        },
    },

    "Drifters": {
        "weak_to": ["omni"],
        "deals":   ["omni"],
        "ew":      ["Warp Scramblers", "Energy Neutralizers", "Stasis Webifiers"],
        "tank":    "omni",
        "name_keywords": ["Drifter", "Karybdis", "Tyrannos", "Autothysian", "Liminal Drifter"],
        "notes": "SUPERWEAPON on overshield break — move away immediately! Break overshield first.",
        "ship_names": {
            "Karybdis Tyrannos": {"threat": "boss",  "notes": "Superweapon on overshield break. Spiral in."},
            "Awakened Drifter":  {"threat": "elite", "notes": "460-820 DPS. Superweapon on overshield."},
            "Autothysian Lancer":{"threat": "normal","notes": "Drifter frigate. Targets drones."},
        },
    },

    # ── ABYSSAL ──────────────────────────────────────────────────────

    "Triglavian Collective": {
        "weak_to": ["Explosive", "Thermal"],
        "deals":   ["Thermal", "Explosive"],
        "ew":      ["Stasis Webifiers", "Warp Scramblers", "Energy Neutralizers",
                    "Tracking Disruptors", "Sensor Dampeners", "Target Painters"],
        "tank":    "armor",
        "name_keywords": ["Damavik", "Kikimora", "Vedmak", "Rodiva", "Drekavac",
                          "Leshak", "Swarmer", "Vila", "Triglavian", "Liminal",
                          "Renewing", "Anchoring", "Tangling", "Harrowing",
                          "Blinding", "Starving", "Ghosting", "Striking",
                          "Perun", "Veles", "Svarog"],
        "notes": "Damage RAMPS — don't let them settle. Kill Rodiva (logi) FIRST.",
        "ship_names": {
            "Leshak":   {"threat": "boss",  "notes": "BS. Extreme ramping DPS. Top threat."},
            "Drekavac": {"threat": "elite", "notes": "BC. High ramping DPS."},
            "Rodiva":   {"threat": "elite", "notes": "LOGI — Remote Armor Repair. Kill FIRST."},
            "Vedmak":   {"threat": "elite", "notes": "Cruiser. High ramping DPS."},
            "Kikimora": {"threat": "normal","notes": "Destroyer. Kill quickly."},
            "Damavik":  {"threat": "normal","notes": "Frigate. Various EWAR by prefix."},
        },
    },

    "CONCORD": {
        "weak_to": ["Kinetic", "Thermal"],
        "deals":   ["Thermal", "Explosive", "EM", "Kinetic"],
        "ew":      [],
        "tank":    "omni",
        "name_keywords": ["Marshal", "Arrester", "Pacifier", "Enforcer",
                          "Skybreaker", "Stormbringer", "Thunderchild"],
        "notes": "Omni resists. Very high DPS. Never stop moving.",
        "ship_names": {
            "Thunderchild": {"threat": "boss",  "notes": "15s fire rate but 2000+ alpha. EM/Kinetic."},
            "Marshal":      {"threat": "boss",  "notes": "RHLM fire rate. Thermal missiles. Deadly."},
            "Skybreaker":   {"threat": "elite", "notes": "EDENCOM cruiser. High EM damage."},
            "Stormbringer": {"threat": "elite", "notes": "EDENCOM cruiser. Kinetic damage."},
        },
    },

    "Sansha Nation (Abyssal)": {
        "weak_to": ["EM", "Thermal"],
        "deals":   ["EM", "Thermal"],
        "ew":      ["Energy Neutralizers", "Tracking Disruptors", "Warp Scramblers"],
        "tank":    "armor",
        "name_keywords": ["Devoted Knight", "Devoted Corruptor", "Devoted Executioner", "Devoted"],
        "notes": "Abyssal Sansha. Slow speed, heavy EWAR. Long range preferred.",
        "ship_names": {
            "Devoted Knight":      {"threat": "elite", "notes": "Weak EM then Explosive (not Thermal here)."},
            "Devoted Corruptor":   {"threat": "elite", "notes": "EM/Thermal weakness. Neuts."},
            "Devoted Executioner": {"threat": "normal","notes": "Frigate class. Tackle + DPS."},
        },
    },

    "Angel Cartel (Abyssal)": {
        "weak_to": ["Explosive", "Kinetic"],
        "deals":   ["Explosive", "Kinetic"],
        "ew":      ["Target Painters"],
        "tank":    "shield",
        "name_keywords": ["Lucifer", "Gist Angel", "Arch Angel"],
        "notes": "Same profile as known-space Angels. TP increases your sig radius.",
        "ship_names": {
            "Lucifer Fury":  {"threat": "elite", "notes": "Cap Neutralizer variant. Very dangerous."},
            "Lucifer Echo":  {"threat": "elite", "notes": "Web + Scramble variant."},
            "Elite Lucifer": {"threat": "elite", "notes": "Higher EHP and DPS."},
        },
    },

    "Rogue Drones (Abyssal)": {
        "weak_to": ["EM", "Thermal"],
        "deals":   ["varies"],
        "ew":      ["Stasis Webifiers"],
        "tank":    "varies",
        "name_keywords": ["Strain", "Splinter", "Decimating", "Infester", "Render",
                          "Swarm", "Fieldweaver", "Plateforger", "Snarecaster"],
        "notes": "EM/Thermal best. Abyssal Overmind: armor tank, weakest to Explosive.",
        "ship_names": {
            "Abyssal Overmind": {"threat": "boss",  "notes": "Extreme HP and range. Weakest to Explosive."},
            "Fieldweaver":      {"threat": "normal","notes": "Repair drone — kill to stop reps."},
            "Snarecaster":      {"threat": "normal","notes": "Webifier drone — prioritize."},
        },
    },

    # ── EMPIRE / MISSIONS ────────────────────────────────────────────

    "Amarr Empire": {
        "weak_to": ["EM", "Thermal"],
        "deals":   ["EM", "Thermal"],
        "ew":      ["Energy Neutralizers", "Tracking Disruptors"],
        "tank":    "armor",
        "name_keywords": ["Imperial", "Amarr", "Divine", "Crusader", "Templar", "Paladin", "Inquisitor"],
        "notes": "Armor tank. EM primary. Laser weapons. Neuts + TDs.",
    },

    "Caldari State": {
        "weak_to": ["Kinetic", "Thermal"],
        "deals":   ["Kinetic", "Thermal"],
        "ew":      ["ECM"],
        "tank":    "shield",
        "name_keywords": ["Caldari", "State", "Provist", "Warden"],
        "notes": "Shield tank. Kinetic/Thermal. ECM breaks locks.",
    },

    "Gallente Federation": {
        "weak_to": ["Kinetic", "Thermal"],
        "deals":   ["Kinetic", "Thermal"],
        "ew":      ["Sensor Dampeners"],
        "tank":    "armor",
        "name_keywords": ["Federation", "Gallente", "Marine", "Roden"],
        "notes": "Armor tank. Kinetic/Thermal. Sensor Damps reduce lock range.",
    },

    "Minmatar Republic": {
        "weak_to": ["Explosive", "Kinetic"],
        "deals":   ["Explosive", "Kinetic"],
        "ew":      ["Target Painters"],
        "tank":    "shield",
        "name_keywords": ["Republic", "Minmatar", "Tribal", "Freedom", "Liberation"],
        "notes": "Shield tank. Explosive primary. Target Painters.",
    },

    "Khanid Kingdom": {
        "weak_to": ["EM", "Thermal"],
        "deals":   ["Thermal", "EM"],
        "ew":      [],
        "tank":    "armor",
        "name_keywords": ["Khanid", "Kingdom"],
        "notes": "Armor tank. EM/Thermal. Similar profile to Amarr.",
    },

    "Equilibrium of Mankind": {
        "weak_to": ["Kinetic"],
        "deals":   ["Kinetic", "Thermal"],
        "ew":      [],
        "tank":    "armor",
        "name_keywords": ["EoM", "Equilibrium", "Mankind"],
        "notes": "Armor tank. Kinetic is primary weakness by a large margin.",
    },
}

RARE_SPAWN_KEYWORDS = [
    "Cynabal", "Machariel", "Dramiel", "Vindicator", "Vigilant", "Daredevil",
    "Rattlesnake", "Gila", "Worm", "Bhaalgorn", "Ashimmu", "Cruor",
    "Nightmare", "Phantasm", "Succubus", "Barghest", "Orthrus", "Garmur",
    "Dread Guristas", "True Sansha", "Shadow Serpentis", "Dark Blood",
    "Domination", "Leshak", "Karybdis Tyrannos",
]
