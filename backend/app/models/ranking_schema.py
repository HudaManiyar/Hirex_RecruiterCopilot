from pydantic import BaseModel, Field
from typing import Optional


class CandidateEvaluation(BaseModel):
    candidate_name: str
    source_file: Optional[str] = None
    grade: str
    matched_skills: list[str] = Field(default_factory=list)
    missing_skills: list[str] = Field(default_factory=list)
    evidence: list[str] = Field(default_factory=list)
    reasoning: str
    confidence: str
    suggested_interview_questions: list[str] = Field(default_factory=list)


class RankingResponse(BaseModel):
    evaluations: list[CandidateEvaluation] = Field(default_factory=list)