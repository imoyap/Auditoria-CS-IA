# GETTING STARTED — Specs Auditoria-CS-IA v2.0

**Guía rápida para entender y usar estas especificaciones**

---

## 🎯 ¿QUÉ ES ESTO?

Un conjunto de **8 especificaciones técnicas** que definen cómo mejorar Auditoria-CS-IA para cerrar brechas de verificabilidad y agregar capacidades MCP + Skills.

**No es código.** Es diseño: interfaces, schemas, ejemplos, acceptance criteria, antes de implementar.

---

## 📋 LOS 8 SPECS (en orden de implementación)

### 🔴 BLOCKING (Semana 1)

1. **SPEC-1: MCP filesystem-operations** — Audit trail para comandos del SO
   - Resuelve: Cadena de custodia (brecha #1)
   - Esfuerzo: 2-3h
   - Leer: `1-mcp-filesystem-ops/spec.md`

2. **SPEC-2: MCP audit-log-persistence** — Trazabilidad de prompts IA
   - Resuelve: Reproducibilidad análisis IA (brecha #3)
   - Esfuerzo: 2-3h
   - Leer: `2-mcp-audit-log/spec.md`

3. **SPEC-3: MCP webhook-audit-trail** — Audit de webhooks + delivery
   - Resuelve: Compliance accountability (brecha #4)
   - Esfuerzo: 2h
   - Leer: `3-mcp-webhook-audit/spec.md`

### 🟡 MEDIUM PRIORITY (Semana 2-3)

5. **SPEC-5: Skill evidence-verify** — Detecta tampering en findings
   - Resuelve: Integridad de evidence chain
   - Esfuerzo: 2-3h
   - Leer: `5-skill-evidence-verify/spec.md`

6. **SPEC-6: Skill audit-baseline** — Drift detection vs baseline histórico
   - Resuelve: Trending y comparación histórica
   - Esfuerzo: 2h
   - Leer: `6-skill-audit-baseline/spec.md`

4. **SPEC-4: MCP task-versioning** — Change log para scheduled tasks
   - Resuelve: Auditable task management
   - Esfuerzo: 2-3h
   - Leer: `4-mcp-task-versioning/spec.md`

### 🟢 OPCIONAL (Semana 3+)

7. **SPEC-7: Integration Semgrep** — SAST integration
   - Resuelve: Análisis profundo filesystem
   - Esfuerzo: 4-6h
   - Puede postergar

8. **SPEC-8: Integration Breach-Check** — Verificación de secrets
   - Resuelve: Validar si credenciales están en breach DB
   - Esfuerzo: 3-4h
   - Puede postergar

---

## 🚀 CÓMO USAR ESTAS SPECS

### Para Arquitecto/Lead
```bash
# 1. Entender el problema
cat ../EVALUACION_AGENTIA.md | grep "Brecha"

# 2. Revisar specs (5 min cada una)
cat 0-INDEX.md                    # Visión general
cat 1-mcp-filesystem-ops/spec.md  # SPEC-1
# ... etc

# 3. Revisar roadmap
cat IMPLEMENTATION_ROADMAP.md     # Semanas, esfuerzo, checklist

# 4. Aprobar o pedir cambios
# → Feedback en RFC.md
```

### Para Desarrollador (Backend)
```bash
# 1. Leer spec completo (30 min)
cat 1-mcp-filesystem-ops/spec.md

# 2. Implementar según checklist
# - Crear tabla command_executions
# - Implementar run_command() MCP tool
# - Tests >= 5 AC cases
# Ver IMPLEMENTATION_ROADMAP.md > SPEC-1 checklist

# 3. Validar acceptance criteria
pytest tests/spec_1_acceptance.py -v

# 4. PR review vs spec
# Revisor verifica: ¿código sigue spec exactamente?
```

### Para QA/Tester
```bash
# 1. Leer Acceptance Criteria (AC)
cat 1-mcp-filesystem-ops/spec.md | grep "AC"

# 2. Escribir tests
pytest tests/spec_1_acceptance.py::test_ac1_execution_success

# 3. Test todos los AC + error cases
pytest tests/spec_1_acceptance.py -v --tb=short
```

### Para Product/Auditor
```bash
# 1. Leer "Visión General" de cada spec
# 2. Leer ejemplos (JSON request/response)
# 3. Verificar que Acceptance Criteria son verificables
# → Si no entiendes un AC, escalate a Arquitecto
```

---

## 📊 ESTRUCTURA DE ARCHIVOS

```
specs/
├── 0-INDEX.md                                     ← START HERE
├── GETTING_STARTED.md                            ← Este archivo
├── RFC.md                                        ← Proceso de review
├── IMPLEMENTATION_ROADMAP.md                     ← Timeline + checklist
│
├── 1-mcp-filesystem-ops/
│   ├── spec.md                                   ← Especificación
│   ├── schema.sql                                ← SQL DDL (en spec.md)
│   └── examples/
│       ├── firewall_check.json
│       └── ...
│
├── 2-mcp-audit-log/
│   ├── spec.md
│   └── examples/
│
├── 3-mcp-webhook-audit/
│   ├── spec.md
│   └── examples/
│
├── 4-mcp-task-versioning/
│   └── spec.md
│
├── 5-skill-evidence-verify/
│   └── spec.md
│
├── 6-skill-audit-baseline/
│   └── spec.md
│
├── 7-integration-semgrep/
│   └── spec.md
│
├── 8-integration-breach-check/
│   └── spec.md
│
└── _templates/
    ├── spec_template.md                         ← Para nuevos specs
    └── acceptance_criteria_template.md
```

---

## ✅ WORKFLOW TÍPICO

### Día 1: Arquitecto revisa
```bash
# Lee INDEX + 3 specs BLOCKING
cat 0-INDEX.md
for i in 1 2 3; do
  echo "=== SPEC-$i ==="
  cat $i-*/spec.md | head -100
done

# Aprueba o pide cambios en RFC.md
```

### Día 2-5: Developers implementan
```bash
# Backend Dev 1: SPEC-1
cd ../auditoria
# Crear tabla command_executions
# Implementar run_command() MCP tool
# Tests

# Backend Dev 2: SPEC-2
# Crear tabla ai_analysis_logs
# Implementar log_ai_analysis() MCP tool
# Tests

# Backend Dev 3: SPEC-3
# Crear webhooks_audit, webhook_delivery_events
# Implementar MCP tools
# Tests
```

### Día 6-10: Skills + Integration
```bash
# Skill Dev 1: SPEC-5
# Implementar evidence-verify skill

# Skill Dev 2: SPEC-6
# Implementar audit-baseline skill

# Security Dev: SPEC-7
# Implementar Semgrep wrapper
```

### Día 11-20: Testing + Hardening
```bash
# QA: E2E tests
# Security: Hardening
# DevOps: Migration planning
```

### Día 21: Deployment
```bash
# Apply migrations
# Deploy code
# Validate
# Monitor
```

---

## 🎯 CHECKPOINTS DE APROBACIÓN

### ✅ Spec está READY cuando:
- [ ] Especificación completa (todas secciones)
- [ ] 2+ ejemplos funcionales
- [ ] >= 5 Acceptance Criteria
- [ ] Schema SQL definido (si aplica)
- [ ] Dependencias mapeadas
- [ ] Decision Log incluido (por qué se diseñó así)

### ✅ Implementación está READY cuando:
- [ ] Código sigue spec exactamente
- [ ] 100% de AC tests pasando
- [ ] DB migrations probadas (forward + rollback)
- [ ] Code review aprobado
- [ ] Security review aprobado (si aplica)

### ✅ Listo para producción cuando:
- [ ] E2E tests pasando
- [ ] Performance baseline OK
- [ ] User docs actualizado
- [ ] Runbook de deployment listo
- [ ] Rollback plan documentado

---

## 🆘 PREGUNTAS FRECUENTES

**P: ¿Tengo que implementar TODO?**
A: No. Specs 1-6 son prioritarios (4 semanas). Specs 7-8 son opcionales.

**P: ¿Qué pasa si encuentro un problema en la spec?**
A: Abre issue en GitHub/specs, marca como [SPEC-X]. Arquitecto responde.

**P: ¿Puedo cambiar el implementation sin cambiar spec?**
A: Solo si AC sigue pasando. Si cambias interfaz MCP/DB, necesitas cambiar spec.

**P: ¿Cómo sé si una spec es "buena"?**
A: Si puedes implementar exactamente siguiendo ella sin preguntar, es buena.

**P: ¿Debo leer todos los specs antes de empezar?**
A: No. Lee el que vas a implementar + sus dependencias.

---

## 📚 REFERENCIAS RÁPIDAS

| Archivo | Para qué | Tiempo |
|---------|----------|--------|
| 0-INDEX.md | Visión general de todos specs | 5 min |
| [N]-*/spec.md | Implementar SPEC-N | 30 min |
| IMPLEMENTATION_ROADMAP.md | Timeline + checklist | 10 min |
| RFC.md | Cómo se revisan specs | 15 min |
| EVALUATION_AGENTIA.md | Por qué existen estas brechas | 20 min |

---

## 🚀 PRÓXIMO PASO

1. Si eres **Arquitecto:** Lee 0-INDEX.md + RFC.md, aprueba specs
2. Si eres **Developer:** Lee IMPLEMENTATION_ROADMAP.md, elige spec, lee spec.md completo
3. Si eres **QA:** Lee Acceptance Criteria en cada spec, escribe tests
4. Si eres **Product:** Lee visión general + ejemplos, valida que resuelve problemas

---

**¿Listo? Abre 0-INDEX.md y empeza.**

---

Versión: 1.0 | Última actualización: 2026-07-29
