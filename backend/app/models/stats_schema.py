from pydantic import BaseModel


class CategoryCount(BaseModel):
    category: str
    count: int


class SourceBreakdown(BaseModel):
    real: int
    synthetic: int


class StatsResponse(BaseModel):
    total_resumes: int
    categories: list[CategoryCount]
    source_breakdown: SourceBreakdown
