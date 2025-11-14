"""
FastAPI main application
"""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.database import connect_to_mongo, close_mongo_connection
from app.config import settings
from app.agents.agent1_ingestion import IngestionAgent
from app.agents.agent2_cleaning import CleaningCorrelationAgent
from app.agents.agent3_prediction import PredictiveCongestionAgent
from app.api.routes import segments, zones, predictions, health, explain

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Scheduler instance
scheduler = AsyncIOScheduler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("Starting Smart City Dashboard...")
    
    # Connect to MongoDB
    await connect_to_mongo()
    
    # Start scheduler
    await setup_scheduler()
    scheduler.start()
    logger.info("Scheduler started")
    
    yield
    
    # Shutdown
    logger.info("Shutting down...")
    scheduler.shutdown()
    await close_mongo_connection()
    logger.info("Shutdown complete")


async def setup_scheduler():
    """Setup APScheduler jobs for agents"""
    ingestion_agent = IngestionAgent()
    cleaning_agent = CleaningCorrelationAgent()
    prediction_agent = PredictiveCongestionAgent()
    
    # Agent 1: Data Ingestion
    # Traffic: every 30 seconds (or configured interval)
    scheduler.add_job(
        ingestion_agent.ingest_all_sources,
        "interval",
        seconds=settings.ingestion_interval_traffic,
        id="ingestion_traffic",
        replace_existing=True
    )
    
    # Agent 2: Cleaning + Correlation
    # Run every 2 minutes (after ingestion has data)
    scheduler.add_job(
        cleaning_agent.process_raw_data,
        "interval",
        seconds=120,  # 2 minutes
        id="cleaning_correlation",
        replace_existing=True
    )
    
    # Agent 3: Prediction
    # Run every 5 minutes
    scheduler.add_job(
        prediction_agent.generate_predictions,
        "interval",
        seconds=300,  # 5 minutes
        id="prediction",
        replace_existing=True
    )
    
    logger.info("Scheduler jobs configured")


# Create FastAPI app
app = FastAPI(
    title="Smart City Dashboard API",
    description="NYC DOT Smart City Dashboard - Traffic, Transit, and Air Quality Monitoring",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(segments.router)
app.include_router(zones.router)
app.include_router(predictions.router)
app.include_router(health.router)
app.include_router(explain.router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Smart City Dashboard",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "segments": "/api/segments/current",
            "zones": "/api/zones/current",
            "predictions": "/api/predictions",
            "health": "/api/health",
            "validation": "/api/health/validation",
            "explain": "/api/explain/hotspots"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )

