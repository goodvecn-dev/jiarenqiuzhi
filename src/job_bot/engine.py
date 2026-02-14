from __future__ import annotations

import asyncio
from dataclasses import dataclass

from playwright.async_api import async_playwright

from .matcher import JobMatcher
from .models import ApplyResult, CandidateProfile
from .platforms.base import PlatformAdapter
from .qa import QAEngine


@dataclass(slots=True)
class PlatformCredential:
    username: str
    password: str


class JobApplyEngine:
    def __init__(self, adapters: list[PlatformAdapter], matcher: JobMatcher, qa_engine: QAEngine):
        self.adapters = adapters
        self.matcher = matcher
        self.qa_engine = qa_engine

    async def run_once(self, profile: CandidateProfile, credentials: dict[str, PlatformCredential], dry_run: bool = True) -> list[ApplyResult]:
        results: list[ApplyResult] = []

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            for adapter in self.adapters:
                cred = credentials.get(adapter.name)
                if cred is None:
                    results.append(ApplyResult(platform=adapter.name, job_id="-", success=False, reason="missing credential"))
                    continue

                context = await browser.new_context()
                page = await context.new_page()

                await adapter.login(page, cred.username, cred.password)
                postings = await adapter.search_jobs(page, profile)
                matches = self.matcher.filter_matches(profile, postings)

                for match in matches:
                    result = await adapter.apply(page, profile, match.posting, self.qa_engine, dry_run=dry_run)
                    result.metadata["score"] = match.score
                    result.metadata["matched_skills"] = match.matched_skills
                    results.append(result)

                await context.close()

            await browser.close()

        return results


def run_engine(profile: CandidateProfile, adapters: list[PlatformAdapter], credentials: dict[str, PlatformCredential], min_score: float, qa_rules: dict[str, str], dry_run: bool = True) -> list[ApplyResult]:
    engine = JobApplyEngine(adapters=adapters, matcher=JobMatcher(min_score=min_score), qa_engine=QAEngine(custom_rules=qa_rules))
    return asyncio.run(engine.run_once(profile=profile, credentials=credentials, dry_run=dry_run))
