from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class AssessmentCreate(BaseModel):
    citizen_username: str = Field(..., example="Dr_EcoSteward")
    stream_name: str = Field(..., example="Mondego Urban Canal Segment 4B")
    latitude: float = Field(..., ge=-90, le=90, example=40.2033)
    longitude: float = Field(..., ge=-180, le=180, example=-8.4103)
    
    # Physico-Chemical Telemetry
    water_clarity: int = Field(..., ge=1, le=5, description="1: Opaque/Muddy, 5: Crystal Clear")
    water_flow: int = Field(..., ge=1, le=5, description="1: Stagnant Pool, 5: Rapid Torrent")
    odor_type: str = Field(default="Natural", description="Natural, Sewage, Chemical, Rotten Egg, Musty")
    garbage_presence: int = Field(..., ge=1, le=5, description="1: Severe Dumping, 5: Pristine")
    vegetation_cover: int = Field(..., ge=1, le=5, description="1: Concrete Channel, 5: Dense Riparian Buffer")
    
    # Advanced Scientific Fields
    ph_level: Optional[float] = Field(default=7.2, ge=0.0, le=14.0, description="Standard pH units")
    dissolved_oxygen_mg_l: Optional[float] = Field(default=6.5, ge=0.0, le=20.0, description="mg/L DO")
    water_temp_celsius: Optional[float] = Field(default=18.5, description="Water temperature in °C")
    recent_rainfall_hours: int = Field(default=0, description="Hours since last heavy rainfall event")
    discharge_pipe_nearby: bool = Field(default=False, description="Presence of stormwater or industrial outflow nearby")
    
    # Biological Indicators (Macroinvertebrate counts)
    mayfly_nymph_count: int = Field(default=0, ge=0, description="Sensitive bio-indicator")
    dragonfly_nymph_count: int = Field(default=0, ge=0, description="Moderate tolerance bio-indicator")
    mosquito_larvae_count: int = Field(default=0, ge=0, description="Vector risk bio-indicator")
    
    user_notes: Optional[str] = Field(default=None, description="Detailed field notes from observer")
    image_base64: Optional[str] = Field(default=None, description="Base64 encoded field photo")

class AssessmentResponse(BaseModel):
    id: str
    timestamp: datetime
    stream_name: str
    water_quality_index: float
    ecological_integrity_index: float
    vector_risk_score: float
    human_wellbeing_impact_score: float
    
    # Gamification & Rewards
    points_earned: int
    badge_unlocked: Optional[str] = None
    
    # Expert AI Insights & Action Plan
    ai_diagnostic_report: str
    municipal_action_plan: List[str]
    citizen_action_plan: List[str]
    public_health_warning: Optional[str] = None