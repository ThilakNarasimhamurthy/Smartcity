"""
API routes for segment data
"""
from fastapi import APIRouter, Query
from typing import Optional
from datetime import datetime
from app.database import get_database
from app.models.schemas import SegmentsResponse, SegmentState

router = APIRouter(prefix="/api/segments", tags=["segments"])


@router.get("/current", response_model=SegmentsResponse)
async def get_current_segments(
    limit: int = Query(100, ge=1, le=1000),
    zone_id: Optional[str] = None
):
    """
    Get current segment states
    
    Args:
        limit: Maximum number of segments to return
        zone_id: Optional zone filter
    
    Returns:
        Current segment states
    """
    db = get_database()
    
    # Get most recent timestamp bucket
    latest = await db.segments_state.find_one(
        {},
        sort=[("timestamp_bucket", -1)]
    )
    
    if not latest:
        return SegmentsResponse(
            segments=[],
            count=0,
            timestamp=datetime.utcnow(),
            data_freshness_minutes=None
        )
    
    latest_bucket = latest["timestamp_bucket"]
    
    # Calculate data freshness
    if isinstance(latest_bucket, datetime):
        age = datetime.utcnow() - latest_bucket
        freshness_minutes = int(age.total_seconds() / 60)
    else:
        freshness_minutes = None
    
    # Build query
    query = {"timestamp_bucket": latest_bucket}
    # TODO: Add zone_id filtering when zone boundaries are properly defined
    
    # Fetch segments
    cursor = db.segments_state.find(query).limit(limit)
    segments_docs = await cursor.to_list(length=limit)
    
    # Convert to Pydantic models
    segments = [SegmentState(**doc) for doc in segments_docs]
    
    return SegmentsResponse(
        segments=segments,
        count=len(segments),
        timestamp=datetime.utcnow(),
        data_freshness_minutes=freshness_minutes
    )


@router.get("/{segment_id}", response_model=SegmentState)
async def get_segment(segment_id: str):
    """
    Get current state for a specific segment
    
    Args:
        segment_id: Segment identifier
    
    Returns:
        Segment state
    """
    db = get_database()
    
    segment = await db.segments_state.find_one(
        {"segment_id": segment_id},
        sort=[("timestamp_bucket", -1)]
    )
    
    if not segment:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Segment not found")
    
    return SegmentState(**segment)

