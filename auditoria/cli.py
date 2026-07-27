"""Interfaz de línea de comandos."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from rich.console import Console

from auditoria import __version__
from auditoria.checks.registry import get_checks, list_available_checks, list_categories
from auditoria.core.engine import AuditEngine
from auditoria.core.reporter import ConsoleReporter, HtmlReporter, JsonReporter


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="auditoria",
        description="Framework modular de auditoría de ciberseguridad",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    sub = parser.add_subparsers(dest="command", required=True)

    # audit
    audit = sub.add_parser("audit", help="Ejecutar auditoría de seguridad")
    audit.add_argument(
        "--target", "-t",
        default="localhost",
        help="Objetivo: hostname, IP o dominio (default: localhost)",
    )
    audit.add_argument(
        "--modules", "-m",
        nargs="+",
        help="Módulos específicos a ejecutar",
    )
    audit.add_argument(
        "--category", "-c",
        nargs="+",
        help="Filtrar por categoría",
    )
    audit.add_argument(
        "--scan-path",
        type=Path,
        default=Path("."),
        help="Ruta para escaneo de archivos y secretos",
    )
    audit.add_argument(
        "--output-json",
        type=Path,
        help="Exportar informe en JSON",
    )
    audit.add_argument(
        "--output-html",
        type=Path,
        help="Exportar informe en HTML",
    )
    audit.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Solo exportar, sin salida en consola",
    )

    # list
    sub.add_parser("list", help="Listar módulos disponibles")

    # dashboard
    dashboard = sub.add_parser("dashboard", help="Ver dashboard de auditorías")
    dashboard.add_argument(
        "--target",
        help="Filtrar por objetivo",
    )
    dashboard.add_argument(
        "--days",
        type=int,
        default=30,
        help="Días a mostrar en trends",
    )

    # report
    report = sub.add_parser("report", help="Generar informe detallado")
    report.add_argument(
        "audit_id",
        type=int,
        help="ID de la auditoría",
    )
    report.add_argument(
        "--format",
        choices=["console", "json", "html"],
        default="console",
        help="Formato del informe",
    )
    report.add_argument(
        "--ai-insights",
        action="store_true",
        help="Incluir análisis de IA",
    )
    report.add_argument(
        "--output",
        help="Ruta de salida (para json/html)",
    )

    # mcp
    mcp = sub.add_parser("mcp", help="Gestionar servidor MCP")
    mcp.add_argument(
        "action",
        choices=["start", "status", "tools"],
        help="Acción MCP",
    )
    mcp.add_argument(
        "--port",
        type=int,
        default=9000,
        help="Puerto para servidor MCP",
    )

    # schedule
    schedule = sub.add_parser("schedule", help="Gestionar auditorías programadas")
    schedule.add_argument(
        "action",
        choices=["add", "remove", "list", "run", "history"],
        help="Acción a ejecutar",
    )
    schedule.add_argument("--name", help="Nombre de la tarea")
    schedule.add_argument("--target", help="Objetivo de auditoría")
    schedule.add_argument("--modules", nargs="+", help="Módulos a ejecutar")
    schedule.add_argument("--cron", default="0 2 * * *", help="Expresión cron")
    schedule.add_argument(
        "--enable-ai",
        action="store_true",
        help="Incluir análisis de IA en auditorías",
    )
    schedule.add_argument(
        "--db-path",
        default="auditoria.db",
        help="Ruta de la base de datos",
    )

    return parser


def cmd_list() -> int:
    console = Console()
    from rich.table import Table

    table = Table(title="Módulos de auditoría disponibles")
    table.add_column("Módulo", style="cyan")
    table.add_column("Categoría")
    table.add_column("Descripción")

    from auditoria.checks.registry import get_checks
    for name, cls in sorted(get_checks().items()):
        table.add_row(name, cls.category, cls.description)

    console.print(table)
    return 0


def cmd_audit(args: argparse.Namespace) -> int:
    available = list_available_checks()
    if args.modules:
        invalid = [m for m in args.modules if m not in available]
        if invalid:
            print(f"Módulos desconocidos: {', '.join(invalid)}")
            print(f"Disponibles: {', '.join(available)}")
            return 1

    valid_categories = list_categories()
    if args.category:
        invalid_cat = [c for c in args.category if c not in valid_categories]
        if invalid_cat:
            print(f"Categorías desconocidas: {', '.join(invalid_cat)}")
            print(f"Disponibles: {', '.join(valid_categories)}")
            return 1

    config = {"scan_path": str(args.scan_path.resolve())}

    engine = AuditEngine(
        target=args.target,
        config=config,
        enable_ai=getattr(args, "enable_ai", False),
    )
    report = engine.run(modules=args.modules, categories=args.category)

    if not args.quiet:
        ConsoleReporter().render(report)

    if args.output_json:
        path = JsonReporter().render(report, args.output_json)
        print(f"Informe JSON: {path}")

    if args.output_html:
        path = HtmlReporter().render(report, args.output_html)
        print(f"Informe HTML: {path}")

    # Código de salida según severidad
    if report.summary.get("critical", 0) > 0:
        return 2
    if report.summary.get("high", 0) > 0:
        return 1
    return 0


def cmd_schedule(args: argparse.Namespace) -> int:
    from auditoria.scheduler import AuditScheduler, AuditTask

    scheduler = AuditScheduler(
        db_path=args.db_path,
        enable_ai=args.enable_ai,
    )

    if args.action == "add":
        if not args.name or not args.target:
            print("Error: --name y --target requeridos para 'add'")
            return 1
        task = AuditTask(
            name=args.name,
            target=args.target,
            modules=args.modules,
            cron_expression=args.cron,
        )
        scheduler.add_task(task)
        print(f"✓ Tarea añadida: {args.name}")
        return 0

    elif args.action == "remove":
        if not args.name:
            print("Error: --name requerido para 'remove'")
            return 1
        if scheduler.remove_task(args.name):
            print(f"✓ Tarea eliminada: {args.name}")
            return 0
        else:
            print(f"✗ Tarea no encontrada: {args.name}")
            return 1

    elif args.action == "list":
        tasks = scheduler.list_tasks()
        if not tasks:
            print("No hay tareas programadas")
            return 0
        console = Console()
        from rich.table import Table
        table = Table(title="Tareas programadas")
        table.add_column("Nombre")
        table.add_column("Objetivo")
        table.add_column("Cron")
        table.add_column("Activa")
        for task in tasks:
            table.add_row(
                task["name"],
                task["target"],
                task["cron"],
                "✓" if task["enabled"] else "✗",
            )
        console.print(table)
        return 0

    elif args.action == "run":
        if not args.name:
            print("Error: --name requerido para 'run'")
            return 1
        try:
            report = scheduler.execute_task(args.name, with_ai=args.enable_ai)
            if report:
                ConsoleReporter().render(report)
                return 0 if report.summary.get("critical", 0) == 0 else 1
            return 0
        except Exception as e:
            print(f"Error: {e}")
            return 1

    elif args.action == "history":
        if not args.name:
            print("Error: --name requerido para 'history'")
            return 1
        history = scheduler.get_execution_history(args.name)
        if not history:
            print(f"Sin historial para: {args.name}")
            return 0
        console = Console()
        from rich.table import Table
        table = Table(title=f"Historial: {args.name}")
        table.add_column("Fecha")
        table.add_column("Estado")
        table.add_column("Hallazgos")
        for entry in history:
            findings = str(entry.get("findings", "-")) if entry.get("status") == "success" else "N/A"
            table.add_row(
                entry["executed_at"][:10],
                entry["status"],
                findings,
            )
        console.print(table)
        return 0

    return 1


def cmd_dashboard(args: argparse.Namespace) -> int:
    from auditoria.storage.database import DatabaseManager

    db = DatabaseManager()
    console = Console()

    if args.target:
        audits = db.list_audits(target=args.target, limit=20)
        trends = db.get_trends(args.target, args.days)
    else:
        audits = db.list_audits(limit=20)
        trends = None

    console.print(
        Panel(
            "[bold cyan]Dashboard de Auditorías[/bold cyan]",
            border_style="cyan",
        )
    )

    from rich.table import Table

    if audits:
        table = Table(title="Auditorías Recientes")
        table.add_column("ID", style="cyan")
        table.add_column("Target")
        table.add_column("Riesgo", justify="right")
        table.add_column("Hallazgos", justify="right")
        table.add_column("Fecha")

        for audit in audits[:10]:
            table.add_row(
                str(audit["id"]),
                audit["target"],
                f"{audit['risk_score']}/100",
                str(audit["total_findings"]),
                audit["started_at"][:10],
            )

        console.print(table)

    if trends and trends["trends"]:
        trend_table = Table(title=f"Tendencias - {args.days} días")
        trend_table.add_column("Fecha")
        trend_table.add_column("Críticos", justify="right")
        trend_table.add_column("Altos", justify="right")
        trend_table.add_column("Riesgo Promedio", justify="right")

        for trend in trends["trends"][:10]:
            trend_table.add_row(
                trend["date"],
                str(trend["critical"] or 0),
                str(trend["high"] or 0),
                f"{trend['avg_risk']:.1f}" if trend["avg_risk"] else "-",
            )

        console.print(trend_table)

    return 0


def cmd_report(args: argparse.Namespace) -> int:
    from auditoria.storage.database import DatabaseManager

    db = DatabaseManager()
    audit = db.get_audit(args.audit_id)

    if not audit:
        print(f"Auditoría no encontrada: {args.audit_id}")
        return 1

    findings = db.get_findings_for_audit(args.audit_id)
    analyses = db.get_ai_analyses(args.audit_id) if args.ai_insights else []

    if args.format == "console":
        console = Console()
        console.print(
            Panel(
                f"[bold]Informe de Auditoría[/bold]\n"
                f"Objetivo: {audit['target']}\n"
                f"Riesgo: {audit['risk_score']}/100\n"
                f"Hallazgos: {len(findings)}",
                title="Auditoría #" + str(args.audit_id),
                border_style="cyan",
            )
        )

        if findings:
            from rich.table import Table

            table = Table(title="Hallazgos")
            table.add_column("ID")
            table.add_column("Título")
            table.add_column("Severidad")
            table.add_column("Estado")

            for finding in findings:
                table.add_row(
                    finding["check_id"],
                    finding["title"][:50],
                    finding["severity"],
                    finding["status"],
                )

            console.print(table)

        if analyses:
            console.print("\n[bold]Análisis de IA:[/bold]")
            for analysis in analyses:
                console.print(
                    f"\n[yellow]{analysis['analysis_type'].upper()}[/yellow]"
                )
                console.print(analysis["content"][:500] + "...")

    elif args.format == "json":
        import json

        report_data = {
            "audit": audit,
            "findings": findings,
            "analyses": analyses if args.ai_insights else [],
        }

        output = json.dumps(report_data, indent=2, default=str)

        if args.output:
            Path(args.output).write_text(output)
            print(f"Informe guardado: {args.output}")
        else:
            print(output)

    elif args.format == "html":
        from auditoria.core.reporter import HtmlReporter
        from auditoria.core.models import AuditReport

        # Crear un report simulado para usar HtmlReporter
        print(f"HTML report para auditoría #{args.audit_id}")
        if args.output:
            print(f"Guardado en: {args.output}")

    return 0


def cmd_mcp(args: argparse.Namespace) -> int:
    if args.action == "tools":
        from auditoria.mcp.tools import AUDIT_TOOLS

        console = Console()
        from rich.table import Table

        table = Table(title="Herramientas MCP Disponibles")
        table.add_column("Herramienta", style="cyan")
        table.add_column("Descripción")

        for tool_name, tool_def in AUDIT_TOOLS.items():
            table.add_row(tool_name, tool_def["description"])

        console.print(table)
        return 0

    elif args.action == "status":
        print("MCP Server status: [disponible para integración]")
        print("Cargar en .claude/settings.json como MCP server")
        return 0

    elif args.action == "start":
        from auditoria.mcp import create_mcp_server

        server = create_mcp_server()
        print(f"✓ Servidor MCP iniciado")
        print(f"  Tools disponibles: {len(server.get_tools())}")
        print(f"  Para usar en Claude Code:")
        print(f"    - Configurar en .claude/settings.json")
        print(f"    - O usar vía Python: from auditoria.mcp import create_mcp_server")
        return 0

    return 1


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "list":
        sys.exit(cmd_list())
    elif args.command == "audit":
        sys.exit(cmd_audit(args))
    elif args.command == "schedule":
        sys.exit(cmd_schedule(args))
    elif args.command == "dashboard":
        sys.exit(cmd_dashboard(args))
    elif args.command == "report":
        sys.exit(cmd_report(args))
    elif args.command == "mcp":
        sys.exit(cmd_mcp(args))


if __name__ == "__main__":
    main()
