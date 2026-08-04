"""Ejecutor autónomo de auditorías programadas."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Callable, Optional

from auditoria.core.engine import AuditEngine
from auditoria.core.models import AuditReport


@dataclass
class AuditTask:
    """Define una auditoría programada."""

    name: str
    target: str
    modules: Optional[list[str]] = None
    categories: Optional[list[str]] = None
    config: dict[str, Any] = field(default_factory=dict)
    cron_expression: str = "0 2 * * *"  # 2am diariamente por defecto
    enabled: bool = True
    description: str = ""
    on_complete: Optional[Callable[[AuditReport], None]] = None

    def to_dict(self) -> dict:
        """Serializa a JSON (sin callbacks)."""
        return {
            "name": self.name,
            "target": self.target,
            "modules": self.modules,
            "categories": self.categories,
            "config": self.config,
            "cron_expression": self.cron_expression,
            "enabled": self.enabled,
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, data: dict) -> AuditTask:
        """Deserializa desde JSON."""
        return cls(**data)


class AuditScheduler:
    """Gestiona ejecución autónoma de auditorías programadas."""

    def __init__(
        self,
        db_path: str = "auditoria.db",
        config_path: Optional[str] = None,
        enable_ai: bool = False,
    ):
        self.db_path = db_path
        self.config_path = config_path or "audit_tasks.json"
        self.enable_ai = enable_ai
        self.tasks: dict[str, AuditTask] = {}
        self.execution_history: dict[str, list[dict]] = {}
        self._load_tasks()

    def _load_tasks(self) -> None:
        """Carga tareas desde archivo JSON."""
        config_file = Path(self.config_path)
        if config_file.exists():
            try:
                data = json.loads(config_file.read_text())
                for task_data in data.get("tasks", []):
                    task = AuditTask.from_dict(task_data)
                    self.tasks[task.name] = task
            except Exception as e:
                print(f"Advertencia: No se pudieron cargar tareas: {e}")

    def save_tasks(self) -> None:
        """Guarda tareas en archivo JSON."""
        data = {
            "tasks": [task.to_dict() for task in self.tasks.values()],
            "saved_at": datetime.now().isoformat(),
        }
        Path(self.config_path).write_text(json.dumps(data, indent=2))

    def add_task(self, task: AuditTask) -> None:
        """Añade nueva tarea programada."""
        self.tasks[task.name] = task
        self.execution_history[task.name] = []
        self.save_tasks()

    def remove_task(self, task_name: str) -> bool:
        """Elimina una tarea programada."""
        if task_name in self.tasks:
            del self.tasks[task_name]
            self.save_tasks()
            return True
        return False

    def execute_task(self, task_name: str, with_ai: bool = None) -> Optional[AuditReport]:
        """Ejecuta una tarea manualmente."""
        if task_name not in self.tasks:
            raise ValueError(f"Tarea no encontrada: {task_name}")

        task = self.tasks[task_name]
        if not task.enabled:
            print(f"Tarea deshabilitada: {task_name}")
            return None

        use_ai = with_ai if with_ai is not None else self.enable_ai

        engine = AuditEngine(
            target=task.target,
            config={**task.config, "persist_audits": True, "db_path": self.db_path},
            enable_ai=use_ai,
        )

        try:
            report = engine.run(modules=task.modules, categories=task.categories)

            self.execution_history[task_name].append({
                "executed_at": datetime.now().isoformat(),
                "status": "success",
                "risk_score": report.risk_score,
                "findings": len(report.all_findings),
            })

            if task.on_complete:
                task.on_complete(report)

            return report
        except Exception as e:
            self.execution_history[task_name].append({
                "executed_at": datetime.now().isoformat(),
                "status": "error",
                "error": str(e),
            })
            raise

    def execute_all_due(self) -> dict[str, Optional[AuditReport]]:
        """Ejecuta todas las tareas programadas que están vencidas (simulado)."""
        results = {}
        for task_name, task in self.tasks.items():
            if task.enabled:
                try:
                    results[task_name] = self.execute_task(task_name)
                except Exception as e:
                    print(f"Error ejecutando {task_name}: {e}")
                    results[task_name] = None
        return results

    def get_execution_history(self, task_name: str, limit: int = 10) -> list[dict]:
        """Obtiene historial de ejecución de una tarea."""
        return self.execution_history.get(task_name, [])[:limit]

    def list_tasks(self) -> list[dict]:
        """Lista todas las tareas con su estado."""
        return [
            {
                "name": task.name,
                "target": task.target,
                "enabled": task.enabled,
                "cron": task.cron_expression,
                "description": task.description,
                "last_execution": (
                    self.execution_history[task.name][-1]
                    if self.execution_history.get(task.name)
                    else None
                ),
            }
            for task in self.tasks.values()
        ]
