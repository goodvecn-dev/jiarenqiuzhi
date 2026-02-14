from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class WorkExperience:
    company: str
    title: str
    years: float
    skills: list[str] = field(default_factory=list)


@dataclass(slots=True)
class CandidateProfile:
    name: str
    city: str
    target_titles: list[str]
    experiences: list[WorkExperience]
    resume_path: str


@dataclass(slots=True)
class JobPosting:
    platform: str
    job_id: str
    title: str
    company: str
    city: str
    description: str
    required_skills: list[str]
    apply_url: str
    extra_questions: list[str] = field(default_factory=list)


@dataclass(slots=True)
class MatchResult:
    posting: JobPosting
    score: float
    matched_skills: list[str]


@dataclass(slots=True)
class ApplyResult:
    platform: str
    job_id: str
    success: bool
    reason: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
