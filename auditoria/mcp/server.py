"""Servidor MCP (Model Context Protocol) para Auditoria."""

from __future__ import annotations

import json
from typing import Any, Callable

from auditoria.api.webhooks import WebhookManager
from auditoria.core.engine import AuditEngine
from auditoria.mcp.tools import AUDIT_TOOLS
from auditoria.scheduler import AuditScheduler
from auditoria.storage.database import DatabaseManager


def create_mcp_server(
    db_path: str = "auditoria.db",
    webhooks_path: str = "webhooks.json",
):
    """Factory para crear servidor MCP."""
    db_manager = DatabaseManager(db_path)
    scheduler = AuditScheduler(db_path=db_path)
    webhook_manager = WebhookManager(webhooks_path)

    class AuditoriaMCPServer:
        """Servidor MCP para herramientas de auditoría."""

        def __init__(self):
            self.tools = AUDIT_TOOLS
            self.handlers = {
                "execute_audit": self._handle_execute_audit,
                "get_audit_history": self._handle_get_history,
                "get_audit_details": self._handle_get_details,
                "analyze_findings": self._handle_analyze_findings,
                "create_scheduled_task": self._handle_create_task,
                "list_scheduled_tasks": self._handle_list_tasks,
                "execute_scheduled_task": self._handle_execute_task,
                "get_trends": self._handle_get_trends,
                "register_webhook": self._handle_register_webhook,
            }

        def get_tools(self) -> dict[str, Any]:
            """Retorna herramientas disponibles."""
            return self.tools

        def call_tool(self, tool_name: str, arguments: dict[str, Any]) -> str:
            """Ejecuta una herramienta MCP."""
            if tool_name not in self.handlers:
                return json.dumps({"error": f"Herramienta no encontrada: {tool_name}"})

            try:
                result = self.handlers[tool_name](**arguments)
                return json.dumps(result, default=str)
            except Exception as e:
                return json.dumps({"error": str(e)})

        def _handle_execute_audit(
            self,
            target: str,
            modules: list[str] = None,
            categories: list[str] = None,
            enable_ai: bool = True,
            scan_path: str = ".",
        ) -> dict[str, Any]:
            """Ejecuta una auditoría."""
            engine = AuditEngine(
                target=target,
                config={
                    "persist_audits": True,
                    "db_path": db_path,
                    "scan_path": scan_path,
                },
                enable_ai=enable_ai,
            )

            report = engine.run(modules=modules, categories=categories)

            webhook_manager.trigger_event(
                "audit.completed",
                {
                    "audit_id": report.metadata.get("audit_id"),
                    "target": target,
                },
                report,
            )

            return {
                "status": "completed",
                "audit_id": report.metadata.get("audit_id"),
                "target": report.target,
                "risk_score": report.risk_score,
                "total_findings": len(report.all_findings),
                "summary": report.summary,
            }

        def _handle_get_history(
            self, target: str = None, limit: int = 10
        ) -> dict[str, Any]:
            """Obtiene historial de auditorías."""
            audits = db_manager.list_audits(target=target, limit=limit)
            return {"audits": audits, "count": len(audits)}

        def _handle_get_details(self, audit_id: int) -> dict[str, Any]:
            """Obtiene detalles de una auditoría."""
            audit = db_manager.get_audit(audit_id)
            if not audit:
                return {"error": "Auditoría no encontrada"}

            findings = db_manager.get_findings_for_audit(audit_id)
            analyses = db_manager.get_ai_analyses(audit_id)

            return {
                "audit": audit,
                "findings": findings,
                "ai_analyses": analyses,
            }

        def _handle_analyze_findings(
            self, audit_id: int, analysis_type: str
        ) -> dict[str, Any]:
            """Obtiene análisis de IA."""
            analyses = db_manager.get_ai_analyses(audit_id)

            matching = [
                a for a in analyses if a.get("analysis_type") == analysis_type
            ]

            if not matching:
                return {
                    "error": f"No hay análisis tipo '{analysis_type}' para auditoría {audit_id}"
                }

            return {"analysis_type": analysis_type, "content": matching[0]["content"]}

        def _handle_create_task(
            self,
            name: str,
            target: str,
            cron: str = "0 2 * * *",
            modules: list[str] = None,
            enable_ai: bool = True,
        ) -> dict[str, Any]:
            """Crea tarea programada."""
            from auditoria.scheduler import AuditTask

            task = AuditTask(
                name=name,
                target=target,
                modules=modules,
                cron_expression=cron,
                config={"enable_ai": enable_ai},
            )

            scheduler.add_task(task)

            return {
                "status": "created",
                "name": task.name,
                "target": task.target,
                "cron": task.cron_expression,
            }

        def _handle_list_tasks(self) -> dict[str, Any]:
            """Lista tareas programadas."""
            tasks = scheduler.list_tasks()
            return {"tasks": tasks, "count": len(tasks)}

        def _handle_execute_task(
            self, task_name: str, enable_ai: bool = True
        ) -> dict[str, Any]:
            """Ejecuta tarea programada."""
            try:
                report = scheduler.execute_task(task_name, with_ai=enable_ai)
                if not report:
                    return {"error": "Tarea deshabilitada"}

                return {
                    "status": "executed",
                    "audit_id": report.metadata.get("audit_id"),
                    "target": report.target,
                    "risk_score": report.risk_score,
                }
            except Exception as e:
                return {"error": str(e)}

        def _handle_get_trends(
            self, target: str, days: int = 30
        ) -> dict[str, Any]:
            """Obtiene tendencias."""
            return db_manager.get_trends(target, days)

        def _handle_register_webhook(
            self,
            webhook_id: str,
            url: str,
            events: list[str],
            secret: str = None,
        ) -> dict[str, Any]:
            """Registra webhook."""
            webhook = webhook_manager.register_webhook(
                webhook_id=webhook_id,
                url=url,
                events=events,
                secret=secret,
            )

            return {
                "status": "registered",
                "webhook_id": webhook.id,
                "events": webhook.events,
            }

    return AuditoriaMCPServer()
