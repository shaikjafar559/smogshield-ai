"""
Data repository for SmogShield AI:
- City winter smog & thermal inversion profiles
- IAQ Hacks & DIY Air Purifier Engineering Specs
- Emission factors & health impact models
- Community action templates
"""

CITIES_DATA = {
    "Delhi-NCR, India": {
        "city": "Delhi-NCR",
        "country": "India",
        "base_aqi": 385,
        "base_pm25": 285.0,
        "base_pm10": 420.0,
        "no2": 68.0,
        "co": 3.4,
        "temperature_c": 11.5,
        "humidity_pct": 82.0,
        "wind_speed_kmh": 4.2,
        "inversion_level": "Strong Inversion (Boundary layer collapses to <150m)",
        "smog_alert_level": "Severe Hazardous (GRAP Stage IV)",
        "primary_sources": ["Vehicular cold starts & congestion", "Biomass & waste open burning", "Industrial boilers", "Trapped secondary particulates"],
        "peak_smog_hours": ["06:00 - 10:30 (Morning ground inversion)", "19:30 - 23:30 (Evening cooling & traffic peak)"],
        "best_ventilation_window": "13:30 - 15:30 (Peak solar mixing layer expansion)",
        "diurnal_multipliers": [
            {"hour": "00:00", "factor": 1.25, "inversion": "Severe"},
            {"hour": "02:00", "factor": 1.30, "inversion": "Severe"},
            {"hour": "04:00", "factor": 1.35, "inversion": "Severe (Peak Night Trap)"},
            {"hour": "06:00", "factor": 1.40, "inversion": "Extreme (Morning Cold Trap)"},
            {"hour": "08:00", "factor": 1.45, "inversion": "Extreme + Rush Hour"},
            {"hour": "10:00", "factor": 1.20, "inversion": "Breaking up"},
            {"hour": "12:00", "factor": 0.85, "inversion": "Weakened"},
            {"hour": "14:00", "factor": 0.65, "inversion": "Minimum (Solar Mixing High)"},
            {"hour": "16:00", "factor": 0.75, "inversion": "Re-forming"},
            {"hour": "18:00", "factor": 1.15, "inversion": "Strong Inversion Starts"},
            {"hour": "20:00", "factor": 1.35, "inversion": "Severe + Evening Rush"},
            {"hour": "22:00", "factor": 1.30, "inversion": "Severe Ground Trapping"}
        ]
    },
    "Lahore, Pakistan": {
        "city": "Lahore",
        "country": "Pakistan",
        "base_aqi": 410,
        "base_pm25": 310.0,
        "base_pm10": 460.0,
        "no2": 72.0,
        "co": 3.8,
        "temperature_c": 10.0,
        "humidity_pct": 88.0,
        "wind_speed_kmh": 3.1,
        "inversion_level": "Extreme Inversion (Stagnant anticyclone)",
        "smog_alert_level": "Severe Hazardous Emergency",
        "primary_sources": ["Low-grade fuel emissions", "Brick kilns & industrial corridors", "Crop residue smoke drift", "Winter cold air trapping"],
        "peak_smog_hours": ["05:30 - 10:00 (Heavy radiation fog)", "18:30 - 23:00 (Evening settling)"],
        "best_ventilation_window": "13:00 - 15:00 (Brief solar dispersion)",
        "diurnal_multipliers": [
            {"hour": "00:00", "factor": 1.28, "inversion": "Severe"},
            {"hour": "03:00", "factor": 1.35, "inversion": "Severe"},
            {"hour": "06:00", "factor": 1.45, "inversion": "Extreme Fog Trap"},
            {"hour": "09:00", "factor": 1.40, "inversion": "Extreme"},
            {"hour": "12:00", "factor": 0.90, "inversion": "Moderate"},
            {"hour": "14:00", "factor": 0.68, "inversion": "Lowest of the Day"},
            {"hour": "17:00", "factor": 0.85, "inversion": "Re-stabilizing"},
            {"hour": "20:00", "factor": 1.38, "inversion": "Severe Trapping"},
            {"hour": "22:00", "factor": 1.32, "inversion": "Severe Trapping"}
        ]
    },
    "Beijing, China": {
        "city": "Beijing",
        "country": "China",
        "base_aqi": 185,
        "base_pm25": 115.0,
        "base_pm10": 175.0,
        "no2": 45.0,
        "co": 1.8,
        "temperature_c": -3.0,
        "humidity_pct": 52.0,
        "wind_speed_kmh": 6.8,
        "inversion_level": "Moderate Inversion (Mountain basin trapping)",
        "smog_alert_level": "Unhealthy (Orange Alert Warning)",
        "primary_sources": ["Regional heavy industry", "Residential heating coal/gas", "Regional transport", "Winter valley pooling"],
        "peak_smog_hours": ["07:00 - 09:30", "20:00 - 23:00"],
        "best_ventilation_window": "12:30 - 14:30",
        "diurnal_multipliers": [
            {"hour": "00:00", "factor": 1.15, "inversion": "Moderate"},
            {"hour": "06:00", "factor": 1.30, "inversion": "Strong"},
            {"hour": "12:00", "factor": 0.85, "inversion": "Moderate"},
            {"hour": "14:00", "factor": 0.70, "inversion": "Mild"},
            {"hour": "18:00", "factor": 1.10, "inversion": "Moderate"},
            {"hour": "21:00", "factor": 1.25, "inversion": "Strong"}
        ]
    },
    "Salt Lake City, Utah, USA": {
        "city": "Salt Lake City",
        "country": "USA",
        "base_aqi": 158,
        "base_pm25": 68.0,
        "base_pm10": 92.0,
        "no2": 38.0,
        "co": 1.2,
        "temperature_c": -4.0,
        "humidity_pct": 74.0,
        "wind_speed_kmh": 3.0,
        "inversion_level": "Persistent Winter Valley Inversion (PCAP)",
        "smog_alert_level": "Unhealthy for Sensitive Groups",
        "primary_sources": ["Mobile vehicular emissions in valley bowl", "Residential wood burning & gas furnaces", "Industrial point sources"],
        "peak_smog_hours": ["07:00 - 10:00 (Cold pool capping)", "17:30 - 21:00 (Commute smoke pooling)"],
        "best_ventilation_window": "13:00 - 15:30 (Partial solar thermal punch)",
        "diurnal_multipliers": [
            {"hour": "00:00", "factor": 1.12, "inversion": "Valley Cold Pool"},
            {"hour": "06:00", "factor": 1.28, "inversion": "Cap Trapped"},
            {"hour": "08:00", "factor": 1.32, "inversion": "Cap Trapped + Cold Starts"},
            {"hour": "13:00", "factor": 0.80, "inversion": "Partial Thermal Punch"},
            {"hour": "17:00", "factor": 1.20, "inversion": "Evening Trap Reset"},
            {"hour": "21:00", "factor": 1.24, "inversion": "Valley Cold Pool"}
        ]
    },
    "Milan / Po Valley, Italy": {
        "city": "Milan (Po Valley)",
        "country": "Italy",
        "base_aqi": 165,
        "base_pm25": 78.0,
        "base_pm10": 110.0,
        "no2": 54.0,
        "co": 1.6,
        "temperature_c": 3.0,
        "humidity_pct": 89.0,
        "wind_speed_kmh": 2.5,
        "inversion_level": "Sub-Alpine Stagnation Inversion",
        "smog_alert_level": "Unhealthy",
        "primary_sources": ["Diesel traffic emissions", "Biomass & pellet heating", "Intensive agricultural ammonia (secondary aerosol)"],
        "peak_smog_hours": ["07:30 - 10:00", "19:00 - 22:30"],
        "best_ventilation_window": "13:00 - 15:00",
        "diurnal_multipliers": [
            {"hour": "00:00", "factor": 1.18, "inversion": "Po Valley Cap"},
            {"hour": "07:00", "factor": 1.32, "inversion": "Fog + Inversion"},
            {"hour": "13:00", "factor": 0.78, "inversion": "Partial Break"},
            {"hour": "19:00", "factor": 1.28, "inversion": "Po Valley Cap"}
        ]
    },
    "Ulaanbaatar, Mongolia": {
        "city": "Ulaanbaatar",
        "country": "Mongolia",
        "base_aqi": 340,
        "base_pm25": 245.0,
        "base_pm10": 390.0,
        "no2": 62.0,
        "co": 4.1,
        "temperature_c": -21.0,
        "humidity_pct": 68.0,
        "wind_speed_kmh": 2.0,
        "inversion_level": "Extreme Siberian High Arctic Inversion",
        "smog_alert_level": "Severe Hazardous",
        "primary_sources": ["Ger district raw coal & briquette stoves", "Combined heat/power plants", "Low wind mountain valley trap"],
        "peak_smog_hours": ["06:00 - 11:00", "18:00 - 23:30"],
        "best_ventilation_window": "Avoid open outdoor ventilation during sub-zero smog spikes",
        "diurnal_multipliers": [
            {"hour": "00:00", "factor": 1.25, "inversion": "Extreme Deep Freeze"},
            {"hour": "06:00", "factor": 1.45, "inversion": "Ger Morning Stove Ignite"},
            {"hour": "12:00", "factor": 0.88, "inversion": "Valley Low Cold"},
            {"hour": "18:00", "factor": 1.40, "inversion": "Ger Evening Stove Ignite"}
        ]
    },
    "Krakow, Poland": {
        "city": "Krakow",
        "country": "Poland",
        "base_aqi": 172,
        "base_pm25": 84.0,
        "base_pm10": 118.0,
        "no2": 42.0,
        "co": 1.5,
        "temperature_c": 0.5,
        "humidity_pct": 84.0,
        "wind_speed_kmh": 3.8,
        "inversion_level": "Vistula River Basin Inversion",
        "smog_alert_level": "Unhealthy",
        "primary_sources": ["Outskirt coal & wood furnaces ('kopciuchy')", "Urban transit diesel", "River basin topography trapping"],
        "peak_smog_hours": ["07:00 - 09:30", "18:30 - 22:00"],
        "best_ventilation_window": "12:30 - 14:30",
        "diurnal_multipliers": [
            {"hour": "00:00", "factor": 1.15, "inversion": "Basin Pool"},
            {"hour": "07:00", "factor": 1.30, "inversion": "Morning Peak"},
            {"hour": "13:00", "factor": 0.75, "inversion": "Breeze Shift"},
            {"hour": "19:00", "factor": 1.32, "inversion": "Domestic Stove Peak"}
        ]
    },
    "Central Valley (Bakersfield/Fresno), CA, USA": {
        "city": "Central Valley (Bakersfield)",
        "country": "USA",
        "base_aqi": 162,
        "base_pm25": 72.0,
        "base_pm10": 105.0,
        "no2": 39.0,
        "co": 1.1,
        "temperature_c": 6.0,
        "humidity_pct": 86.0,
        "wind_speed_kmh": 2.8,
        "inversion_level": "Tule Fog Radiation Inversion",
        "smog_alert_level": "Unhealthy",
        "primary_sources": ["Heavy I-5 / Hwy 99 freight diesel", "Agricultural burning & secondary ammonium nitrate", "Valley rim stagnant trap"],
        "peak_smog_hours": ["07:00 - 10:00 (Tule fog trap)", "18:00 - 21:30"],
        "best_ventilation_window": "13:00 - 15:30",
        "diurnal_multipliers": [
            {"hour": "00:00", "factor": 1.14, "inversion": "Fog Trap"},
            {"hour": "07:00", "factor": 1.35, "inversion": "Dense Tule Fog"},
            {"hour": "13:00", "factor": 0.72, "inversion": "Fog Burnoff"},
            {"hour": "19:00", "factor": 1.25, "inversion": "Cooling Re-cap"}
        ]
    }
}

IAQ_HACKS_CATALOG = [
    {
        "id": "corsi-rosenthal-box",
        "title": "The Corsi-Rosenthal (C-R) Box (High-CADR DIY Air Cleaner)",
        "category": "DIY Filtration",
        "difficulty": "Medium (30 min)",
        "est_cost_usd": 45.0,
        "cadr_rating": "550 - 650 CFM (Equal to $500 commercial HEPA)",
        "pm25_reduction_pct": "85% - 93% within 25 minutes in 400 sq ft room",
        "materials_needed": [
            "1x Standard 20-inch box fan (approx $20)",
            "4x or 5x 20x20x2 or 20x20x1 MERV 13 furnace filters (approx $6-$8 each)",
            "1x Heavy-duty duct tape or painters tape",
            "1x Cardboard shroud cutout (14-inch circular opening to prevent fan blade back-flow)"
        ],
        "instructions": [
            "1. Tape 4 MERV-13 filters together in a cube formation, ensuring arrows point inward toward the fan intake.",
            "2. Seal the cardboard bottom base with duct tape so no unfiltered air leaks underneath.",
            "3. Place the 20-inch box fan on top, with airflow blowing UPWARD (exhausting clean air into the room).",
            "4. Cut a circular cardboard shroud with an inner hole matching the fan blades diameter (approx 14 inches) and tape to the fan front; this prevents backward air recirculation at the blade corners.",
            "5. Run continuously on Low or Medium speed during severe winter smog episodes."
        ],
        "scientific_rationale": "Large surface area of 4 pleated MERV 13 filters produces extremely low pressure drop across the fan blades compared to a single filter, resulting in whisper-quiet operation and massive Clean Air Delivery Rate (CADR). Validated by UC Davis and ASHRAE.",
        "safety_cautions": [
            "Always inspect fan motor for thermal overload fuse (modern 2012+ box fans have fused plugs).",
            "Keep dry and away from humidifiers or open bathtubs.",
            "Do not use MERV 16 or HEPA in a DIY single box fan without multi-filter cube due to motor strain."
        ]
    },
    {
        "id": "single-filter-budget-fan",
        "title": "Budget Single-Filter Box Fan with Cardboard Shroud",
        "category": "DIY Filtration",
        "difficulty": "Easy (10 min)",
        "est_cost_usd": 28.0,
        "cadr_rating": "220 - 280 CFM",
        "pm25_reduction_pct": "70% - 80% in small rooms (150 sq ft)",
        "materials_needed": [
            "1x 20-inch standard box fan",
            "1x 20x20x1 MERV 13 filter",
            "Duct tape or 2 large bungee cords",
            "Cardboard corner shroud"
        ],
        "instructions": [
            "1. Place MERV 13 filter flush against the BACK (intake) of the box fan. Follow arrow pointing into the fan.",
            "2. Secure corners tightly with duct tape or bungee cords to prevent edge air leakage.",
            "3. Cut a cardboard ring and tape to front of the fan covering the outer 2 inches of the blade edge to eliminate vortex leakage.",
            "4. Run on speed 1 (low) or 2 (medium)."
        ],
        "scientific_rationale": "High-velocity air at blade tips creates reverse suction if unshielded. Adding the cardboard shroud increases forward airflow velocity by up to 20% while protecting the motor.",
        "safety_cautions": [
            "Check motor casing periodically with hand. If warm, step down fan speed to low.",
            "Replace filter every 4-6 weeks during hazardous smog months."
        ]
    },
    {
        "id": "window-infiltration-bubblewrap-draft-seal",
        "title": "Thermal Infiltration & Smog Draft Defense Protocol",
        "category": "Infiltration Defense",
        "difficulty": "Easy (20 min)",
        "est_cost_usd": 12.0,
        "cadr_rating": "Passive barrier (cuts infiltration by 65%)",
        "pm25_reduction_pct": "Prevents 40-60 ug/m3 ambient smog intrusion",
        "materials_needed": [
            "Roll of medium/large bubble wrap or window shrink film",
            "Spray bottle with clean water + 2 drops mild soap",
            "Silicone bottom draft stopper strip or rolled towel 'door snake'",
            "Painter's removable masking tape"
        ],
        "instructions": [
            "1. Spray a light mist of water onto the interior glass pane of non-primary windows.",
            "2. Press bubble wrap sheet against the damp glass (bubble side to glass); surface tension adheres it instantly without glue.",
            "3. Tape around window seams using painter's tape to seal tiny cracks where winter outdoor PM2.5 draft slips in.",
            "4. Install silicone door snakes at main exterior door sweeps and balcony doors to eliminate micro-drafts."
        ],
        "scientific_rationale": "Cold winter air is dense and forces its way through window micro-crevices via chimney stack effect. The bubble wrap acts as both a thermal R-2 insulator and physical air barrier, reducing heating energy consumption while stopping microscopic PM2.5 infiltration.",
        "safety_cautions": [
            "Ensure at least one egress window is easily peelable in an emergency.",
            "Use only painter's or low-tack tape to prevent peeling interior window frame paint."
        ]
    },
    {
        "id": "wet-cleaning-dust-suppression",
        "title": "Zero-Resuspension Wet Cleaning & Deposition Protocol",
        "category": "Infiltration Defense",
        "difficulty": "Easy (15 min daily)",
        "est_cost_usd": 5.0,
        "cadr_rating": "Surface source suppression",
        "pm25_reduction_pct": "Prevents indoor PM2.5 spikes of 80-150 ug/m3 caused by dry sweeping",
        "materials_needed": [
            "Microfiber flat mop or damp cloth",
            "Warm water with dash of vinegar or mild eco-detergent",
            "Spray bottle for misting entryways"
        ],
        "instructions": [
            "1. STRICTLY AVOID dry sweeping with standard brooms or vacuuming without a HEPA exhaust filter during smog peaks. Dry brooms aerosolize settled toxic heavy metal particles directly into breathing zones.",
            "2. Use a damp microfiber mop in an 'S' motion across hard flooring.",
            "3. Mist entryway floor mats with a light water spray when returning from outdoors to capture shoe-tracked soot.",
            "4. Leave shoes in a sealed entryway cabinet or dedicated drop zone."
        ],
        "scientific_rationale": "Dry brooms generate significant PM10 and PM2.5 re-suspension that stays airborne for 4 to 8 hours. Damp capillary adhesion binds microscopic soot and PAHs to the cloth, eliminating airborne re-inhalation.",
        "safety_cautions": [
            "Wash microfiber cloths with warm water; do not shake dirty dry cloths indoors."
        ]
    },
    {
        "id": "kitchen-combustion-and-exhaust-isolation",
        "title": "Kitchen Toxic Byproduct Isolation & Safe Cooking Mode",
        "category": "Kitchen & Combustion",
        "difficulty": "Easy (Daily Habit)",
        "est_cost_usd": 0.0,
        "cadr_rating": "Eliminates up to 300 ug/m3 indoor source PM",
        "pm25_reduction_pct": "Reduces indoor PM2.5 spikes by 75%",
        "materials_needed": [
            "Lids for all cooking pots/pans",
            "Range hood exhaust or portable cross-breeze exhaust fan",
            "Electric kettle / induction cooker if available"
        ],
        "instructions": [
            "1. Never cook on high flame without the range hood running on maximum from 2 minutes BEFORE igniting until 5 minutes AFTER turning off.",
            "2. Close kitchen sliding door or partition to create negative kitchen pressure, preventing ultrafine oils and NO2 from escaping into family bedrooms.",
            "3. Prioritize boiling, steaming, slow simmering, and pressure cooking over deep frying, broiling, or dry wok charring during severe smog days.",
            "4. Ban indoor incense, scented candles, and mosquito coils; a single mosquito coil emits PM2.5 equivalent to 75-100 cigarettes."
        ],
        "scientific_rationale": "Frying oils decompose at smoke point into acrolein, polycyclic aromatic hydrocarbons (PAHs), and ultrafine particles (<0.1 micron) which enter deep alveolar tissue. Gas stoves without active extraction generate NO2 exceeding WHO annual guidelines in 15 minutes.",
        "safety_cautions": [
            "If using range hood while whole home is sealed tight, crack a nearby kitchen-only window by 1/2 inch to provide make-up air and prevent back-drafting boiler/water heater flues."
        ]
    },
    {
        "id": "respiratory-mucosa-humidity-shield",
        "title": "Mucociliary Escalator Shield: 40-50% RH Balancing",
        "category": "Humidity & Mucosa",
        "difficulty": "Easy (10 min)",
        "est_cost_usd": 20.0,
        "cadr_rating": "Biological defense reinforcement",
        "pm25_reduction_pct": "Doubles natural bronchial particulate clearance speed",
        "materials_needed": [
            "Digital hygrometer (approx $6)",
            "Evaporative or ultrasonic humidifier (using distilled or boiled water), OR wide ceramic water bowls near radiators"
        ],
        "instructions": [
            "1. Place digital hygrometer in the main sleeping area at head height.",
            "2. Keep winter indoor relative humidity strictly between 40% and 50%.",
            "3. If using radiator heat: Place wide shallow stainless/ceramic bowls of clean water directly on radiator tops for passive evaporation.",
            "4. If using ultrasonic humidifier: Use only reverse osmosis (RO) or distilled water. Tap water contains dissolved minerals that ultrasonic transducers aerosolize into white PM2.5 dust."
        ],
        "scientific_rationale": "When indoor winter air drops below 30% relative humidity, airway mucosal secretions thicken and the cilia (microscopic sweeping hairs in bronchi) become paralyzed. Maintaining 40-50% humidity preserves mucosal fluid dynamics, allowing the body to mechanically sweep inhaled smog particles out of airways.",
        "safety_cautions": [
            "Do not exceed 55% RH to avoid dust mite proliferation and mold spores.",
            "Clean humidifier reservoirs every 48 hours to prevent bacterial biofilm."
        ]
    },
    {
        "id": "clean-room-sleeping-sanctuary",
        "title": "The 'Sleeping Sanctuary' Clean Room Protocol",
        "category": "Infiltration Defense",
        "difficulty": "Medium (25 min)",
        "est_cost_usd": 15.0,
        "cadr_rating": "Concentrated micro-climate",
        "pm25_reduction_pct": "Achieves indoor PM2.5 < 15 ug/m3 even during 400+ outside smog",
        "materials_needed": [
            "Air purifier or DIY C-R Box placed in bedroom",
            "Door threshold draft excluder",
            "Weather-stripping tape on bedroom window frame"
        ],
        "instructions": [
            "1. Select the smallest bedroom where children/vulnerable members sleep as the designated Clean Sanctuary.",
            "2. Seal window edges with removable weather-strip foam.",
            "3. Place door snake or heavy rolled towel at the base of the bedroom door.",
            "4. Position air purifier 2 feet away from walls, blowing clean filtered air directly toward head height of beds.",
            "5. Keep bedroom door closed continuously. Run purifier on high for 45 minutes before bedtime, then step down to quiet sleep mode for the entire night."
        ],
        "scientific_rationale": "Humans spend 8 hours motionless in bed breathing 4,000-6,000 liters of air. Focusing purification capacity on a sealed smaller room achieves 5x-8x higher air changes per hour (ACH) than trying to clean open living/dining rooms, drastically slashing 1/3 of total daily cumulative PM2.5 dose.",
        "safety_cautions": [
            "Keep a hygrometer and CO2 monitor if possible. If CO2 rises above 1200 ppm overnight, crack bedroom door to inner hallway for 5 minutes."
        ]
    }
]

EMISSION_FACTORS = {
    "ice_car_cold_start_multiplier": 7.5, # 7.5x higher emissions in first 3 km of winter drive
    "ice_car_co2_kg_per_km": 0.192,
    "ice_car_pm25_tailpipe_g_per_km": 0.015,
    "ice_car_brake_tire_pm_g_per_km": 0.012,
    "metro_co2_kg_per_km": 0.035,
    "metro_pm25_g_per_km": 0.001,
    "ev_carpool_co2_kg_per_km_per_person": 0.022,
    "wood_stove_pm25_g_per_hour": 30.0, # Equivalent to driving 2,000 km in an ICE car
    "electric_heater_direct_pm25": 0.0,
    "cigarette_pm25_equivalent_ug": 22.0 # 22 ug/m3 inhaled over 24h roughly equals 1 cigarette
}

COMMUNITY_INITIATIVES = [
    {
        "id": "zero-idle-school-dropoff",
        "title": "Neighborhood 'Zero-Idle' School Zone Campaign",
        "category": "Community Shield",
        "description": "Parents pledge to turn off vehicle ignitions while waiting at morning school pick-up / drop-off points. In winter thermal inversions, idling cars create a toxic ground-level exhaust cloud at children's breathing height.",
        "impact_metric": "Prevents 450 kg of localized VOCs & PM2.5 at school gates every winter season",
        "pledges_count": 142
    },
    {
        "id": "bulk-c-r-box-building-bee",
        "title": "Community C-R Box DIY Building Bee",
        "category": "Mutual Aid",
        "description": "Neighborhood associations bulk-purchase MERV-13 filters and box fans at 40% wholesale discount, holding weekend assembly workshops for elderly neighbors and local public schools.",
        "impact_metric": "Brought 85 clean air scrubbers to low-income senior households and classrooms",
        "pledges_count": 89
    },
    {
        "id": "winter-trip-chaining-collective",
        "title": "Neighborhood Trip Chaining & Bulk Grocery Carpools",
        "category": "Mobility Transition",
        "description": "Families coordinate errands through shared schedules to eliminate short, cold-engine winter car trips (<3 km), which produce 7x higher smog toxins due to unheated catalytic converters.",
        "impact_metric": "Reduced neighborhood morning cold-starts by 32%",
        "pledges_count": 67
    },
    {
        "id": "stubble-and-waste-reporting-network",
        "title": "Clean Skies Community Watch & Fast Alert",
        "category": "Civic Vigilance",
        "description": "Volunteers use mobile geolocation to instantly flag roadside leaf burning, construction dust violations, and waste burning to municipal green enforcement teams.",
        "impact_metric": "310 unauthorized open fires halted within 30 minutes of ignition",
        "pledges_count": 215
    }
]
