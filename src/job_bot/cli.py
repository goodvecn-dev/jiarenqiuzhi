from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml

from .engine import PlatformCredential, run_engine
from .models import CandidateProfile, WorkExperience
from .platforms.boss import BossAdapter
from .platforms.zhilian import ZhilianAdapter


def load_config(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def build_profile(raw: dict) -> CandidateProfile:
    experiences = [
        WorkExperience(
            company=e["company"],
            title=e["title"],
            years=float(e["years"]),
            skills=e.get("skills", []),
        )
        for e in raw["experiences"]
    ]
    return CandidateProfile(
        name=raw["name"],
        city=raw["city"],
        target_titles=raw["target_titles"],
        experiences=experiences,
        resume_path=raw["resume_path"],
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Auto job apply bot")
    sub = parser.add_subparsers(dest="command", required=True)

    run_parser = sub.add_parser("run")
    run_parser.add_argument("--config", required=True)
    run_parser.add_argument("--dry-run", action="store_true")

    args = parser.parse_args()

    if args.command == "run":
        cfg = load_config(Path(args.config))
        profile = build_profile(cfg["candidate"])
        credentials = {
            name: PlatformCredential(username=v["username"], password=v["password"])
            for name, v in cfg["platform_credentials"].items()
        }
        adapters = [BossAdapter(), ZhilianAdapter()]

        results = run_engine(
            profile=profile,
            adapters=adapters,
            credentials=credentials,
            min_score=float(cfg.get("min_match_score", 0.35)),
            qa_rules=cfg.get("qa_rules", {}),
            dry_run=args.dry_run,
        )
        print(json.dumps([r.__dict__ for r in results], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
