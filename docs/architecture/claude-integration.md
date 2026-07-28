# Auditoria-CS-IA — Documentación para Claude Code

Bienvenido al framework de auditoría autónoma asistida por IA. Este documento describe la arquitectura, herramientas disponibles y cómo integrar Auditoria en tu flujo de trabajo.

## Arquitectura General

```
┌─────────────────────────────────────────────────┐
│  CLI / API / MCP Interfaces                     │
├─────────────────────────────────────────────────┤
│  auditoria/cli.py | auditoria/api/ | auditoria/mcp/
├─────────────────────────────────────────────────┤
│  Core Engine Layer                              │
│  ├── AuditEngine (orquestación)                 │
│  ├── AuditScheduler (tareas programadas)        │
│  └── AuditAnalyzer (análisis con IA)            │
├─────────────────────────────────────────────────┤
│  Storage Layer                                  │
│  ├── DatabaseManager (SQLite)                   │
│  └── WebhookManager (notificaciones)            │
├─────────────────────────────────────────────────┤
│  Security Checks                                │
│  ├── SystemCheck, NetworkCheck, SSLCheck        │
│  ├── FilesystemCheck, SecretsCheck              │
│  └── BaseCheck (extensible)                     │
└─────────────────────────────────────────────────┘
```

## Directorios Clave

```
Auditoria-CS-IA/
├── auditoria/
│   ├── ai/                    # Módulo de análisis con Claude API
│   │   ├── analyzer.py        # AuditAnalyzer
│   │   └── prompts.py         # Templates de prompts
│   ├── api/                   # API REST con Flask
│   │   ├── server.py          # Routes y endpoints
│   │   └── webhooks.py        # WebhookManager
│   ├── checks/                # Módulos de auditoría
│   │   ├── base.py            # BaseCheck
│   │   ├── system.py, network.py, ssl_tls.py, etc.
│   │   └── registry.py        # Registro de checks
│   ├── core/
│   │   ├── engine.py          # AuditEngine
│   │   ├── models.py          # Modelos de datos
│   │   └── reporter.py        # Generadores de reportes
│   ├── mcp/                   # Servidor MCP
│   │   ├── server.py          # MCP Server
│   │   └── tools.py           # Definiciones de herramientas
│   ├── scheduler/             # Ejecución programada
│   │   └── executor.py        # AuditScheduler
│   ├── storage/               # Persistencia
│   │   └── database.py        # DatabaseManager
│   ├── cli.py                 # Interfaz de línea de comandos
│   └── __init__.py
├── .claude/
│   ├── settings.json          # Configuración de harness
│   └── skills/                # Skills personalizadas
│       ├── quick-audit.md
│       ├── audit-status.md
│       ├── audit-api.md
│       └── audit-report.md
├── API.md                     # Documentación de REST API
├── ANALYSIS.md                # Análisis de arquitectura
└── README.md                  # Guía de inicio
```

## Interfaces Disponibles

### 1. CLI (Interfaz de Línea de Comandos)

```bash
# Auditoría rápida
auditoria audit --target localhost --enable-ai

# Gestionar tareas programadas
auditoria schedule add --name daily-audit --target example.com --cron "0 2 * * *" --enable-ai
auditoria schedule run --name daily-audit

# Listar módulos
auditoria list
```

### 2. REST API

```bash
# Iniciar servidor
python run_api.py --port 5000

# Ejecutar auditoría
curl -X POST http://localhost:5000/api/v1/audits \
  -H "Content-Type: application/json" \
  -d '{"target": "example.com", "enable_ai": true}'

# Registrar webhook
curl -X POST http://localhost:5000/api/v1/webhooks \
  -H "Content-Type: application/json" \
  -d '{
    "id": "slack-alerts",
    "url": "https://hooks.slack.com/...",
    "events": ["audit.completed"]
  }'
```

### 3. Skills de Claude Code

```
/quick-audit localhost --ai
/audit-status --task daily-audit --history
/audit-api start --port 5000
/audit-report 1 --ai-insights --format html
```

### 4. MCP Server

Auditoria expone un servidor MCP con herramientas para integración con Claude:

```python
from auditoria.mcp import create_mcp_server

server = create_mcp_server()
tools = server.get_tools()  # Obtener definiciones de herramientas

# Llamar herramienta
result = server.call_tool(
    "execute_audit",
    {"target": "example.com", "enable_ai": True}
)
```

**Herramientas disponibles:**
- `execute_audit` — Ejecutar auditoría inmediata
- `get_audit_history` — Obtener historial
- `get_audit_details` — Detalles de auditoría
- `analyze_findings` — Análisis de IA
- `create_scheduled_task` — Crear tarea programada
- `list_scheduled_tasks` — Listar tareas
- `execute_scheduled_task` — Ejecutar tarea
- `get_trends` — Análisis de tendencias
- `register_webhook` — Registrar webhook

## Flujos de Trabajo Comunes

### Flujo 1: Auditoría Manual Rápida

```bash
# Con CLI
auditoria audit --target localhost --modules system network --enable-ai

# O con skill
/quick-audit localhost --modules system network --ai
```

### Flujo 2: Auditorías Programadas

```bash
# Crear tarea
auditoria schedule add \
  --name "daily-prod" \
  --target prod.example.com \
  --cron "0 2 * * *" \
  --modules network ssl \
  --enable-ai

# Ver status
auditoria schedule list

# Ejecutar manualmente
auditoria schedule run --name daily-prod
```

### Flujo 3: Notificaciones en Tiempo Real

```bash
# Registrar webhook Slack
curl -X POST http://localhost:5000/api/v1/webhooks \
  -d '{
    "id": "slack",
    "url": "https://hooks.slack.com/services/...",
    "events": ["audit.completed", "finding.critical"],
    "secret": "my-secret"
  }'

# Las auditorías ahora notificarán automáticamente
```

### Flujo 4: Análisis Histórico

```bash
# Obtener tendencias
curl http://localhost:5000/api/v1/targets/example.com/trends?days=30

# Generar reporte
/audit-report 1 --ai-insights --export report.html
```

## Extensibilidad

### Crear Nuevo Check de Auditoría

```python
from auditoria.checks.base import BaseCheck
from auditoria.checks.registry import register_check
from auditoria.core.models import Finding, Severity, Status

@register_check
class MyCustomCheck(BaseCheck):
    name = "my-check"
    category = "custom"
    description = "Mi verificación personalizada"

    def run(self) -> list[Finding]:
        findings = []
        # Lógica de auditoría aquí
        if something_bad:
            findings.append(Finding(
                check_id="CUSTOM-001",
                title="Problema detectado",
                description="Descripción detallada",
                severity=Severity.HIGH,
                status=Status.FAIL,
                recommendation="Acción recomendada"
            ))
        return findings
```

Importar en `auditoria/checks/__init__.py`:
```python
from auditoria.checks.my_module import MyCustomCheck  # noqa: F401
```

### Crear Nueva Skill

Crear archivo `.claude/skills/mi-skill.md`:

```markdown
# Skill: mi-skill

Descripción de lo que hace la skill.

## Usage
/mi-skill [argumentos]

## Examples
/mi-skill example

## What it does
- Paso 1
- Paso 2
- Paso 3
```

## Configuración

### Variables de Entorno

```bash
# API key para análisis de IA
export ANTHROPIC_API_KEY="sk-ant-..."

# Ruta de base de datos
export AUDITORIA_DB_PATH="/path/to/auditoria.db"

# Puerto de API
export AUDITORIA_API_PORT=5000
```

### Configuración en .claude/settings.json

- `permissions`: Permisos para Bash, Read, Edit, etc.
- `hooks`: Comandos para ejecutar en eventos (after edit, before commit)
- `environment`: Variables de entorno
- `integrations.mcp_servers`: Servidores MCP a cargar
- `cli.aliases`: Alias personalizados de comandos

## Desarrollo y Testing

```bash
# Instalar en modo desarrollo
pip install -e ".[dev,api]"

# Ejecutar tests
pytest tests/

# Ejecutar con cobertura
pytest --cov=auditoria tests/

# Linter
flake8 auditoria/

# Type checking
mypy auditoria/
```

## Performance y Optimizaciones

- **Caché de resultados**: Los análisis de IA se cachean en SQLite
- **Paralelización**: Los checks se pueden ejecutar en paralelo (futuro)
- **Lazy loading**: Los módulos se importan bajo demanda
- **Connection pooling**: SQLite maneja pools de conexión

## Seguridad

- ✅ Webhook signatures (HMAC-SHA256)
- ✅ Secrets detection en código
- ✅ Permisos de archivo validados
- 🔄 TODO: JWT para API
- 🔄 TODO: Rate limiting
- 🔄 TODO: Encrypted config

## Troubleshooting

### API no inicia

```bash
# Verificar puerto disponible
netstat -an | grep 5000

# Cambiar puerto
python run_api.py --port 8000
```

### Auditoría no detecta secretos

```bash
# Verificar ruta de escaneo
auditoria audit --target localhost --scan-path /path/to/code

# Ver archivos escaneados
auditoria audit --target localhost --scan-path /path/to/code --modules secrets
```

### AI análisis falla

```bash
# Verificar API key
echo $ANTHROPIC_API_KEY

# Reintentar sin AI
auditoria audit --target localhost  # sin --enable-ai
```

## Roadmap Futuro

- [ ] Dashboard web integrado
- [ ] Soporte para múltiples bases de datos (PostgreSQL, MongoDB)
- [ ] Reportes en PDF
- [ ] Integración con SIEM (Splunk, ELK)
- [ ] Compliance reporting (PCI-DSS, HIPAA, ISO 27001)
- [ ] Machine learning para predicción de riesgos
- [ ] Remediación automática de hallazgos
- [ ] Integración con DevOps (GitLab CI, GitHub Actions)

## Contribuciones y Feedback

Para reportar bugs, sugerir features, o contribuir:
1. Crear issue descriptivo
2. Fork la rama
3. Implementar cambios con tests
4. Push a rama feature
5. Crear Pull Request

---

**Última actualización**: 2026-07-27  
**Versión**: 1.0.0  
**Contacto**: herrera.jara.cristobal@gmail.com
