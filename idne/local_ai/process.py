"""Unified post-response processing pipeline."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from idne.local_ai.proposal_builder import build_proposal
from idne.local_ai.proposal_validate import validate_proposal
from idne.local_ai.response_parser import ParseError, parse_response
from idne.local_ai.response_validate import ResponseValidationError, validate_response


@dataclass
class ProcessResult:
    success: bool
    stopped_at: str
    duration_seconds: float
    details: dict[str, Any] = field(default_factory=dict)


def process_task(run_dir: Path) -> ProcessResult:
    """Parse, validate response, build proposal, validate proposal — stop at first failure."""
    start = time.perf_counter()
    try:
        parse_result = parse_response(run_dir)
    except ParseError as exc:
        return ProcessResult(
            success=False,
            stopped_at="parse",
            duration_seconds=time.perf_counter() - start,
            details={"code": exc.code, "message": str(exc)},
        )
    try:
        response_validation = validate_response(run_dir)
    except ResponseValidationError as exc:
        return ProcessResult(
            success=False,
            stopped_at="validate-response",
            duration_seconds=time.perf_counter() - start,
            details={"message": str(exc)},
        )
    if not response_validation.passed:
        return ProcessResult(
            success=False,
            stopped_at="validate-response",
            duration_seconds=time.perf_counter() - start,
            details={"findings": [f.to_dict() for f in response_validation.findings]},
        )
    try:
        proposal = build_proposal(run_dir)
    except RuntimeError as exc:
        return ProcessResult(
            success=False,
            stopped_at="build-proposal",
            duration_seconds=time.perf_counter() - start,
            details={"message": str(exc)},
        )
    try:
        proposal_validation = validate_proposal(run_dir)
    except RuntimeError as exc:
        return ProcessResult(
            success=False,
            stopped_at="validate-proposal",
            duration_seconds=time.perf_counter() - start,
            details={"message": str(exc)},
        )
    if not proposal_validation.get("passed"):
        return ProcessResult(
            success=False,
            stopped_at="validate-proposal",
            duration_seconds=time.perf_counter() - start,
            details={"findings": proposal_validation.get("findings", [])},
        )
    return ProcessResult(
        success=True,
        stopped_at="complete",
        duration_seconds=time.perf_counter() - start,
        details={
            "parse_seconds": parse_result.duration_seconds,
            "proposal": proposal,
            "proposal_validation": proposal_validation,
        },
    )
