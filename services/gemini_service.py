from google import genai
from config import settings
import base64
import json
from typing import Optional  # <-- Add this import

class GeminiService:
    def __init__(self):
        self.client = genai.Client(api_key=settings.gemini_api_key)
        self.model = settings.gemini_model

    def generate_expert_environmental_analysis(self, metrics: dict, user_notes: str, image_base64: Optional[str] = None) -> dict:
        """
        Expert System Prompt enforcing rigorous One Health diagnostic reporting, 
        vector-borne disease forecasting, and actionable municipal/citizen interventions.
        """
        system_instruction = (
            "You are an elite European One Health Environmental Scientist and Public Health Epidemiologist. "
            "Your job is to analyze urban freshwater telemetry submitted by citizen scientists, cross-reference "
            "biodiversity indicators (macroinvertebrates), chemical parameters (pH, DO), and vector breeding risks "
            "to produce rigorous, life-saving, and policy-ready intelligence."
        )

        prompt = f"""
        Analyze the following comprehensive stream telemetry and field observation:
        - Stream Name: {metrics.get('stream_name')}
        - Water Quality Index (WQI): {metrics.get('wqi')}/100
        - Ecological Integrity Index (EII): {metrics.get('eii')}/100
        - Vector Disease Risk Score: {metrics.get('vector_risk')}/100
        - Physico-Chemicals: pH {metrics.get('ph')}, Dissolved Oxygen {metrics.get('do')} mg/L, Temp {metrics.get('temp')}°C
        - Odor Profile: {metrics.get('odor')}
        - Discharge Pipe Nearby: {metrics.get('pipe')}
        - Bio-indicators: Mayflies ({metrics.get('mayflies')}), Mosquito Larvae ({metrics.get('larvae')})
        - Citizen Field Notes: '{user_notes or "None"}'

        Return a strictly formatted JSON object with exact keys:
        {{
            "ai_diagnostic_report": "A thorough, professional 3-sentence scientific breakdown of the ecosystem's health, linking water stressors to biological decline and community health risks.",
            "municipal_action_plan": [
                "Specific engineering or policy action 1 for city planners",
                "Specific action 2 for environmental enforcement agencies"
            ],
            "citizen_action_plan": [
                "Actionable step 1 for local community members",
                "Actionable step 2 for stream stewards"
            ],
            "public_health_warning": "If vector risk or chemical threat is high, state a direct public health advisory; otherwise state 'No immediate public health hazard detected.'"
        }}
        """

        try:
            contents = [prompt]
            if image_base64:
                contents.insert(0, base64.b64decode(image_base64))

            response = self.client.models.generate_content(
                model=self.model,
                contents=contents,
                config={
                    "system_instruction": system_instruction,
                    "response_mime_type": "application/json"
                }
            )
            
            return json.loads(response.text.strip())
        except Exception as e:
            return {
                "ai_diagnostic_report": f"Telemetry indicates WQI at {metrics.get('wqi')}% with vector risk at {metrics.get('vector_risk')}%. Ecosystem requires standard monitoring.",
                "municipal_action_plan": ["Inspect local discharge channels for diffuse runoff.", "Verify riparian vegetation health."],
                "citizen_action_plan": ["Report unusual odors to municipal water authorities.", "Avoid direct water contact if turbidity is high."],
                "public_health_warning": "Routine monitoring advised."
            }