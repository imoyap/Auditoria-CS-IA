"""Generadores de informes de auditoría."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from jinja2 import Environment, PackageLoader, select_autoescape
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from auditoria.core.models import AuditReport, Finding, Severity, Status


SEVERITY_COLORS = {
    Severity.CRITICAL: "red bold",
    Severity.HIGH: "red",
    Severity.MEDIUM: "yellow",
    Severity.LOW: "blue",
    Severity.INFO: "cyan",
}

STATUS_ICONS = {
    Status.PASS: "[green][OK][/green]",
    Status.FAIL: "[red][X][/red]",
    Status.WARN: "[yellow][!][/yellow]",
    Status.SKIP: "[dim][-][/dim]",
    Status.ERROR: "[red][E][/red]",
}


class ConsoleReporter:
    """Muestra el informe en consola con formato Rich."""

    def __init__(self, console: Console | None = None) -> None:
        self.console = console or Console()

    def render(self, report: AuditReport) -> None:
        self.console.print()
        self.console.print(
            Panel(
                f"[bold]Objetivo:[/bold] {report.target}\n"
                f"[bold]Puntuación de riesgo:[/bold] {report.risk_score}/100\n"
                f"[bold]Hallazgos:[/bold] {report.summary['total_findings']}",
                title="[bold cyan]Auditoría de Ciberseguridad[/bold cyan]",
                border_style="cyan",
            )
        )

        summary = report.summary
        summary_table = Table(title="Resumen por severidad", show_header=True)
        summary_table.add_column("Severidad", style="bold")
        summary_table.add_column("Cantidad", justify="right")
        for sev in Severity:
            count = summary.get(sev.value, 0)
            if count > 0:
                summary_table.add_row(sev.value.upper(), str(count))
        self.console.print(summary_table)

        for result in report.results:
            if result.error:
                self.console.print(
                    f"\n[red]Error en {result.module}:[/red] {result.error}"
                )
                continue

            self.console.print(f"\n[bold underline]{result.module}[/bold underline] "
                               f"({result.category}) — {result.duration_ms:.0f}ms")

            for finding in result.findings:
                self._print_finding(finding)

        self.console.print()

    def _print_finding(self, finding: Finding) -> None:
        icon = STATUS_ICONS.get(finding.status, "?")
        color = SEVERITY_COLORS.get(finding.severity, "white")
        self.console.print(
            f"  {icon} [{color}]{finding.severity.value.upper()}[/{color}] "
            f"{finding.title}"
        )
        if finding.status in (Status.FAIL, Status.WARN):
            self.console.print(f"    [dim]{finding.description}[/dim]")
            if finding.recommendation:
                self.console.print(f"    [green]> {finding.recommendation}[/green]")


class JsonReporter:
    """Exporta el informe a JSON."""

    def render(self, report: AuditReport, output_path: Path) -> Path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            json.dumps(report.to_dict(), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        return output_path


class HtmlReporter:
    """Exporta el informe a HTML usando plantilla Jinja2."""

    def __init__(self) -> None:
        self.env = Environment(
            loader=PackageLoader("auditoria", "templates"),
            autoescape=select_autoescape(["html"]),
        )

    def render(self, report: AuditReport, output_path: Path) -> Path:
        template = self.env.get_template("report.html")
        html = template.render(
            report=report,
            findings=report.all_findings,
            summary=report.summary,
            risk_score=report.risk_score,
            generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            severity_order=list(Severity),
        )
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(html, encoding="utf-8")
        return output_path
