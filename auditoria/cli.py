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

    engine = AuditEngine(target=args.target, config=config)
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


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "list":
        sys.exit(cmd_list())
    elif args.command == "audit":
        sys.exit(cmd_audit(args))


if __name__ == "__main__":
    main()
