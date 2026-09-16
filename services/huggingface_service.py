from config import settings
# import requests # Used if calling actual HF Inference API

class HuggingFaceService:
    def __init__(self):
        # In a full deployment, this connects to the HF Inference API
        self.api_url = f"https://api-inference.huggingface.co/models/{settings.hf_model_repo}"
        self.headers = {"Authorization": f"Bearer {settings.hf_api_key}"}

    def compute_disease_vector_risk(self, vegetation: int, flow: int, larvae_count: int) -> float:
        """
        Track 6: Resilience Informatics.
        Calculates environmental risk for vector-borne diseases based on physical stream conditions.
        """
        risk_score = 0.0
        
        # Flow: Stagnant water (1) is high risk, fast flow (5) is low risk
        if flow <= 2: risk_score += 40
        elif flow == 3: risk_score += 15
        
        # Vegetation: Dense vegetation (5) near stagnant water increases habitat risk
        if vegetation >= 4: risk_score += 20
        
        # Direct biological observation
        if larvae_count > 0:
            risk_score += min(larvae_count * 10, 40)
            
        return min(risk_score, 100.0)