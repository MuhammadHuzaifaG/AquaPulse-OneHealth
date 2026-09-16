from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
import uuid
import datetime

from database.models import CitizenProfile, StreamAssessment
from schemas.assessment_schemas import AssessmentCreate, AssessmentResponse
from services.huggingface_service import HuggingFaceService
from services.gemini_service import GeminiService

class OneHealthEngine:
    def __init__(self):
        self.hf_service = HuggingFaceService()
        self.gemini_service = GeminiService()

    async def _handle_gamification(self, db: AsyncSession, username: str, has_image: bool, wqi_score: float) -> tuple[CitizenProfile, int, str]:
        """Track 5: Community & Gamification - Real database tracking of user progress"""
        # Fetch or create user
        result = await db.execute(select(CitizenProfile).where(CitizenProfile.username == username))
        citizen = result.scalars().first()
        
        if not citizen:
            citizen = CitizenProfile(
                id=str(uuid.uuid4()),
                username=username,
                total_points=0,
                current_badge="Novice Observer"
            )
            db.add(citizen)
            await db.commit()
            await db.refresh(citizen)

        # Calculate points for this specific action
        points_earned = 50 if has_image else 20
        if wqi_score > 80: 
            points_earned += 10 # Bonus for finding healthy streams
            
        new_total = citizen.total_points + points_earned
        
        # Level up logic
        new_badge = citizen.current_badge
        if new_total > 500 and citizen.current_badge != "Eco-Steward Elite":
            new_badge = "Eco-Steward Elite"
        elif new_total > 200 and citizen.current_badge == "Novice Observer":
            new_badge = "Stream Guardian"
            
        badge_unlocked = new_badge if new_badge != citizen.current_badge else None

        # Update user profile
        citizen.total_points = new_total
        citizen.current_badge = new_badge
        await db.commit()
        await db.refresh(citizen)
        
        return citizen, points_earned, badge_unlocked

    async def process_assessment(self, db: AsyncSession, data: AssessmentCreate) -> AssessmentResponse:
        """Core pipeline processing the incoming citizen data into actionable insights."""
        
        # 1. Compute Base Indexes (Track 2)
        score_base = (data.water_clarity * 5) + (data.odor_level * 5) + (data.garbage_presence * 10)
        wqi = min((score_base / 50.0) * 100, 100.0)
        
        # 2. Vector Risk (Track 6) - Using HuggingFace heuristic model
        vector_risk = self.hf_service.compute_disease_vector_risk(
            vegetation=data.vegetation_cover,
            flow=data.water_flow,
            larvae_count=data.mosquito_larvae_count
        )

        # 3. AI Vision Analysis (Track 3)
        ai_result = {"confidence": 0.0, "summary": "No visual data."}
        if data.image_base64:
            ai_result = self.gemini_service.analyze_stream_image(data.image_base64, data.user_notes)

        # 4. Generate Story (Track 4)
        wqi_category = "Good" if wqi > 60 else "Poor"
        story_context = {"stream": data.stream_name, "quality": wqi_category, "vector_risk": vector_risk}
        story = self.gemini_service.generate_story(story_context)

        # 5. DB Interactions: Gamification & Saving Assessment
        citizen, points, badge = await self._handle_gamification(db, data.citizen_username, bool(data.image_base64), wqi)
        
        assessment_id = str(uuid.uuid4())
        new_assessment = StreamAssessment(
            id=assessment_id,
            citizen_id=citizen.id,
            stream_name=data.stream_name,
            latitude=data.latitude,
            longitude=data.longitude,
            water_clarity=data.water_clarity,
            water_flow=data.water_flow,
            odor_level=data.odor_level,
            garbage_presence=data.garbage_presence,
            vegetation_cover=data.vegetation_cover,
            user_notes=data.user_notes,
            mosquito_larvae_count=data.mosquito_larvae_count,
            ai_verified=ai_result.get("confidence", 0) > 70.0,
            ai_confidence=ai_result.get("confidence", 0.0),
            ai_vision_summary=ai_result.get("summary"),
            water_quality_index=wqi,
            vector_risk_score=vector_risk
        )
        
        db.add(new_assessment)
        await db.commit()

        # 6. Generate Recommendations
        actions = []
        if data.garbage_presence <= 2: actions.append("Organize a community cleanup.")
        if vector_risk > 70: actions.append("High mosquito risk: clear debris blocking flow.")

        return AssessmentResponse(
            id=assessment_id,
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            stream_name=data.stream_name,
            water_quality_index=round(wqi, 2),
            vector_risk_score=round(vector_risk, 2),
            points_earned=points,
            badge_unlocked=badge,
            ai_story=story,
            recommended_actions=actions if actions else ["Great job! Keep monitoring."]
        )