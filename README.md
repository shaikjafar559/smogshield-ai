# SmogShield AI 🛡️
### GenAI-Powered Winter Smog & Community Air Navigator

SmogShield AI is an intelligent assistant designed to help families and urban communities navigate severe winter smog and air pollution episodes (such as those driven by boundary-layer thermal inversions, biomass burning, vehicular cold-starts, and industrial stagnation).

The application recommends **low-emission daily routines**, **indoor air quality (IAQ) engineering hacks**, and **sustainable lifestyle alternatives** tailored to the family's location and vulnerability profile, while providing clear, quantitative explanations of the **direct biological and environmental impacts** of their choices.

---

## 🌟 Key Features

### 1. Diurnal Inversion & Smog Tracking
- **Atmospheric Boundary Layer (ABL) Inversion Modeling**: Tracks how cold surface air traps vehicular soot and biomass smoke near breathing height during early mornings (06:00–10:00) and late evenings.
- **Safe Ventilation Windows**: Predicts the optimal midday solar mixing window (e.g. 13:00–15:30) for rapid cross-ventilation (*Stoßlüften*) without saturating indoor air with toxic PM2.5.
- **Global Smog Hotspots & Custom Simulation**: Pre-configured profiles for Delhi-NCR, Lahore, Beijing, Salt Lake City (PCAP inversion), Milan/Po Valley, Krakow, Ulaanbaatar, and Central Valley CA, with real-time slider controls for custom AQI simulation.

### 2. Personalized Low-Emission Daily Routines
- **Vulnerability-First Adaptation**: Customizes 24-hour phased routines based on family composition (infants, elderly, asthmatics/COPD patients, pregnant women, pets).
- **Phased 24-Hour Plan**:
  - *Phase 1 (Morning Inversion Peak)*: Zero outdoor cardio alerts, indoor sanctuary activation, school commute protection.
  - *Phase 2 (School Drop-Off & Rush)*: Anti-idling enforcement, internal vehicle air recirculation, child KF94/N95 facial seals.
  - *Phase 3 (Midday Solar Mixing)*: Targeted 15-minute cross-ventilation, chained grocery/errand routes to avoid multiple cold starts.
  - *Phase 4 (Evening Inversion & Cooking)*: Range hood negative-pressure isolation, boiling/steaming over high-smoke frying, ban on indoor candles/incense, radiant zone heating instead of wood fires.
  - *Phase 5 (Nighttime Sleeping Sanctuary)*: Sealed bedroom sanctuary, continuous quiet C-R box/HEPA filtration, 40–50% relative humidity control.

### 3. Indoor Air Quality (IAQ) Engineering Lab
- **The Corsi-Rosenthal (C-R) Box**: Step-by-step blueprints and schematic visualizer for the 4-filter MERV 13 box-fan cleaner that delivers **550–650 CFM CADR** for ~$45 (equivalent to $500 commercial HEPA units). Includes cardboard aerodynamic shroud template.
- **Thermal Bubble-Wrap & Draft Defense**: Zero-glue adhesive window micro-draft sealing that cuts outdoor PM2.5 infiltration by up to 65%.
- **Zero-Resuspension Damp Mopping**: Replaces dry brooms and non-HEPA vacuums to stop settled heavy metal soot from becoming airborne.
- **Mucociliary Escalator Defense**: Explains why maintaining 40–50% indoor relative humidity prevents cilia paralysis in cold dry winter air.

### 4. Direct Impact Calculator (Micro & Macro Pillars)
- **Family Biological Defense (Micro)**:
  - Daily PM2.5 lung intake averted ($\mu g$).
  - Cigarette equivalents spared per day (Harvard/EPA epidemiological conversion).
  - Acute respiratory episode risk reduction percentage.
- **Community Airshed Relief (Macro)**:
  - Daily $CO_2$ emissions avoided ($kg$).
  - Primary tailpipe fine particulates and VOCs prevented ($g$).
  - Neighborhood network multiplier: Impact if 100 households adopt the routine over 90 days of winter smog.

### 5. Multi-Persona GenAI Copilot
- Conversational assistant with specialized persona modes:
  - *Routine & Commute Advisor*
  - *DIY IAQ Filtration Engineer*
  - *Pediatric & Sensitive Lung Guard*
  - *Community Clean Air Organizer*
- Built-in atmospheric and public health reasoning engine, with optional live Google Gemini API integration.

### 6. Community Action & Neighborhood Pledges
- Action toolkits for Zero-Idle School Zones, Community C-R Box Building Bees, and Neighborhood Errand Trip-Chaining.
- Interactive pledge board with live community impact counter.

---

## 🚀 Quickstart Guide

### Prerequisites
- Python 3.10+
- Modern Web Browser (Chrome, Edge, Firefox, Safari)

### Installation & Run

1. Navigate to the project directory:
   ```powershell
   cd "C:\Users\ShaikAli\.gemini\antigravity\scratch\smogshield-ai"
   ```

2. Run the application:
   ```powershell
   python run.py
   ```

3. Open your browser and navigate to:
   ```
   http://127.0.0.1:8080
   ```

### Running Automated Tests
```powershell
python -m pytest tests/test_api.py -v
```

---

## 🏛️ Architecture Overview

```
smogshield-ai/
│
├── app/
│   ├── __init__.py
│   ├── main.py            # FastAPI endpoints, static file server, and route handlers
│   ├── models.py          # Pydantic schemas for family profile, IAQ hacks, impact models
│   ├── data.py            # Atmospheric inversion profiles, IAQ catalog, emission factors
│   ├── ai_engine.py       # GenAI reasoning, routine generator & impact calculator
│   └── static/
│       ├── index.html     # Single Page Application (Tailwind, Lucide, Chart.js)
│       ├── app.js         # Frontend controller, Chart.js rendering, API communication
│       └── styles.css     # Glassmorphic UI styles, animations, blueprint schematics
│
├── tests/
│   └── test_api.py        # Complete automated test suite
├── run.py                 # Server startup entrypoint
└── README.md              # Documentation
```

---

## 🧬 Scientific Frameworks & References
- **U.S. EPA MOVES (Motor Vehicle Emission Simulator)**: Cold-start emission factor multipliers and catalytic converter warmup dynamics.
- **WHO Global Air Quality Guidelines (2021)**: Particulate matter exposure metrics and biological damage thresholds.
- **ASHRAE Standard 62.2 / Epidemic Task Force**: Ventilation rates and MERV 13 filtration effectiveness.
- **UC Davis Department of Civil & Environmental Engineering (Corsi & Rosenthal)**: Clean Air Delivery Rate (CADR) dynamics of multi-filter box-fan air cleaners.
