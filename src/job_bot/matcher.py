from __future__ import annotations

from .models import CandidateProfile, JobPosting, MatchResult


class JobMatcher:
    def __init__(self, min_score: float = 0.35):
        self.min_score = min_score

    def extract_candidate_skills(self, profile: CandidateProfile) -> set[str]:
        skills: set[str] = set()
        for exp in profile.experiences:
            skills.update(s.lower() for s in exp.skills)
            skills.add(exp.title.lower())
        skills.update(t.lower() for t in profile.target_titles)
        return skills

    def score(self, profile: CandidateProfile, posting: JobPosting) -> MatchResult:
        candidate_skills = self.extract_candidate_skills(profile)
        required = {s.lower() for s in posting.required_skills}

        if not required:
            base_score = 0.3
            matched = []
        else:
            overlap = candidate_skills & required
            base_score = len(overlap) / len(required)
            matched = sorted(overlap)

        title_bonus = 0.2 if any(t.lower() in posting.title.lower() for t in profile.target_titles) else 0.0
        city_bonus = 0.1 if profile.city.lower() in posting.city.lower() else 0.0
        final_score = min(base_score + title_bonus + city_bonus, 1.0)

        return MatchResult(posting=posting, score=final_score, matched_skills=matched)

    def filter_matches(self, profile: CandidateProfile, postings: list[JobPosting]) -> list[MatchResult]:
        ranked = [self.score(profile, p) for p in postings]
        return sorted((r for r in ranked if r.score >= self.min_score), key=lambda x: x.score, reverse=True)
