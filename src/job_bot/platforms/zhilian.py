from __future__ import annotations

from playwright.async_api import Page

from ..models import ApplyResult, CandidateProfile, JobPosting
from ..qa import QAEngine
from .base import PlatformAdapter


class ZhilianAdapter(PlatformAdapter):
    name = "zhilian"

    async def login(self, page: Page, username: str, password: str) -> None:
        await page.goto("https://www.zhaopin.com")
        # TODO: 根据页面结构完善登录动作

    async def search_jobs(self, page: Page, profile: CandidateProfile) -> list[JobPosting]:
        # TODO: 实际抓取页面岗位列表
        return [
            JobPosting(
                platform=self.name,
                job_id="zhilian-demo-1",
                title="招聘流程自动化工程师",
                company="样例人力",
                city=profile.city,
                description="搭建岗位匹配与自动投递链路",
                required_skills=["python", "招聘", "流程自动化"],
                apply_url="https://jobs.zhaopin.com/demo",
                extra_questions=["为什么适合本岗位？"],
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
