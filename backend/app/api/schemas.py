from pydantic import BaseModel, Field

from app.models.jd_schema import JDAnalysis
from app.models.ranking_schema import CandidateEvaluation


class JDAnalyzeRequest(BaseModel):
    jd_text: str = Field(..., min_length=1, description="Raw job description text to analyze")


class RankingRequest(BaseModel):
    job_requirement: str = Field(..., min_length=1, description="Job requirement / JD text to match candidates against")
    top_k: int = Field(5, ge=1, le=50, description="Number of top candidates to retrieve and evaluate")


class ReportRequest(BaseModel):
    jd_text: str = Field(..., min_length=1, description="Raw job description text")
    top_k: int = Field(5, ge=1, le=50, description="Number of top candidates to include in the report")


class ReportResponse(BaseModel):
    jd_analysis: JDAnalysis
    candidate_evaluations: list[CandidateEvaluation] = Field(default_factory=list)
