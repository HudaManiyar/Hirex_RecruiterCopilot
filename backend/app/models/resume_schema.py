from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re


class Education(BaseModel):
    degree: Optional[str] = None
    institution: Optional[str] = None
    year: Optional[str] = None
    cgpa: Optional[str] = None


class Experience(BaseModel):
    company: Optional[str] = None
    role: Optional[str] = None
    duration: Optional[str] = None
    description: Optional[str] = None

    @field_validator("description", mode="before")
    @classmethod
    def join_description_list(cls, v):
        if isinstance(v, list):
            return " ".join(str(item).strip() for item in v)
        return v


class Project(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    tech_stack: list[str] = Field(default_factory=list)


class ResumeSchema(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    education: list[Education] = Field(default_factory=list)
    experience: list[Experience] = Field(default_factory=list)
    skills: list[str] = Field(default_factory=list)
    projects: list[Project] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)
    total_years_experience: Optional[float] = None
    summary: Optional[str] = None

    @field_validator("total_years_experience", mode="before")
    @classmethod
    def normalize_years_experience(cls, v):
        if v is None or isinstance(v, (int, float)):
            return v
        if isinstance(v, str):
            # Extract first number found in strings like "10+", "over 10 years", "8 yrs", "15 months"
            match = re.search(r"(\d+(?:\.\d+)?)", v)
            if match:
                num = float(match.group(1))
                # crude unit handling: if the string says "months", convert to years
                if "month" in v.lower():
                    return round(num / 12, 1)
                return num
            return None  # couldn't parse anything numeric, don't crash
        return None

    @field_validator("certifications", mode="before")
    @classmethod
    def normalize_certifications(cls, v):
        if not v:
            return v
        result = []
        for item in v:
            if isinstance(item, dict):
                parts = [str(item.get(k)) for k in ("name", "institution", "date") if item.get(k)]
                result.append(", ".join(parts))
            else:
                result.append(str(item))
        return result