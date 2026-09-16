from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class AssessmentCreate(BaseModel):
    citizen_username: str = Field(..., example="EcoWarrior99")
    stream_name: str = Field(..., example="Mondego River Tributary")
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    
    # Simplified UX for Track 1
    water_clarity: int = Field(..., ge=1, le=5, description="1: Murky, 5: Clear")
    water_flow: int = Field(..., ge=1, le=5, description="1: Stagnant, 5: Fast")
    odor_level: int = Field(..., ge=1, le=5, description="1: Bad odor, 5: Natural")
    garbage_presence: int = Field(..., ge=1, le=5, description="1: Heavy litter, 5: Clean")
    vegetation_cover: int = Field(..., ge=1, le=5, description="1: Concrete, 5: Dense Nature")
    
    mosquito_larvae_count: int = Field(default=0, ge=0)
    user_notes: Optional[str] = None
    
    # Base64 string for multimodal AI processing
    image_base64: Optional[str] = None

class AssessmentResponse(BaseModel):
    id: str
    timestamp: datetime
    stream_name: str
    water_quality_index: float
    vector_risk_score: float
    
    # Gamification feedback
    points_earned: int
    badge_unlocked: Optional[str] = None
    
    # AI Feedback
    ai_story: str
    recommended_actions: List[str]

    class Config:
        from_attributes = True