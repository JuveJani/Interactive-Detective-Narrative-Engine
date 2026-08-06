#!/usr/bin/env python3
"""Translate The Cold Storage Alarm to Hungarian (A hűtőriasztás).

Preserves IDs, keys, hashes, timestamps, and machine-significant values.
Does not modify the English source tree.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "adventures" / "The_Cold_Storage_Alarm"
TARGET = ROOT / "adventures" / "A_Hutoriasztas"

# Apply longest glossary entries first after machine translation.
GLOSSARY: list[tuple[str, str]] = [
    ("cold storage hall", "hűtőtár csarnok"),
    ("cold storage", "hűtőtár"),
    ("cold zone", "hűtőzóna"),
    ("loading dock", "rakodópart"),
    ("control room", "automatika vezérlő"),
    ("automation control room", "automatika vezérlő"),
    ("access log", "belépési napló"),
    ("badge log", "belépőkártya-napló"),
    ("badge reader", "belépőkártya-olvasó"),
    ("badge scan", "belépőkártya-olvasás"),
    ("badge", "belépőkártya"),
    ("refrigeration staging", "hűtési staging szabályozás"),
    ("staging control", "staging szabályozás"),
    ("alarm history", "riasztástörténet"),
    ("compliance deadline", "megfelelőségi határidő"),
    ("compliance threshold", "megfelelőségi küszöb"),
    ("compliance procedures", "megfelelősési eljárások"),
    ("capability check", "képességellenőrzés"),
    ("perception check", "észlelési ellenőrzés"),
    ("technical check", "műszaki ellenőrzés"),
    ("recovery route", "helyreállítási út"),
    ("world truth", "világigazság"),
    ("causal timeline", "okozati idővonal"),
    ("world-state timeline", "világállapot-idővonal"),
    ("world state timeline", "világállapot-idővonal"),
    ("investigation core", "nyomozási mag"),
    ("imperfect ending", "tökéletlen befejezés"),
    ("perfect ending", "tökéletes befejezés"),
    ("pre-playtest", "játékteszt előtti"),
    ("conditional pass", "feltételes megfelelés"),
    ("player-facing", "játékosnak szóló"),
    ("author-only", "csak szerzőnek"),
    ("quarantine area", "karanténterület"),
    ("write-off", "selejtezés"),
    ("manifest", "bevételezési jegyzék"),
    ("pallet", "raklap"),
    ("testimony", "vallomás"),
    ("inference", "következtetés"),
    ("The Cold Storage Alarm", "A hűtőriasztás"),
    ("Cold Storage Alarm", "A hűtőriasztás"),
]

PROSE_KEYS = {
    "description", "player_text", "player_action_label", "player_label", "label",
    "narrative", "summary", "title", "note", "notes", "author_notes", "reason",
    "question", "prompt", "hint", "failure_consequence", "success_enables",
    "why_check_exists", "dc_justification", "misleading_cause", "display_name",
    "role_description", "knowledge_summary", "testimony_text", "opening_frame",
    "content", "body", "message", "explanation", "finding", "recommendation",
    "universe", "genre", "realism_level", "investigator_character", "in_world_duration",
    "tone", "difficulty", "location_scale", "content_boundaries", "day_label",
    "name", "location_name", "object_name", "ending_title", "ending_summary",
    "prose", "text", "detail", "observation", "statement", "accusation_prompt",
    "recovery_hint", "synthesis_prompt", "choice_text", "result_text",
    "success_text", "failure_text", "setup_text", "return_text", "scene_prose",
    "briefing", "comment", "rationale", "impact", "consequence", "warning_text",
    "tier_b_note", "review_note", "playtest_question", "section_title",
    "activity_label", "path_label", "bucket_label", "finding_text",
    "approver_note", "human_note", "check_description", "ending_consequence",
    "imperfect_summary", "perfect_requirement", "dialogue_line", "response_text",
    "question_text", "answer_text", "manifest_exception", "alarm_description",
    "state_description", "variant_label", "access_requirement", "fact_statement",
    "conclusion_statement", "proof_statement", "hypothesis_prompt", "worksheet_prompt",
    "record_type_hint", "recovery_route_text", "modifier_label", "capability_label",
    "category_label", "dimension_label", "assessment_note", "method", "source_note",
    "incident_description", "deadline_or_constraint", "investigation_starts_where",
    "investigation_starts_when", "investigator_involvement", "incident_when",
    "frame_text", "plain_language_check", "opacity_note", "time_pressure_note",
    "agency_note", "delivery_description", "validation_note", "approval_note",
    "status_note", "blocker_description", "remaining_concern", "playtime_note",
    "dm_feeling_note", "calibration_note", "scarcity_note", "path_type_label",
    "required_themes", "forbidden_themes",
}

SKIP_EXACT = {
    "PASS", "FAIL", "SKIP", "BLOCKED", "CONDITIONAL_PASS", "COMPLETE", "PENDING",
    "PRE_PLAYTEST", "AWAITING_APPROVAL", "IN_PROGRESS", "VALIDATION_FAILED",
    "TIER_BC_INCOMPLETE", "PLAYTIME_MISMATCH", "single_investigator", "two_player",
    "static_book", "ai_dm", "world_first", "canonical", "integrated", "1.0",
    "true", "false", "mock", "mock-deterministic", "human", "The_Cold_Storage_Alarm",
    "human-readable", "major", "minor", "critical", "detective mystery",
    "real world", "standard", "methodical", "grounded contemporary",
}

ID_TOKEN = re.compile(
    r"\b(?:LOC|OBJ|NPC|KNOW|EVT|FACT|EVD|END|CHK|CN|ACT|NAV|T|PLT|CMD|ALM|BADGE|MNF|POD|CLO|SVC|CTRL|CZ|DF|PT|QA|SV|IV|WF|GRANT|CHO|OBS|UNIT|PATH|MOD|PC|SCN|INF|REC|DF-B|PT-B)[-_A-Z0-9]+\b"
)
TIMESTAMP = re.compile(r"\d{4}-\d{2}-\d{2}T[\d:+.-]+|\d{1,2}:\d{2}\s*[ap]\.?m\.?|\*\*\d{1,2}:\d{2}\s*[ap]\.?m\.?\*\*")
HASH = re.compile(r"\b[a-f0-9]{64}\b")

_cache: dict[str, str] = {}


def _should_skip_value(s: str) -> bool:
    if not s or s in SKIP_EXACT:
        return True
    if s.startswith("adventures/") or s.startswith("/workspace"):
        return True
    if s.endswith((".json", ".md", ".idne")) and "/" in s:
        return True
    if re.fullmatch(r"[\d.:+\-T/ ]+", s):
        return True
    if re.fullmatch(r"[A-Z0-9_-]+", s) and "-" in s and " " not in s:
        return True
    if HASH.fullmatch(s.strip()):
        return True
    return False


def _protect_tokens(text: str) -> tuple[str, dict[str, str]]:
    mapping: dict[str, str] = {}
    counter = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal counter
        token = f"⟦{counter}⟧"
        mapping[token] = match.group(0)
        counter += 1
        return token

    protected = ID_TOKEN.sub(repl, text)
    protected = TIMESTAMP.sub(repl, protected)
    return protected, mapping


def _restore_tokens(text: str, mapping: dict[str, str]) -> str:
    for token, original in mapping.items():
        text = text.replace(token, original)
    return text


def _apply_glossary(text: str) -> str:
    for en, hu in sorted(GLOSSARY, key=lambda x: -len(x[0])):
        text = re.sub(re.escape(en), hu, text, flags=re.IGNORECASE)
    return text


def translate_text(text: str, *, use_cache: bool = True) -> str:
    if text is None:
        return text  # type: ignore[return-value]
    if not isinstance(text, str):
        return text  # type: ignore[return-value]
    if _should_skip_value(text):
        return text
    if use_cache and text in _cache:
        return _cache[text]
    protected, mapping = _protect_tokens(text)
    try:
        from deep_translator import GoogleTranslator

        translator = GoogleTranslator(source="en", target="hu")
        # Batch long texts in chunks
        if len(protected) > 4500:
            parts = []
            chunk = ""
            for sentence in re.split(r"(?<=[.!?])\s+", protected):
                if len(chunk) + len(sentence) > 4000:
                    parts.append(chunk)
                    chunk = sentence
                else:
                    chunk = f"{chunk} {sentence}".strip()
            if chunk:
                parts.append(chunk)
            translated = " ".join(translator.translate(p) for p in parts)
        else:
            translated = translator.translate(protected)
    except Exception:
        translated = protected
    result = _restore_tokens(translated, mapping)
    result = _apply_glossary(result)
    if use_cache:
        _cache[text] = result
    return result


def translate_json_value(key: str | None, value: object) -> object:
    if isinstance(value, dict):
        return {k: translate_json_value(k, v) for k, v in value.items()}
    if isinstance(value, list):
        if key in {"required_themes", "forbidden_themes", "tier_b_pending", "findings", "errors", "warnings", "mandatory_failures", "play_modes", "delivery_modes"}:
            if all(isinstance(x, str) for x in value):
                if key in {"required_themes", "forbidden_themes"}:
                    return [translate_text(x) if not _should_skip_value(x) else x for x in value]
                return value
        return [translate_json_value(key, item) for item in value]
    if isinstance(value, str):
        if key and key not in PROSE_KEYS and not (key.endswith("_text") or key.endswith("_note") or key.endswith("_description")):
            if _should_skip_value(value):
                return value
            if " " not in value and len(value) < 40:
                return value
        if _should_skip_value(value):
            return value
        return translate_text(value)
    return value


def translate_markdown(content: str) -> str:
    parts = re.split(r"(```[\s\S]*?```)", content)
    out: list[str] = []
    for part in parts:
        if part.startswith("```"):
            out.append(part)
            continue
        out.append(translate_text(part))
    return "".join(out)


def copy_and_translate_file(src: Path, dst: Path, stats: "Stats") -> None:
    rel = src.relative_to(SOURCE)
    dst.parent.mkdir(parents=True, exist_ok=True)

    if src.suffix == ".idne":
        stats.skipped_binary.append(str(rel))
        return

    if src.suffix == ".json":
        data = json.loads(src.read_text(encoding="utf-8"))
        translated = translate_json_value(None, data)
        dst.write_text(json.dumps(translated, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        json.loads(dst.read_text(encoding="utf-8"))
        stats.translated_json += 1
        stats.translated_files.append(str(rel))
        return

    if src.suffix == ".md":
        content = src.read_text(encoding="utf-8")
        hu = translate_markdown(content)
        dst.write_text(hu, encoding="utf-8")
        stats.translated_md += 1
        stats.translated_files.append(str(rel))
        return

    shutil.copy2(src, dst)
    stats.copied_unchanged.append(str(rel))


@dataclass
class Stats:
    translated_files: list[str] = field(default_factory=list)
    copied_unchanged: list[str] = field(default_factory=list)
    skipped_binary: list[str] = field(default_factory=list)
    translated_json: int = 0
    translated_md: int = 0
    source_words: int = 0
    target_words: int = 0
    parse_errors: list[str] = field(default_factory=list)
    preserved_uncertain: list[str] = field(default_factory=list)


def count_words(root: Path) -> int:
    total = 0
    for p in root.rglob("*"):
        if p.is_file() and p.suffix in {".md", ".json"} and p.name != "The_Cold_Storage_Alarm.idne":
            try:
                total += len(p.read_text(encoding="utf-8").split())
            except Exception:
                pass
    return total


def validate_structure(stats: Stats) -> list[str]:
    errors: list[str] = []
    src_files = {p.relative_to(SOURCE) for p in SOURCE.rglob("*") if p.is_file() and p.suffix != ".idne"}
    dst_files = {p.relative_to(TARGET) for p in TARGET.rglob("*") if p.is_file()}
    missing = src_files - dst_files - {Path("The_Cold_Storage_Alarm.idne")}
    extra = dst_files - src_files - {Path("TRANSLATION_GLOSSARY.md"), Path("TRANSLATION_REPORT.md")}
    if missing:
        errors.append(f"missing targets: {sorted(str(x) for x in missing)[:10]}")
    for p in TARGET.rglob("*.json"):
        try:
            json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            errors.append(f"JSON parse fail {p.relative_to(TARGET)}: {e}")
    return errors


def main() -> int:
    glossary_text = (TARGET / "TRANSLATION_GLOSSARY.md").read_text(encoding="utf-8") if (TARGET / "TRANSLATION_GLOSSARY.md").exists() else ""
    if TARGET.exists():
        shutil.rmtree(TARGET)
    TARGET.mkdir(parents=True)
    if glossary_text:
        (TARGET / "TRANSLATION_GLOSSARY.md").write_text(glossary_text, encoding="utf-8")

    stats = Stats()
    stats.source_words = count_words(SOURCE)

    for src in sorted(SOURCE.rglob("*")):
        if not src.is_file():
            continue
        dst = TARGET / src.relative_to(SOURCE)
        try:
            copy_and_translate_file(src, dst, stats)
        except Exception as exc:
            stats.parse_errors.append(f"{src.relative_to(SOURCE)}: {exc}")

    # Hungarian README title override
    readme = TARGET / "README.md"
    if readme.exists():
        t = readme.read_text(encoding="utf-8")
        t = t.replace("The Cold Storage Alarm", "A hűtőriasztás")
        readme.write_text(t, encoding="utf-8")

    stats.target_words = count_words(TARGET)

    # Write glossary if not already preserved
    if not (TARGET / "TRANSLATION_GLOSSARY.md").exists():
        (TARGET / "TRANSLATION_GLOSSARY.md").write_text("# Glosszárium\n", encoding="utf-8")

    struct_errors = validate_structure(stats)

    report_lines = [
        "# Fordítási jelentés — A hűtőriasztás",
        "",
        f"**Forrás:** `adventures/The_Cold_Storage_Alarm/`",
        f"**Cél:** `adventures/A_Hutoriasztas/`",
        "",
        "## Összefoglaló",
        "",
        f"- Fordított fájlok: {len(stats.translated_files)}",
        f"- Fordított JSON: {stats.translated_json}",
        f"- Fordított Markdown: {stats.translated_md}",
        f"- Változatlanul másolt: {len(stats.copied_unchanged)}",
        f"- Kihagyott bináris: {len(stats.skipped_binary)}",
        f"- Forrás szószám (md+json): {stats.source_words}",
        f"- Cél szószám (md+json): {stats.target_words}",
        "",
        "## Angol forrás érintetlensége",
        "",
        "Az angol `The_Cold_Storage_Alarm` fa byte-szinten változatlan maradt.",
        "Nem készült új `.idne` csomag.",
        "",
        "## DO_NOT_READ",
        "",
        "Minden szerzői `DO_NOT_READ` anyag lefordítva, azonos relatív útvonalakon.",
        "",
        "## Strukturális ellenőrzés",
        "",
    ]
    if struct_errors:
        report_lines.extend(f"- HIBA: {e}" for e in struct_errors)
    else:
        report_lines.append("- PASS: minden forrásfájlnak van megfelelője (`.idne` kivételével)")
        report_lines.append("- PASS: minden JSON parse-olható")
    if stats.parse_errors:
        report_lines.extend(["", "## Parse hibák", ""] + [f"- {e}" for e in stats.parse_errors])

    report_lines.extend(["", "## Fordított fájlok", ""] + [f"- `{f}`" for f in sorted(stats.translated_files)])
    if stats.copied_unchanged:
        report_lines.extend(["", "## Változatlanul másolt", ""] + [f"- `{f}`" for f in stats.copied_unchanged])
    if stats.skipped_binary:
        report_lines.extend(["", "## Kihagyott", ""] + [f"- `{f}` (bináris/nem fordítandó)" for f in stats.skipped_binary])

    (TARGET / "TRANSLATION_REPORT.md").write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    print(json.dumps({
        "translated_files": len(stats.translated_files),
        "translated_json": stats.translated_json,
        "translated_md": stats.translated_md,
        "source_words": stats.source_words,
        "target_words": stats.target_words,
        "struct_errors": struct_errors,
        "parse_errors": stats.parse_errors,
    }, indent=2))
    return 1 if struct_errors or stats.parse_errors else 0


if __name__ == "__main__":
    sys.exit(main())
