# SPEC 5: Skill — evidence-chain-verify

**Validación de integridad de evidence chain contra tampering**

---

## 📋 VISIÓN GENERAL

### Problema
Findings se guardan en BD con evidence fields, pero sin verificación de integridad:
- Si alguien modifica stdout de comando, no se detecta
- Si alguien borra evidence_hash, no hay trace
- Si response IA se edita, no hay prueba de alteración
- Brecha: "¿fueron los findings alterados post-audit?"

### Solución
Skill que valida:
- Checksums de evidence fields (SHA256)
- Integridad de command_executions vs evidence_hash guardado
- Integridad de ai_analysis_logs vs prompt/response_hash
- Integridad de webhook events vs delivery logs
- Genera verification_report con status de cada finding

---

## 🎯 INTERFAZ

### Skill: `/evidence-verify`

**Invocación:**
```bash
/evidence-verify <audit_id> [--findings-only] [--repair]
```

**Parámetros:**
- `audit_id` (required): ID de auditoría a verificar
- `--findings-only` (optional): Solo validar findings, no IA analysis ni webhooks
- `--repair` (optional): Corregir hashes detectados como inválidos

**Entrada (CLI/UI):**
```json
{
  "audit_id": 456,
  "mode": "verify",  // verify, verify-findings-only, repair, repair-and-log
  "include": ["findings", "ai_analysis", "webhooks", "commands"]
}
```

**Salida:**
```json
{
  "verification_report": {
    "audit_id": 456,
    "verified_at": "2026-07-29T15:00:00Z",
    "overall_status": "verified",  // verified, tampered, inconclusive
    "findings_checked": 12,
    "findings_valid": 12,
    "findings_tampered": 0,
    "findings_inconclusive": 0,
    
    "ai_analysis_checked": 3,
    "ai_analysis_valid": 3,
    "ai_analysis_tampered": 0,
    
    "webhooks_checked": 5,
    "webhooks_valid": 5,
    "webhooks_tampered": 0,
    
    "commands_checked": 8,
    "commands_valid": 8,
    "commands_tampered": 0,
    
    "issues": [
      {
        "type": "finding_hash_mismatch",
        "finding_id": 123,
        "title": "Certificate Expired",
        "stored_hash": "abc123",
        "calculated_hash": "def456",
        "evidence_field": "evidence.cert_expiry_date",
        "severity": "critical"
      }
    ],
    "verification_record_id": 789
  }
}
```

---

## 💾 SCHEMA BASE DE DATOS

**Nueva tabla:** `evidence_verifications`

```sql
CREATE TABLE IF NOT EXISTS evidence_verifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    audit_id INTEGER NOT NULL,
    verified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    verified_by TEXT,  -- User/skill name
    
    overall_status TEXT NOT NULL,  -- verified, tampered, inconclusive
    
    findings_checked INTEGER,
    findings_valid INTEGER,
    findings_tampered INTEGER,
    findings_inconclusive INTEGER,
    
    ai_analysis_checked INTEGER,
    ai_analysis_valid INTEGER,
    ai_analysis_tampered INTEGER,
    
    webhooks_checked INTEGER,
    webhooks_valid INTEGER,
    webhooks_tampered INTEGER,
    
    commands_checked INTEGER,
    commands_valid INTEGER,
    commands_tampered INTEGER,
    
    issues TEXT,  -- JSON array de issues
    repair_executed BOOLEAN DEFAULT FALSE,
    repair_details TEXT,
    
    FOREIGN KEY (audit_id) REFERENCES audits(id)
);

-- Nueva columna a tabla findings
ALTER TABLE findings 
ADD COLUMN IF NOT EXISTS evidence_hash TEXT,
ADD COLUMN IF NOT EXISTS evidence_verified_at TIMESTAMP,
ADD COLUMN IF NOT EXISTS evidence_tampered BOOLEAN DEFAULT FALSE;

-- Nueva columna a ai_analyses
ALTER TABLE ai_analyses 
ADD COLUMN IF NOT EXISTS evidence_verified_at TIMESTAMP,
ADD COLUMN IF NOT EXISTS evidence_tampered BOOLEAN DEFAULT FALSE;
```

---

## 📋 ALGORITMO DE VERIFICACIÓN

### Paso 1: Verificar findings

Para cada finding en audit_id:

```python
def verify_finding(finding):
    # Recalcular hash de evidence
    evidence_str = json.dumps(finding.evidence, sort_keys=True)
    calculated_hash = sha256(evidence_str.encode()).hexdigest()
    
    if finding.evidence_hash is None:
        return "inconclusive"  # No hay hash (legacy finding)
    
    if calculated_hash != finding.evidence_hash:
        return "tampered"  # Hash no coincide
    
    return "verified"
```

### Paso 2: Verificar AI Analysis

Para cada ai_analysis_log en audit_id:

```python
def verify_ai_analysis(log):
    prompt_hash_calc = sha256(log.prompt_sent.encode()).hexdigest()
    response_hash_calc = sha256(log.response_received.encode()).hexdigest()
    
    if prompt_hash_calc != log.prompt_hash:
        return "tampered"  # Prompt fue modificado
    
    if response_hash_calc != log.response_hash:
        return "tampered"  # Response fue modificado
    
    return "verified"
```

### Paso 3: Verificar Commands

Para cada command_execution:

```python
def verify_command(cmd):
    output = cmd.stdout + cmd.stderr
    evidence_hash_calc = sha256(output.encode()).hexdigest()
    
    if evidence_hash_calc != cmd.evidence_hash:
        return "tampered"  # Output fue modificado
    
    return "verified"
```

### Paso 4: Verificar Webhooks

Para cada webhook_delivery_event:

```python
def verify_webhook_delivery(event):
    # Verificar que event_id existe en webhook_changes
    # Verificar que entradas de webhook_changes son consistentes
    # Detectar: "¿webhook fue modificado después de delivery?"
    
    changes_after = get_webhook_changes(event.webhook_id, after=event.delivered_at)
    if len(changes_after) > 0:
        return "inconclusive"  # Webhook fue modificado después
    
    return "verified"
```

---

## 📝 EJEMPLOS

### Ejemplo 1: Auditoría sin tampering

**Invocación:**
```bash
/evidence-verify 456
```

**Salida:**
```json
{
  "verification_report": {
    "audit_id": 456,
    "verified_at": "2026-07-29T15:00:00Z",
    "overall_status": "verified",
    
    "findings_checked": 12,
    "findings_valid": 12,
    "findings_tampered": 0,
    "findings_inconclusive": 0,
    
    "ai_analysis_checked": 3,
    "ai_analysis_valid": 3,
    "ai_analysis_tampered": 0,
    
    "webhooks_checked": 5,
    "webhooks_valid": 5,
    "webhooks_tampered": 0,
    
    "commands_checked": 8,
    "commands_valid": 8,
    "commands_tampered": 0,
    
    "issues": [],
    "verification_record_id": 789
  }
}
```

**Console output:**
```
✅ EVIDENCE CHAIN VERIFICATION
   Audit ID: 456
   Status: VERIFIED ✓
   
   ✓ 12/12 findings verified
   ✓ 3/3 AI analyses verified
   ✓ 5/5 webhook deliveries verified
   ✓ 8/8 command executions verified
   
   No issues detected.
   Verification record: #789
```

### Ejemplo 2: Tampering detectado

**Salida:**
```json
{
  "verification_report": {
    "audit_id": 456,
    "overall_status": "tampered",
    
    "findings_checked": 12,
    "findings_valid": 11,
    "findings_tampered": 1,
    "findings_inconclusive": 0,
    
    "issues": [
      {
        "type": "finding_hash_mismatch",
        "finding_id": 123,
        "title": "Windows Firewall Disabled",
        "severity": "high",
        "stored_hash": "abc123def456",
        "calculated_hash": "xyz789",
        "evidence_field": "evidence.firewall_output",
        "detected_at": "2026-07-29T15:00:00Z",
        "suggested_action": "Investigate: finding evidence was modified. Revert from backup or rebuild audit."
      }
    ]
  }
}
```

**Alert (si integrado con webhook):**
```
🚨 EVIDENCE TAMPERING DETECTED
   Audit: 456
   Finding: "Windows Firewall Disabled" (ID: 123)
   Issue: Evidence hash mismatch
   Stored:     abc123def456
   Calculated: xyz789
   
   Action: Investigate immediately. Review webhook logs to see who accessed BD.
```

---

## ✅ ACCEPTANCE CRITERIA

### AC1: Verificación de findings OK
**Given** audit con 10 findings que nunca fueron modificados
**When** `/evidence-verify 456`
**Then**
- ✅ findings_checked = 10
- ✅ findings_valid = 10
- ✅ findings_tampered = 0
- ✅ overall_status = "verified"

### AC2: Detección de tampering en evidence
**Given** finding con evidence modificado
**When** Alguien cambia findings.evidence.stdout directamente en BD
**Then**
- ✅ Skill recalcula hash
- ✅ Detecta mismatch
- ✅ Status = "tampered"
- ✅ Issue incluye qué campo cambió

### AC3: Reparación de hashes (opcional)
**Given** findings con hashes inválidos (legacy)
**When** `/evidence-verify 456 --repair`
**Then**
- ✅ Recalcula hashes correctos
- ✅ Actualiza evidence_hash fields
- ✅ repair_executed = TRUE
- ✅ repair_details documenta qué se arregló

### AC4: IA Analysis verification
**Given** ai_analysis_log con prompt/response
**When** Verificar
**Then**
- ✅ Recalcula prompt_hash y response_hash
- ✅ Compara vs valores guardados
- ✅ Detecta si fueron modificados

### AC5: Command execution verification
**Given** command_execution con stdout/stderr
**When** Verificar
**Then**
- ✅ Recalcula evidence_hash
- ✅ Compara vs guardado
- ✅ Detecta si output fue modificado

### AC6: Webhook delivery verification
**Given** webhook_delivery_event con timestamps
**When** Verificar
**Then**
- ✅ Detecta si webhook_changes posteriores existen
- ✅ Status = "inconclusive" si webhook fue modificado después de delivery
- ✅ Puede indicar: "webhook URL cambió después de este evento"

### AC7: Audit trail de verificaciones
**Given** Múltiples verificaciones del mismo audit
**When** Consultar evidence_verifications table
**Then**
- ✅ Puedo ver histórico de todas las verificaciones
- ✅ Puedo comparar: "¿cambió el status entre verificación 1 y 2?"
- ✅ Puedo detectar: "¿cuándo se detectó tampering?"

---

## ⚠️ ERROR HANDLING

| Caso | Acción |
|------|--------|
| `audit_not_found` | Retornar error 404 |
| `no_findings` | Status = "verified" (audit vacío, válido) |
| `legacy_no_hashes` | Status = "inconclusive" (puede reparar con --repair) |
| `db_connection_error` | Retornar error 500, log del problema |

---

## 📦 INTEGRACIÓN CON SPECS

**Upstream (usa):**
- ← 1-mcp-filesystem-ops: evidence_hash de commands
- ← 2-mcp-audit-log: prompt_hash, response_hash
- ← 3-mcp-webhook-audit: webhook delivery logs

**Downstream (usado por):**
- → skill: evidence-chain-verify es standalone
- → compliance automation: puede disparar alerts

---

## 🚀 IMPLEMENTACIÓN

**Ubicación:** `.claude/skills/evidence-verify.md`

**Lógica:** Python en `auditoria/skills/evidence_verify.py`

**Tests:** `tests/spec_5_acceptance.py`

---

**Versión:** 1.0 | **Estado:** Draft — Ready for implementation
