# IMPLEMENTATION ROADMAP — Auditoria-CS-IA v2.0

**Plan de implementación ejecutable: specs → código → testing → producción**

---

## 🎯 OVERVIEW

Implementar 8 especificaciones (3 MCP servers, 2 skills, 1 integración SAST, 1 integración breach-check, 1 versioning) en 4 semanas.

**Inversión total:** ~40-50 horas | **Timeline:** 4 semanas | **Status:** Ready to Start

---

## 📅 TIMELINE RECOMENDADO

### SEMANA 1: Specs Blocking (15-18 horas)

**Lunes-Martes (4h):** RFC + Approval
- [ ] RFC review meeting (1h)
- [ ] Architecture review (1h)
- [ ] Security review (1h)
- [ ] DB schema review (1h)

**Miércoles-Viernes (10-14h):** Implementación SPEC-1 + SPEC-2 + SPEC-3

| Spec | Componente | Esfuerzo | Responsable |
|------|-----------|----------|-------------|
| 1 | MCP filesystem-ops | 2-3h | Backend Dev |
| 2 | MCP audit-log | 2-3h | Backend Dev |
| 3 | MCP webhook-audit | 2h | Backend Dev |
| Tests | Unit + Integration | 3-4h | QA |

**Entregables:**
- [ ] 3 MCP servers funcionales, registrados en settings.json
- [ ] 3 nuevas DB tables + migrations
- [ ] Tests: 20+ test cases (AC coverage)
- [ ] PR #1 merged

---

### SEMANA 2: Skills + Integration (12-15 horas)

**Lunes-Jueves (10-12h):** SPEC-5 + SPEC-6 + SPEC-7

| Spec | Componente | Esfuerzo | Responsable |
|------|-----------|----------|-------------|
| 5 | Skill evidence-verify | 2-3h | Skill Dev |
| 6 | Skill audit-baseline | 2h | Skill Dev |
| 7 | Integration Semgrep | 4-6h | Security Dev |
| Tests | Acceptance tests | 2-3h | QA |

**Viernes (2-3h):** Integration testing + bug fixes

**Entregables:**
- [ ] 2 skills funcionales en .claude/skills/
- [ ] Semgrep wrapper MCP server
- [ ] 15+ test cases
- [ ] PR #2 merged

---

### SEMANA 3: Integration + Hardening (8-10 horas)

**Lunes-Miércoles (4-5h):** SPEC-8 (breach-check service) + SPEC-4 (task-versioning)

| Spec | Componente | Esfuerzo |
|------|-----------|----------|
| 8 | Breach-check service | 3-4h |
| 4 | Task versioning MCP | 1-2h |

**Jueves-Viernes (4-5h):** System testing + docs

- [ ] E2E tests (audit flow completo con todas nuevas features)
- [ ] Performance baseline
- [ ] Security hardening (input validation, sanitization)
- [ ] Documentation updates

**Entregables:**
- [ ] 4 specs implementadas
- [ ] E2E tests passing
- [ ] PR #3 merged
- [ ] Docs/README.md actualizado

---

### SEMANA 4: Beta + Deployment Prep (5-7 horas)

**Lunes-Miércoles (3-4h):** Beta testing + refinements

- [ ] Internal testing con QA team
- [ ] Performance profiling
- [ ] Bug fixes
- [ ] Edge case handling

**Jueves-Viernes (2-3h):** Release prep

- [ ] CHANGELOG.md update
- [ ] Migration plan documentado
- [ ] Runbook para deployment
- [ ] User documentation

**Entregables:**
- [ ] v2.0.0-beta release
- [ ] Ready for production deployment
- [ ] PR #4 (final) merged

---

## 🔄 DEPENDENCIAS ENTRE SPECS

```
SPEC-1 (filesystem-ops)
    ├─→ SPEC-3 (webhook-audit): dispatch events
    ├─→ SPEC-5 (evidence-verify): validar hashes
    └─→ SPEC-7 (semgrep): usa run_command

SPEC-2 (audit-log)
    ├─→ SPEC-5 (evidence-verify): check hashes
    └─→ engine.py: integración IA analysis

SPEC-3 (webhook-audit)
    ├─→ SPEC-5 (evidence-verify): validar integridad
    └─→ standalone

SPEC-4 (task-versioning)
    └─→ scheduler.py: change logging

SPEC-5 (evidence-verify)
    ├─ SPEC-1, SPEC-2, SPEC-3: data a validar
    └─→ (skill, no bloquea otros)

SPEC-6 (audit-baseline)
    └─→ (skill, standalone)

SPEC-7 (semgrep-integration)
    └─ SPEC-1 (run_command)

SPEC-8 (breach-check)
    └─→ secrets.py: enrich findings
```

**Orden de implementación:** 1 → 2 → 3 → (5,6 paralelo) → 4 → 7 → 8

---

## 📋 CHECKLIST DE IMPLEMENTACIÓN

### SPEC-1: MCP filesystem-operations

**Phase 1: Schema & Foundation (1h)**
- [ ] Crear tabla command_executions
- [ ] Crear indexes
- [ ] Migration: scripts/migrations/20260729_001_command_executions.sql

**Phase 2: MCP Tool (1h)**
- [ ] Implementar run_command() en auditoria/mcp/tools.py
- [ ] Agregar a AUDIT_TOOLS registry
- [ ] Input validation (whitelist, args sanitization)
- [ ] Output capture (stdout, stderr, exit_code)
- [ ] Hash generation (SHA256)

**Phase 3: Integration (30m)**
- [ ] Integrar en system.py: reemplazar self._run_cmd() → MCP call
- [ ] Webhook event dispatch
- [ ] settings.json: whitelist de comandos

**Phase 4: Tests (1h)**
- [ ] Unit tests: 5 AC cases
- [ ] Integration test: system.py end-to-end
- [ ] Rollback test: migration revert

**Completion:** Todos los tests pasando, PR review-ready

---

### SPEC-2: MCP audit-log-persistence

**Phase 1: Schema (1h)**
- [ ] Crear tabla ai_analysis_logs
- [ ] ALTER table ai_analyses (add prompt_sent, execution_hash, etc.)
- [ ] Migration + rollback

**Phase 2: MCP Tool (1h)**
- [ ] log_ai_analysis(): capturar prompt/response/model
- [ ] get_ai_analysis_log(): retrieval con verificación
- [ ] Hash generation (SHA256)

**Phase 3: Engine Integration (1h)**
- [ ] engine._run_ai_analysis() → log_ai_analysis()
- [ ] Error handling
- [ ] Logging

**Phase 4: Tests (1h)**
- [ ] Unit: 5 AC cases
- [ ] Integration: engine.run() con enable_ai=true

**Completion:** AC coverage 100%, PR ready

---

### SPEC-3: MCP webhook-audit-trail

**Phase 1: Schema (1h)**
- [ ] Crear 3 tablas (webhooks_audit, webhook_delivery_events, webhook_changes)
- [ ] Indexes
- [ ] Migration

**Phase 2: MCP Tools (1h)**
- [ ] register_webhook_audited()
- [ ] log_webhook_delivery()
- [ ] get_webhook_audit_history()

**Phase 3: Integration (45m)**
- [ ] Reemplazar WebhookManager.register_webhook() → MCP tool
- [ ] Log delivery events
- [ ] Change tracking (update/delete)

**Phase 4: Tests (1h)**
- [ ] Unit: 7 AC
- [ ] Integration: webhook registration → delivery → audit trail

**Completion:** PR ready

---

### SPEC-5: Skill evidence-chain-verify

**Phase 1: Logic (1.5h)**
- [ ] Implementar verify_finding()
- [ ] Implementar verify_ai_analysis()
- [ ] Implementar verify_command()
- [ ] Implementar verify_webhook()
- [ ] Hash recalculation engine

**Phase 2: Skill Definition (30m)**
- [ ] Crear .claude/skills/evidence-verify.md
- [ ] Agregar a settings.json

**Phase 3: Tests (1h)**
- [ ] Unit: 7 AC
- [ ] Test tampering detection

**Phase 4: Report Generation (30m)**
- [ ] Generar verification_report JSON
- [ ] Console output formatting

**Completion:** Skill functional, tests passing

---

### SPEC-6: Skill audit-baseline

**Phase 1: Schema (1h)**
- [ ] Crear 2 tablas (audit_baselines, baseline_comparisons)
- [ ] Indexes
- [ ] Migration

**Phase 2: Logic (1.5h)**
- [ ] Capture baseline: snapshot findings + metadata
- [ ] Compare vs baseline: delta detection
- [ ] List baselines: query recent

**Phase 3: Skill Definition (30m)**
- [ ] Crear .claude/skills/audit-baseline.md
- [ ] settings.json

**Phase 4: Tests (1h)**
- [ ] Unit: 7 AC
- [ ] Integration: capture → compare workflow

**Completion:** Skill functional

---

### SPEC-7: Integration Semgrep (MEDIUM priority)

**Phase 1: Wrapper (2h)**
- [ ] Implementar semgrep-wrapper MCP server
- [ ] Parse Semgrep output → Auditoria Finding format
- [ ] Map severity: semgrep → Auditoria scale

**Phase 2: Integration (1h)**
- [ ] Integrar en filesystem.py
- [ ] Ejecutar Semgrep en scan_path
- [ ] Merge findings

**Phase 3: Tests (1-2h)**
- [ ] Test Semgrep wrapper
- [ ] Integration: filesystem.py + semgrep

**Completion:** Optional para v2.0, puede defer

---

### SPEC-8: Integration Breach-Check Service (MEDIUM priority)

**Phase 1: Service Wrapper (1.5h)**
- [ ] Implementar breach-check MCP server
- [ ] Integrar con HIBP API (Have I Been Pwned)
- [ ] Cache results (rate limiting)

**Phase 2: Integration (1h)**
- [ ] Integrar en secrets.py
- [ ] Enrich findings con verification status
- [ ] Mark as "verified" vs "unverified"

**Phase 3: Tests (1h)**
- [ ] Mock HIBP API
- [ ] Test verification workflow

**Completion:** Optional para v2.0, puede defer

---

## 🧪 TESTING STRATEGY

### Unit Tests
- Cada spec tiene >= 5 test cases (AC coverage)
- Pytest framework
- Fixtures para BD (SQLite in-memory)

### Integration Tests
- End-to-end workflows
- MCP tool registration + invocation
- DB persistence + query

### E2E Tests (Semana 3)
- Audit flow completo: execute_audit() → MCP tools → evidence verification
- Webhook delivery simulation
- Baseline capture + comparison

### Performance Tests
- Command execution timeout robustness
- DB query performance (1M rows scenario)
- Hash calculation overhead

### Security Tests
- Command injection prevention
- SQL injection prevention
- Privilege escalation tests

---

## 📦 DELIVERABLES POR SEMANA

### Semana 1
- [ ] 3 MCP servers implementados + tested
- [ ] 3 DB migrations (reversibles)
- [ ] PR #1 (specs 1,2,3)
- [ ] 20+ test cases passing

### Semana 2
- [ ] 2 skills implementadas
- [ ] Semgrep integration (optional)
- [ ] PR #2 (specs 4,5,6,7)
- [ ] 35+ total test cases

### Semana 3
- [ ] Breach-check integration (optional)
- [ ] E2E tests passing
- [ ] Performance baseline
- [ ] PR #3 (spec 8 + hardening)
- [ ] 50+ total test cases

### Semana 4
- [ ] v2.0.0-beta release
- [ ] User docs updated
- [ ] Migration runbook
- [ ] PR #4 (final)

---

## 🚀 DEPLOYMENT PLAN

### Pre-deployment (Jueves Semana 4)
- [ ] DB backup
- [ ] Migration test en staging
- [ ] Rollback procedure validated
- [ ] Monitoring alerts configured

### Deployment (Viernes Semana 4)
```bash
# 1. Backup
pg_dump production > backup_20260731.sql

# 2. Apply migrations (in order)
psql < migration_001_command_executions.sql
psql < migration_002_ai_analysis_logs.sql
psql < migration_003_webhook_audit.sql

# 3. Update MCP server
git checkout v2.0.0
python -m auditoria.mcp.server  # Restart

# 4. Validate
pytest tests/ -v
/quick-audit localhost --enable-ai

# 5. Monitor
watch -n 5 'select count(*) from command_executions'
```

### Post-deployment
- [ ] Monitor performance (db query times, MCP latency)
- [ ] User feedback collection
- [ ] Bug fixes (2-3 días)
- [ ] v2.0.0 stable release

---

## 💰 RESOURCE ALLOCATION

| Role | Semana 1 | Semana 2 | Semana 3 | Semana 4 | Total |
|------|----------|----------|----------|----------|-------|
| Backend Dev | 6h | 4h | 2h | 1h | 13h |
| Skill Dev | - | 5h | 2h | - | 7h |
| Security Dev | 1h | 2h | 2h | - | 5h |
| QA | 3h | 3h | 3h | 1h | 10h |
| DevOps | - | - | 1h | 2h | 3h |
| **Total** | **10h** | **14h** | **10h** | **4h** | **38h** |

---

## 🎯 SUCCESS CRITERIA

### Funcional
- ✅ Todas 8 specs implementadas y tested
- ✅ 50+ test cases (AC coverage >= 95%)
- ✅ DB migrations ejecutadas en staging
- ✅ MCP tools registrados y funcionales

### Performance
- ✅ Command execution: < 5s promedio (timeout 30s)
- ✅ DB queries: < 100ms (99th percentile)
- ✅ Hash generation: < 1ms por finding

### Quality
- ✅ Code review: 100% changes reviewed
- ✅ Security review: Zero critical issues
- ✅ Documentation: 100% coverage (specs + user guides)

### User-facing
- ✅ Skills funcionan sin errores
- ✅ Evidence verification detecta tampering
- ✅ Baseline comparison útil para drift detection
- ✅ Webhooks confiables (audit trail completo)

---

## 📞 DECISION AUTHORITY

| Decisión | Quien | Escalación |
|----------|-------|-----------|
| Spec details | Tech Lead | Architecture board |
| Implementation approach | Developer | Tech Lead |
| Performance tradeoff | DevOps | CTO |
| Security issue | Security Lead | CISO |
| Timeline delay | Project Manager | VP Engineering |

---

## 📚 REFERENCIAS

- Especificaciones: specs/[1-8]/spec.md
- Evaluación base: EVALUACION_AGENTIA.md (scratchpad)
- Settings: .claude/settings.json
- MCP registry: auditoria/mcp/server.py

---

**Versión:** 1.0 | **Última actualización:** 2026-07-29 | **Status:** Ready to Execute
