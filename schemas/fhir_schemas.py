from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class FHIRCoding(BaseModel):
    system: str
    code: str
    display: str

class FHIRCodeableConcept(BaseModel):
    coding: List[FHIRCoding]
    text: str

class FHIRValueQuantity(BaseModel):
    value: float
    unit: str
    system: str = "http://unitsofmeasure.org"
    code: str

class FHIRObservation(BaseModel):
    resourceType: str = "Observation"
    id: str
    status: str = "final"
    category: List[FHIRCodeableConcept] = Field(default_factory=list)
    code: FHIRCodeableConcept
    subject: Dict[str, str] = Field(default_factory=lambda: {"display": "Urban Freshwater Ecosystem Stream Segment"})
    effectiveDateTime: str
    performer: List[Dict[str, str]]
    valueQuantity: Optional[FHIRValueQuantity] = None
    interpretation: Optional[List[FHIRCodeableConcept]] = None

class FHIRRiskAssessment(BaseModel):
    resourceType: str = "RiskAssessment"
    id: str
    status: str = "final"
    subject: Dict[str, str] = Field(default_factory=lambda: {"display": "Local Urban Community Health"})
    occurrenceDateTime: str
    basis: List[Dict[str, str]]
    prediction: List[Dict[str, Any]]
    note: List[Dict[str, str]]