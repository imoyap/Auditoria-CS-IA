"""API REST para auditorías autónomas."""

from __future__ import annotations

import json
from typing import Any, Optional

from auditoria.api.webhooks import WebhookManager
from auditoria.core.engine import AuditEngine
from auditoria.core.models import AuditReport
from auditoria.scheduler import AuditScheduler, AuditTask
from auditoria.storage.database import DatabaseManager


def create_app(
    db_path: str = "auditoria.db",
    webhooks_path: str = "webhooks.json",
):
    """Factory para crear aplicación Flask."""
    try:
        from flask import Flask, jsonify, request
    except ImportError:
        raise ImportError("Flask no instalado. Ejecute: pip install flask")

    app = Flask(__name__)
    db_manager = DatabaseManager(db_path)
    webhook_manager = WebhookManager(webhooks_path)
    scheduler = AuditScheduler(db_path=db_path)

    @app.route("/health", methods=["GET"])
    def health():
        """Health check endpoint."""
        return jsonify({
            "status": "healthy",
            "version": "1.0.0",
        })

    @app.route("/api/v1/audits", methods=["POST"])
    def create_audit():
        """Ejecuta una auditoría inmediata."""
        data = request.get_json()

        target = data.get("target")
        modules = data.get("modules")
        categories = data.get("categories")
        enable_ai = data.get("enable_ai", False)

        if not target:
            return jsonify({"error": "target requerido"}), 400

        try:
            engine = AuditEngine(
                target=target,
                config={
                    "persist_audits": True,
                    "db_path": db_path,
                    **data.get("config", {}),
                },
                enable_ai=enable_ai,
            )

            report = engine.run(modules=modules, categories=categories)

            webhook_manager.trigger_event(
                "audit.completed",
                {
                    "audit_id": report.metadata.get("audit_id"),
                    "target": target,
                    "risk_score": report.risk_score,
                },
                report,
            )

            return jsonify({
                "audit_id": report.metadata.get("audit_id"),
                "target": report.target,
                "risk_score": report.risk_score,
                "total_findings": len(report.all_findings),
                "summary": report.summary,
            }), 201

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/v1/audits/<int:audit_id>", methods=["GET"])
    def get_audit(audit_id: int):
        """Obtiene detalles de una auditoría."""
        audit = db_manager.get_audit(audit_id)
        if not audit:
            return jsonify({"error": "Auditoría no encontrada"}), 404

        findings = db_manager.get_findings_for_audit(audit_id)
        analyses = db_manager.get_ai_analyses(audit_id)

        return jsonify({
            "audit": audit,
            "findings": findings,
            "ai_analyses": analyses,
        })

    @app.route("/api/v1/audits", methods=["GET"])
    def list_audits():
        """Lista auditorías con filtros opcionales."""
        target = request.args.get("target")
        limit = int(request.args.get("limit", 50))

        audits = db_manager.list_audits(target=target, limit=limit)
        return jsonify({"audits": audits})

    @app.route("/api/v1/audits/<int:audit_id>/findings", methods=["GET"])
    def get_findings(audit_id: int):
        """Obtiene hallazgos de una auditoría."""
        findings = db_manager.get_findings_for_audit(audit_id)
        if not findings and not db_manager.get_audit(audit_id):
            return jsonify({"error": "Auditoría no encontrada"}), 404

        return jsonify({"findings": findings})

    @app.route("/api/v1/audits/<int:audit_id>/analyses", methods=["GET"])
    def get_analyses(audit_id: int):
        """Obtiene análisis de IA de una auditoría."""
        analyses = db_manager.get_ai_analyses(audit_id)
        if not analyses and not db_manager.get_audit(audit_id):
            return jsonify({"error": "Auditoría no encontrada"}), 404

        return jsonify({"analyses": analyses})

    @app.route("/api/v1/targets/<target>/trends", methods=["GET"])
    def get_trends(target: str):
        """Obtiene tendencias de riesgo para un objetivo."""
        days = int(request.args.get("days", 30))
        trends = db_manager.get_trends(target, days)
        return jsonify(trends)

    @app.route("/api/v1/tasks", methods=["POST"])
    def create_task():
        """Crea una auditoría programada."""
        data = request.get_json()

        name = data.get("name")
        target = data.get("target")
        cron = data.get("cron", "0 2 * * *")

        if not name or not target:
            return jsonify({"error": "name y target requeridos"}), 400

        task = AuditTask(
            name=name,
            target=target,
            modules=data.get("modules"),
            categories=data.get("categories"),
            cron_expression=cron,
            description=data.get("description", ""),
            config=data.get("config", {}),
        )

        scheduler.add_task(task)

        return jsonify({
            "name": task.name,
            "target": task.target,
            "cron": task.cron_expression,
        }), 201

    @app.route("/api/v1/tasks", methods=["GET"])
    def list_tasks():
        """Lista tareas programadas."""
        tasks = scheduler.list_tasks()
        return jsonify({"tasks": tasks})

    @app.route("/api/v1/tasks/<task_name>", methods=["DELETE"])
    def delete_task(task_name: str):
        """Elimina una tarea programada."""
        if scheduler.remove_task(task_name):
            return jsonify({"message": f"Tarea eliminada: {task_name}"}), 200
        return jsonify({"error": "Tarea no encontrada"}), 404

    @app.route("/api/v1/tasks/<task_name>/run", methods=["POST"])
    def run_task(task_name: str):
        """Ejecuta una tarea programada manualmente."""
        enable_ai = request.get_json().get("enable_ai", False) if request.is_json else False

        try:
            report = scheduler.execute_task(task_name, with_ai=enable_ai)
            if not report:
                return jsonify({"error": "Tarea deshabilitada"}), 400

            webhook_manager.trigger_event(
                "task.executed",
                {
                    "task_name": task_name,
                    "audit_id": report.metadata.get("audit_id"),
                },
                report,
            )

            return jsonify({
                "audit_id": report.metadata.get("audit_id"),
                "target": report.target,
                "risk_score": report.risk_score,
                "total_findings": len(report.all_findings),
            }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/v1/tasks/<task_name>/history", methods=["GET"])
    def get_task_history(task_name: str):
        """Obtiene historial de ejecución de una tarea."""
        limit = int(request.args.get("limit", 10))
        history = scheduler.get_execution_history(task_name, limit)
        return jsonify({"history": history})

    @app.route("/api/v1/webhooks", methods=["POST"])
    def register_webhook():
        """Registra un nuevo webhook."""
        data = request.get_json()

        webhook_id = data.get("id")
        url = data.get("url")
        events = data.get("events")

        if not all([webhook_id, url, events]):
            return jsonify({"error": "id, url y events requeridos"}), 400

        webhook = webhook_manager.register_webhook(
            webhook_id=webhook_id,
            url=url,
            events=events,
            secret=data.get("secret"),
            headers=data.get("headers"),
        )

        return jsonify(webhook.to_dict()), 201

    @app.route("/api/v1/webhooks", methods=["GET"])
    def list_webhooks():
        """Lista todos los webhooks registrados."""
        webhooks = webhook_manager.list_webhooks()
        return jsonify({"webhooks": webhooks})

    @app.route("/api/v1/webhooks/<webhook_id>", methods=["DELETE"])
    def delete_webhook(webhook_id: str):
        """Elimina un webhook."""
        if webhook_manager.unregister_webhook(webhook_id):
            return jsonify({"message": f"Webhook eliminado: {webhook_id}"}), 200
        return jsonify({"error": "Webhook no encontrado"}), 404

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Endpoint no encontrado"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "Error interno del servidor"}), 500

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
