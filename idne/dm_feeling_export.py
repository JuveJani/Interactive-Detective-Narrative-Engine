"""Tier B export and Markdown reports for DM Feeling Validator (Milestone 10)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


PLAYTEST_QUESTIONNAIRE = """
# DM Feeling — Human Playtest Questionnaire (Tier C)

Complete after playing the adventure. Quote PLAYER text where noted.

## Agency
1. Did choices feel like understandable in-world actions? (1–5)
2. Any moment where you had no basis for deciding? Describe with page/section quote.

## Discovery
3. Did major information feel discovered rather than delivered? (1–5)
4. List any clue that appeared without effort.

## Exploration
5. Did locations and objects reward inspection? (1–5)
6. Note any one-paragraph room or object fully exposed on arrival.

## Inference
7. Could you explain your theory before the ending? (1–5)
8. Any inference that felt like a checkbox or obvious answer?

## Aha
9. Recall one moment information connected unexpectedly. If none, say none.

## World response
10. Did time, NPCs, or object state visibly change play? (1–5)

## Time pressure
11. Did the deadline matter to your decisions? (1–5)

## Failure
12. When checks failed, did something meaningful change? Examples?

## Conversation
13. Did NPC dialogue respond to how you approached them? (1–5)

## Ending
14. Did the ending follow from your investigation? (1–5)
15. Which ending did you reach and why?

## Mode
16. Solo: any artificial partner/split remnants? Two-player: joint investigation share? (1–5 each player)

## Overall
17. Did it feel like investigating a world or reading a branching storybook? (1–5)
18. Confusion stalls (count) and longest idle wait (minutes).
"""


def build_tier_b_export(
    adventure_root: Path,
    package: dict[str, Any],
    findings: list[Any],
    player_text: dict[str, str],
) -> dict[str, Any]:
    tier_b_findings = [f for f in findings if f.review_owner in ("tier_b", "Tier B") or f.tier == "B"]
    excerpts = []
    for rel, text in player_text.items():
        for line_no, line in enumerate(text.splitlines(), 1):
            if line.strip():
                excerpts.append({"file": rel, "line": line_no, "text": line.strip()[:300]})
    return {
        "adventure_id": package.get("adventure_id"),
        "play_modes": package.get("play_modes"),
        "tier_b_findings": [f.to_dict() for f in tier_b_findings],
        "player_excerpts_sample": excerpts[:50],
        "review_prompt": "Assess whether PLAYER prose supports agency, discovery, and neutrality.",
    }


def build_markdown_report(
    result: Any,
    category_scores: dict[str, str],
) -> str:
    lines = [
        "# DM Feeling Validation Report",
        "",
        f"**Status:** {result.status}",
        f"**Adventure:** {result.adventure_root}",
        "",
        "## Category scores",
        "",
    ]
    for cat, score in category_scores.items():
        from idne.dm_feeling_categories import CATEGORY_LABELS

        lines.append(f"- **{CATEGORY_LABELS.get(cat, cat)}:** {score}")
    lines.extend(["", "## Checks", ""])
    for k, v in sorted(result.checks.items()):
        lines.append(f"- `{k}`: {v}")
    if result.findings:
        lines.extend(["", "## Findings (summary)", ""])
        for f in result.findings[:30]:
            lines.append(
                f"- `{f.finding_id}` ({f.category}, {f.severity}): {f.observed_behavior}"
            )
    if result.tier_b_pending:
        lines.extend(["", "## Tier B pending", ""])
        for t in result.tier_b_pending:
            lines.append(f"- {t}")
    if not result.tier_c_complete:
        lines.extend(["", "## Tier C", "", "Human playtest evidence required."])
    return "\n".join(lines) + "\n"


def write_reports(
    adventure_root: Path,
    result: Any,
    package: dict[str, Any],
    category_scores: dict[str, str],
    player_text: dict[str, str],
) -> dict[str, str]:
    out_dir = adventure_root / "DO_NOT_READ" / "dm_feeling_reports"
    out_dir.mkdir(parents=True, exist_ok=True)
    paths: dict[str, str] = {}
    md = build_markdown_report(result, category_scores)
    md_path = out_dir / "dm_feeling_report.md"
    md_path.write_text(md, encoding="utf-8")
    paths["markdown"] = str(md_path)
    tier_b = build_tier_b_export(adventure_root, package, result.findings, player_text)
    tier_b_path = out_dir / "tier_b_export.json"
    tier_b_path.write_text(json.dumps(tier_b, indent=2) + "\n", encoding="utf-8")
    paths["tier_b_json"] = str(tier_b_path)
    ai_path = out_dir / "local_ai_review.json"
    ai_export = {
        "offline_runnable": package.get("local_ai_export", {}).get("offline_runnable", True),
        "tier_b_export_path": "DO_NOT_READ/dm_feeling_reports/tier_b_export.json",
        "categories": category_scores,
        "finding_count": len(result.findings),
    }
    ai_path.write_text(json.dumps(ai_export, indent=2) + "\n", encoding="utf-8")
    paths["local_ai_json"] = str(ai_path)
    return paths
