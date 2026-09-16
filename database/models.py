from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database.engine import Base

class CitizenProfile(Base):
    """Tracks community engagement, points, and gamification to drive sustained participation."""
    __tablename__ = "citizens"

    id = Column(String, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    total_points = Column(Integer, default=0)
    current_badge = Column(String, default="Novice Observer")
    join_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    assessments = relationship("StreamAssessment", back_populates="citizen")

class StreamAssessment(Base):
    """Core environmental data model mapping to real-world stream conditions."""
    __tablename__ = "assessments"

    id = Column(String, primary_key=True, index=True)
    citizen_id = Column(String, ForeignKey("citizens.id"))
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Location Metadata
    stream_name = Column(String, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    
    # Raw Citizen Inputs
    water_clarity = Column(Integer)
    water_flow = Column(Integer)
    odor_level = Column(Integer)
    garbage_presence = Column(Integer)
    vegetation_cover = Column(Integer)
    user_notes = Column(Text, nullable=True)
    
    # Biological counts (Optional real-world metrics)
    mosquito_larvae_count = Column(Integer, default=0)
    
    # AI Processed Fields (Track 3)
    ai_verified = Column(Boolean, default=False)
    ai_confidence = Column(Float, default=0.0)
    ai_vision_summary = Column(Text, nullable=True)
    
    # Computed Analytics (Track 2 & 6)
    water_quality_index = Column(Float)
    vector_risk_score = Column(Float)
    
    citizen = relationship("CitizenProfile", back_populates="assessments")