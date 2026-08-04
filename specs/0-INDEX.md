# ESPECIFICACIONES TÉCNICAS — Auditoria-CS-IA v2.0

**Spec-driven roadmap para cerrar brechas de verificabilidad y agregar capacidades MCP + Skills**

---

## 📋 ÍNDICE DE ESPECIFICACIONES

### Fase 1: Brechas Blocking (Semana 1-2)

| # | Spec | Componente | Bloquea | Esfuerzo | Estado |
|---|------|-----------|---------|----------|--------|
| 1 | [1-mcp-filesystem-ops](./1-mcp-filesystem-ops/spec.md) | MCP Server | Audit trail de comandos del SO | 1-2h | 📝 Spec |
| 2 | [2-mcp-audit-log](./2-mcp-audit-log/spec.md) | MCP + Schema DB | Reproducibilidad IA analysis | 2-3h | 📝 Spec |
| 3 | [3-mcp-webhook-audit](./3-mcp-webhook-audit/spec.md) | MCP + Schema DB | Compliance accountability webhooks | 2h | 📝 Spec |

### Fase 2: Brechas Medium-Priority (Semana 3-4)

| # | Spec | Componente | Cierra brecha | Esfuerzo | Estado |
|---|------|-----------|--------------|----------|--------|
| 4 | [4-mcp-task-versioning](./4-mcp-task-versioning/spec.md) | MCP + Schema DB | Change log auditable de scheduled tasks | 2-3h | 📝 Spec |
| 5 | [5-skill-evidence-verify](./5-skill-evidence-verify/spec.md) | Skill + Validator | Detecta tampering en findings | 2-3h | 📝 Spec |
| 6 | [6-skill-audit-baseline](./6-skill-audit-baseline/spec.md) | Skill + Historical data | Drift detection trimestral | 2h | 📝 Spec |

### Fase 3: Integraciones Externas (Semana 5+)

| # | Spec | Componente | Funcionalidad | Esfuerzo | Estado |
|---|------|-----------|--------------|----------|--------|
| 7 | [7-integration-semgrep](./7-integration-semgrep/spec.md) | MCP Wrapper | SAST integration (filesystem brecha) | 4-6h | 📝 Spec |
| 8 | [8-integration-breach-check](./8-integration-breach-check/spec.md) | MCP + Service API | Secret verification (secrets brecha) | 3-4h | 📝 Spec |

---

## 🎯 PRINCIPIOS DE DISEÑO

### 1. **Spec-First, Code-Second**
Cada especificación incluye:
- ✅ Interfaz / Schema (tipos, JSON schema, SQL)
- ✅ Ejemplos request/response
- ✅ Acceptance criteria (tests)
- ✅ Error handling
- ❌ Código (generado después de spec review)

### 2. **Trazabilidad Completa**
Toda acción genera:
- **Quién:** user/executor context
- **Cuándo:** ISO 8601 timestamp
- **Qué:** command/prompt/change descripción
- **Por qué:** reason/audit_event field
- **Dónde:** source context (IP, cwd, process_id)

### 3. **Reproducibilidad Verificable**
- Toda ejecución se graba: inputs, outputs, intermediate states
- Generación de hashes/checksums de evidence
- Capacidad de replay de auditorías idénticas

### 4. **Compatibilidad Backward**
- MCP tools nuevos se registran sin breaking existing tools
- Schema DB con migrations atomícas
- Settings.json tolerante a nuevos fields

---

## 📊 RESUMEN DE CAMBIOS

### Base de datos

**Nuevas tablas:**
- `command_executions` — Audit trail de comandos del SO
- `ai_analysis_logs` — Prompts + responses de Claude
- `webhook_events` — Registro de webhooks (registro + deliveries)
- `task_change_log` — Versioning de scheduled tasks

**Cambios a tablas existentes:**
- `ai_analyses` — Agregar: prompt_sent, response_received, execution_plan
- `findings` — Agregar: evidence_hash, verified_by, tamper_detected

### MCP Tools (nuevos)

| Tool | Servidor | Parámetros | Output |
|------|----------|-----------|--------|
| `run_command` | filesystem-ops | cmd, args, cwd, timeout | stdout, stderr, exit_code, executor, timestamp |
| `capture_audit_context` | filesystem-ops | command_id, context_data | saved_context_id, checksum |
| `get_ai_log` | audit-log | audit_id, analysis_type | full_prompt, response, model_version, tokens |
| `log_webhook_event` | webhook-audit | webhook_id, event_type, payload | event_id, stored_at |
| `get_task_versions` | task-versioning | task_id, limit | versions[], diff_from_current |

### Skills (nuevas)

| Skill | Entrada | Salida | Automatiza |
|-------|---------|--------|-----------|
| `/evidence-verify` | audit_id | verification_report | Valida integrity de evidence chain |
| `/audit-baseline` | target | baseline_id, findings_snapshot | Captura baseline para drift detection |
| `/audit-drift-report` | target, baseline_id, days | drift_summary, new_findings | Compara vs baseline histórico |

---

## 🔄 DEPENDENCIAS ENTRE SPECS

```
1-mcp-filesystem-ops
    ├─→ 3-mcp-webhook-audit (dispatch command_executed event)
    └─→ 5-skill-evidence-verify (validar evidence_hash de commands)

2-mcp-audit-log
    └─→ 5-skill-evidence-verify (check prompt integrity)

3-mcp-webhook-audit
    └─→ (standalone)

4-mcp-task-versioning
    └─→ (standalone, pero notifica via webhook)

5-skill-evidence-verify
    ├─ 1-mcp-filesystem-ops
    ├─ 2-mcp-audit-log
    └─ 3-mcp-webhook-audit

6-skill-audit-baseline
    └─ Requiere: findings históricos en DB (ya existe)

7-integration-semgrep
    └─ 1-mcp-filesystem-ops (usa run_command)

8-integration-breach-check
    └─ (standalone, pero enriquece findings de secrets.py)
```

**Orden de implementación recomendado:** 1 → 2 → 3 → (5 en paralelo) → 4 → 6 → 7 → 8

---

## ✅ DEFINITION OF DONE

Cada especificación está DONE cuando:

- [ ] Spec.md completado y revisado
- [ ] Schema.json o schema.sql definido
- [ ] 3+ ejemplos request/response funcionales
- [ ] Acceptance criteria >= 5 casos (happy path + edge cases)
- [ ] Error handling: >= 3 error types defined
- [ ] Migración DB (si aplica) con rollback plan
- [ ] Integración settings.json documentada
- [ ] RFC aprobado (si breaking change)

---

## 📋 CHECKLIST DE VALIDACIÓN GLOBAL

- [ ] Toda nueva table tiene `created_at` + `updated_at` timestamps
- [ ] Toda nueva MCP tool está en `AUDIT_TOOLS` registry (mcp/tools.py)
- [ ] Toda nueva skill está en `.claude/skills/` + settings.json
- [ ] Migraciones DB tienen rollback atómica
- [ ] No hay hard-coded secrets en specs
- [ ] Evidence fields siempre incluyen checksum/hash
- [ ] Audit trail siempre incluye `executor` + `reason` fields
- [ ] Ejemplos usan datos no-sensibles (fixtures)

---

## 📞 RFC PROCESS

Para cambios significativos (breaking changes, nuevos componentes):

1. Proponer en issue (referencing spec file)
2. Diskutir en PR antes de implementar código
3. Documentar decisiones en spec file (## Decision Log)
4. Obtener sign-off de arquitecto

Ver [RFC.md](./RFC.md) para detalles.

---

## 🚀 CÓMO USAR ESTAS SPECS

**Para implementadores:**
```bash
# 1. Leer spec.md completo
cat specs/1-mcp-filesystem-ops/spec.md

# 2. Validar schema
jsonschema -i examples/run_command.json schema.json

# 3. Implementar código
# ... implementar según spec ...

# 4. Ejecutar tests de acceptance
pytest tests/spec_1_acceptance.py -v

# 5. Validar DB migrations (si aplica)
python scripts/validate_migration.py specs/2-mcp-audit-log/migration.sql
```

**Para product/auditoría:**
- Leer sección "Acceptance Criteria" de cada spec
- Validar que acceptance criteria se cumple en PR
- Checkear evidence fields en specs de auditoria

**Para arquitectos:**
- Revisar "Design Decisions" y "Tradeoffs" en cada spec
- Validar que no hay conflictos entre specs (ver dependencias)
- Asegurar backward compatibility

---

## 📈 METRICS ESPERADAS POST-IMPLEMENTACIÓN

| Métrica | Antes | Target | Spec |
|---------|-------|--------|------|
| % findings con evidence_hash verificable | 0% | 100% | 1,2,5 |
| % AI analysis con prompt auditable | 0% | 100% | 2 |
| % webhooks con delivery audit trail | 0% | 100% | 3 |
| % tasks con change log | 0% | 100% | 4 |
| Falsos positivos en secrets (unverified) | Alto | Bajo | 8 |
| SAST findings integrados en report | 0 | 100% | 7 |

---

## 📚 REFERENCIAS

- Evaluación base: `../EVALUACION_AGENTIA.md` (en scratchpad)
- Settings.json: `../.claude/settings.json`
- MCP server: `../auditoria/mcp/server.py`
- DB schema: `../auditoria/storage/database.py`

---

**Versión:** 2.0 | **Última actualización:** 2026-07-29 | **Estado:** Draft
