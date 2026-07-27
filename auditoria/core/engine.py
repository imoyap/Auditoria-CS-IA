"""Motor de ejecución de auditorías."""

from __future__ import annotations

import time
from typing import Any

from auditoria.checks.base import BaseCheck
from auditoria.checks.registry import get_checks, list_available_checks
from auditoria.core.models import AuditReport, CheckResult


class AuditEngine:
    """Orquesta la ejecución de módulos de auditoría registrados."""

    def __init__(
        self,
        target: str = "localhost",
        config: dict[str, Any] | None = None,
    ) -> None:
        self.target = target
        self.config = config or {}

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

        return report.finalize()

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
