# Capacidades Avanzadas — Auditoria-CS-IA

Guía rápida de las nuevas capacidades: Harness, Skills, MCP Server y Advanced Commands.

## 🎯 Resumen de Capacidades

| Capacidad | Descripción | Ubicación |
|-----------|-------------|-----------|
| **Harness** | Integración con Claude Code settings | `.claude/settings.json` |
| **Skills** | Comandos personalizados de Claude Code | `.claude/skills/` |
| **MCP Server** | Protocol Model Context para integración | `auditoria/mcp/` |
| **CLI Avanzado** | Nuevos comandos dashboard, report, mcp | `auditoria/cli.py` |

---

## 1. ⚙️ Harness Integration

### Configuración
El archivo `.claude/settings.json` configura automáticamente:

```json
{
  "permissions": {
    "global": {
      "Bash": ["auditoria audit", "python -m auditoria", "git"],
      "Read": true,
      "Edit": true,
      "Write": true
    }
  },
  "hooks": {
    "after_edit_file": [
      {
        "pattern": "auditoria/**/*.py",
        "command": "python -m pytest auditoria/tests/ -v",
        "description": "Run tests after code changes"
      }
    ]
  },
  "environment": {
    "ANTHROPIC_API_KEY": "${ANTHROPIC_API_KEY}",
    "AUDITORIA_DB_PATH": "auditoria.db"
  },
  "integrations": {
    "mcp_servers": [
      {
        "name": "auditoria",
        "command": "python -m auditoria.mcp.server"
      }
    ]
  }
}
```

### Beneficios
- ✅ Permisos configurados automáticamente
- ✅ Tests ejecutados en cada cambio
- ✅ MCP server registrado
- ✅ Variables de entorno centralizadas
- ✅ Aliases de CLI: `/qa`, `/status`, `/api`

---

## 2. 📚 Skills para Claude Code

### Skill: /quick-audit
Ejecuta auditoría rápida con análisis de IA.

```bash
/quick-audit localhost --ai
/quick-audit example.com --modules network ssl --ai
/quick-audit /path/to/project --modules secrets
```

**Parámetros:**
- `target` (requerido): objetivo de auditoría
- `--modules`: módulos específicos
- `--ai`: incluir análisis de IA
- `--json`: output como JSON

---

### Skill: /audit-status
Revisar estado de tareas programadas.

```bash
/audit-status --list
/audit-status --task daily-prod-audit
/audit-status --task daily-prod-audit --history --limit 5
/audit-status --target example.com --history
```

**Parámetros:**
- `--list`: listar todas las tareas
- `--task`: estado de tarea específica
- `--history`: ver historial de ejecuciones
- `--target`: filtrar por objetivo
- `--limit`: límite de resultados

---

### Skill: /audit-api
Gestionar servidor REST API.

```bash
/audit-api start
/audit-api start --port 8000 --debug
/audit-api status
/audit-api stop
```

**Endpoints disponibles tras iniciar:**
- `POST /api/v1/audits` — Ejecutar auditoría
- `GET /api/v1/audits` — Listar auditorías
- `POST /api/v1/tasks` — Crear tarea
- `POST /api/v1/webhooks` — Registrar webhook
- Ver API.md para documentación completa

---

### Skill: /audit-report
Generar reportes detallados.

```bash
/audit-report 1
/audit-report 1 --format html --export /tmp/report.html
/audit-report 1 --ai-insights --format json
```

**Formatos:**
- `console` — Salida formateada en terminal
- `json` — JSON exportable
- `html` — Reporte web
- `pdf` — Documento PDF (futuro)

---

## 3. 🔌 MCP Server (Model Context Protocol)

### Inicio

**Via CLI:**
```bash
auditoria mcp start
auditoria mcp tools
auditoria mcp status
```

**Via Python:**
```python
from auditoria.mcp import create_mcp_server

server = create_mcp_server()
tools = server.get_tools()
result = server.call_tool("execute_audit", {"target": "example.com"})
```

### Herramientas Disponibles

| Herramienta | Parámetros | Retorna |
|-------------|-----------|---------|
| `execute_audit` | target, modules, enable_ai | audit_id, risk_score, findings |
| `get_audit_history` | target, limit | list[audit] |
| `get_audit_details` | audit_id | audit + findings + analyses |
| `analyze_findings` | audit_id, analysis_type | AI analysis |
| `create_scheduled_task` | name, target, cron | task_id |
| `list_scheduled_tasks` | - | list[task] |
| `execute_scheduled_task` | task_name | audit_result |
| `get_trends` | target, days | trend_data |
| `register_webhook` | webhook_id, url, events | webhook_id |

### Ejemplo Completo

```python
import json
from auditoria.mcp import create_mcp_server

server = create_mcp_server()

# Ejecutar auditoría
result = server.call_tool(
    "execute_audit",
    {"target": "localhost", "enable_ai": True}
)
audit = json.loads(result)
audit_id = audit["audit_id"]

# Analizar hallazgos
analysis = server.call_tool(
    "analyze_findings",
    {"audit_id": audit_id, "analysis_type": "prioritize"}
)

# Registrar webhook para notificaciones
webhook = server.call_tool(
    "register_webhook",
    {
        "webhook_id": "slack-alerts",
        "url": "https://hooks.slack.com/...",
        "events": ["audit.completed"]
    }
)

print(json.dumps({
    "audit": audit,
    "analysis": json.loads(analysis),
    "webhook": json.loads(webhook)
}, indent=2))
```

---

## 4. ⚙️ Comandos CLI Avanzados

### dashboard
Ver dashboard en tiempo real.

```bash
# Dashboard de todas las auditorías
auditoria dashboard

# Filtrar por objetivo
auditoria dashboard --target example.com

# Mostrar tendencias de 60 días
auditoria dashboard --target example.com --days 60
```

**Muestra:**
- Auditorías recientes con puntuación de riesgo
- Tabla de tendencias (críticos, altos, promedio)
- Evolución temporal de hallazgos

---

### report
Generar reportes flexibles.

```bash
# Ver en consola
auditoria report 1

# Exportar a JSON
auditoria report 1 --format json --output report.json

# Reporte HTML con análisis de IA
auditoria report 1 --format html --ai-insights --output report.html

# Reporte JSON con AI insights
auditoria report 1 --format json --ai-insights
```

**Secciones del reporte:**
- Executive Summary (AI-generado)
- Risk Assessment
- Findings by Severity
- Remediation Plan (AI-prioritized)
- Pattern Analysis
- Compliance References

---

### mcp
Gestionar servidor MCP.

```bash
# Listar herramientas disponibles
auditoria mcp tools

# Ver estado de MCP server
auditoria mcp status

# Iniciar servidor MCP
auditoria mcp start --port 9000
```

---

## 5. 🔗 Integración End-to-End

### Flujo: Auditoría → IA → Webhook → Reporte

```bash
# 1. Ejecutar auditoría con IA
auditoria audit --target prod.example.com --enable-ai

# 2. Ver resultados en dashboard
auditoria dashboard --target prod.example.com

# 3. Registrar webhook para notificaciones
curl -X POST http://localhost:5000/api/v1/webhooks \
  -d '{
    "id": "slack-critical",
    "url": "https://hooks.slack.com/...",
    "events": ["audit.completed"]
  }'

# 4. Generar reporte ejecutivo
auditoria report 1 --ai-insights --format html --output report.html

# 5. Programar auditorías recurrentes
auditoria schedule add \
  --name daily-prod \
  --target prod.example.com \
  --cron "0 2 * * *" \
  --enable-ai
```

---

## 6. 📊 Casos de Uso Avanzados

### Use Case 1: Auditoría Automática Diaria
```bash
# Programar
auditoria schedule add \
  --name daily-audit \
  --target prod.example.com \
  --cron "0 2 * * *" \
  --enable-ai

# Monitorear con webhooks
curl -X POST http://localhost:5000/api/v1/webhooks \
  -d '{
    "id": "daily-notifier",
    "url": "https://example.com/audit-webhook",
    "events": ["audit.completed"],
    "secret": "verify-signature"
  }'

# Ver historial
auditoria schedule history --name daily-audit --limit 30
```

### Use Case 2: Integración con DevOps
```bash
# Iniciar API en background
nohup python run_api.py --port 5000 &

# Integración con CI/CD via REST
curl -X POST http://localhost:5000/api/v1/audits \
  -H "Content-Type: application/json" \
  -d '{
    "target": "staging.example.com",
    "modules": ["secrets", "filesystem"],
    "enable_ai": true
  }'

# Fallar CI si hay hallazgos críticos
if [ "$(curl -s http://localhost:5000/api/v1/audits/1 | jq .summary.critical)" -gt 0 ]; then
  exit 1
fi
```

### Use Case 3: Reportes para Junta Directiva
```bash
# Ejecutar auditoría con IA
auditoria audit --target prod.example.com --enable-ai

# Generar reporte ejecutivo
auditoria report 1 \
  --format html \
  --ai-insights \
  --output /tmp/exec-summary.html

# Compartir resumen
cat /tmp/exec-summary.html | mail -s "Security Audit Summary" cto@example.com
```

### Use Case 4: Análisis de Patrones
```bash
# Obtener análisis de patrones via MCP
python examples/mcp_integration.py

# Ver trends en dashboard
auditoria dashboard --target example.com --days 90

# Generar reporte con análisis
auditoria report 5 --ai-insights --format json > trends.json
```

---

## 7. 🛠️ Configuración Personalizada

### Variables de Entorno
```bash
# Clave de API para análisis de IA
export ANTHROPIC_API_KEY="sk-ant-..."

# Ruta de base de datos
export AUDITORIA_DB_PATH="/var/lib/auditoria/auditoria.db"

# Puerto de API
export AUDITORIA_API_PORT=5000
```

### Configuración en settings.json
```json
{
  "cli": {
    "aliases": {
      "qa": "auditoria audit --enable-ai",
      "status": "auditoria schedule list",
      "api": "python run_api.py"
    }
  }
}
```

### Agregar Hooks Personalizados
```json
{
  "hooks": {
    "after_edit_file": [
      {
        "pattern": "auditoria/checks/**/*.py",
        "command": "python -m pytest tests/test_checks.py -v",
        "description": "Test checks on change"
      }
    ]
  }
}
```

---

## 8. 📡 Arquitectura de Integración

```
┌─────────────────────────────────────────────────┐
│      Claude Code Harness                        │
│  (.claude/settings.json)                        │
├─────────────────────────────────────────────────┤
│ ┌────────────────┬────────────────┬────────────┐
│ │ Skills         │ MCP Server     │ Hooks      │
│ │ (/quick-audit) │ (registered)   │ (auto-test)
│ └────────────────┴────────────────┴────────────┘
├─────────────────────────────────────────────────┤
│      Auditoria Framework                        │
│  ├── CLI: audit, schedule, dashboard, report   │
│  ├── API: REST endpoints                        │
│  ├── Core: Engine, Scheduler, Analyzer          │
│  └── Storage: Database, Webhooks                │
├─────────────────────────────────────────────────┤
│      Integrations                               │
│  ├── Claude API (IA Analysis)                   │
│  ├── Slack/Email (Webhooks)                     │
│  ├── CI/CD (REST API)                           │
│  └── External Systems (MCP)                     │
└─────────────────────────────────────────────────┘
```

---

## 9. ✅ Checklist de Configuración

- [ ] Instalar: `pip install -e ".[api]"`
- [ ] API Key: `export ANTHROPIC_API_KEY="..."`
- [ ] Recargar harness: Cerrar y abrir Claude Code
- [ ] Verificar skills: `/quick-audit --help`
- [ ] Iniciar API: `python run_api.py`
- [ ] Probar MCP: `auditoria mcp tools`
- [ ] Ver dashboard: `auditoria dashboard`

---

## 10. 📖 Documentación Relacionada

- **CLAUDE.md** — Guía completa de integración
- **API.md** — Documentación de REST API
- **README.md** — Guía de inicio
- **examples/** — Scripts de ejemplo

---

**Versión**: 1.0.0  
**Última actualización**: 2026-07-27  
**Estado**: ✅ Producción-listo
