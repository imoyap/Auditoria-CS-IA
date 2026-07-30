# TRACEABILITY MATRIX — Brechas → Specs → Implementación

**Matriz que conecta evaluación agéntica → especificaciones → código**

---

## 🎯 OVERVIEW

Cada brecha de verificabilidad de la evaluación agéntica se cierra con una o más especificaciones, que se convierten en código.

---

## 📊 MATRIX: Brechas → Specs

| Brecha | Problema | Spec | Componente | Cierre |
|--------|----------|------|-----------|--------|
| #1 | System commands sin audit trail (netsh, PowerShell) | SPEC-1 | MCP filesystem-ops | run_command() tool con evidence_hash |
| #1 | Comando ejecutado no se graba | SPEC-1 | DB command_executions | stdout + stderr + exit_code + executor |
| #2 | Port scan sin verificabilidad punto-en-tiempo | SPEC-1 | MCP filesystem-ops | Timestamp exacto en command_executions |
| #3 | IA analysis sin trazabilidad de prompt | SPEC-2 | MCP audit-log | log_ai_analysis() con prompt_sent + prompt_hash |
| #3 | No reproducible: no se graba prompt | SPEC-2 | DB ai_analysis_logs | prompt_sent field completo |
| #4 | Webhooks sin audit de quién/cuándo registró | SPEC-3 | MCP webhook-audit | register_webhook_audited() con registered_by |
| #4 | No hay log de webhook delivery attempts | SPEC-3 | DB webhook_delivery_events | Log cada intento (success/fail/retry) |
| #4 | No hay audit de cambios en webhook | SPEC-3 | DB webhook_changes | Change log: quién cambió qué |
| #5 | Scheduled tasks sin change log | SPEC-4 | MCP task-versioning | task_change_log table |
| #5 | Imposible detect unauthorized task changes | SPEC-4 | DB task_change_log | changed_by, change_reason, old/new_value |
| #6 | Filesystem checks sin SAST profundo | SPEC-7 | Integration Semgrep | semgrep-wrapper MCP server |
| #7 | Secrets sin verificación real (solo regex) | SPEC-8 | Integration Breach-Check | breach-check-service MCP server |
| *Cross* | Evidence chain sin verificabilidad integral | SPEC-5 | Skill evidence-verify | Validar integridad de todos hashes |
| *Cross* | No hay baseline para comparación histórica | SPEC-6 | Skill audit-baseline | Captura + compara vs baseline |

---

## 🔍 DETAIL: SPEC-1 vs Brecha #1

**Brecha:** "System commands sin audit trail — Firewall, antivirus, OS updates"

**Problem statement:**
```
Problema identificado en: auditoria/checks/system.py:79
Descripción: `fw_result = self._run_cmd(["netsh", ...])`
Captura solo output recortado (500 chars), sin:
  - Comando ejecutado
  - stderr
  - exit_code
  - timestamp exacto
  - usuario/executor
  - contexto de ejecución (cwd, env)
  
Impacto: 
  - Auditoría forense: imposible probar qué comando se ejecutó
  - Compliance: no hay cadena de custodia para evidencia
  - Reproducibilidad: no se puede re-ejecutar exacto
```

**Solución (SPEC-1):**

| Componente | Implementación | Cierre |
|-----------|-----------------|--------|
| **MCP Tool** | `run_command(command, args, cwd, timeout, audit_context)` | Ejecución controlada + completa |
| **DB Table** | `command_executions` con stdout, stderr, exit_code, executor, evidence_hash | Persistencia con trazabilidad |
| **Audit Trail** | Fields: audit_check_id, audit_reason, related_finding_id | Linkaje a finding original |
| **Integrity** | `evidence_hash = SHA256(stdout + stderr)` | Detecta tampering |
| **Integration** | system.py reemplaza `self._run_cmd()` → MCP call | Uso transparente |

**Antes (vulnerable):**
```python
# system.py línea 79
fw_result = self._run_cmd(["netsh", "advfirewall", "show", "allprofiles", "state"])
# Resultado: "State                                 ON" (500 chars max, sin contexto)
```

**Después (verificable):**
```python
# system.py línea 79
from auditoria.mcp.server import call_mcp_tool

result = call_mcp_tool("run_command", {
    "command": "netsh",
    "args": ["advfirewall", "show", "allprofiles", "state"],
    "audit_context": {
        "check_id": "SYS-003",
        "reason": "Windows Firewall status verification"
    }
})
# Resultado:
# {
#   "command_execution_id": 42,
#   "stdout": "...",
#   "stderr": "",
#   "exit_code": 0,
#   "executor": "DOMAIN\\admin-user",
#   "executed_at": "2026-07-29T14:23:45Z",
#   "evidence_hash": "a3f7c8d9..."
# }
```

**BD ahora contiene:**
```sql
SELECT * FROM command_executions WHERE id=42;
-- id: 42
-- command: netsh
-- args: ["advfirewall", "show", "allprofiles", "state"]
-- stdout: "State                                 ON..." (full)
-- stderr: ""
-- exit_code: 0
-- executor: DOMAIN\admin-user
-- executed_at: 2026-07-29 14:23:45
-- evidence_hash: a3f7c8d9...
-- audit_check_id: SYS-003
```

**Verificación de integridad:**
```python
# Skill evidence-verify (SPEC-5)
evidence_str = "State  ON..."  # stdout capturado
calculated_hash = SHA256(evidence_str)
if calculated_hash != command.evidence_hash:
    raise IntegrityError("Evidence tampering detected!")
```

---

## 🔍 DETAIL: SPEC-2 vs Brecha #3

**Brecha:** "IA Analysis sin trazabilidad del prompt ejecutado"

**Problem statement:**
```
Problema identificado en: auditoria/core/engine.py:76-96
Descripción: self.ai_analyzer.prioritize_findings(report)
Genera análisis IA pero NO se graba el prompt enviado a Claude.

BD actual (ai_analyses table):
- analysis_type: "priority_plan"
- content: "..." (response)
- model_used: "claude-opus-5"
- tokens_used: 1234
- created_at: timestamp

Falta:
- prompt_sent: ¿QUÉ PREGUNTA SE HIZO?
- prompt_hash: ¿Es reproducible?
- execution_plan: ¿QUÉ HALLAZGOS SE CONSIDERARON?

Impacto:
- Si resultado IA se cuestiona: imposible reproducir
- Si hubo prompt injection: no se detecta
- No hay verificabilidad de recomendaciones críticas
```

**Solución (SPEC-2):**

| Componente | Implementación | Cierre |
|-----------|-----------------|--------|
| **MCP Tool** | `log_ai_analysis(audit_id, analysis_type, prompt_sent, response_received, model_used)` | Registro de prompts |
| **DB Table** | `ai_analysis_logs` con prompt_sent, response_received, prompt_hash, response_hash | Trazabilidad completa |
| **Hashes** | prompt_hash = SHA256(prompt_sent), response_hash = SHA256(response_received) | Integridad verificable |
| **Reproducibilidad** | execution_hash = SHA256(audit_id + analysis_type + prompt_hash + model) | Puede re-ejecutar |
| **Integration** | engine._run_ai_analysis() → log_ai_analysis() | Transparente |

**Antes (débil):**
```python
# engine.py línea 76
plan = self.ai_analyzer.prioritize_findings(report)  # ← Sin logging
self.db_manager.save_ai_analysis(audit_id, "priority_plan", plan["priority_plan"])
# Se guarda solo content, no prompt
```

**Después (verificable):**
```python
# engine.py línea 76
prompt = self.ai_analyzer._build_prompt(report)  # Construir prompt
response = self.ai_analyzer.prioritize_findings(report)  # Ejecutar

# Registrar en BD
self.call_mcp_tool("log_ai_analysis", {
    "audit_id": audit_id,
    "analysis_type": "priority_plan",
    "prompt_sent": prompt,
    "response_received": response["content"],
    "model_used": "claude-opus-5",
    "tokens_used": {"input": 1234, "output": 567}
})

# BD now contains:
# ai_analysis_logs:
#   prompt_sent: "Here are findings from security audit..."
#   prompt_hash: "abc123..."
#   response_received: "Priority Plan: 1. Critical: ..."
#   response_hash: "def456..."
#   execution_hash: "xyz789..."
```

**Verificación de reproducibilidad:**
```python
# Skill evidence-verify (SPEC-5)
log = ai_analysis_logs[123]
if SHA256(log.prompt_sent) != log.prompt_hash:
    raise IntegrityError("Prompt was modified!")

# Puedo regenerar exacto:
response_new = claude.messages.create(
    model=log.model_used,
    messages=[{"role": "user", "content": log.prompt_sent}]
)
# Debería dar resultado idéntico
```

---

## 🔗 INTEGRACIÓN ENTRE SPECS

```
Evaluación Agéntica (7 brechas)
    ↓
Especificaciones (8 specs)
    ├─ SPEC-1 (filesystem-ops) ← Brecha #1
    ├─ SPEC-2 (audit-log) ← Brecha #3
    ├─ SPEC-3 (webhook-audit) ← Brecha #4
    ├─ SPEC-4 (task-versioning) ← Brecha #5
    ├─ SPEC-5 (evidence-verify) ← Todas las brechas (cross-cutting)
    ├─ SPEC-6 (audit-baseline) ← Brecha #2 (tendencias)
    ├─ SPEC-7 (semgrep) ← Brecha #6
    └─ SPEC-8 (breach-check) ← Brecha #7
    ↓
Código (Python)
    ├─ auditoria/mcp/tools.py (SPEC-1,2,3,4,7,8)
    ├─ auditoria/storage/database.py (SPEC-1,2,3,4)
    ├─ auditoria/skills/*.py (SPEC-5,6)
    ├─ auditoria/core/engine.py (SPEC-2)
    └─ auditoria/checks/system.py, etc. (SPEC-1)
    ↓
Base de Datos (SQLite)
    ├─ command_executions (SPEC-1)
    ├─ ai_analysis_logs (SPEC-2)
    ├─ webhooks_audit (SPEC-3)
    ├─ webhook_delivery_events (SPEC-3)
    ├─ webhook_changes (SPEC-3)
    ├─ task_change_log (SPEC-4)
    ├─ audit_baselines (SPEC-6)
    └─ evidence_verifications (SPEC-5)
    ↓
Tests (pytest)
    ├─ tests/spec_1_acceptance.py (7 AC)
    ├─ tests/spec_2_acceptance.py (7 AC)
    ├─ tests/spec_3_acceptance.py (7 AC)
    ├─ tests/spec_5_acceptance.py (7 AC)
    ├─ tests/spec_6_acceptance.py (7 AC)
    └─ tests/e2e_audit_flow.py (full workflow)
    ↓
Producción
```

---

## ✅ VERIFICATION CHECKLIST

Usar esta matriz para verificar que cada brecha está cubierta:

- [ ] Brecha #1: SPEC-1 implementado + AC1 pasando (command_execution creado con full output)
- [ ] Brecha #2: SPEC-6 implementado + AC3 pasando (baseline capture + comparison)
- [ ] Brecha #3: SPEC-2 implementado + AC1 pasando (prompt_sent grabado)
- [ ] Brecha #4: SPEC-3 implementado + AC1 pasando (webhook audit trail completo)
- [ ] Brecha #5: SPEC-4 implementado + AC1 pasando (task change log)
- [ ] Brecha #6: SPEC-7 implementado (Semgrep wrapper, opcional)
- [ ] Brecha #7: SPEC-8 implementado (Breach-check service, opcional)
- [ ] Cross: SPEC-5 implementado + AC1 pasando (evidence verification detecta tampering)

---

## 📊 RISK MATRIX: Before vs After

### ANTES (Vulnerable)

| Riesgo | Severidad | Causa |
|--------|-----------|-------|
| Tampering: command output modificado en BD | CRITICAL | Sin evidence_hash, sin audit trail |
| No reproducible: IA analysis sin prompt | HIGH | No se graba qué pregunta se hizo |
| Webhooks no auditables | HIGH | Sin webhook audit trail |
| Compliance: cadena de custodia rota | CRITICAL | Sin timestamps/executor/context |
| Accidental data loss: scheduled tasks sin versioning | MEDIUM | Sin change log |

### DESPUÉS (Verified)

| Riesgo | Severidad | Mitigación |
|--------|-----------|-----------|
| Tampering: command output modificado | MITIGATED | evidence_hash + skill evidence-verify |
| No reproducible: IA analysis | MITIGATED | prompt_sent + execution_hash en BD |
| Webhooks no auditables | MITIGATED | webhook_audit_trail + changes log |
| Compliance: cadena de custodia | MITIGATED | Timestamps + executor + context en todas tablas |
| Accidental data loss: tasks | MITIGATED | task_change_log con versioning |

---

## 📈 VERIFICATION METRICS

Tracking verificabilidad pre vs post-implementación:

| Métrica | Antes | Target | Spec |
|---------|-------|--------|------|
| % findings con evidence reproducible | 0% | 100% | SPEC-1,2,5 |
| % AI analysis con prompt auditable | 0% | 100% | SPEC-2 |
| % webhooks con delivery audit trail | 0% | 100% | SPEC-3 |
| % scheduled tasks con change log | 0% | 100% | SPEC-4 |
| Evidence tampering detection rate | N/A | 100% | SPEC-5 |
| Baseline comparisons available | 0 | Unlimited | SPEC-6 |
| SAST findings integrated | 0 | 100% | SPEC-7 |
| Verified secrets (not false positives) | 0% | 80%+ | SPEC-8 |

---

## 🎯 HOW TO USE THIS MATRIX

**Para Arquitecto:** Validar que cada brecha está cubierta por al menos 1 spec

**Para Developer:** Ver qué brecha debe resolver su spec

**Para QA:** Mapear AC a brecha que resuelven

**Para Auditor:** Verificar post-deployment que brechas están cerradas

---

**Versión:** 1.0 | **Última actualización:** 2026-07-29
