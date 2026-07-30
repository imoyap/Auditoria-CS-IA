# SPEC 2: MCP Server — audit-log-persistence

**Trazabilidad completa de prompts + responses de análisis IA (Claude API)**

---

## 📋 VISIÓN GENERAL

### Problema
Actualmente, engine.py ejecuta análisis IA (prioritize_findings, detect_patterns, generate_executive_summary) pero:
- No se graba el prompt enviado a Claude
- ai_analyses table solo guarda: analysis_type, content, model_used, tokens_used
- Sin prompt, es imposible reproducir/auditar si el análisis es correcto
- Brecha de custodia: "¿cuál fue la pregunta que hizo generar este resumen?"

**Bloquea:** Verificabilidad de recomendaciones críticas en compliance (brecha #3).

### Solución
MCP server que:
- Intercepta/registra prompts enviados a Claude antes de llamada
- Captura response completo (content, model, usage)
- Graba execution_plan (qué checks generaron este análisis)
- Genera execution_hash (SHA256 de inputs, modelo útil para reproducibilidad)
- Permite replay: ejecutar exacto mismo prompt con mismo reporte

### Scope
- ✅ priority_plan (qué findings son críticos)
- ✅ pattern_analysis (correlaciones encontradas)
- ✅ executive_summary (resumen narrativo)
- ✅ future: remediation_plan, risk_scorecard
- ❌ Almacenar full response de Claude (usa tokens, storage)
- ❌ Análisis en tiempo real (batch, post-audit)

---

## 🎯 INTERFAZ MCP

### Tool: `log_ai_analysis`

**Descripción:** Registra prompt + response de análisis IA con trazabilidad completa.

**Parámetros:**

```json
{
  "name": "log_ai_analysis",
  "description": "Log AI analysis execution: prompt sent, response received, model, tokens, execution context",
  "inputSchema": {
    "type": "object",
    "properties": {
      "audit_id": {
        "type": "integer",
        "description": "ID de la auditoría que dispara este análisis"
      },
      "analysis_type": {
        "type": "string",
        "enum": ["priority_plan", "pattern_analysis", "executive_summary", "remediation_plan"],
        "description": "Tipo de análisis ejecutado"
      },
      "prompt_template_name": {
        "type": "string",
        "description": "Nombre del template usado (ej: 'priority_plan_v1', para reproducibilidad)",
        "examples": ["priority_plan_v1", "pattern_analysis_v2", "executive_summary_v1"]
      },
      "prompt_sent": {
        "type": "string",
        "description": "Prompt exacto enviado a Claude (sin sensitive data)",
        "minLength": 50
      },
      "response_received": {
        "type": "string",
        "description": "Response completa de Claude (máx 32KB, truncar si needed)",
        "minLength": 1
      },
      "model_used": {
        "type": "string",
        "description": "Model ID (ej: 'claude-opus-5')",
        "examples": ["claude-opus-5", "claude-sonnet-5", "claude-haiku-4.5"]
      },
      "tokens_used": {
        "type": "object",
        "description": "Token usage",
        "properties": {
          "input_tokens": {"type": "integer"},
          "output_tokens": {"type": "integer"},
          "cache_creation_input_tokens": {"type": "integer"},
          "cache_read_input_tokens": {"type": "integer"}
        },
        "required": ["input_tokens", "output_tokens"]
      },
      "execution_context": {
        "type": "object",
        "description": "Contexto de ejecución",
        "properties": {
          "check_modules": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Módulos auditados (ej: ['system', 'network', 'ssl'])"
          },
          "findings_count": {"type": "integer", "description": "# hallazgos en auditoría"},
          "risk_score": {"type": "number", "description": "Puntuación de riesgo pre-IA"},
          "target": {"type": "string", "description": "Objetivo auditado"},
          "duration_ms": {"type": "number", "description": "Tiempo total ejecución"}
        }
      },
      "execution_plan": {
        "type": "object",
        "description": "Plan de ejecución que resultó en este análisis",
        "properties": {
          "triggered_by": {"type": "string", "enum": ["engine.run()", "manual_skill", "scheduled_task"]},
          "ai_enabled_from_start": {"type": "boolean"},
          "findings_processed": {"type": "integer"}
        }
      }
    },
    "required": ["audit_id", "analysis_type", "prompt_sent", "response_received", "model_used", "tokens_used"]
  }
}
```

**Output:**

```json
{
  "type": "object",
  "properties": {
    "ai_analysis_log_id": {
      "type": "integer",
      "description": "ID único del registro"
    },
    "audit_id": {
      "type": "integer"
    },
    "analysis_type": {
      "type": "string"
    },
    "prompt_hash": {
      "type": "string",
      "description": "SHA256(prompt_sent) para verificación integridad"
    },
    "response_hash": {
      "type": "string",
      "description": "SHA256(response_received) para verificación"
    },
    "execution_hash": {
      "type": "string",
      "description": "SHA256(audit_id + analysis_type + prompt_hash + model_used) para reproducibilidad",
      "example": "abc123def456..."
    },
    "model_used": {
      "type": "string"
    },
    "tokens_input": {
      "type": "integer"
    },
    "tokens_output": {
      "type": "integer"
    },
    "created_at": {
      "type": "string",
      "format": "date-time"
    },
    "status": {
      "type": "string",
      "enum": ["logged", "verified", "failed"]
    }
  }
}
```

### Tool: `get_ai_analysis_log`

**Descripción:** Recupera análisis IA con auditoría completa (prompt + response).

**Parámetros:**

```json
{
  "name": "get_ai_analysis_log",
  "inputSchema": {
    "type": "object",
    "properties": {
      "audit_id": {"type": "integer"},
      "analysis_type": {"type": "string", "enum": ["priority_plan", "pattern_analysis", "executive_summary"]},
      "include_prompt": {"type": "boolean", "default": true}
    },
    "required": ["audit_id", "analysis_type"]
  }
}
```

**Output:**

```json
{
  "analysis": {
    "ai_analysis_log_id": 123,
    "audit_id": 456,
    "analysis_type": "executive_summary",
    "prompt_sent": "Here are the findings from an audit...",
    "prompt_hash": "abc123...",
    "response_received": "Executive Summary:\n\n1. Critical Issues Found: 2...",
    "response_hash": "def456...",
    "execution_hash": "xyz789...",
    "model_used": "claude-opus-5",
    "tokens_input": 1234,
    "tokens_output": 567,
    "created_at": "2026-07-29T14:23:45Z",
    "status": "verified"
  }
}
```

---

## 💾 SCHEMA BASE DE DATOS

**Nueva tabla:** `ai_analysis_logs`

```sql
CREATE TABLE IF NOT EXISTS ai_analysis_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    audit_id INTEGER NOT NULL,
    analysis_type TEXT NOT NULL,  -- priority_plan, pattern_analysis, executive_summary
    
    -- Prompts & Responses
    prompt_sent TEXT NOT NULL,  -- Prompt exacto (máx 16384 chars)
    response_received TEXT NOT NULL,  -- Response completa (máx 32768 chars)
    
    -- Hashes para verificación de integridad
    prompt_hash TEXT NOT NULL,  -- SHA256(prompt_sent)
    response_hash TEXT NOT NULL,  -- SHA256(response_received)
    execution_hash TEXT NOT NULL,  -- SHA256(audit_id + analysis_type + prompt_hash + model_used) — para reproducibilidad
    
    -- Modelo & Tokens
    model_used TEXT NOT NULL,  -- claude-opus-5, etc.
    prompt_template_version TEXT,  -- v1, v2, etc. para reproducibilidad
    
    -- Token usage
    tokens_input INTEGER NOT NULL,
    tokens_output INTEGER NOT NULL,
    tokens_cache_creation INTEGER DEFAULT 0,
    tokens_cache_read INTEGER DEFAULT 0,
    total_tokens INTEGER GENERATED ALWAYS AS (tokens_input + tokens_output + tokens_cache_creation + tokens_cache_read) STORED,
    
    -- Execution context
    check_modules TEXT,  -- JSON array de módulos auditados
    findings_count INTEGER,
    risk_score_pre_analysis REAL,
    target TEXT,
    execution_duration_ms REAL,
    
    -- Status
    status TEXT DEFAULT 'logged',  -- logged, verified, failed
    verification_timestamp TIMESTAMP,
    verifier_note TEXT,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (audit_id) REFERENCES audits(id),
    CHECK (status IN ('logged', 'verified', 'failed'))
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_ai_analysis_logs_unique 
    ON ai_analysis_logs(audit_id, analysis_type);
CREATE INDEX IF NOT EXISTS idx_ai_analysis_logs_created_at 
    ON ai_analysis_logs(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_ai_analysis_logs_model 
    ON ai_analysis_logs(model_used);
```

**Cambios a tabla existente:** `ai_analyses`

```sql
ALTER TABLE ai_analyses 
ADD COLUMN IF NOT EXISTS prompt_sent TEXT,
ADD COLUMN IF NOT EXISTS execution_hash TEXT,
ADD COLUMN IF NOT EXISTS prompt_hash TEXT,
ADD COLUMN IF NOT EXISTS ai_analysis_log_id INTEGER REFERENCES ai_analysis_logs(id);
```

---

## 📝 EJEMPLOS

### Ejemplo 1: Executive Summary

**Request:**
```json
{
  "audit_id": 456,
  "analysis_type": "executive_summary",
  "prompt_template_name": "executive_summary_v1",
  "prompt_sent": "You are a security auditor. Analyze these findings from a recent security audit and provide an executive summary focusing on critical and high-severity issues. Findings:\n\n1. Finding ID: 1, Severity: CRITICAL, Title: Certificate Expired...",
  "response_received": "EXECUTIVE SUMMARY\n\nCritical Issues (1):\n- SSL Certificate Expired: example.com certificate expired on 2026-01-15. Immediate renewal required...",
  "model_used": "claude-opus-5",
  "tokens_used": {
    "input_tokens": 2145,
    "output_tokens": 823,
    "cache_creation_input_tokens": 0,
    "cache_read_input_tokens": 0
  },
  "execution_context": {
    "check_modules": ["system", "network", "ssl"],
    "findings_count": 12,
    "risk_score": 67.5,
    "target": "example.com",
    "duration_ms": 4234
  },
  "execution_plan": {
    "triggered_by": "engine.run()",
    "ai_enabled_from_start": true,
    "findings_processed": 12
  }
}
```

**Response:**
```json
{
  "ai_analysis_log_id": 789,
  "audit_id": 456,
  "analysis_type": "executive_summary",
  "prompt_hash": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6",
  "response_hash": "z6y5x4w3v2u1t0s9r8q7p6o5n4m3l2k1j0i9h8g7f6e5d4c3b2a1",
  "execution_hash": "exec_hash_12345abcde",
  "model_used": "claude-opus-5",
  "tokens_input": 2145,
  "tokens_output": 823,
  "created_at": "2026-07-29T14:23:45Z",
  "status": "logged"
}
```

### Ejemplo 2: Pattern Analysis

**Request:**
```json
{
  "audit_id": 456,
  "analysis_type": "pattern_analysis",
  "prompt_template_name": "pattern_analysis_v2",
  "prompt_sent": "Analyze these security findings and identify patterns, clusters, or correlated issues:\n\n[Findings JSON...]",
  "response_received": "PATTERN ANALYSIS\n\nCluster 1: Firewall Rules (3 findings)\n- Multiple ports exposed that correlate with service misconfigurations...",
  "model_used": "claude-opus-5",
  "tokens_used": {
    "input_tokens": 3456,
    "output_tokens": 1234
  }
}
```

**Response:**
```json
{
  "ai_analysis_log_id": 790,
  "audit_id": 456,
  "analysis_type": "pattern_analysis",
  "prompt_hash": "b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a1",
  "response_hash": "a1z6y5x4w3v2u1t0s9r8q7p6o5n4m3l2k1j0i9h8g7f6e5d4c3b",
  "execution_hash": "exec_hash_67890fghij",
  "model_used": "claude-opus-5",
  "tokens_input": 3456,
  "tokens_output": 1234,
  "created_at": "2026-07-29T14:25:12Z",
  "status": "logged"
}
```

---

## ✅ ACCEPTANCE CRITERIA

### AC1: Prompt capturado completo
**Given** ejecución de engine._run_ai_analysis()
**When** se genera executive_summary
**Then**
- ✅ prompt_sent se graba completo (no truncado)
- ✅ response_received captura full response
- ✅ prompt_hash = SHA256(prompt_sent)
- ✅ Record creado en ai_analysis_logs table
- ✅ Status = 'logged'

### AC2: Reproducibilidad vía execution_hash
**Given** ai_analysis_log con execution_hash='xyz789'
**When** Consulto BD para "qué análisis generó esta conclusión?"
**Then**
- ✅ Puedo encontrar audit_id, analysis_type, model
- ✅ Puedo regenerar exacto: mismo prompt + modelo → mismo resultado esperado
- ✅ execution_hash permanece invariante

### AC3: Integridad verificable
**Given** ai_analysis_log guardado
**When** Alguien intenta modificar response_received
**Then**
- ✅ response_hash != SHA256(modified_response)
- ✅ Skill evidence-verify detecta discrepancia
- ✅ Alert: "Evidence tampering detected on ai_analysis_log_id=789"

### AC4: Token tracking completo
**Given** ejecución con cache hits (claude API prompt caching)
**When** Registro de análisis
**Then**
- ✅ tokens_cache_creation captura si hubo cache creation
- ✅ tokens_cache_read captura si hubo cache reads
- ✅ total_tokens = input + output + cache_creation + cache_read
- ✅ Permite calcular costo real vs presupuesto

### AC5: Reversibilidad de decisiones
**Given** audit_id=456 con 3 análisis (priority_plan, pattern_analysis, executive_summary)
**When** Director ejecutivo cuestiona una recomendación
**Then**
- ✅ Puedo mostrar exacto prompt que generó recomendación
- ✅ Puedo demostrar qué hallazgos se consideraron
- ✅ Puedo mostrar checks que se ejecutaron

### AC6: Model versioning
**Given** análisis ejecutado con claude-opus-5
**When** Meses después, claude-sonnet-6 es disponible
**Then**
- ✅ model_used field preserva versión original
- ✅ No hay riesgo de "retrospective model changes"
- ✅ Puedo comparar: ¿misma conclusión con nuevo modelo?

### AC7: Truncation & size limits
**Given** prompt > 16384 chars o response > 32768 chars
**When** MCP tool intenta guardar
**Then**
- ✅ Prompts largas se truncan con marker "(truncated)"
- ✅ Response se trunca a 32KB max
- ✅ Hashes se calculan sobre truncated version
- ✅ Warning: "Prompt/response truncated for storage"

---

## ⚠️ ERROR HANDLING

| Error Type | Causa | Acción |
|-----------|-------|--------|
| `audit_not_found` | audit_id no existe | Verificar audit_id válido |
| `duplicate_analysis` | Ya existe analysis_type para audit_id | Permitir update o rechazar |
| `malformed_prompt` | prompt_sent < 50 chars | Enviar prompt válido |
| `model_unknown` | model_used no reconocido | Usar modelo válido |
| `tokens_invalid` | tokens_used negativos o inconsistentes | Verificar API response |
| `response_too_large` | Response > 32KB | Truncar (automatizado) |
| `hash_mismatch` | Hash verification falla | Reintentar; si persiste: corrupted data |

---

## 🔒 SEGURIDAD & COMPLIANCE

### Sensitive data handling
- ✅ Guardar prompts (contienen findings, no PII)
- ❌ NO guardar API keys, credentials
- ❌ NO guardar PII de usuarios
- Recomendación: Sanitize findings.evidence antes de enviar a Claude

### Audit trail
- Crear_at timestamp inmutable
- model_used, tokens_used no modificables post-creation
- verification_timestamp: auditor validation point

### GDPR/Privacy
- Si findings contienen PII: anónimizar antes de enviar prompt
- Considerar: masking de emails, IPs sensibles
- Retención: 90 días default, configurable

---

## 📦 DEPENDENCIAS

### Externas
- **hashlib.sha256** (stdlib)
- **anthropic** SDK (ya en requirements.txt)

### Internas
- `auditoria.storage.database.DatabaseManager`
- `auditoria.core.engine.AuditEngine`
- `auditoria.ai.analyzer.AuditAnalyzer`

---

## 🔄 INTEGRACIÓN CON SPECS

**Upstream (usa):**
- ← engine.py: llama a log_ai_analysis() después de cada análisis

**Downstream (usado por):**
- → 5-skill-evidence-verify: validar prompt_hash, response_hash

---

## 📋 DEFINITION OF DONE

- [ ] spec.md completo
- [ ] schema.sql + ALTER TABLE ai_analyses
- [ ] 2+ ejemplos funcionales
- [ ] 7 AC pasadas
- [ ] Migration: scripts/migrations/20260729_002_ai_analysis_logs.sql
- [ ] tests/spec_2_acceptance.py >= 8 test cases

---

## 🚀 ROADMAP

**Fase 1: Schema & Base (1-1.5h)**
- [ ] Crear ai_analysis_logs table
- [ ] ALTER ai_analyses table
- [ ] Indexes

**Fase 2: Tool Implementation (1h)**
- [ ] log_ai_analysis() MCP tool
- [ ] get_ai_analysis_log() MCP tool
- [ ] Hash generation (SHA256)

**Fase 3: Engine Integration (1h)**
- [ ] engine._run_ai_analysis() → llama log_ai_analysis()
- [ ] Error handling, retries
- [ ] Logging

**Fase 4: Testing (45m)**
- [ ] Unit tests (7 AC)
- [ ] Integration tests (end-to-end)
- [ ] DB migration validation

---

**Versión:** 1.0 | **Estado:** Draft — Ready for implementation
