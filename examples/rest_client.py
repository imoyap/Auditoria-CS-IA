#!/usr/bin/env python
"""Ejemplo cliente REST para Auditoria API."""

import json
import requests
from pathlib import Path


class AuditorialClient:
    """Cliente para Auditoria REST API."""

    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url
        self.session = requests.Session()

    def health_check(self) -> dict:
        """Verifica salud de la API."""
        resp = self.session.get(f"{self.base_url}/health")
        return resp.json()

    def execute_audit(
        self,
        target: str,
        modules: list[str] = None,
        enable_ai: bool = True,
    ) -> dict:
        """Ejecuta una auditoría."""
        payload = {
            "target": target,
            "modules": modules,
            "enable_ai": enable_ai,
        }
        resp = self.session.post(
            f"{self.base_url}/api/v1/audits",
            json=payload,
        )
        return resp.json()

    def get_audit(self, audit_id: int) -> dict:
        """Obtiene detalles de auditoría."""
        resp = self.session.get(f"{self.base_url}/api/v1/audits/{audit_id}")
        return resp.json()

    def list_audits(self, target: str = None, limit: int = 50) -> dict:
        """Lista auditorías."""
        params = {"limit": limit}
        if target:
            params["target"] = target
        resp = self.session.get(f"{self.base_url}/api/v1/audits", params=params)
        return resp.json()

    def create_task(
        self,
        name: str,
        target: str,
        cron: str = "0 2 * * *",
        modules: list[str] = None,
    ) -> dict:
        """Crea tarea programada."""
        payload = {
            "name": name,
            "target": target,
            "cron": cron,
            "modules": modules,
        }
        resp = self.session.post(f"{self.base_url}/api/v1/tasks", json=payload)
        return resp.json()

    def execute_task(self, task_name: str) -> dict:
        """Ejecuta tarea programada."""
        resp = self.session.post(f"{self.base_url}/api/v1/tasks/{task_name}/run")
        return resp.json()

    def register_webhook(
        self,
        webhook_id: str,
        url: str,
        events: list[str],
        secret: str = None,
    ) -> dict:
        """Registra webhook."""
        payload = {
            "id": webhook_id,
            "url": url,
            "events": events,
            "secret": secret,
        }
        resp = self.session.post(f"{self.base_url}/api/v1/webhooks", json=payload)
        return resp.json()

    def get_trends(self, target: str, days: int = 30) -> dict:
        """Obtiene tendencias."""
        resp = self.session.get(
            f"{self.base_url}/api/v1/targets/{target}/trends",
            params={"days": days},
        )
        return resp.json()


def main():
    """Ejemplo de uso del cliente."""
    client = AuditorialClient()

    print("🔍 Auditoria REST Client - Ejemplo\n")

    # 1. Health check
    print("1️⃣  Health check...")
    health = client.health_check()
    print(f"   Status: {health.get('status')}\n")

    # 2. Ejecutar auditoría
    print("2️⃣  Ejecutando auditoría...")
    audit = client.execute_audit(target="localhost", enable_ai=False)
    if "error" in audit:
        print(f"   Error: {audit['error']}")
    else:
        print(f"   Audit ID: {audit.get('audit_id')}")
        print(f"   Risk Score: {audit.get('risk_score')}/100")
        print(f"   Findings: {audit.get('total_findings')}\n")

        audit_id = audit.get("audit_id")
        if audit_id:
            # 3. Obtener detalles
            print(f"3️⃣  Obteniendo detalles de auditoría #{audit_id}...")
            details = client.get_audit(audit_id)
            print(f"   Audit: {details['audit']['target']}")
            print(f"   Findings: {len(details.get('findings', []))}\n")

    # 4. Crear tarea
    print("4️⃣  Creando tarea programada...")
    task = client.create_task(
        name="demo-task",
        target="example.com",
        modules=["network", "ssl"],
    )
    if "error" in task:
        print(f"   Error: {task['error']}")
    else:
        print(f"   Task: {task.get('name')}")
        print(f"   Cron: {task.get('cron')}\n")

    # 5. Registrar webhook
    print("5️⃣  Registrando webhook...")
    webhook = client.register_webhook(
        webhook_id="demo-webhook",
        url="https://example.com/webhook",
        events=["audit.completed"],
    )
    if "error" in webhook:
        print(f"   Error: {webhook['error']}")
    else:
        print(f"   Webhook ID: {webhook.get('webhook_id')}")
        print(f"   Events: {webhook.get('events')}\n")

    # 6. Obtener tendencias
    print("6️⃣  Obteniendo tendencias...")
    trends = client.get_trends(target="localhost", days=30)
    if "error" in trends:
        print(f"   Error: {trends['error']}")
    else:
        print(f"   Target: {trends.get('target')}")
        print(f"   Period: {trends.get('period_days')} días")
        print(f"   Data points: {len(trends.get('trends', []))}\n")

    print("✅ Ejemplo completado")


if __name__ == "__main__":
    main()
