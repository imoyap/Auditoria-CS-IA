# SPEC 1: MCP Server — filesystem-operations

**Audit trail completo para ejecución de comandos del SO (Windows/Linux/macOS)**

---

## 📋 VISIÓN GENERAL

### Problema
Actualmente, system.py ejecuta comandos como `netsh advfirewall show allprofiles state` pero:
- No graba comando ejecutado (solo output recortado)
- No captura stderr, exit_code, timestamp de ejecución
- No registra quién/desde dónde ejecutó
- No hay contexto para reproducir exactamente

**Bloquea:** Cadena de custodia para auditoría forense y compliance (brecha #1).

### Solución
MCP server que expone herramienta `run_command` con:
- Ejecución controlada (timeout, whitelist de comandos)
- Capture completo: stdout, stderr, exit_code, cwd, executor, timestamp
- Logging automático en tabla `command_executions` (auditoria BD)
- Generación de evidence_hash (checksum de output)
- Integración con webhook (dispatch event `command_executed`)

### Scope
- ✅ Windows: netsh, powershell, tasklist, wmic
- ✅ Linux: ip, ss, systemctl, journalctl, lsof
- ✅ macOS: networksetup, launchctl, softwareupdate
- ✅ Cross-platform: python -m, curl, git
- ❌ Interactive commands (ssh, telnet, vim)
- ❌ Interactive stdin/stdout (read-only execution)

---

## 🎯 INTERFAZ MCP

### Tool: `run_command`

**Descripción:** Ejecuta comando del SO con capture completo de output y audit trail.

**Parámetros:**

```json
{
  "name": "run_command",
  "description": "Execute system command with full audit trail (stdout, stderr, exit_code, timestamp, executor)",
  "inputSchema": {
    "type": "object",
    "properties": {
      "command": {
        "type": "string",
        "description": "Comando a ejecutar (ej: 'netsh', 'powershell', 'ip')",
        "enum": ["netsh", "powershell", "systemctl", "journalctl", "ip", "ss", "lsof", "taskset", "curl", "python", "git", "windowsupdate", "launchctl", "softwareupdate"]
      },
      "args": {
        "type": "array",
        "items": {"type": "string"},
        "description": "Argumentos del comando (ej: ['advfirewall', 'show', 'allprofiles', 'state'])"
      },
      "cwd": {
        "type": "string",
        "description": "Working directory (default: current)",
        "default": "."
      },
      "timeout_seconds": {
        "type": "integer",
        "minimum": 1,
        "maximum": 300,
        "default": 30,
        "description": "Timeout en segundos (máx 300s)"
      },
      "audit_context": {
        "type": "object",
        "description": "Contexto para audit trail",
        "properties": {
          "check_id": {"type": "string", "description": "Ej: 'SYS-003' (firewall check)"},
          "reason": {"type": "string", "description": "Por qué se ejecuta este comando"},
          "related_finding_id": {"type": "integer", "description": "ID del finding que disparó esto"}
        }
      }
    },
    "required": ["command", "args"]
  }
}
```

**Output:**

```json
{
  "type": "object",
  "properties": {
    "command_execution_id": {
      "type": "integer",
      "description": "ID único para este comando en BD"
    },
    "command": {
      "type": "string",
      "description": "Comando ejecutado"
    },
    "args": {
      "type": "array",
      "description": "Argumentos exactos"
    },
    "exit_code": {
      "type": "integer",
      "description": "Exit code (0 = éxito)"
    },
    "stdout": {
      "type": "string",
      "description": "Standard output (UTF-8, max 64KB)"
    },
    "stderr": {
      "type": "string",
      "description": "Standard error (UTF-8, max 64KB)"
    },
    "cwd": {
      "type": "string",
      "description": "Working directory usado"
    },
    "duration_ms": {
      "type": "number",
      "description": "Duración ejecución en ms"
    },
    "executor": {
      "type": "string",
      "description": "Usuario/proceso que ejecutó (ej: 'DOMAIN\\username' o 'root')"
    },
    "executed_at": {
      "type": "string",
      "format": "date-time",
      "description": "ISO 8601 timestamp de ejecución"
    },
    "evidence_hash": {
      "type": "string",
      "description": "SHA256(stdout + stderr) para verificación de integridad"
    }
  }
}
```

---

## 💾 SCHEMA BASE DE DATOS

**Nueva tabla:** `command_executions`

```sql
CREATE TABLE IF NOT EXISTS command_executions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    command TEXT NOT NULL,
    args TEXT NOT NULL,  -- JSON array
    cwd TEXT,
    exit_code INTEGER,
    stdout TEXT,  -- máx 65536 chars
    stderr TEXT,  -- máx 65536 chars
    stdout_truncated BOOLEAN DEFAULT FALSE,
    stderr_truncated BOOLEAN DEFAULT FALSE,
    duration_ms REAL,
    executor TEXT,  -- usuario/proceso que ejecutó
    executed_at TIMESTAMP NOT NULL,
    evidence_hash TEXT,  -- SHA256 de output
    
    -- Audit trail
    audit_check_id TEXT,  -- ej: 'SYS-003'
    audit_reason TEXT,
    audit_finding_id INTEGER,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (audit_finding_id) REFERENCES findings(id)
);

CREATE INDEX IF NOT EXISTS idx_command_executions_executor ON command_executions(executor);
CREATE INDEX IF NOT EXISTS idx_command_executions_executed_at ON command_executions(executed_at);
CREATE INDEX IF NOT EXISTS idx_command_executions_audit_check ON command_executions(audit_check_id);
```

---

## 📝 EJEMPLOS

### Ejemplo 1: Firewall Check (Windows)

**Request:**
```json
{
  "command": "netsh",
  "args": ["advfirewall", "show", "allprofiles", "state"],
  "timeout_seconds": 30,
  "audit_context": {
    "check_id": "SYS-003",
    "reason": "Windows Firewall status verification",
    "related_finding_id": null
  }
}
```

**Response (éxito):**
```json
{
  "command_execution_id": 42,
  "command": "netsh",
  "args": ["advfirewall", "show", "allprofiles", "state"],
  "exit_code": 0,
  "stdout": "Domain Profile Settings:\nState                                 ON\nDomain Profile Settings:\nState                                 ON",
  "stderr": "",
  "cwd": "C:\\Windows\\System32",
  "duration_ms": 234.5,
  "executor": "DOMAIN\\admin-user",
  "executed_at": "2026-07-29T14:23:45Z",
  "evidence_hash": "a3f7c8d9e2b1f4c6a8d0e1f3a5b7c9d1e3f5a7b9c1d3e5f7a9b1c3d5e7f9a1"
}
```

**Response (error):**
```json
{
  "error": "command_timeout",
  "message": "Command 'netsh...' exceeded 30 seconds",
  "command_execution_id": null,
  "partial_stdout": "<output capturado antes de timeout>",
  "executed_at": "2026-07-29T14:23:45Z"
}
```

### Ejemplo 2: DNS Resolution (Linux)

**Request:**
```json
{
  "command": "systemctl",
  "args": ["status", "systemd-resolved.service"],
  "cwd": "/tmp",
  "timeout_seconds": 10,
  "audit_context": {
    "check_id": "NET-001",
    "reason": "DNS resolver status check"
  }
}
```

**Response:**
```json
{
  "command_execution_id": 43,
  "command": "systemctl",
  "args": ["status", "systemd-resolved.service"],
  "exit_code": 0,
  "stdout": "● systemd-resolved.service - systemd DNS resolver\n     Loaded: loaded (/usr/lib/systemd/system/systemd-resolved.service; enabled; ...)\n     Active: active (running) since Mon 2026-07-29 14:20:31 UTC; 3min ago",
  "stderr": "",
  "cwd": "/tmp",
  "duration_ms": 45.2,
  "executor": "root",
  "executed_at": "2026-07-29T14:23:50Z",
  "evidence_hash": "b4c8d9e1f2a3b5c6d8e0f1a3b5c7d9e1f3a5b7c9d1e3f5a7b9c1d3e5f7a9b1"
}
```

---

## ✅ ACCEPTANCE CRITERIA

### AC1: Ejecución exitosa con captura completa
**Given** comando `netsh advfirewall show allprofiles state`
**When** MCP tool `run_command` se ejecuta
**Then**
- ✅ exit_code == 0
- ✅ stdout contiene "State" (al menos 100 chars)
- ✅ stderr es vacío o no-crítico
- ✅ evidence_hash coincide SHA256(stdout+stderr)
- ✅ record se crea en command_executions table
- ✅ executor field captura usuario (DOMAIN\user o uid)
- ✅ executed_at es timestamp válido ISO 8601

### AC2: Timeout manejo
**Given** comando que tarda > timeout_seconds
**When** MCP tool ejecuta con timeout_seconds=2
**Then**
- ✅ Proceso se termina antes de 3 segundos
- ✅ partial_stdout contiene lo que se capturó
- ✅ Error type: "command_timeout"
- ✅ Record en command_executions con exit_code != 0
- ✅ evidence_hash se calcula sobre partial output

### AC3: Comando no whitelist
**Given** comando "rm -rf /" (no en whitelist)
**When** MCP tool se ejecuta
**Then**
- ✅ Rechazo inmediato (no execution)
- ✅ Error: "command_not_whitelisted"
- ✅ Log de intento fallido en audit trail
- ✅ Mensaje: "Command 'rm' not in whitelist: [netsh, powershell, ...]"

### AC4: Evidence integrity
**Given** command_execution_id=42 se ejecutó hace 1 hora
**When** Usuario/analyst consulta BD
**Then**
- ✅ evidence_hash no cambió
- ✅ stdout no puede modificarse (readonly field en BD)
- ✅ Detecta tampering si hash != SHA256(stdout actual)

### AC5: Audit trail completitud
**Given** comando con audit_context={check_id, reason}
**When** Se ejecuta
**Then**
- ✅ Campos audit_check_id, audit_reason se guardan
- ✅ related_finding_id vincula a findings table
- ✅ Permite query: "¿qué comandos ejecutó finding_id=123?"

### AC6: Cross-platform compatibilidad
**Given** mismo command_execution_id=X
**When** Se ejecuta en Windows vs Linux
**Then**
- ✅ Respuesta consistente (mismo schema)
- ✅ executor refleja contexto OS (DOMAIN\user vs root)
- ✅ cwd usa separadores nativos (\ vs /)

### AC7: Truncation handling
**Given** comando que genera >64KB stdout
**When** MCP tool ejecuta
**Then**
- ✅ stdout se trunca a 65536 chars
- ✅ stdout_truncated flag = TRUE
- ✅ evidence_hash se calcula sobre truncated output
- ✅ Usuario informado: "(output truncated, 1.2MB total)"

---

## ⚠️ ERROR HANDLING

| Error Type | HTTP Status | Descripción | Recuperación |
|-----------|-------------|-------------|--------------|
| `command_not_whitelisted` | 400 | Comando no en lista permitida | Verificar whitelist en settings.json |
| `command_timeout` | 408 | Excedió timeout_seconds | Aumentar timeout, investigar proceso lento |
| `command_not_found` | 404 | Comando no existe en sistema | Verificar disponibilidad en PATH |
| `insufficient_permissions` | 403 | Usuario no tiene permisos para ejecutar | Ejecutar con elevados permisos si es legítimo |
| `malformed_args` | 400 | args contiene caracteres sospechosos | Usar array sanitizado |
| `cwd_not_found` | 404 | Working directory no existe | Usar cwd válido |
| `execution_error` | 500 | Error interno (permission denied, etc.) | Revisar logs, puede indicar tampering |

---

## 🔒 SEGURIDAD & COMPLIANCE

### Whitelist de comandos

**Windows:**
```
netsh, powershell, wmic, tasklist, ipconfig, getmac, systeminfo, 
sc (services), regedit, dir, attrib, icacls, cipher, certutil
```

**Linux:**
```
ip, ss, netstat, systemctl, journalctl, lsof, ps, ls, stat, 
getfacl, chattr, openssl, curl, dig, nslookup
```

**macOS:**
```
networksetup, launchctl, softwareupdate, system_profiler, 
dscl, chmod, stat, openssl, curl
```

**Cross-platform:**
```
python, git, curl, wget (read-only)
```

### Restricciones de argumentos
- ❌ Redirección a archivos (>, >>)
- ❌ Pipe operators (|, ||)
- ❌ Subshells (``, $())
- ❌ Múltiples comandos (;, &&)
- ✅ Array args: ["advfirewall", "show", "allprofiles", "state"]

### Logging & Auditing
- Toda ejecución se graba en command_executions
- Non-repudiation: executor, timestamp, evidence_hash inmutables
- SOAR/SIEM: webhook event `command_executed` permite alertas

---

## 📦 DEPENDENCIAS

### Externas
- **subprocess** (Python stdlib) — ejecución comando
- **hashlib.sha256** (Python stdlib) — evidence hash
- **os.getuser()** o equivalent — capture executor
- **psutil** (ya en requirements.txt para scheduler) — opcional para process monitoring

### Internas
- `auditoria.storage.database.DatabaseManager` — save command_executions
- `auditoria.api.webhooks.WebhookManager` — dispatch `command_executed` event
- `auditoria.mcp.tools.AUDIT_TOOLS` — registry

---

## 🔄 INTEGRACIÓN CON SPECS

**Upstream (usa):**
- ← checks/system.py: reemplaza `self._run_cmd()` por MCP call

**Downstream (usado por):**
- → 3-mcp-webhook-audit: dispatch event
- → 5-skill-evidence-verify: validar evidence_hash

---

## 📋 DEFINITION OF DONE

- [ ] spec.md (este documento) completado
- [ ] schema.sql probado en SQLite (create table, indexes)
- [ ] 3 ejemplos (Windows firewall, Linux systemctl, error case)
- [ ] 7 AC pasadas (unit tests)
- [ ] Error handling definido (7 tipos)
- [ ] Migration: `scripts/migrations/20260729_001_command_executions.sql`
- [ ] settings.json: whitelist de comandos configurable
- [ ] tests/spec_1_acceptance.py: pytest >= 8 cases

---

## 🚀 ROADMAP DE IMPLEMENTACIÓN

**Fase 1: Foundation (1h)**
- [ ] Crear tabla command_executions
- [ ] Implementar run_command() en mcp/tools.py
- [ ] Agregar to AUDIT_TOOLS registry

**Fase 2: Integration (30m)**
- [ ] Integrar con filesystem-operations MCP
- [ ] Webhook event dispatch
- [ ] settings.json whitelist

**Fase 3: Hardening (30m)**
- [ ] Input validation + sanitization
- [ ] Timeout robustness
- [ ] Error handling

**Fase 4: Tests & Acceptance (45m)**
- [ ] Unit tests (7+ AC cases)
- [ ] Integration tests (end-to-end)
- [ ] DB migration rollback test

---

**Versión:** 1.0 | **Autor:** Architecture Review | **Estado:** Draft — Ready for implementation
