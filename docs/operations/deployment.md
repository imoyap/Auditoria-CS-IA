# 🚀 Deployment & Quick Start

Framework de auditoría autónoma asistida por IA — **PRODUCCIÓN-LISTO**

---

## ⚡ Inicio Rápido

### 1. Instalación
```bash
cd C:\Users\c4all\Documents\Auditoria-CS-IA
pip install -e ".[api]"
```

### 2. Configurar API Key
```bash
# Windows
set ANTHROPIC_API_KEY=sk-ant-xxxxx

# Linux/macOS
export ANTHROPIC_API_KEY=sk-ant-xxxxx
```

### 3. Auditoría Inmediata
```bash
# Con análisis de IA
auditoria audit --target localhost --enable-ai

# Ver resultados en dashboard
auditoria dashboard
```

---

## 📡 Iniciar API Server

```bash
# Puerto 5000 (default)
python run_api.py

# Puerto personalizado
python run_api.py --port 8000 --debug

# Servidor en background
nohup python run_api.py > api.log 2>&1 &
```

**URL base**: `http://localhost:5000`  
**Docs**: Leer `API.md`

---

## 📅 Auditorías Programadas

### Crear tarea diaria
```bash
auditoria schedule add \
  --name daily-prod-audit \
  --target prod.example.com \
  --cron "0 2 * * *" \
  --modules network ssl \
  --enable-ai
```

### Ejecutar manualmente
```bash
auditoria schedule run --name daily-prod-audit
```

### Ver historial
```bash
auditoria schedule history --name daily-prod-audit --limit 10
```

---

## 🔗 Webhooks (Notificaciones)

### Registrar webhook Slack
```bash
curl -X POST http://localhost:5000/api/v1/webhooks \
  -H "Content-Type: application/json" \
  -d '{
    "id": "slack-prod-alerts",
    "url": "https://hooks.slack.com/services/YOUR/WEBHOOK/URL",
    "events": ["audit.completed"],
    "secret": "my-webhook-secret"
  }'
```

### Webhook recibirá payloads como:
```json
{
  "event": "audit.completed",
  "timestamp": "2026-07-27T20:00:00",
  "data": {
    "audit_id": 1,
    "target": "prod.example.com"
  },
  "report": {
    "target": "prod.example.com",
    "risk_score": 42.5,
    "total_findings": 5
  }
}
```

---

## 📊 Visualización

### Dashboard real-time
```bash
# Todas las auditorías
auditoria dashboard

# Filtrar por objetivo
auditoria dashboard --target prod.example.com

# Ver 60 días de trends
auditoria dashboard --target prod.example.com --days 60
```

### Generar reporte
```bash
# Ver en consola
auditoria report 1

# Exportar a HTML
auditoria report 1 --format html --ai-insights --output report.html

# Exportar a JSON
auditoria report 1 --format json --ai-insights --output report.json
```

---

## 🔌 MCP Server

### Ver herramientas disponibles
```bash
auditoria mcp tools
```

### Iniciar servidor MCP
```bash
auditoria mcp start --port 9000
```

### Usar desde Python
```python
from auditoria.mcp import create_mcp_server
import json

server = create_mcp_server()

# Ejecutar auditoría
result = server.call_tool(
    "execute_audit",
    {"target": "localhost", "enable_ai": True}
)

audit = json.loads(result)
print(f"Audit ID: {audit['audit_id']}")
print(f"Risk Score: {audit['risk_score']}/100")
```

---

## 💻 Claude Code Integration

### Skills disponibles
```bash
/quick-audit localhost --ai
/audit-status --task daily-audit --history
/audit-api start --port 5000
/audit-report 1 --ai-insights --format html
```

### Harness configurado
- Settings en `.claude/settings.json`
- MCP server registrado automáticamente
- Permisos y hooks configurados
- Aliases de CLI listos

---

## 🔌 Integración REST API

### Cliente Python
```python
from examples.rest_client import AuditorialClient

client = AuditorialClient("http://localhost:5000")

# Ejecutar auditoría
result = client.execute_audit("example.com", enable_ai=True)
print(f"Audit ID: {result['audit_id']}")

# Crear tarea programada
task = client.create_task(
    name="daily",
    target="example.com",
    modules=["network", "ssl"]
)
print(f"Task: {task['name']}")

# Ver tendencias
trends = client.get_trends("example.com", days=30)
print(f"Trend data points: {len(trends['trends'])}")
```

### cURL
```bash
# Ejecutar auditoría
curl -X POST http://localhost:5000/api/v1/audits \
  -H "Content-Type: application/json" \
  -d '{"target": "example.com", "enable_ai": true}'

# Listar auditorías
curl http://localhost:5000/api/v1/audits?limit=10

# Ver detalles
curl http://localhost:5000/api/v1/audits/1

# Obtener tendencias
curl "http://localhost:5000/api/v1/targets/example.com/trends?days=30"
```

---

## 🐳 Docker (Opcional)

### Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install -e ".[api]"

ENV PYTHONUNBUFFERED=1
ENV ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}

EXPOSE 5000
CMD ["python", "run_api.py", "--host", "0.0.0.0"]
```

### Build & Run
```bash
docker build -t auditoria:latest .
docker run -e ANTHROPIC_API_KEY=sk-ant-xxx -p 5000:5000 auditoria:latest
```

---

## 🔐 Seguridad en Producción

### Variables de entorno críticas
```bash
export ANTHROPIC_API_KEY="sk-ant-..."           # API key
export AUDITORIA_DB_PATH="/var/lib/auditoria.db" # DB path
export AUDITORIA_API_PORT=5000                  # API port
```

### Webhook secrets
```bash
# Siempre usar secret en webhooks
{
  "id": "slack-prod",
  "url": "https://hooks.slack.com/...",
  "events": ["audit.completed"],
  "secret": "use-strong-secret-here"  # ← IMPORTANTE
}
```

### Verificar firma webhook (servidor receptor)
```python
import hmac
import hashlib

def verify_webhook(request_body, signature, secret):
    computed = "sha256=" + hmac.new(
        secret.encode(),
        request_body,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(computed, signature)
```

### Permisos de archivos
```bash
chmod 600 auditoria.db           # Solo propietario
chmod 600 webhooks.json          # Solo propietario
chmod 600 audit_tasks.json       # Solo propietario
```

### Firewall
```bash
# Solo locales pueden acceder a DB
# Only expose API en puerto 5000 si es necesario
# Use reverse proxy (nginx) en producción
```

---

## 📈 Monitoreo

### Logs de API
```bash
# Ver logs en tiempo real
tail -f api.log

# Ver errores
grep ERROR api.log
```

### Base de datos
```bash
# Verificar estado
sqlite3 auditoria.db "SELECT COUNT(*) FROM audits;"

# Ver auditorías recientes
sqlite3 auditoria.db "SELECT * FROM audits ORDER BY created_at DESC LIMIT 5;"

# Análisis de hallazgos
sqlite3 auditoria.db "SELECT severity, COUNT(*) FROM findings GROUP BY severity;"
```

### Health check
```bash
# Via curl
curl http://localhost:5000/health

# Via Python
import requests
resp = requests.get("http://localhost:5000/health")
print(resp.json())
```

---

## 🚨 Troubleshooting

### API no inicia
```bash
# Verificar puerto disponible
netstat -an | grep 5000

# Cambiar puerto
python run_api.py --port 8000

# Ver logs de error
python run_api.py --debug
```

### BD corrupta
```bash
# Respaldar
cp auditoria.db auditoria.db.bak

# Verificar integridad
sqlite3 auditoria.db ".schema"

# Limpiar si es necesario (CUIDADO)
# rm auditoria.db
# Se recrearía vacía
```

### AI análisis falla
```bash
# Verificar API key
echo $ANTHROPIC_API_KEY

# Intentar sin AI
auditoria audit --target localhost

# Verificar conectividad
curl https://api.anthropic.com/health
```

---

## 📚 Documentación Completa

| Documento | Propósito |
|-----------|-----------|
| **README.md** | Inicio rápido |
| **CLAUDE.md** | Integración Claude Code |
| **API.md** | Referencia REST API |
| **ADVANCED_FEATURES.md** | Características avanzadas |
| **PROJECT_SUMMARY.md** | Resumen de proyecto |
| **DEPLOYMENT.md** | Este documento |

---

## ✅ Checklist de Deploymet

- [ ] Instalar: `pip install -e ".[api]"`
- [ ] API Key: `export ANTHROPIC_API_KEY=...`
- [ ] Testear: `auditoria audit --target localhost`
- [ ] API: `python run_api.py`
- [ ] Webhook: Registrar en Slack/Email
- [ ] Scheduler: Crear tarea programada
- [ ] Dashboard: `auditoria dashboard`
- [ ] Reporte: Generar `auditoria report 1`
- [ ] Monitorear: Verificar logs y DB
- [ ] Documentar: Compartir con team

---

## 🎯 Casos de Uso por Rol

### Security Engineer
```bash
# Auditoría completa con análisis profundo
auditoria audit --target prod.example.com --enable-ai

# Ver hallazgos por severidad
auditoria report 1 --ai-insights --format html

# Configurar monitoreo contínuo
auditoria schedule add --name daily-prod --target prod.example.com --cron "0 2 * * *" --enable-ai
```

### DevOps/SRE
```bash
# Integración en CI/CD
curl -X POST http://localhost:5000/api/v1/audits \
  -d '{"target": "staging.example.com", "enable_ai": true}'

# Alertas en Slack
# (webhook configurado previamente)

# Dashboard para oncall
auditoria dashboard --target prod.example.com
```

### CTO/Director
```bash
# Reporte ejecutivo
auditoria report 1 --ai-insights --format html

# Tendencias de riesgo
auditoria dashboard --days 90

# Exportar para junta
auditoria report 1 --format json | mail -s "Security Summary" board@company.com
```

### Security Analyst
```bash
# Investigar hallazgos específicos
auditoria report 1 --ai-insights

# Análisis de patrones
curl http://localhost:5000/api/v1/targets/example.com/trends?days=30

# Comparar auditorías
curl http://localhost:5000/api/v1/audits?target=example.com&limit=20
```

---

## 🎓 Próximos Pasos

1. **Dashboard Web** — Interfaz visual completa
2. **PostgreSQL Support** — Escalabilidad
3. **SIEM Integration** — Splunk/ELK
4. **PDF Reports** — Documentos profesionales
5. **ML Predictions** — Predicción de vulnerabilidades
6. **Auto-Remediation** — Fixes automáticos
7. **Compliance Reports** — PCI-DSS, HIPAA, ISO 27001

---

## 📞 Soporte

**Documentación**: Leer archivos .md en repo  
**Ejemplos**: Ver `examples/` directory  
**Código**: Revisar `auditoria/` modules  
**Issues**: Reportar bugs con contexto

---

## 📄 Licencia

MIT — Free and open source

---

**Versión**: 1.0.0  
**Estado**: ✅ Production Ready  
**Última actualización**: 2026-07-27  
**Contacto**: herrera.jara.cristobal@gmail.com
