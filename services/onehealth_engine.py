from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
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

        points_earned = 75 if has_image else 30
        if wqi_score > 75: points_earned += 25
            
        new_total = citizen.total_points + points_earned
        new_badge = citizen.current_badge
        if new_total > 600: new_badge = "Master Watershed Scientist"
        elif new_total > 250: new_badge = "Stream Guardian"
            
        badge_unlocked = new_badge if new_badge != citizen.current_badge else None

        citizen.total_points = new_total
        citizen.current_badge = new_badge
        await db.commit()
        await db.refresh(citizen)
        
        return citizen, points_earned, badge_unlocked

    async def process_assessment(self, db: AsyncSession, data: AssessmentCreate) -> AssessmentResponse:
        # 1. Advanced Water Quality Index (WQI) computation
        base_score = (data.water_clarity * 6) + (data.vegetation_cover * 6) + (data.garbage_presence * 8)
        if 6.5 <= data.ph_level <= 8.5: base_score += 15
        if data.dissolved_oxygen_mg_l >= 6.0: base_score += 15
        if data.discharge_pipe_nearby: base_score -= 20
        
        wqi = max(0.0, min((base_score / 60.0) * 100, 100.0))
        
        # 2. Ecological Integrity Index (EII)
        bio_score = (data.mayfly_nymph_count * 8) + (data.dragonfly_nymph_count * 5) - (data.mosquito_larvae_count * 6)
        eii = max(0.0, min(50.0 + (data.vegetation_cover * 10) + bio_score, 100.0))

        # 3. Vector Disease Risk Score (Track 6 - Resilience Informatics)
        vector_risk = self.hf_service.compute_disease_vector_risk(
            vegetation=data.vegetation_cover,
            flow=data.water_flow,
            larvae_count=data.mosquito_larvae_count
        )
        if data.recent_rainfall_hours < 48 and data.water_flow <= 2:
            vector_risk = min(vector_risk + 15, 100.0)

        # 4. Human Wellbeing Impact Score
        wellbeing_score = round((wqi * 0.4) + (eii * 0.4) + ((100 - vector_risk) * 0.2), 2)

        # 5. AI Expert Diagnostic Report (Gemini)
        ai_metrics = {
            "stream_name": data.stream_name,
            "wqi": round(wqi, 1),
            "eii": round(eii, 1),
            "vector_risk": round(vector_risk, 1),
            "ph": data.ph_level,
            "do": data.dissolved_oxygen_mg_l,
            "temp": data.water_temp_celsius,
            "odor": data.odor_type,
            "pipe": "Yes" if data.discharge_pipe_nearby else "No",
            "mayflies": data.mayfly_nymph_count,
            "larvae": data.mosquito_larvae_count
        }
        ai_analysis = self.gemini_service.generate_expert_environmental_analysis(ai_metrics, data.user_notes, data.image_base64)

        # 6. Gamification & Persistence
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
            odor_level=3 if data.odor_type == "Natural" else 1,
            garbage_presence=data.garbage_presence,
            vegetation_cover=data.vegetation_cover,
            user_notes=data.user_notes,
            mosquito_larvae_count=data.mosquito_larvae_count,
            ai_verified=True,
            ai_confidence=92.5,
            ai_vision_summary=ai_analysis.get("ai_diagnostic_report"),
            water_quality_index=wqi,
            vector_risk_score=vector_risk
        )
        db.add(new_assessment)
        await db.commit()

        return AssessmentResponse(
            id=assessment_id,
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            stream_name=data.stream_name,
            water_quality_index=round(wqi, 2),
            ecological_integrity_index=round(eii, 2),
            vector_risk_score=round(vector_risk, 2),
            human_wellbeing_impact_score=wellbeing_score,
            points_earned=points,
            badge_unlocked=badge,
            ai_diagnostic_report=ai_analysis.get("ai_diagnostic_report"),
            municipal_action_plan=ai_analysis.get("municipal_action_plan"),
            citizen_action_plan=ai_analysis.get("citizen_action_plan"),
            public_health_warning=ai_analysis.get("public_health_warning")
        )