from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies import get_ranking_service
from app.api.schemas import RankingRequest
from app.models.ranking_schema import RankingResponse
from app.services.ranking_service import RankingService

router = APIRouter(prefix="/ranking", tags=["ranking"])


@router.post("/rank", response_model=RankingResponse)
def rank_candidates(
    request: RankingRequest,
    service: RankingService = Depends(get_ranking_service),
) -> RankingResponse:
    try:
        return service.rank(request.job_requirement, top_k=request.top_k)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Ranking failed: {e}")
