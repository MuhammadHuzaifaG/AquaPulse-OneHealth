from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import desc
from typing import List

from database.engine import get_db
from database.models import StreamAssessment, CitizenProfile
from schemas.assessment_schemas import AssessmentCreate, AssessmentResponse
from services.onehealth_engine import OneHealthEngine

router = APIRouter(prefix="/api/v1", tags=["Assessments & Gamification"])
onehealth_engine = OneHealthEngine()

@router.post("/assessments", response_model=AssessmentResponse)
async def submit_assessment(
    data: AssessmentCreate, 
    db: AsyncSession = Depends(get_db)
):
    """
    Submit a new citizen science stream assessment. 
    Triggers AI validation, gamification tracking, and ecological risk calculations.
    """
    try:
        result = await onehealth_engine.process_assessment(db, data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process assessment: {str(e)}")

@router.get("/assessments/stream/{stream_name}")
async def get_stream_history(
    stream_name: str, 
    limit: int = 10, 
    db: AsyncSession = Depends(get_db)
):
    """
    Track 2: Data-to-Insight Dashboard
    Fetch historical data for a specific stream to plot trends over time.
    """
    query = select(StreamAssessment).where(
        StreamAssessment.stream_name.ilike(f"%{stream_name}%")
    ).order_by(desc(StreamAssessment.timestamp)).limit(limit)
    
    result = await db.execute(query)
    assessments = result.scalars().all()
    
    if not assessments:
        raise HTTPException(status_code=404, detail="No data found for this stream.")
        
    return assessments

@router.get("/leaderboard")
async def get_community_leaderboard(
    limit: int = 10, 
    db: AsyncSession = Depends(get_db)
):
    """
    Track 5: Community & Gamification
    Fetch top citizen scientists to drive sustained participation and community engagement.
    """
    query = select(CitizenProfile).order_by(desc(CitizenProfile.total_points)).limit(limit)
    result = await db.execute(query)
    citizens = result.scalars().all()
    
    return [
        {
            "username": c.username, 
            "points": c.total_points, 
            "badge": c.current_badge,
            "join_date": c.join_date
        } 
        for c in citizens
    ]