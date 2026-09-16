import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "AquaPulse OneHealth (Production)"
    version: str = "2.0.0"
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Using SQLite for hackathon portability, easily swapped to PostgreSQL for real deployment
    database_url: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./aquapulse.db")
    
    # AI Models & APIs
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    hf_api_key: str = os.getenv("HF_API_KEY", "")
    
    gemini_model: str = "gemini-2.5-flash"
    hf_model_repo: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    class Config:
        env_file = ".env"

settings = Settings()