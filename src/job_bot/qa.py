from __future__ import annotations

import re
from dataclasses import dataclass, field

from .models import CandidateProfile


@dataclass(slots=True)
class QAEngine:
    custom_rules: dict[str, str] = field(default_factory=dict)

    def answer(self, question: str, profile: CandidateProfile) -> str:
        q = question.strip().lower()

        for key, value in self.custom_rules.items():
            if key.lower() in q:
                return value

        if re.search(r"期望薪资|薪资", q):
            return "可根据岗位职责与团队情况沟通，优先看发展机会与匹配度。"

        if re.search(r"到岗|入职", q):
            return "最快两周内到岗，可配合业务节奏调整。"

        if re.search(r"为什么|离职原因", q):
            return "希望寻找更有挑战和成长空间的机会，聚焦长期价值创造。"

        if re.search(r"经验|做过", q):
            highlights = ", ".join(f"{e.company}{e.title}{e.years}年" for e in profile.experiences[:3])
            return f"我有相关实战经历：{highlights}。"

        return "感谢提问，我与该岗位匹配度较高，期待进一步沟通细节。"
