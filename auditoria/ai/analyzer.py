"""Analizador de auditorías con Claude API."""

from __future__ import annotations

import os
from typing import Optional

from auditoria.ai.prompts import (
    ANALYZE_FINDINGS,
    DETECT_PATTERNS,
    GENERATE_EXECUTIVE_SUMMARY,
    PRIORITIZE_FINDINGS,
)
from auditoria.core.models import AuditReport, Finding


class AuditAnalyzer:
    """Proporciona análisis inteligente de hallazgos usando Claude."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY no configurado. "
                "Establezca la variable de entorno o pase api_key."
            )
        self._init_client()

    def _init_client(self) -> None:
        """Inicializa cliente de Anthropic."""
        try:
            from anthropic import Anthropic
            self.client = Anthropic(api_key=self.api_key)
        except ImportError:
            raise ImportError("anthropic no instalado. Ejecute: pip install anthropic")

    def analyze_finding(
        self,
        finding: Finding,
        report: AuditReport,
        related_count: int = 0,
    ) -> dict[str, str]:
        """Analiza un hallazgo individual con contexto de la auditoría.

        Returns:
            {
                "analysis": "Análisis contextual",
                "impact": "1-10 escala de impacto",
                "remediation": "Pasos de remediación",
                "references": "Frameworks relevantes"
            }
        """
        prompt = ANALYZE_FINDINGS.user.format(
            type=finding.title,
            title=finding.description[:100],
            severity=finding.severity.value,
            description=finding.description,
            target=report.target,
            modules=", ".join(set(r.module for r in report.results)),
            related_count=related_count,
        )

        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            system=ANALYZE_FINDINGS.system,
            messages=[{"role": "user", "content": prompt}],
        )

        return {
            "analysis": response.content[0].text,
            "finding_id": finding.check_id,
            "severity": finding.severity.value,
        }

    def prioritize_findings(self, report: AuditReport) -> dict:
        """Crea plan de remediación priorizando hallazgos.

        Returns:
            {
                "priority_plan": "Plan de acción",
                "timeline": "Cronograma estimado",
                "resources": "Recursos necesarios"
            }
        """
        critical = sum(1 for f in report.all_findings if f.severity.value == "critical")
        high = sum(1 for f in report.all_findings if f.severity.value == "high")
        medium = sum(1 for f in report.all_findings if f.severity.value == "medium")
        low = sum(1 for f in report.all_findings if f.severity.value == "low")

        types_summary = {}
        for finding in report.all_findings:
            ftype = finding.title
            types_summary[ftype] = types_summary.get(ftype, 0) + 1

        types_str = "\n".join(
            f"- {ftype}: {count}" for ftype, count in sorted(
                types_summary.items(), key=lambda x: -x[1]
            )[:10]
        )

        prompt = PRIORITIZE_FINDINGS.user.format(
            count=len(report.all_findings),
            target=report.target,
            critical=critical,
            high=high,
            medium=medium,
            low=low,
            types=types_str,
        )

        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1500,
            system=PRIORITIZE_FINDINGS.system,
            messages=[{"role": "user", "content": prompt}],
        )

        return {
            "priority_plan": response.content[0].text,
            "total_findings": len(report.all_findings),
            "risk_score": report.risk_score,
        }

    def generate_executive_summary(self, report: AuditReport) -> str:
        """Genera resumen ejecutivo para stakeholders."""
        critical_findings = [
            f for f in report.all_findings if f.severity.value == "critical"
        ][:3]

        critical_str = "\n".join(
            f"- {f.title}: {f.description[:80]}" for f in critical_findings
        )

        prompt = GENERATE_EXECUTIVE_SUMMARY.user.format(
            target=report.target,
            risk_score=report.risk_score,
            total_findings=len(report.all_findings),
            critical_findings=critical_str or "Ninguno",
        )

        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=800,
            system=GENERATE_EXECUTIVE_SUMMARY.system,
            messages=[{"role": "user", "content": prompt}],
        )

        return response.content[0].text

    def detect_patterns(self, report: AuditReport) -> dict:
        """Detecta patrones y causas raíz comunes en hallazgos."""
        findings_list = "\n".join(
            f"- [{f.severity.value.upper()}] {f.title}: {f.description[:100]}"
            for f in report.all_findings[:15]
        )

        prompt = DETECT_PATTERNS.user.format(
            count=len(report.all_findings),
            findings_list=findings_list,
        )

        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1200,
            system=DETECT_PATTERNS.system,
            messages=[{"role": "user", "content": prompt}],
        )

        return {
            "patterns": response.content[0].text,
            "analysis_date": report.finished_at.isoformat() if report.finished_at else None,
        }
