"""Sistema de webhooks para notificaciones en tiempo real."""

from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Optional

import requests

from auditoria.core.models import AuditReport


@dataclass
class Webhook:
    """Define un webhook para eventos de auditoría."""

    id: str
    url: str
    events: list[str]  # "audit.completed", "finding.critical", etc.
    active: bool = True
    secret: Optional[str] = None
    headers: dict[str, str] = None
    created_at: str = None

    def __post_init__(self):
        if self.headers is None:
            self.headers = {}
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()

    def to_dict(self) -> dict:
        data = asdict(self)
        return data


class WebhookManager:
    """Gestiona webhooks y notificaciones."""

    def __init__(self, webhooks_path: str = "webhooks.json"):
        self.webhooks_path = Path(webhooks_path)
        self.webhooks: dict[str, Webhook] = {}
        self._load_webhooks()

    def _load_webhooks(self) -> None:
        """Carga webhooks desde archivo JSON."""
        if self.webhooks_path.exists():
            try:
                data = json.loads(self.webhooks_path.read_text())
                for webhook_data in data.get("webhooks", []):
                    webhook = Webhook(**webhook_data)
                    self.webhooks[webhook.id] = webhook
            except Exception as e:
                print(f"Advertencia: No se pudieron cargar webhooks: {e}")

    def save_webhooks(self) -> None:
        """Guarda webhooks en archivo JSON."""
        data = {
            "webhooks": [w.to_dict() for w in self.webhooks.values()],
            "saved_at": datetime.now().isoformat(),
        }
        self.webhooks_path.write_text(json.dumps(data, indent=2))

    def register_webhook(
        self,
        webhook_id: str,
        url: str,
        events: list[str],
        secret: Optional[str] = None,
        headers: Optional[dict[str, str]] = None,
    ) -> Webhook:
        """Registra un nuevo webhook."""
        webhook = Webhook(
            id=webhook_id,
            url=url,
            events=events,
            secret=secret,
            headers=headers or {},
        )
        self.webhooks[webhook_id] = webhook
        self.save_webhooks()
        return webhook

    def unregister_webhook(self, webhook_id: str) -> bool:
        """Elimina un webhook."""
        if webhook_id in self.webhooks:
            del self.webhooks[webhook_id]
            self.save_webhooks()
            return True
        return False

    def trigger_event(
        self,
        event_type: str,
        data: dict[str, Any],
        report: Optional[AuditReport] = None,
    ) -> dict[str, Any]:
        """Dispara un evento y notifica webhooks interesados."""
        results = {}

        for webhook in self.webhooks.values():
            if not webhook.active or event_type not in webhook.events:
                continue

            payload = {
                "event": event_type,
                "timestamp": datetime.now().isoformat(),
                "data": data,
            }

            if report:
                payload["report"] = {
                    "target": report.target,
                    "risk_score": report.risk_score,
                    "total_findings": len(report.all_findings),
                    "summary": report.summary,
                }

            results[webhook.id] = self._send_webhook(webhook, payload)

        return results

    def _send_webhook(self, webhook: Webhook, payload: dict) -> dict[str, Any]:
        """Envía una notificación a un webhook."""
        headers = {
            "Content-Type": "application/json",
            **webhook.headers,
        }

        if webhook.secret:
            import hmac
            import hashlib

            signature = hmac.new(
                webhook.secret.encode(),
                json.dumps(payload).encode(),
                hashlib.sha256,
            ).hexdigest()
            headers["X-Webhook-Signature"] = f"sha256={signature}"

        try:
            response = requests.post(
                webhook.url,
                json=payload,
                headers=headers,
                timeout=10,
            )
            return {
                "status": "success",
                "status_code": response.status_code,
                "timestamp": datetime.now().isoformat(),
            }
        except requests.exceptions.RequestException as e:
            return {
                "status": "failed",
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }

    def list_webhooks(self) -> list[dict]:
        """Lista todos los webhooks."""
        return [w.to_dict() for w in self.webhooks.values()]

    def get_webhook(self, webhook_id: str) -> Optional[Webhook]:
        """Obtiene un webhook por ID."""
        return self.webhooks.get(webhook_id)
