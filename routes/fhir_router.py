from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database.engine import get_db
from database.models import StreamAssessment, CitizenProfile
from schemas.fhir_schemas import (
    FHIRObservation, FHIRRiskAssessment, FHIRCodeableConcept, 
    FHIRCoding, FHIRValueQuantity
)

router = APIRouter(prefix="/api/fhir", tags=["Digital Health Standards (Track 7)"])

@router.get("/Observation/{assessment_id}", response_model=FHIRObservation)
async def export_observation_to_fhir(
    assessment_id: str, 
    db: AsyncSession = Depends(get_db)
):
    """
    Track 7: Transforms a citizen stream assessment into a standard HL7 FHIR R4 
    Observation resource for interoperability with European public health systems.
    """
    result = await db.execute(
        select(StreamAssessment, CitizenProfile)
        .join(CitizenProfile)
        .where(StreamAssessment.id == assessment_id)
    )
    row = result.first()
    
    if not row:
        raise HTTPException(status_code=404, detail="Assessment not found")
        
    assessment, citizen = row
    timestamp_iso = assessment.timestamp.isoformat() + "Z"
    
    # Map Water Quality Index string
    wqi_category = "Good" if assessment.water_quality_index >= 60 else "Poor"
    interpretation_code = "N" if wqi_category == "Good" else "A"
    
    return FHIRObservation(
        id=f"obs-{assessment.id}",
        effectiveDateTime=timestamp_iso,
        performer=[{"display": citizen.username}],
        code=FHIRCodeableConcept(
            coding=[FHIRCoding(
                system="http://loinc.org",
                code="77598-1", 
                display="Water quality assessment"
            )],
            text="Citizen Science Stream Water Quality Index"
        ),
        valueQuantity=FHIRValueQuantity(
            value=round(assessment.water_quality_index, 2),
            unit="WQI Score",
            code="{score}"
        ),
        interpretation=[FHIRCodeableConcept(
            coding=[FHIRCoding(
                system="http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation",
                code=interpretation_code,
                display=wqi_category
            )],
            text=f"Stream condition categorized as {wqi_category}"
        )]
    )

@router.get("/RiskAssessment/{assessment_id}", response_model=FHIRRiskAssessment)
async def export_risk_to_fhir(
    assessment_id: str, 
    db: AsyncSession = Depends(get_db)
):
    """
    Track 7: Transforms AI-computed environmental vector risks into an HL7 FHIR 
    RiskAssessment resource, directly alerting healthcare systems of ecological threats.
    """
    result = await db.execute(select(StreamAssessment).where(StreamAssessment.id == assessment_id))
    assessment = result.scalars().first()
    
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
        
    timestamp_iso = assessment.timestamp.isoformat() + "Z"
    
    return FHIRRiskAssessment(
        id=f"risk-{assessment.id}",
        occurrenceDateTime=timestamp_iso,
        basis=[{"reference": f"Observation/obs-{assessment.id}"}],
        prediction=[{
            "outcome": {
                "text": "Vector-borne disease (e.g., Culex mosquito) proliferation risk due to stream eutrophication/stagnation."
            },
            "probabilityDecimal": round(assessment.vector_risk_score / 100.0, 2),
            "rationale": "Score derived via OneHealth Engine analyzing physical flow, vegetation cover, and larvae presence."
        }],
        note=[{"text": "Data sourced via OneAquaHealth citizen science platform and verified by AI."}]
    )