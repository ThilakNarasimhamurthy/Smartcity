"""
API routes for zone data
"""
from fastapi import APIRouter
from datetime import datetime
from app.database import get_database
from app.models.schemas import ZonesResponse, ZoneState

router = APIRouter(prefix="/api/zones", tags=["zones"])


@router.get("/current", response_model=ZonesResponse)
async def get_current_zones():
    """
    Get current zone states
    
    Returns:
        Current zone states
    """
    db = get_database()
    
    # Get most recent timestamp bucket
    latest = await db.zones_state.find_one(
        {},
        sort=[("timestamp_bucket", -1)]
    )
    
    if not latest:
        return ZonesResponse(
            zones=[],
            count=0,
            timestamp=datetime.utcnow()
        )
    
    latest_bucket = latest["timestamp_bucket"]
    
    # Fetch zones
    cursor = db.zones_state.find({"timestamp_bucket": latest_bucket})
    zones_docs = await cursor.to_list(length=100)
    
    # Convert to Pydantic models
    zones = [ZoneState(**doc) for doc in zones_docs]
    
    return ZonesResponse(
        zones=zones,
        count=len(zones),
        timestamp=datetime.utcnow()
    )


@router.get("/{zone_id}", response_model=ZoneState)
async def get_zone(zone_id: str):
    """
    Get current state for a specific zone
    
    Args:
        zone_id: Zone identifier
    
    Returns:
        Zone state
    """
    db = get_database()
    
    zone = await db.zones_state.find_one(
        {"zone_id": zone_id},
        sort=[("timestamp_bucket", -1)]
    )
    
    if not zone:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Zone not found")
    
    return ZoneState(**zone)

