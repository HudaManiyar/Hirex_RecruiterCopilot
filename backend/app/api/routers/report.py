from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies import get_report_service
from app.api.schemas import ReportRequest, ReportResponse
from app.services.report_service import ReportService

router = APIRouter(prefix="/report", tags=["report"])


@router.post("/generate", response_model=ReportResponse)
def generate_report(
    request: ReportRequest,
    service: ReportService = Depends(get_report_service),
) -> ReportResponse:
    try:
        result = service.generate_report(request.jd_text, top_k=request.top_k)
        return ReportResponse(
            jd_analysis=result["jd_analysis"],
            candidate_evaluations=result["candidate_evaluations"],
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Report generation failed: {e}")
