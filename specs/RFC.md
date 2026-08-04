# RFC PROCESS — Auditoria-CS-IA Specs

**Request for Comments — Proceso de revisión y aprobación de especificaciones**

---

## 🎯 OBJETIVO

Establecer un proceso riguroso para:
1. Revisar especificaciones antes de implementación
2. Documentar decisiones de diseño
3. Capturar feedback y tradeoffs
4. Asegurar backward compatibility
5. Mantener rastreabilidad de cambios

---

## 📋 ETAPAS DEL RFC

### 1. PROPUESTA (Draft)

**Estado:** Spec.md en branch feature

**Checklist:**
- [ ] Spec.md completado (todas secciones)
- [ ] Schema SQL definido (si aplica)
- [ ] 2+ ejemplos funcionales
- [ ] AC >= 5 casos
- [ ] Dependencias mapeadas
- [ ] DOD (Definition of Done) claro

**Formato de commit:**
```
RFC: [SPEC-NUMBER] — [Título corto]

Spec: 1-mcp-filesystem-ops
Title: MCP Server — filesystem-operations
Status: Draft → Proposal
Issue: #NNN (si aplica)

Changes:
- specs/1-mcp-filesystem-ops/spec.md: proposed

Acceptance:
- [ ] Architecture review
- [ ] Security review (si aplica)
- [ ] DB schema validation (si aplica)
- [ ] Performance impact analysis
- [ ] Backward compatibility check
```

---

### 2. REVISIÓN POR ARQUITECTO (Proposal → Review)

**Responsable:** Architecture Lead

**Duración:** 2-3 días

**Checklist:**
- [ ] Especificación es clara y completa
- [ ] Interfaz MCP/Tool está bien definida
- [ ] Schema SQL es normalizado
- [ ] Ejemplos son realistas
- [ ] AC son verificables
- [ ] Dependencias con otras specs mapeadas
- [ ] No hay breaking changes undocumented
- [ ] Performance concerns identificados

**Feedback esperado:**
```markdown
## Architecture Review — SPEC-1

### ✅ LGTM
- Clear interface
- Good examples
- AC well-defined

### 🤔 Questions
1. Why timeout_seconds max 300? Consider use cases > 5 min?
2. Are we handling Windows vs Linux PATH differences?

### ⚠️ Concerns
1. Output truncation to 64KB — consider streaming for large logs?
2. Evidence_hash approach: SHA256 OK or need HMAC for authentication?

### 🔧 Suggestions
- Consider adding `environment` field for context (Python version, OS version)
- Document retry strategy explicitly

### 👍 Approved
Status: Review → Accepted (conditional on addressing 🤔 Q2)
```

---

### 3. REVISIÓN DE SEGURIDAD (si aplica)

**Responsable:** Security Lead

**Cuándo aplica:**
- MCP tools que ejecutan comandos del SO
- Manejo de secrets/credentials
- Webhook delivery
- Access control changes

**Checklist:**
- [ ] Input validation definida
- [ ] Command injection risks mitigados
- [ ] Secrets handling (nunca en claro)
- [ ] Audit trail para todas las acciones
- [ ] HTTPS/TLS para comunicaciones
- [ ] Authentication & authorization verificado
- [ ] SQL injection risks assessed

**Feedback:**
```markdown
## Security Review — SPEC-1

### ✅ APPROVED
- Whitelist de comandos es exhaustivo
- Args validación via schema
- SHA256 para evidence integrity OK

### ⚠️ Remediation Required
1. Document secret rotation strategy
2. Add rate limiting para run_command calls
3. Log all command executions (even failed) for forensics

Status: Security → Conditional Approval
Remediation: Must add docs/SECURITY.md section
```

---

### 4. REVISIÓN DE ESQUEMA DB (si aplica)

**Responsable:** Database Architect

**Checklist:**
- [ ] Normalización (3NF mínimo)
- [ ] Indexes apropiados para queries esperadas
- [ ] FK constraints válidas
- [ ] Migrations son reversibles
- [ ] No hay circular dependencies
- [ ] Scalability: ¿10M rows OK?
- [ ] Backward compatibility: ¿ALTER TABLE es additive?

**Feedback:**
```markdown
## DB Schema Review — SPEC-2

### ✅ Approved
- Schema is normalized
- Indexes are well-chosen
- Migration is reversible

### 🤔 Questions
1. ai_analysis_logs: prompt_sent puede ser NULL para compatibility con old ai_analyses?
2. Considerar partitioning de ai_analysis_logs por audit_id si tabla crece > 100M rows?

### 🔧 Optimization
- Considerar: generated column para total_tokens para performance
- Considerar: JSON indexes en ai_analysis_logs.execution_context para queries complejas

Status: Approved
```

---

### 5. DECISION LOG

Una vez aprobado, spec.md debe incluir sección **Decision Log**:

```markdown
## Decision Log

### Decision 1: SHA256 vs HMAC para evidence_hash
**Proposed:** SHA256(stdout + stderr) para evidence integrity
**Alternatives:** 
- HMAC-SHA256(secret): más seguro contra tampering deliberado
- CRC32: más rápido, menos seguridad
**Decision:** SHA256 (balance entre seguridad y simplicity)
**Rationale:** 
- Findings son en BD segura (acceso controlado)
- SHA256 suficiente para detectar corruption
- HMAC requeriría secret management adicional
**Tradeoff:** No detecta tampering deliberado por admin BD

**Approved by:** Architecture Lead
**Date:** 2026-07-29
**Reviewed by:** [List reviewers]

---

### Decision 2: Truncation de output a 64KB
**Proposed:** Max 64KB para stdout en command_executions
**Alternatives:**
- 256KB (más datos, más storage)
- Streaming (más complejidad)
- Variable según comando
**Decision:** 64KB fixed (mejor que 256KB para mayoría casos)
**Rationale:**
- La mayoría comandos (netsh, systemctl) < 1KB
- Rare cases > 64KB (logs extensos)
- 64KB = buen balance storage vs completeness
**Tradeoff:** Comandos con output > 64KB se truncan, user debe re-ejecutar con redirection

**Approved by:** Database Architect
**Date:** 2026-07-29
```

---

## 📝 FORMATO DE ESPECIFICACIÓN

Toda especificación debe incluir estas secciones:

```markdown
# SPEC [N]: [Component Name]

## 📋 VISIÓN GENERAL
- Problema
- Solución
- Scope

## 🎯 INTERFAZ MCP / SKILL
- Tool/Skill name
- Parámetros (JSON schema)
- Output (JSON schema)

## 💾 SCHEMA BASE DE DATOS (si aplica)
- Nueva tabla(s)
- Cambios a tablas existentes
- Indexes

## 📝 EJEMPLOS
- 2+ ejemplos request/response

## ✅ ACCEPTANCE CRITERIA
- AC1, AC2, ... AC7+

## ⚠️ ERROR HANDLING
- Tabla de errores + handling

## 🔒 SEGURIDAD & COMPLIANCE
- Input validation
- Secrets handling
- Audit trail

## 📦 DEPENDENCIAS
- Externas
- Internas

## 🔄 INTEGRACIÓN CON SPECS
- Upstream (usa)
- Downstream (usado por)

## 📋 DEFINITION OF DONE
- Checklist de tareas

## 🚀 ROADMAP DE IMPLEMENTACIÓN
- Fases con horarios

## Decision Log
- Decisiones de diseño tomadas

---

## APPENDIX: Schema Details
- schema.json (JSON schema para inputs)
- schema.sql (SQL DDL)
- migration.sql (SQL migration)
```

---

## ✅ APPROVAL WORKFLOW

```
[Spec Author] → Draft
    ↓
[Architecture Review] → ✅ Architecture Approved? 
    ├→ ❌ Revisión Needed → [Author] → Redraft
    └→ ✅ Yes
        ↓
[Security Review] (if applicable)
    ├→ ✅ Approved
    └→ ⚠️ Remediation Required
        ↓
[DB Review] (if applicable)
    ├→ ✅ Approved
    └→ 🤔 Optimizations Suggested
        ↓
[APPROVED] → Ready for Implementation
    ↓
[Implementation + Tests]
    ↓
[PR + Merge]
```

---

## 📊 TRACKING APPROVAL

En cada spec.md, agregar sección "Approval Status":

```markdown
## Approval Status

| Review | Status | Reviewer | Date | Notes |
|--------|--------|----------|------|-------|
| Architecture | ✅ Approved | John Doe | 2026-07-29 | See comments #42 |
| Security | ✅ Approved | Jane Smith | 2026-07-30 | Whitelist is good |
| Database | ⏳ In Progress | Bob Johnson | TBD | - |
| Overall | ⏳ Pending | - | - | Waiting on DB review |
```

---

## 🔄 POST-APPROVAL

### 1. Implementación
- [ ] Código sigue spec exactamente
- [ ] Tests cubren todos AC
- [ ] DB migrations ejecutadas
- [ ] settings.json actualizado

### 2. PR Review
- [ ] Spec reviewer firma PR
- [ ] Code reviewer valida vs spec

### 3. Merge & Release
- [ ] Tag: v2.0.0-spec-1-approved
- [ ] Release notes menciona specs implementadas
- [ ] Migration DB ejecutada en prod

---

## ❌ REJECTION CRITERIA

Spec puede ser REJECTED si:

1. **Breaking change undocumented** — Sin migration path claro
2. **Security concerns unresolved** — After remediation request
3. **DB scalability concern** — Sin sharding/partitioning plan
4. **Duplica spec existente** — Without clear improvement
5. **Incompleto** — Faltan secciones críticas (AC, schema, ejemplos)

**Reversal:** Si spec es rechazada, autor puede:
- Revisar y resubmitir (nuevo RFC)
- Proponer alternativa
- Escalar a steering committee

---

## 📞 GOVERNANCE

### Steering Committee
Aprueba decisiones que afecten arquitectura general:
- Breaking changes
- Cambios a MCP protocol
- Nueva arquitectura de componentes

### Architecture Review Board
Revisa todas las specs (daily/weekly)

### Security Team
Revisa specs con implicaciones de seguridad

---

## 🎯 EJEMPLOS DE RFC OUTCOMES

### ✅ APPROVED — SPEC-1
```
RFC: SPEC-1 — MCP Server filesystem-operations
Status: APPROVED (2026-07-29)
Approvers: Architecture (John Doe), Security (Jane Smith)
Implementation: Ready
Timeline: Semana 1, 1-2 horas
Notes: Excellent whitelist strategy, security team approved.
```

### ⚠️ APPROVED WITH REMEDIATION — SPEC-2
```
RFC: SPEC-2 — MCP Server audit-log-persistence
Status: APPROVED WITH REMEDIATION (2026-07-29)
Approvers: Architecture (John Doe)
Remediation: 
  - [ ] Add prompt_encryption (AES-256) for sensitive prompts
  - [ ] Document retention policy (90 days default)
Implementation: Blocked until remediation
```

### ❌ REJECTED — (hypothetical)
```
RFC: SPEC-REJECTED — MCP Server foo-bar
Status: REJECTED (2026-07-29)
Reason: Duplicates existing MCP server "audit-log". Consider extending instead.
Appeal: Author can propose as extension to SPEC-2
```

---

**RFC Process Version:** 1.0 | **Effective:** 2026-07-29
