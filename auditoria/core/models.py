"""Modelos de datos del framework de auditoría."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class Severity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

    @property
    def score(self) -> int:
        return {
            Severity.CRITICAL: 100,
            Severity.HIGH: 75,
            Severity.MEDIUM: 50,
            Severity.LOW: 25,
            Severity.INFO: 0,
        }[self]


class Status(str, Enum):
    PASS = "pass"
    FAIL = "fail"
    WARN = "warn"
    SKIP = "skip"
    ERROR = "error"


@dataclass
class Finding:
    """Hallazgo individual de una verificación de seguridad."""

    check_id: str
    title: str
    description: str
    severity: Severity
    status: Status
    recommendation: str = ""
    evidence: dict[str, Any] = field(default_factory=dict)
    references: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "check_id": self.check_id,
            "title": self.title,
            "description": self.description,
            "severity": self.severity.value,
            "status": self.status.value,
            "recommendation": self.recommendation,
            "evidence": self.evidence,
            "references": self.references,
        }


@dataclass
class CheckResult:
    """Resultado de un módulo de auditoría completo."""

    module: str
    category: str
    findings: list[Finding] = field(default_factory=list)
    duration_ms: float = 0.0
    error: str | None = None

    @property
    def passed(self) -> bool:
        return not any(
            f.status in (Status.FAIL, Status.ERROR)
            and f.severity in (Severity.CRITICAL, Severity.HIGH)
            for f in self.findings
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "module": self.module,
            "category": self.category,
            "duration_ms": self.duration_ms,
            "error": self.error,
            "findings": [f.to_dict() for f in self.findings],
        }


@dataclass
class AuditReport:
    """Informe consolidado de una auditoría."""

    target: str
    started_at: datetime
    finished_at: datetime | None = None
    results: list[CheckResult] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def all_findings(self) -> list[Finding]:
        findings: list[Finding] = []
        for result in self.results:
            findings.extend(result.findings)
        return findings

    @property
    def risk_score(self) -> float:
        """Puntuación de riesgo 0-100 (mayor = más riesgo)."""
        findings = [
            f
            for f in self.all_findings
            if f.status in (Status.FAIL, Status.WARN, Status.ERROR)
        ]
        if not findings:
            return 0.0
        total = sum(f.severity.score for f in findings)
        max_possible = len(findings) * 100
        return round((total / max_possible) * 100, 1)

    @property
    def summary(self) -> dict[str, int]:
        counts = {s.value: 0 for s in Severity}
        for finding in self.all_findings:
            if finding.status in (Status.FAIL, Status.WARN):
                counts[finding.severity.value] += 1
        counts["total_findings"] = sum(
            1 for f in self.all_findings if f.status in (Status.FAIL, Status.WARN)
        )
        counts["passed_checks"] = sum(
            1 for r in self.results if r.error is None and r.passed
        )
        counts["failed_modules"] = sum(1 for r in self.results if r.error)
        return counts

    def to_dict(self) -> dict[str, Any]:
        return {
            "target": self.target,
            "started_at": self.started_at.isoformat(),
            "finished_at": self.finished_at.isoformat() if self.finished_at else None,
            "risk_score": self.risk_score,
            "summary": self.summary,
            "metadata": self.metadata,
            "results": [r.to_dict() for r in self.results],
        }

    @classmethod
    def create(cls, target: str, **metadata: Any) -> AuditReport:
        return cls(
            target=target,
            started_at=datetime.now(timezone.utc),
            metadata=metadata,
        )

    def finalize(self) -> AuditReport:
        self.finished_at = datetime.now(timezone.utc)
        return self
