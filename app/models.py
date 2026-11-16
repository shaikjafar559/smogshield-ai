from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class VulnerabilityGroup(BaseModel):
    infants_toddlers: int = 0
    elderly: int = 0
    respiratory_patients: int = 0  # Asthma, COPD, bronchitis
    pregnant: int = 0
    active_outdoor_athletes: int = 0
    pets: int = 0

class FamilyProfile(BaseModel):
    family_name: str = "My Family"
    household_size: int = 4
    vulnerabilities: VulnerabilityGroup = Field(default_factory=VulnerabilityGroup)
    housing_type: str = "Apartment (mid-level)"  # Ground floor, Mid-level apartment, Top floor/Penthouse, Independent House
    window_sealing_quality: str = "Standard / Moderate Drafts"  # Well-sealed double glazed, Standard, Older drafty
    heating_source: str = "Electric / Heat Pump"  # Electric, Gas Boiler, Wood/Pellet Stove, Coal/Kerosene, District Heating
    cooking_style: str = "Standard with Range Hood"  # High smoke/frying, Standard with hood, Boiling/Steaming focus
    primary_commute: str = "Personal Car (ICE)"  # Personal Car (ICE), Public Transit (Bus/Metro), Electric Vehicle, Walking/Biking, Carpool
    daily_commute_km: float = 20.0
    has_air_purifier: bool = False
    purifier_count: int = 0

class LocationQuery(BaseModel):
    city: str
    country: Optional[str] = None
    custom_aqi: Optional[int] = None
    custom_pm25: Optional[float] = None

class AirQualityReport(BaseModel):
    city: str
    country: str
    aqi: int
    pm25: float  # ug/m3
    pm10: float  # ug/m3
    no2: float   # ppb
    co: float    # ppm
    temperature_c: float
    humidity_pct: float
    wind_speed_kmh: float
    inversion_level: str  # Strong Inversion (Extreme Trapping), Moderate, Weak / Dispersing
    smog_alert_level: str  # Moderate, Unhealthy for Sensitive Groups, Unhealthy, Very Unhealthy, Severe Hazardous
    peak_smog_hours: List[str]
    best_ventilation_window: str
    hourly_forecast: List[Dict[str, Any]]

class RoutineStep(BaseModel):
    time_window: str
    phase: str  # Morning Inversion Peak, Midday Dispersion, Evening Spike, Overnight
    outdoor_smog_risk: str  # Extreme, High, Moderate, Low
    action_title: str
    recommended_action: str
    sustainable_alternative: str
    iaq_protocol: str
    direct_impact_explanation: str
    emission_savings: str
    health_benefit: str

class DailyRoutinePlan(BaseModel):
    city: str
    aqi: int
    family_profile: FamilyProfile
    summary_headline: str
    routine_steps: List[RoutineStep]
    key_sustainable_swaps: List[Dict[str, str]]
    critical_family_warnings: List[str]
    total_estimated_intake_prevented_ug: float
    total_co2_prevented_kg: float

class IAQGuide(BaseModel):
    id: str
    title: str
    category: str  # DIY Filtration, Infiltration Defense, Kitchen & Combustion, Humidity & Mucosa, Monitoring
    difficulty: str  # Easy (10 min), Medium (30 min), Advanced (1 hr)
    est_cost_usd: float
    cadr_rating: Optional[str] = None
    pm25_reduction_pct: str
    materials_needed: List[str]
    instructions: List[str]
    scientific_rationale: str
    safety_cautions: List[str]

class ImpactCalculationRequest(BaseModel):
    household_size: int = 4
    has_vulnerable_members: bool = True
    current_outdoor_pm25: float = 180.0  # ug/m3
    commute_mode: str = "Personal Car (ICE)"
    daily_commute_km: float = 25.0
    implemented_actions: List[str] = []

class ImpactBreakdown(BaseModel):
    daily_pm25_inhaled_baseline_ug: float
    daily_pm25_inhaled_optimized_ug: float
    pm25_prevented_ug: float
    cigarette_equivalent_prevented: float
    acute_respiratory_risk_drop_pct: float
    daily_co2_saved_kg: float
    daily_pm_tailpipe_saved_grams: float
    neighborhood_scale_pm25_kg_year: float
    explanation_narrative: str

class ChatMessage(BaseModel):
    role: str  # 'user' or 'assistant' or 'system'
    content: str

class ChatRequest(BaseModel):
    message: str
    history: List[ChatMessage] = []
    location: Optional[str] = "Delhi, India"
    family_profile: Optional[FamilyProfile] = None
    current_aqi: Optional[int] = 320
    persona: Optional[str] = "routine_advisor"  # routine_advisor, iaq_engineer, community_organizer, pediatric_smog_guard
    api_key: Optional[str] = None

class ChatResponse(BaseModel):
    reply: str
    citations: List[str] = []
    suggested_quick_actions: List[str] = []

class CommunityPledge(BaseModel):
    neighborhood: str
    family_name: str
    actions_pledged: List[str]
    community_message: str
    timestamp: Optional[str] = None
