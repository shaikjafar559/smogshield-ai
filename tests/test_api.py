"""
Automated Test Suite for SmogShield AI
Tests API routes, AI engine logic, impact calculations, and routine generation.
"""

import sys
import os
import pytest
from fastapi.testclient import TestClient

# Ensure root dir is in python path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from app.main import app
from app.ai_engine import ai_engine
from app.models import FamilyProfile, VulnerabilityGroup

client = TestClient(app)

def test_root_serves_html():
    """Verify that root endpoint serves the SPA application."""
    response = client.get("/")
    assert response.status_code == 200
    assert "SmogShield" in response.text

def test_get_locations():
    """Verify that location catalog returns expected high-smog urban centers."""
    response = client.get("/api/locations")
    assert response.status_code == 200
    locations = response.json()
    assert len(locations) >= 5
    cities = [l["city"] for l in locations]
    assert "Delhi-NCR" in cities
    assert "Lahore" in cities
    assert "Beijing" in cities

def test_get_location_details():
    """Verify detailed atmospheric inversion profile for a city."""
    response = client.get("/api/location/Delhi-NCR,%20India")
    assert response.status_code == 200
    data = response.json()
    assert data["city"] == "Delhi-NCR"
    assert data["base_aqi"] > 300
    assert "diurnal_multipliers" in data
    assert "best_ventilation_window" in data

def test_generate_routine_endpoint():
    """Verify daily routine generation with family vulnerability profile."""
    profile_data = {
        "family_name": "Sharma Household",
        "household_size": 4,
        "vulnerabilities": {
            "infants_toddlers": 1,
            "elderly": 1,
            "respiratory_patients": 1,
            "pregnant": 0,
            "active_outdoor_athletes": 0,
            "pets": 0
        },
        "housing_type": "Apartment (mid-level)",
        "window_sealing_quality": "Older drafty",
        "heating_source": "Electric / Heat Pump",
        "cooking_style": "Standard with Range Hood",
        "primary_commute": "Personal Car (ICE)",
        "daily_commute_km": 25.0,
        "has_air_purifier": False,
        "purifier_count": 0
    }
    response = client.post("/api/routine/generate?city=Delhi-NCR,%20India", json=profile_data)
    assert response.status_code == 200
    plan = response.json()
    assert plan["city"] == "Delhi-NCR"
    assert len(plan["routine_steps"]) >= 4
    assert plan["total_estimated_intake_prevented_ug"] > 0
    assert plan["total_co2_prevented_kg"] > 0
    assert len(plan["critical_family_warnings"]) > 0

def test_iaq_hacks_catalog():
    """Verify retrieval of IAQ hacks and Corsi-Rosenthal specifications."""
    response = client.get("/api/iaq-hacks")
    assert response.status_code == 200
    hacks = response.json()
    assert len(hacks) >= 4
    ids = [h["id"] for h in hacks]
    assert "corsi-rosenthal-box" in ids

    # Test single hack detail
    cr_resp = client.get("/api/iaq-hacks/corsi-rosenthal-box")
    assert cr_resp.status_code == 200
    cr_data = cr_resp.json()
    assert cr_data["est_cost_usd"] < 60.0
    assert "MERV 13" in "".join(cr_data["materials_needed"])

def test_impact_calculation():
    """Verify EPA/Harvard-modeled micro & macro impact calculations."""
    calc_req = {
        "household_size": 4,
        "has_vulnerable_members": True,
        "current_outdoor_pm25": 280.0,
        "commute_mode": "Personal Car (ICE)",
        "daily_commute_km": 20.0,
        "implemented_actions": ["C-R Box", "Stoßlüften", "Zero-Idling"]
    }
    response = client.post("/api/impact/calculate", json=calc_req)
    assert response.status_code == 200
    impact = response.json()
    assert impact["pm25_prevented_ug"] > 1000.0
    assert impact["cigarette_equivalent_prevented"] > 0
    assert impact["daily_co2_saved_kg"] > 0
    assert impact["neighborhood_scale_pm25_kg_year"] > 0
    assert len(impact["explanation_narrative"]) > 20

def test_chat_assistant():
    """Verify GenAI conversation with domain-specific science explanations."""
    chat_req = {
        "message": "How do I build a Corsi-Rosenthal box and why is it better than single-filter?",
        "location": "Delhi-NCR, India",
        "current_aqi": 380,
        "persona": "iaq_engineer"
    }
    response = client.post("/api/chat", json=chat_req)
    assert response.status_code == 200
    chat_resp = response.json()
    assert "Corsi-Rosenthal" in chat_resp["reply"] or "CADR" in chat_resp["reply"]
    assert len(chat_resp["citations"]) > 0

def test_community_pledges():
    """Verify posting and retrieving community pledges."""
    new_pledge = {
        "neighborhood": "Sunrise Enclave",
        "family_name": "Bansal Family",
        "actions_pledged": ["Zero-Idling at School Gates", "C-R Box"],
        "community_message": "Organizing filter build bee with neighbors!"
    }
    post_resp = client.post("/api/community/pledge", json=new_pledge)
    assert post_resp.status_code == 200
    pledge = post_resp.json()
    assert pledge["family_name"] == "Bansal Family"

    get_resp = client.get("/api/community/pledges")
    assert get_resp.status_code == 200
    pledges = get_resp.json()
    assert any(p["family_name"] == "Bansal Family" for p in pledges)
