from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies import get_stats_service
from app.models.stats_schema import StatsResponse
from app.services.stats_service import StatsService

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("", response_model=StatsResponse)
def get_stats(
    service: StatsService = Depends(get_stats_service),
) -> StatsResponse:
    try:
        return StatsResponse(**service.get_stats())
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Stats lookup failed: {e}")
