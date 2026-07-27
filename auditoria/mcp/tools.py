"""Definición de herramientas MCP para auditorías."""

from typing import Any

# Herramientas disponibles en MCP
AUDIT_TOOLS = {
    "execute_audit": {
        "description": "Ejecuta una auditoría de seguridad sobre un objetivo",
        "inputSchema": {
            "type": "object",
            "properties": {
                "target": {
                    "type": "string",
                    "description": "Objetivo de auditoría (hostname, IP, dominio)",
                },
                "modules": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Módulos a ejecutar (system, network, ssl, filesystem, secrets)",
                },
                "categories": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Categorías a filtrar",
                },
                "enable_ai": {
                    "type": "boolean",
                    "description": "Incluir análisis de IA",
                    "default": True,
                },
                "scan_path": {
                    "type": "string",
                    "description": "Ruta para escaneo de archivos",
                    "default": ".",
                },
            },
            "required": ["target"],
        },
    },
    "get_audit_history": {
        "description": "Obtiene historial de auditorías ejecutadas",
        "inputSchema": {
            "type": "object",
            "properties": {
                "target": {
                    "type": "string",
                    "description": "Filtrar por objetivo (opcional)",
                },
                "limit": {
                    "type": "integer",
                    "description": "Número de auditorías a retornar",
                    "default": 10,
                },
            },
        },
    },
    "get_audit_details": {
        "description": "Obtiene detalles completos de una auditoría",
        "inputSchema": {
            "type": "object",
            "properties": {
                "audit_id": {
                    "type": "integer",
                    "description": "ID de la auditoría",
                },
            },
            "required": ["audit_id"],
        },
    },
    "analyze_findings": {
        "description": "Analiza hallazgos con IA para obtener insights",
        "inputSchema": {
            "type": "object",
            "properties": {
                "audit_id": {
                    "type": "integer",
                    "description": "ID de la auditoría",
                },
                "analysis_type": {
                    "type": "string",
                    "enum": ["prioritize", "patterns", "executive_summary"],
                    "description": "Tipo de análisis a realizar",
                },
            },
            "required": ["audit_id", "analysis_type"],
        },
    },
    "create_scheduled_task": {
        "description": "Crea una tarea de auditoría programada",
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Nombre de la tarea",
                },
                "target": {
                    "type": "string",
                    "description": "Objetivo de la auditoría",
                },
                "cron": {
                    "type": "string",
                    "description": "Expresión cron para programación",
                    "default": "0 2 * * *",
                },
                "modules": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Módulos a ejecutar",
                },
                "enable_ai": {
                    "type": "boolean",
                    "description": "Incluir análisis de IA",
                    "default": True,
                },
            },
            "required": ["name", "target"],
        },
    },
    "list_scheduled_tasks": {
        "description": "Lista todas las tareas programadas",
        "inputSchema": {
            "type": "object",
            "properties": {},
        },
    },
    "execute_scheduled_task": {
        "description": "Ejecuta una tarea programada manualmente",
        "inputSchema": {
            "type": "object",
            "properties": {
                "task_name": {
                    "type": "string",
                    "description": "Nombre de la tarea a ejecutar",
                },
                "enable_ai": {
                    "type": "boolean",
                    "description": "Incluir análisis de IA",
                    "default": True,
                },
            },
            "required": ["task_name"],
        },
    },
    "get_trends": {
        "description": "Obtiene tendencias de riesgo para un objetivo",
        "inputSchema": {
            "type": "object",
            "properties": {
                "target": {
                    "type": "string",
                    "description": "Objetivo a analizar",
                },
                "days": {
                    "type": "integer",
                    "description": "Días a analizar",
                    "default": 30,
                },
            },
            "required": ["target"],
        },
    },
    "register_webhook": {
        "description": "Registra un webhook para notificaciones",
        "inputSchema": {
            "type": "object",
            "properties": {
                "webhook_id": {
                    "type": "string",
                    "description": "ID único del webhook",
                },
                "url": {
                    "type": "string",
                    "description": "URL del webhook",
                },
                "events": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Eventos a notificar",
                },
                "secret": {
                    "type": "string",
                    "description": "Secret para HMAC verification",
                },
            },
            "required": ["webhook_id", "url", "events"],
        },
    },
}
