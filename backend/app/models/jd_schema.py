from pydantic import BaseModel, Field
from typing import Optional


class JDAnalysis(BaseModel):
    quality_score: float  # out of 10
    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)
    missing_elements: list[str] = Field(default_factory=list)  # e.g. "years of experience", "salary range"
    ambiguous_phrases: list[str] = Field(default_factory=list)  # vague terms flagged
    improved_jd: str