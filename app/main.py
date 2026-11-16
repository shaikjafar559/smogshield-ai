"""
SmogShield AI - FastAPI Application
GenAI Assistant for Severe Winter Smog & Urban Air Pollution Navigation
"""

import os
from datetime import datetime
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from app.models import (
    FamilyProfile, DailyRoutinePlan, IAQGuide,
    ImpactCalculationRequest, ImpactBreakdown,
    ChatRequest, ChatResponse, CommunityPledge
)
from app.data import (
    CITIES_DATA, IAQ_HACKS_CATALOG, COMMUNITY_INITIATIVES, EMISSION_FACTORS
)
from app.ai_engine import ai_engine

app = FastAPI(
    title="SmogShield AI",
    description="GenAI Assistant for Navigating Severe Winter Smog and Urban Air Pollution",
    version="1.0.0"
)

# Enable CORS for local integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory store for community pledges
pledges_store: List[CommunityPledge] = [
    CommunityPledge(
        neighborhood="Green Valley Colony",
        family_name="Kapoor Family",
        actions_pledged=["School Zero-Idle Zone", "C-R Box in Bedrooms", "Trip-Chaining Errands"],
        community_message="Turned off the car engine at school gate today. 4 other parents noticed and switched off too!",
        timestamp="2026-11-16 08:30"
    ),
    CommunityPledge(
        neighborhood="Lakeview Heights",
        family_name="Chen Family",
        actions_pledged=["Bubble-wrap window seals", "Shifted commute to Metro", "Wet microfiber mopping"],
        community_message="Indoor PM2.5 dropped from 165 to 18 ug/m3 after sealing the drafty north window!",
        timestamp="2026-11-16 11:15"
    ),
    CommunityPledge(
        neighborhood="Alpina Community Hub",
        family_name="Rossi Family",
        actions_pledged=["Replaced wood fireplace with radiant zone heater", "Community Watch alert"],
        community_message="Zero wood burning in our hearth this week. Electric throws are warmer and keep the court air clean.",
        timestamp="2026-11-16 14:40"
    )
]

# Ensure static directory exists
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(STATIC_DIR, exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
def serve_index():
    index_file = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "SmogShield AI is running. Frontend index.html being initialized."}

@app.get("/api/locations")
def get_locations():
    """Return available pre-configured global smog hotspots."""
    return [
        {
            "name": k,
            "city": v["city"],
            "country": v["country"],
            "base_aqi": v["base_aqi"],
            "base_pm25": v["base_pm25"],
            "smog_alert_level": v["smog_alert_level"],
            "inversion_level": v["inversion_level"]
        }
        for k, v in CITIES_DATA.items()
    ]

@app.get("/api/location/{city_name}")
def get_location_details(city_name: str, custom_aqi: Optional[int] = None):
    """Get atmospheric, diurnal, and smog profile for a location."""
    profile = ai_engine.get_city_profile(city_name, custom_aqi)
    return profile

@app.post("/api/routine/generate", response_model=DailyRoutinePlan)
def generate_routine(
    profile: FamilyProfile,
    city: str = Query(default="Delhi-NCR, India"),
    custom_aqi: Optional[int] = Query(default=None)
):
    """Generate comprehensive, low-emission daily routine tailored to family and smog tier."""
    plan = ai_engine.generate_daily_routine(profile, city, custom_aqi)
    return plan

@app.get("/api/iaq-hacks", response_model=List[IAQGuide])
def get_iaq_hacks(category: Optional[str] = None):
    """Get all DIY IAQ hacks and engineering guides, optionally filtered by category."""
    if category and category != "All":
        filtered = [h for h in IAQ_HACKS_CATALOG if h["category"].lower() == category.lower()]
        return filtered
    return IAQ_HACKS_CATALOG

@app.get("/api/iaq-hacks/{hack_id}", response_model=IAQGuide)
def get_iaq_hack_detail(hack_id: str):
    """Get specific IAQ guide details."""
    for h in IAQ_HACKS_CATALOG:
        if h["id"] == hack_id:
            return h
    raise HTTPException(status_code=404, detail="IAQ hack not found")

@app.post("/api/impact/calculate", response_model=ImpactBreakdown)
def calculate_impact(request: ImpactCalculationRequest):
    """Calculate micro (lung particulate intake averted) & macro (CO2/tailpipe) impact."""
    breakdown = ai_engine.calculate_impact(
        household_size=request.household_size,
        has_vulnerable=request.has_vulnerable_members,
        outdoor_pm25=request.current_outdoor_pm25,
        commute_mode=request.commute_mode,
        commute_km=request.daily_commute_km,
        implemented_actions=request.implemented_actions
    )
    return breakdown

@app.post("/api/chat", response_model=ChatResponse)
def chat_with_assistant(request: ChatRequest):
    """GenAI conversational guidance with atmospheric physics and IAQ reasoning."""
    response = ai_engine.generate_chat_response(request)
    return response

@app.get("/api/community/initiatives")
def get_community_initiatives():
    """Get neighborhood action templates and campaign toolkits."""
    return COMMUNITY_INITIATIVES

@app.get("/api/community/pledges", response_model=List[CommunityPledge])
def get_community_pledges():
    """Get recent community smog defense pledges."""
    return pledges_store

@app.post("/api/community/pledge", response_model=CommunityPledge)
def add_community_pledge(pledge: CommunityPledge):
    """Record a new community action pledge."""
    if not pledge.timestamp:
        pledge.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    pledges_store.insert(0, pledge)
    return pledge
