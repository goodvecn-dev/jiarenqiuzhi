from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from typing import Any

from .models import ApplyResult


@dataclass(slots=True)
class A2AMessage:
    action: str
    payload: dict[str, Any]

    def to_json(self) -> str:
        return json.dumps({"action": self.action, "payload": self.payload}, ensure_ascii=False)

    @classmethod
    def from_json(cls, raw: str) -> "A2AMessage":
        data = json.loads(raw)
        return cls(action=data["action"], payload=data.get("payload", {}))


def build_apply_report(results: list[ApplyResult]) -> A2AMessage:
    return A2AMessage(action="apply.report", payload={"results": [asdict(r) for r in results]})
