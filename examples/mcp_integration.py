#!/usr/bin/env python
"""Ejemplo de integración con Auditoria MCP Server."""

import json
from auditoria.mcp import create_mcp_server


def main():
    """Demuestra uso del servidor MCP."""
    # Crear servidor
    server = create_mcp_server()

    print("🔧 Auditoria MCP Server - Ejemplo de Integración\n")

    # 1. Listar herramientas disponibles
    print("📋 Herramientas disponibles:")
    tools = server.get_tools()
    for tool_name in tools.keys():
        print(f"  - {tool_name}")

    print("\n" + "=" * 60 + "\n")

    # 2. Ejecutar auditoría
    print("▶️  Ejecutando auditoría remota...\n")
    result = server.call_tool(
        "execute_audit",
        {
            "target": "localhost",
            "modules": ["system"],
            "enable_ai": False,  # Cambiar a True si tienes ANTHROPIC_API_KEY
        },
    )
    audit_result = json.loads(result)
    print(json.dumps(audit_result, indent=2))

    if audit_result.get("audit_id"):
        audit_id = audit_result["audit_id"]

        print("\n" + "=" * 60 + "\n")

        # 3. Obtener detalles de auditoría
        print(f"📊 Detalles de auditoría #{audit_id}:\n")
        result = server.call_tool("get_audit_details", {"audit_id": audit_id})
        details = json.loads(result)
        print(json.dumps(details, indent=2, default=str)[:500] + "...\n")

        print("\n" + "=" * 60 + "\n")

        # 4. Crear tarea programada
        print("⏰ Creando tarea programada...\n")
        result = server.call_tool(
            "create_scheduled_task",
            {
                "name": "demo-audit",
                "target": "example.com",
                "cron": "0 2 * * *",
                "modules": ["network", "ssl"],
                "enable_ai": False,
            },
        )
        task_result = json.loads(result)
        print(json.dumps(task_result, indent=2))

        print("\n" + "=" * 60 + "\n")

        # 5. Listar tareas
        print("📝 Tareas programadas:\n")
        result = server.call_tool("list_scheduled_tasks", {})
        tasks = json.loads(result)
        print(json.dumps(tasks, indent=2))

        print("\n" + "=" * 60 + "\n")

        # 6. Registrar webhook
        print("🔗 Registrando webhook...\n")
        result = server.call_tool(
            "register_webhook",
            {
                "webhook_id": "demo-webhook",
                "url": "https://example.com/webhook",
                "events": ["audit.completed"],
                "secret": "my-secret-key",
            },
        )
        webhook_result = json.loads(result)
        print(json.dumps(webhook_result, indent=2))

    print("\n✅ Ejemplo completado\n")


if __name__ == "__main__":
    main()
