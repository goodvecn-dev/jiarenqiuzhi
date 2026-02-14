from __future__ import annotations

from abc import ABC, abstractmethod

from playwright.async_api import Page

from ..models import ApplyResult, CandidateProfile, JobPosting
from ..qa import QAEngine


class PlatformAdapter(ABC):
    name: str

    @abstractmethod
    async def login(self, page: Page, username: str, password: str) -> None:
        ...

    @abstractmethod
    async def search_jobs(self, page: Page, profile: CandidateProfile) -> list[JobPosting]:
        ...

    @abstractmethod
    async def apply(self, page: Page, profile: CandidateProfile, posting: JobPosting, qa_engine: QAEngine, dry_run: bool = True) -> ApplyResult:
        ...
