from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
import uvicorn
import os
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")
from config import settings
from routes.api_v1 import router as api_router
from routes.fhir_router import router as fhir_router
from database.engine import engine, Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize the database tables on startup (Production-ready SQLite/PostgreSQL setup)
    async with engine.begin() as conn:
        # In a strict production environment, use Alembic. 
        # For this hackathon deploy-ready version, we auto-create tables.
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Cleanup resources on shutdown
    await engine.dispose()

app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="Backend API for the AquaPulse OneHealth Intelligence Platform",
    lifespan=lifespan,
    docs_url="/docs", 
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Restrict to specific domains in strict production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure directories exist to prevent mount errors
os.makedirs("frontend/css", exist_ok=True)
os.makedirs("frontend/js", exist_ok=True)

# Mount individual subfolders so /css/... and /js/... resolve correctly
app.mount("/css", StaticFiles(directory="frontend/css"), name="css")
app.mount("/js", StaticFiles(directory="frontend/js"), name="js")

app.include_router(api_router)
app.include_router(fhir_router)

@app.get("/")
async def serve_frontend():
    """Serves the main frontend Single Page Application for Track 2 Data Dashboard."""
    index_path = os.path.join("frontend", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Frontend not found. Please ensure frontend/index.html exists."}

@app.get("/health")
async def health_check():
    """Endpoint for Docker/Kubernetes orchestration health checks."""
    return {
        "status": "healthy", 
        "service": settings.app_name, 
        "version": settings.version
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=settings.debug)