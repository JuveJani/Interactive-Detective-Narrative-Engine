"""UI-independent Simulator v2 application service."""

from __future__ import annotations

import threading
import uuid
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

from simulator_v2.derivation import CanonicalSimulationModel, derive_simulation_model
from simulator_v2.package_loader import load_simulator_package
from simulator_v2.state import SimulationState, initial_state_from_model
from simulator_v2.types import LoadStatus, PackageLoadResult


class RunStatus(str, Enum):
    IDLE = "IDLE"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    BLOCKED = "BLOCKED"


@dataclass
class ReadinessResult:
    ready: bool
    status: str
    errors: list[str] = field(default_factory=list)
    load_result: PackageLoadResult | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "ready": self.ready,
            "status": self.status,
            "errors": self.errors,
        }


@dataclass
class RunProgress:
    run_id: str
    status: RunStatus
    steps: int = 0
    current_location: str = ""
    message: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "status": self.status.value,
            "steps": self.steps,
            "current_location": self.current_location,
            "message": self.message,
        }


@dataclass
class RunResult:
    run_id: str
    status: RunStatus
    final_state: SimulationState | None = None
    derivation_report: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "status": self.status.value,
            "derivation_report": self.derivation_report,
            "final_state_location": self.final_state.location_id if self.final_state else None,
        }


@dataclass
class _RunRecord:
    run_id: str
    status: RunStatus
    model: CanonicalSimulationModel | None = None
    state: SimulationState | None = None
    cancel_requested: bool = False
    steps: int = 0


class SimulatorService:
    """Stable service boundary for future UI and automation clients."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._loaded: PackageLoadResult | None = None
        self._model: CanonicalSimulationModel | None = None
        self._runs: dict[str, _RunRecord] = {}

    def load_package(self, path: str | Path) -> PackageLoadResult:
        result = load_simulator_package(path)
        with self._lock:
            self._loaded = result
            self._model = None
            if result.status == LoadStatus.READY and result.adventure_root:
                self._model = derive_simulation_model(result.adventure_root, result.play_mode)
        return result

    def validate_readiness(self) -> ReadinessResult:
        if not self._loaded:
            return ReadinessResult(ready=False, status="NOT_LOADED", errors=["no package loaded"])
        if self._loaded.status != LoadStatus.READY:
            return ReadinessResult(
                ready=False,
                status=self._loaded.status.value,
                errors=list(self._loaded.errors),
                load_result=self._loaded,
            )
        if not self._loaded.simulation_ready:
            return ReadinessResult(
                ready=False,
                status="NOT_SIMULATION_READY",
                errors=["package loaded but not simulation ready"],
                load_result=self._loaded,
            )
        return ReadinessResult(ready=True, status="READY", load_result=self._loaded)

    def start_run(self) -> str:
        readiness = self.validate_readiness()
        if not readiness.ready or not self._model:
            raise RuntimeError("simulation not ready: " + "; ".join(readiness.errors))

        run_id = str(uuid.uuid4())
        state = initial_state_from_model(self._model)
        record = _RunRecord(
            run_id=run_id,
            status=RunStatus.RUNNING,
            model=self._model,
            state=state,
        )
        with self._lock:
            self._runs[run_id] = record
        return run_id

    def get_progress(self, run_id: str) -> RunProgress:
        with self._lock:
            record = self._runs.get(run_id)
        if not record:
            return RunProgress(run_id=run_id, status=RunStatus.BLOCKED, message="unknown run")
        loc = record.state.location_id if record.state else ""
        return RunProgress(
            run_id=run_id,
            status=record.status,
            steps=record.steps,
            current_location=loc,
        )

    def cancel(self, run_id: str) -> None:
        with self._lock:
            record = self._runs.get(run_id)
            if record:
                record.cancel_requested = True
                record.status = RunStatus.CANCELLED

    def get_results(self, run_id: str) -> RunResult:
        with self._lock:
            record = self._runs.get(run_id)
        if not record:
            return RunResult(run_id=run_id, status=RunStatus.BLOCKED)
        report = record.model.report.to_dict() if record.model else {}
        if record.status == RunStatus.RUNNING and not record.cancel_requested:
            with self._lock:
                record.status = RunStatus.COMPLETED
        return RunResult(
            run_id=run_id,
            status=record.status,
            final_state=record.state.copy() if record.state else None,
            derivation_report=report,
        )

    @property
    def model(self) -> CanonicalSimulationModel | None:
        return self._model

    @property
    def load_result(self) -> PackageLoadResult | None:
        return self._loaded
