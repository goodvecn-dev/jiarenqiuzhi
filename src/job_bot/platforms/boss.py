from __future__ import annotations

from playwright.async_api import Page

from ..models import ApplyResult, CandidateProfile, JobPosting
from ..qa import QAEngine
from .base import PlatformAdapter


class BossAdapter(PlatformAdapter):
    name = "boss"

    async def login(self, page: Page, username: str, password: str) -> None:
        await page.goto("https://www.zhipin.com")
        # TODO: 根据页面结构完善登录动作

    async def search_jobs(self, page: Page, profile: CandidateProfile) -> list[JobPosting]:
        # TODO: 实际抓取页面岗位列表
        return [
            JobPosting(
                platform=self.name,
                job_id="boss-demo-1",
                title="Python 自动化工程师",
                company="示例科技",
                city=profile.city,
                description="负责招聘自动化与流程优化",
                required_skills=["python", "playwright", "自动化"],
                apply_url="https://www.zhipin.com/job_detail/demo",
                extra_questions=["你对自动化招聘流程的理解？"],
            )
        ]

    async def apply(self, page: Page, profile: CandidateProfile, posting: JobPosting, qa_engine: QAEngine, dry_run: bool = True) -> ApplyResult:
        if dry_run:
            return ApplyResult(platform=self.name, job_id=posting.job_id, success=True, reason="dry-run")

        await page.goto(posting.apply_url)
        # TODO: 上传简历、点击投递、填写问题答案
        for question in posting.extra_questions:
            _ = qa_engine.answer(question, profile)

        return ApplyResult(platform=self.name, job_id=posting.job_id, success=True)
