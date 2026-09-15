from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies import get_jd_service
from app.api.schemas import JDAnalyzeRequest
from app.models.jd_schema import JDAnalysis
from app.services.jd_service import JDService

router = APIRouter(prefix="/jd", tags=["job-description"])


@router.post("/analyze", response_model=JDAnalysis)
def analyze_jd(
    request: JDAnalyzeRequest,
    service: JDService = Depends(get_jd_service),
) -> JDAnalysis:
    try:
        return service.analyze(request.jd_text)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"JD analysis failed: {e}")
