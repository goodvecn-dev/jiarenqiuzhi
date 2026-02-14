from job_bot.a2a import A2AMessage, build_apply_report
from job_bot.matcher import JobMatcher
from job_bot.models import ApplyResult, CandidateProfile, JobPosting, WorkExperience
from job_bot.qa import QAEngine


def sample_profile() -> CandidateProfile:
    return CandidateProfile(
        name="张三",
        city="北京",
        target_titles=["自动化工程师"],
        experiences=[
            WorkExperience(company="A", title="Python工程师", years=2, skills=["Python", "Playwright"])
        ],
        resume_path="resume.pdf",
    )


def test_matcher_filters_jobs():
    profile = sample_profile()
    posting = JobPosting(
        platform="boss",
        job_id="1",
        title="Python 自动化工程师",
        company="X",
        city="北京",
        description="",
        required_skills=["Python", "Playwright"],
        apply_url="https://example.com",
    )
    matcher = JobMatcher(min_score=0.5)
    results = matcher.filter_matches(profile, [posting])
    assert len(results) == 1
    assert results[0].score >= 0.5


def test_qa_default_answer():
    profile = sample_profile()
    qa = QAEngine()
    answer = qa.answer("请问你的期望薪资是？", profile)
    assert "沟通" in answer


def test_a2a_roundtrip():
    msg = A2AMessage(action="ping", payload={"k": 1})
    decoded = A2AMessage.from_json(msg.to_json())
    assert decoded.action == "ping"
    assert decoded.payload["k"] == 1

    report = build_apply_report([ApplyResult(platform="boss", job_id="1", success=True)])
    assert report.action == "apply.report"
