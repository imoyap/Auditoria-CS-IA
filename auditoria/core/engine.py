"""Motor de ejecución de auditorías."""

from __future__ import annotations

import time
from typing import Any, Optional

from auditoria.checks.base import BaseCheck
from auditoria.checks.registry import get_checks, list_available_checks
from auditoria.core.models import AuditReport, CheckResult


class AuditEngine:
    """Orquesta la ejecución de módulos de auditoría registrados."""

    def __init__(
        self,
        target: str = "localhost",
        config: dict[str, Any] | None = None,
        enable_ai: bool = False,
        db_path: Optional[str] = None,
    ) -> None:
        self.target = target
        self.config = config or {}
        self.enable_ai = enable_ai
        self.db_manager = None
        self.ai_analyzer = None

        if db_path or config and config.get("persist_audits"):
            try:
                from auditoria.storage.database import DatabaseManager
                db_path = db_path or config.get("db_path", "auditoria.db") if config else "auditoria.db"
                self.db_manager = DatabaseManager(db_path)
            except ImportError:
                pass

        if enable_ai:
            try:
                from auditoria.ai.analyzer import AuditAnalyzer
                self.ai_analyzer = AuditAnalyzer()
            except (ImportError, ValueError):
                pass

    def run(
        self,
        modules: list[str] | None = None,
        categories: list[str] | None = None,
    ) -> AuditReport:
        report = AuditReport.create(
            target=self.target,
            modules=modules or "all",
            config_keys=list(self.config.keys()),
        )

        checks = self._resolve_checks(modules, categories)

        for check_cls in checks:
            result = self._run_check(check_cls)
            report.results.append(result)

        report = report.finalize()

        if self.db_manager:
            audit_id = self.db_manager.save_audit(report)
            report.metadata["audit_id"] = audit_id

            if self.ai_analyzer:
                self._run_ai_analysis(audit_id, report)

        return report

    def _run_ai_analysis(self, audit_id: int, report: AuditReport) -> None:
        """Ejecuta análisis de IA y guarda resultados."""
        try:
            if len(report.all_findings) > 0:
                plan = self.ai_analyzer.prioritize_findings(report)
                self.db_manager.save_ai_analysis(
                    audit_id,
                    "priority_plan",
                    plan["priority_plan"],
                )

            if report.all_findings:
                patterns = self.ai_analyzer.detect_patterns(report)
                self.db_manager.save_ai_analysis(
                    audit_id,
                    "pattern_analysis",
                    patterns["patterns"],
                )

            summary = self.ai_analyzer.generate_executive_summary(report)
            self.db_manager.save_ai_analysis(
                audit_id,
                "executive_summary",
                summary,
            )
        except Exception as e:
            print(f"Advertencia: AI analysis falló: {e}")

    def _resolve_checks(
        self,
        modules: list[str] | None,
        categories: list[str] | None,
    ) -> list[type[BaseCheck]]:
        available = get_checks()

        if modules:
            selected: list[type[BaseCheck]] = []
            for name in modules:
                if name not in available:
                    raise ValueError(
                        f"Módulo desconocido: '{name}'. "
                        f"Disponibles: {', '.join(list_available_checks())}"
                    )
                selected.append(available[name])
            checks = selected
        else:
            checks = list(available.values())

        if categories:
            category_set = {c.lower() for c in categories}
            checks = [c for c in checks if c.category.lower() in category_set]

        return checks

    def _run_check(self, check_cls: type[BaseCheck]) -> CheckResult:
        check = check_cls(target=self.target, config=self.config)
        start = time.perf_counter()

        try:
            findings = check.run()
            duration = (time.perf_counter() - start) * 1000
            return CheckResult(
                module=check.name,
                category=check.category,
                findings=findings,
                duration_ms=round(duration, 2),
            )
        except Exception as exc:
            duration = (time.perf_counter() - start) * 1000
            return CheckResult(
                module=check.name,
                category=check.category,
                duration_ms=round(duration, 2),
                error=str(exc),
            )
