# API REST - Auditoría Autónoma Asistida por IA

API REST para ejecutar auditorías, gestionar tareas programadas y recibir notificaciones en tiempo real mediante webhooks.

## Instalación

```bash
pip install -e ".[api]"
```

## Inicio del servidor

```bash
python -m auditoria.api.server
```

El servidor estará disponible en `http://localhost:5000`

## Autenticación

Actualmente sin autenticación (para producción, agregar JWT/API keys).

## Endpoints

### Health Check
```
GET /health
```

Verifica que la API está disponible.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

### Ejecutar Auditoría Inmediata
```
POST /api/v1/audits
```

Ejecuta una auditoría de seguridad sobre un objetivo.

**Request:**
```json
{
  "target": "localhost",
  "modules": ["system", "network", "ssl"],
  "categories": ["sistema"],
  "enable_ai": true,
  "config": {
    "scan_path": "/path/to/scan"
  }
}
```

**Response (201):**
```json
{
  "audit_id": 1,
  "target": "localhost",
  "risk_score": 42.5,
  "total_findings": 5,
  "summary": {
    "critical": 0,
    "high": 2,
    "medium": 3,
    "low": 0,
    "total_findings": 5,
    "passed_checks": 3,
    "failed_modules": 0
  }
}
```

### Obtener Detalles de Auditoría
```
GET /api/v1/audits/{audit_id}
```

**Response:**
```json
{
  "audit": {
    "id": 1,
    "target": "localhost",
    "risk_score": 42.5,
    "total_findings": 5,
    ...
  },
  "findings": [
    {
      "id": 1,
      "check_id": "NET-001",
      "title": "Puerto abierto detectado",
      "severity": "high",
      "description": "..."
    }
  ],
  "ai_analyses": [
    {
      "id": 1,
      "analysis_type": "priority_plan",
      "content": "Plan de remediación..."
    }
  ]
}
```

### Listar Auditorías
```
GET /api/v1/audits?target=localhost&limit=50
```

Query params:
- `target`: Filtrar por objetivo (opcional)
- `limit`: Límite de resultados (default: 50)

### Obtener Hallazgos de Auditoría
```
GET /api/v1/audits/{audit_id}/findings
```

### Obtener Análisis de IA
```
GET /api/v1/audits/{audit_id}/analyses
```

### Obtener Tendencias
```
GET /api/v1/targets/{target}/trends?days=30
```

Análisis de tendencias de riesgo en el tiempo.

**Response:**
```json
{
  "target": "localhost",
  "period_days": 30,
  "trends": [
    {
      "date": "2026-07-27",
      "audits": 2,
      "critical": 0,
      "high": 1,
      "avg_risk": 35.5
    }
  ]
}
```

## Gestión de Tareas Programadas

### Crear Tarea Programada
```
POST /api/v1/tasks
```

**Request:**
```json
{
  "name": "daily-audit",
  "target": "prod.example.com",
  "cron": "0 2 * * *",
  "modules": ["network", "ssl"],
  "description": "Auditoría diaria de producción",
  "enable_ai": true
}
```

**Response (201):**
```json
{
  "name": "daily-audit",
  "target": "prod.example.com",
  "cron": "0 2 * * *"
}
```

### Listar Tareas
```
GET /api/v1/tasks
```

### Ejecutar Tarea Manualmente
```
POST /api/v1/tasks/{task_name}/run
```

**Request (opcional):**
```json
{
  "enable_ai": true
}
```

### Obtener Historial de Tarea
```
GET /api/v1/tasks/{task_name}/history?limit=10
```

### Eliminar Tarea
```
DELETE /api/v1/tasks/{task_name}
```

## Webhooks

### Registrar Webhook
```
POST /api/v1/webhooks
```

**Request:**
```json
{
  "id": "slack-alerts",
  "url": "https://hooks.slack.com/services/YOUR/WEBHOOK/URL",
  "events": ["audit.completed", "finding.critical"],
  "secret": "webhook-secret-key",
  "headers": {
    "Authorization": "Bearer token"
  }
}
```

**Response (201):**
```json
{
  "id": "slack-alerts",
  "url": "https://hooks.slack.com/services/YOUR/WEBHOOK/URL",
  "events": ["audit.completed", "finding.critical"],
  "active": true,
  "created_at": "2026-07-27T19:30:00"
}
```

### Eventos Disponibles
- `audit.completed` — Auditoría finalizada
- `task.executed` — Tarea programada ejecutada
- `finding.critical` — Hallazgo crítico detectado
- `finding.high` — Hallazgo alto detectado

### Payload de Webhook
```json
{
  "event": "audit.completed",
  "timestamp": "2026-07-27T19:30:00",
  "data": {
    "audit_id": 1,
    "target": "localhost"
  },
  "report": {
    "target": "localhost",
    "risk_score": 42.5,
    "total_findings": 5,
    "summary": {...}
  }
}
```

### Verificación de Firma
Los webhooks incluyen un header `X-Webhook-Signature`:

```
X-Webhook-Signature: sha256=abc123...
```

Verificar en el receptor:
```python
import hmac
import hashlib
import json

secret = "webhook-secret-key"
payload = request.get_data()
signature = hmac.new(
    secret.encode(),
    payload,
    hashlib.sha256
).hexdigest()

expected = request.headers.get("X-Webhook-Signature", "").split("=")[1]
assert hmac.compare_digest(signature, expected)
```

### Listar Webhooks
```
GET /api/v1/webhooks
```

### Eliminar Webhook
```
DELETE /api/v1/webhooks/{webhook_id}
```

## Ejemplos de Uso

### Python - Ejecutar auditoría y esperar resultado
```python
import requests

response = requests.post(
    "http://localhost:5000/api/v1/audits",
    json={
        "target": "example.com",
        "modules": ["network", "ssl"],
        "enable_ai": True
    }
)

audit_id = response.json()["audit_id"]
print(f"Auditoría creada: {audit_id}")
```

### Python - Programar auditoría diaria
```python
requests.post(
    "http://localhost:5000/api/v1/tasks",
    json={
        "name": "daily-prod-audit",
        "target": "prod.example.com",
        "cron": "0 2 * * *",  # 2am diariamente
        "modules": ["network", "ssl", "filesystem"],
        "enable_ai": True
    }
)
```

### cURL - Crear webhook para Slack
```bash
curl -X POST http://localhost:5000/api/v1/webhooks \
  -H "Content-Type: application/json" \
  -d '{
    "id": "slack-critical",
    "url": "https://hooks.slack.com/services/YOUR/WEBHOOK",
    "events": ["audit.completed"],
    "secret": "my-secret"
  }'
```

### cURL - Obtener tendencias
```bash
curl "http://localhost:5000/api/v1/targets/prod.example.com/trends?days=30"
```

## Códigos de Respuesta

| Código | Significado |
|--------|-------------|
| 200    | OK |
| 201    | Creado |
| 400    | Solicitud inválida |
| 404    | No encontrado |
| 500    | Error interno del servidor |

## Limites

- Máximo de auditorías simultáneas: 5
- Timeout de webhook: 10 segundos
- Límite por defecto en listados: 50 items

## Seguridad (TODO)

- [ ] Autenticación JWT
- [ ] Rate limiting
- [ ] CORS configuration
- [ ] Encrypted webhook secrets
- [ ] Audit logging
