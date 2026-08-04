# SPEC 3: MCP Server — webhook-audit-trail

**Auditoría completa de registro, delivery y eventos de webhooks**

---

## 📋 VISIÓN GENERAL

### Problema
Actualmente, webhooks se registran pero sin audit trail:
- No se graba quién/cuándo registró webhook
- Sin log de intentos de delivery (éxito, fallos, retries)
- Sin rastreabilidad de cambios (quién modificó URL, eventos)
- Potencial compliance risk: webhook malicioso sin audit trail

**Bloquea:** Compliance accountability y forensics (brecha #4).

### Solución
MCP server que:
- Log completo de webhook registration (quién, cuándo, por qué)
- Delivery event tracking (attempt, result, retry)
- Change log (si alguien modifica webhook config)
- Status dashboard (health de webhooks)

### Scope
- ✅ Register webhook con audit
- ✅ Log delivery attempts (HTTP status, response time)
- ✅ Retry tracking
- ✅ Update/delete con change log
- ✅ Query audit history
- ❌ Webhook payload inspection (PII risk)
- ❌ Real-time delivery monitoring (dashboard separado)

---

## 🎯 INTERFAZ MCP

### Tool: `register_webhook_audited`

**Descripción:** Registra webhook con audit trail completo.

**Parámetros:**

```json
{
  "name": "register_webhook_audited",
  "inputSchema": {
    "type": "object",
    "properties": {
      "webhook_id": {
        "type": "string",
        "description": "Unique ID (ej: 'siem-alerts-prod', 'slack-notifications')"
      },
      "url": {
        "type": "string",
        "format": "uri",
        "description": "URL de destino"
      },
      "events": {
        "type": "array",
        "items": {"type": "string", "enum": ["audit.completed", "audit.failed", "finding.critical", "command_executed", "task.scheduled"]},
        "description": "Eventos a suscribirse"
      },
      "secret": {
        "type": "string",
        "description": "Secret para HMAC-SHA256 verification (opcional, recomendado)",
        "minLength": 16
      },
      "active": {
        "type": "boolean",
        "default": true
      },
      "max_retries": {
        "type": "integer",
        "minimum": 0,
        "maximum": 5,
        "default": 3
      },
      "timeout_seconds": {
        "type": "integer",
        "minimum": 1,
        "maximum": 60,
        "default": 10
      },
      "audit_context": {
        "type": "object",
        "properties": {
          "registered_by": {"type": "string", "description": "Usuario/principal que registra"},
          "reason": {"type": "string", "description": "Por qué se registra este webhook"},
          "approval_ticket": {"type": "string", "description": "Ej: 'JIRA-1234' (opcional)"}
        },
        "required": ["registered_by", "reason"]
      }
    },
    "required": ["webhook_id", "url", "events", "audit_context"]
  }
}
```

**Output:**

```json
{
  "webhook_id": "string",
  "registered_at": "2026-07-29T14:30:00Z",
  "audit_record_id": "integer",
  "status": "registered",
  "events": ["array"],
  "registered_by": "string"
}
```

### Tool: `log_webhook_delivery`

**Descripción:** Registra intento de delivery de evento.

**Parámetros:**

```json
{
  "name": "log_webhook_delivery",
  "inputSchema": {
    "type": "object",
    "properties": {
      "webhook_id": {"type": "string"},
      "event_type": {"type": "string"},
      "http_status": {"type": "integer", "minimum": 100, "maximum": 599},
      "response_time_ms": {"type": "number"},
      "attempt": {"type": "integer", "minimum": 1, "maximum": 5},
      "success": {"type": "boolean"},
      "error_message": {"type": "string"}
    },
    "required": ["webhook_id", "event_type", "http_status", "attempt", "success"]
  }
}
```

### Tool: `get_webhook_audit_history`

**Descripción:** Consulta audit trail completo de webhook.

**Parámetros:**

```json
{
  "name": "get_webhook_audit_history",
  "inputSchema": {
    "type": "object",
    "properties": {
      "webhook_id": {"type": "string"},
      "limit": {"type": "integer", "default": 100},
      "include_deliveries": {"type": "boolean", "default": false}
    },
    "required": ["webhook_id"]
  }
}
```

---

## 💾 SCHEMA BASE DE DATOS

**Nueva tabla:** `webhooks_audit`

```sql
CREATE TABLE IF NOT EXISTS webhooks_audit (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    webhook_id TEXT NOT NULL UNIQUE,
    url TEXT NOT NULL,
    events TEXT NOT NULL,  -- JSON array
    secret_hash TEXT,  -- SHA256(secret) — no almacenar secret en claro
    active BOOLEAN DEFAULT TRUE,
    max_retries INTEGER DEFAULT 3,
    timeout_seconds INTEGER DEFAULT 10,
    
    -- Audit trail de registro
    registered_by TEXT NOT NULL,
    registered_at TIMESTAMP NOT NULL,
    registration_reason TEXT,
    approval_ticket TEXT,
    
    -- Cambios
    updated_by TEXT,
    updated_at TIMESTAMP,
    update_reason TEXT,
    
    -- Status
    last_delivery_at TIMESTAMP,
    last_delivery_status INTEGER,  -- HTTP status
    delivery_failure_count INTEGER DEFAULT 0,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT active_bool CHECK (active IN (0, 1))
);

CREATE INDEX IF NOT EXISTS idx_webhooks_audit_webhook_id ON webhooks_audit(webhook_id);
```

**Nueva tabla:** `webhook_delivery_events`

```sql
CREATE TABLE IF NOT EXISTS webhook_delivery_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    webhook_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    attempt INTEGER NOT NULL,
    http_status INTEGER,
    response_time_ms REAL,
    success BOOLEAN NOT NULL,
    error_message TEXT,
    retry_scheduled BOOLEAN DEFAULT FALSE,
    retry_at TIMESTAMP,
    
    delivered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (webhook_id) REFERENCES webhooks_audit(webhook_id)
);

CREATE INDEX IF NOT EXISTS idx_webhook_delivery_events_webhook_id ON webhook_delivery_events(webhook_id);
CREATE INDEX IF NOT EXISTS idx_webhook_delivery_events_event_type ON webhook_delivery_events(event_type);
```

**Nueva tabla:** `webhook_changes`

```sql
CREATE TABLE IF NOT EXISTS webhook_changes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    webhook_id TEXT NOT NULL,
    change_type TEXT NOT NULL,  -- register, update, delete, enable, disable
    changed_by TEXT NOT NULL,
    change_reason TEXT,
    old_value TEXT,  -- JSON: qué cambió
    new_value TEXT,  -- JSON: nuevos valores
    approval_ticket TEXT,
    
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (webhook_id) REFERENCES webhooks_audit(webhook_id)
);

CREATE INDEX IF NOT EXISTS idx_webhook_changes_webhook_id ON webhook_changes(webhook_id);
CREATE INDEX IF NOT EXISTS idx_webhook_changes_changed_by ON webhook_changes(changed_by);
```

---

## 📝 EJEMPLOS

### Ejemplo 1: Registrar webhook con audit

**Request:**
```json
{
  "webhook_id": "siem-splunk-prod",
  "url": "https://splunk.company.com/webhook/auditoria",
  "events": ["audit.completed", "finding.critical"],
  "secret": "your-256-bit-secret-here",
  "max_retries": 3,
  "timeout_seconds": 10,
  "audit_context": {
    "registered_by": "security-admin@company.com",
    "reason": "Integrate Auditoria findings into Splunk SIEM",
    "approval_ticket": "SECURITY-4521"
  }
}
```

**Response:**
```json
{
  "webhook_id": "siem-splunk-prod",
  "registered_at": "2026-07-29T14:30:00Z",
  "audit_record_id": 42,
  "status": "registered",
  "events": ["audit.completed", "finding.critical"],
  "registered_by": "security-admin@company.com"
}
```

### Ejemplo 2: Log delivery event

**Request (Éxito):**
```json
{
  "webhook_id": "siem-splunk-prod",
  "event_type": "audit.completed",
  "http_status": 200,
  "response_time_ms": 245.5,
  "attempt": 1,
  "success": true
}
```

**Response:**
```json
{
  "event_id": 1523,
  "webhook_id": "siem-splunk-prod",
  "recorded_at": "2026-07-29T14:35:12Z",
  "status": "logged"
}
```

**Request (Fallo con retry):**
```json
{
  "webhook_id": "siem-splunk-prod",
  "event_type": "finding.critical",
  "http_status": 503,
  "response_time_ms": 30000,
  "attempt": 1,
  "success": false,
  "error_message": "Service Unavailable - retrying in 60 seconds"
}
```

**Response:**
```json
{
  "event_id": 1524,
  "webhook_id": "siem-splunk-prod",
  "recorded_at": "2026-07-29T14:36:00Z",
  "status": "logged",
  "retry_scheduled": true,
  "retry_at": "2026-07-29T14:37:00Z"
}
```

---

## ✅ ACCEPTANCE CRITERIA

### AC1: Webhook registration con audit completo
**Given** usuario 'security-admin@company.com' registra webhook
**When** registra con MCP tool
**Then**
- ✅ Record creado en webhooks_audit
- ✅ registered_by = 'security-admin@company.com'
- ✅ registered_at = timestamp ISO 8601
- ✅ registration_reason se graba
- ✅ approval_ticket se graba (si aplica)
- ✅ secret se hashed (SHA256) — no almacenado en claro

### AC2: Delivery tracking con estado completo
**Given** webhook 'siem-splunk-prod' dispara evento 'audit.completed'
**When** MCP tool log_webhook_delivery() se ejecuta
**Then**
- ✅ Record en webhook_delivery_events
- ✅ http_status capturado (200, 503, timeout, etc.)
- ✅ response_time_ms grabado
- ✅ success flag refleja resultado verdadero
- ✅ attempt counter incremental
- ✅ error_message si falló

### AC3: Retry automático y tracking
**Given** primer intento falla con 503
**When** Retry policy dispara (max_retries=3)
**Then**
- ✅ Nuevo record con attempt=2 después de delay
- ✅ retry_scheduled = TRUE
- ✅ retry_at muestra cuándo se reintentará
- ✅ Sucesivo intento registrado en BD

### AC4: Change log para modificaciones
**Given** admin cambia webhook URL
**When** Ejecuta update
**Then**
- ✅ Nueva entrada en webhook_changes
- ✅ change_type = 'update'
- ✅ old_value = "{\"url\": \"old-url\"}"
- ✅ new_value = "{\"url\": \"new-url\"}"
- ✅ changed_by y change_reason capturados

### AC5: Query audit history completo
**Given** auditor consulta webhook_id='siem-splunk-prod'
**When** Llama get_webhook_audit_history()
**Then**
- ✅ Retorna todos los cambios (register, update, delete)
- ✅ Retorna delivery history (si include_deliveries=true)
- ✅ Ordered by timestamp DESC
- ✅ Puedo responder: "¿cuándo cambió la URL?" "¿cuántas fallas tuvo?"

### AC6: Forensics: correlación entre eventos
**Given** audit log muestra webhook delivery success
**When** Análisis de security
**Then**
- ✅ Puedo correlacionar: "¿a qué audit.completed event corresponde?"
- ✅ Puedo calcular: "latency entre audit completion y webhook delivery"
- ✅ Puedo detectar: "gap: audit completado pero webhook nunca llegó"

### AC7: Compliance: no-repudiation
**Given** webhook registrado por admin
**When** Meses después, se cuestiona
**Then**
- ✅ registered_by es inmutable
- ✅ registered_at no puede cambiar
- ✅ Firma: admin@company.com registró siem-splunk-prod el 2026-07-29 14:30:00Z

---

## ⚠️ ERROR HANDLING

| Error | HTTP | Descripción |
|-------|------|-------------|
| `webhook_already_registered` | 409 | webhook_id duplicado |
| `invalid_url` | 400 | URL malformada o insegura |
| `invalid_events` | 400 | Event type no soportado |
| `webhook_not_found` | 404 | webhook_id no existe (para update/delete) |
| `unauthorized` | 403 | Usuario no tiene permisos |
| `delivery_failed_all_retries` | 500 | Webhook delivery falló después de max_retries |

---

## 🔒 SEGURIDAD

### Secret handling
- ✅ Almacenar SHA256(secret) — nunca el secret en claro
- ✅ HMAC-SHA256 para verificación de payload
- ✅ Considerar: rotation de secrets

### URL validation
- ❌ No permitir localhost, 127.0.0.1, private IPs
- ✅ Permitir solo HTTPS en producción
- ✅ DNS validation antes de registro

### Delivery security
- ✅ Incluir X-Signature header (HMAC)
- ✅ Timeout robusto (default 10s)
- ✅ No incluir sensitive data en payload (PII masking)

---

## 📦 DEPENDENCIAS

### Internas
- `auditoria.storage.database.DatabaseManager`
- `auditoria.api.webhooks.WebhookManager`

---

## 🔄 INTEGRACIÓN

**Upstream (usa):**
- ← mcp/server.py: dispatch `audit.completed` events

**Downstream (usado por):**
- → 5-skill-evidence-verify: validar integridad de webhook changes

---

## 📋 DEFINITION OF DONE

- [ ] spec.md completo
- [ ] 3 tablas SQL + indexes
- [ ] 2+ ejemplos funcionales
- [ ] 7 AC pasadas
- [ ] Migration: scripts/migrations/20260729_003_webhook_audit.sql
- [ ] tests/spec_3_acceptance.py >= 8 cases

---

**Versión:** 1.0 | **Estado:** Draft — Ready for implementation
