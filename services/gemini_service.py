from google import genai
from config import settings
import base64
import json

class GeminiService:
    def __init__(self):
        self.client = genai.Client(api_key=settings.gemini_api_key)
        self.model = settings.gemini_model

    def analyze_stream_image(self, image_base64: str, user_notes: str) -> dict:
        """Track 3: AI-Supported Assessment using Gemini Vision"""
        try:
            image_bytes = base64.b64decode(image_base64)
            prompt = f"""
            Analyze this stream image submitted by a citizen scientist.
            Citizen notes: '{user_notes or "None provided"}'
            
            Return ONLY a JSON object:
            {{
                "confidence": (float 0-100 representing how clearly the stream condition can be verified),
                "summary": "Brief, non-technical summary of water flow and vegetation."
            }}
            """
            response = self.client.models.generate_content(
                model=self.model,
                contents=[image_bytes, prompt]
            )
            cleaned = response.text.strip().replace("```json", "").replace("```", "")
            return json.loads(cleaned)
        except Exception as e:
             # Failsafe for production
            return {"confidence": 0.0, "summary": "Visual analysis unavailable."}

    def generate_story(self, metrics: dict) -> str:
        """Track 4: Awareness & Storytelling"""
        try:
            prompt = f"""
            Write a 2-sentence encouraging update for a citizen scientist about their local stream.
            Stream: {metrics['stream']}
            Water Quality: {metrics['quality']}
            Vector Disease Risk: {metrics['vector_risk']}/100.
            Keep it friendly, avoid dense jargon.
            """
            return self.client.models.generate_content(model=self.model, contents=prompt).text.strip()
        except:
            return "Thank you for monitoring your local stream! Your data helps keep the community healthy."