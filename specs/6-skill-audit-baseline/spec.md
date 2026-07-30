# SPEC 6: Skill — audit-baseline

**Captura y comparación de baseline de auditoría para detección de drift**

---

## 📋 VISIÓN GENERAL

### Problema
Auditorías son punto-en-tiempo, pero no hay forma de detectar cambios históricos:
- "¿Cuándo se abrió ese puerto?" (networking drift)
- "¿Cuándo expiró ese certificado?" (SSL drift)
- "¿Se degradó la postura de seguridad?" (trending)
- Falta: benchmark histórico para comparación

### Solución
Skill que:
1. Captura baseline (snapshot de audit completo + findings)
2. Almacena con identificación (target, timestamp, módulos)
3. Compara auditoría actual vs baseline
4. Genera drift_report (qué cambió, severidad del cambio)
5. Calcula delta de risk_score (0-100 vs baseline)

---

## 🎯 INTERFAZ

### Skill: `/audit-baseline`

**Invocación:**
```bash
# Capturar baseline
/audit-baseline <target> --capture [--modules MODULE1 MODULE2]

# Comparar vs baseline
/audit-baseline <target> --compare [--baseline-id ID] [--days 30]

# Listar baselines disponibles
/audit-baseline <target> --list
```

**Ejemplos:**
```bash
# Capturar baseline inicial
/audit-baseline example.com --capture --modules system network ssl

# Ejecutar audit y comparar vs baseline más reciente
/audit-baseline example.com --compare

# Listar últimos 5 baselines
/audit-baseline example.com --list --limit 5
```

**Entrada (JSON):**
```json
{
  "target": "example.com",
  "operation": "capture",  // capture, compare, list
  "modules": ["system", "network", "ssl"],
  "baseline_id": null,  // null = usar más reciente
  "days": 30
}
```

**Salida (capture):**
```json
{
  "baseline_id": 1001,
  "target": "example.com",
  "captured_at": "2026-07-29T15:00:00Z",
  "findings_count": 12,
  "risk_score": 67.5,
  "modules": ["system", "network", "ssl"],
  "findings_snapshot": [
    {
      "finding_id": 123,
      "check_id": "SSL-002",
      "title": "Certificate Expiring Soon",
      "severity": "high",
      "status": "warn",
      "evidence": {"expiry_days": 15}
    }
  ],
  "metadata": {
    "created_by": "claude/skill",
    "reason": "Trimestral baseline capture"
  }
}
```

**Salida (compare):**
```json
{
  "comparison_report": {
    "audit_id_current": 457,
    "baseline_id": 1001,
    "target": "example.com",
    "compared_at": "2026-07-29T16:00:00Z",
    
    "risk_score_baseline": 67.5,
    "risk_score_current": 72.1,
    "risk_score_delta": 4.6,  // Deterioro
    "risk_trend": "degraded",  // improved, stable, degraded
    
    "findings_baseline": 12,
    "findings_current": 14,
    "findings_delta": 2,  // Nuevos hallazgos
    
    "changes": {
      "new_findings": [
        {
          "finding_id": 234,
          "title": "New Port Open: 3389 (RDP)",
          "severity": "high"
        }
      ],
      "resolved_findings": [
        {
          "finding_id": 111,
          "title": "Old Issue: Weak Cipher"
        }
      ],
      "severity_changes": [
        {
          "finding_id": 123,
          "title": "Certificate Expiring Soon",
          "old_severity": "high",
          "new_severity": "critical",
          "reason": "Days to expiry reduced from 15 to 2"
        }
      ]
    },
    
    "summary": {
      "status": "degraded",
      "key_alerts": [
        "New critical issue: 1",
        "Risk score deteriorated: +4.6 points",
        "New unresolved findings: 2"
      ]
    }
  }
}
```

---

## 💾 SCHEMA BASE DE DATOS

**Nueva tabla:** `audit_baselines`

```sql
CREATE TABLE IF NOT EXISTS audit_baselines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    audit_id INTEGER NOT NULL,
    target TEXT NOT NULL,
    baseline_name TEXT,
    
    captured_at TIMESTAMP NOT NULL,
    created_by TEXT,  -- User/skill name
    capture_reason TEXT,  -- Manual, scheduled, etc.
    
    findings_count INTEGER,
    risk_score REAL,
    modules TEXT,  -- JSON array
    
    findings_snapshot TEXT,  -- JSON: serialized findings
    metadata TEXT,  -- JSON: additional metadata
    
    FOREIGN KEY (audit_id) REFERENCES audits(id),
    UNIQUE (target, captured_at)
);

CREATE INDEX IF NOT EXISTS idx_audit_baselines_target ON audit_baselines(target);
CREATE INDEX IF NOT EXISTS idx_audit_baselines_captured_at ON audit_baselines(captured_at DESC);
```

**Nueva tabla:** `baseline_comparisons`

```sql
CREATE TABLE IF NOT EXISTS baseline_comparisons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    audit_id_current INTEGER NOT NULL,
    baseline_id INTEGER NOT NULL,
    target TEXT NOT NULL,
    
    compared_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    compared_by TEXT,
    
    risk_score_baseline REAL,
    risk_score_current REAL,
    risk_score_delta REAL,
    risk_trend TEXT,  -- improved, stable, degraded
    
    findings_baseline INTEGER,
    findings_current INTEGER,
    findings_delta INTEGER,
    
    changes_summary TEXT,  -- JSON: new, resolved, severity_changes
    
    FOREIGN KEY (audit_id_current) REFERENCES audits(id),
    FOREIGN KEY (baseline_id) REFERENCES audit_baselines(id)
);

CREATE INDEX IF NOT EXISTS idx_baseline_comparisons_target ON baseline_comparisons(target);
```

---

## 📝 EJEMPLOS

### Ejemplo 1: Capturar baseline

**CLI:**
```bash
/audit-baseline example.com --capture --modules network ssl
```

**Salida:**
```
✅ BASELINE CAPTURED
   Baseline ID: 1001
   Target: example.com
   Modules: network, ssl
   
   Summary:
   - Findings: 5
   - Risk Score: 45.3
   - Certificate expires in: 87 days
   - Open ports: 22 (SSH), 80 (HTTP), 443 (HTTPS)
   
   Baseline saved. Use --compare to detect drift.
```

### Ejemplo 2: Comparar vs baseline (sin drift)

**CLI:**
```bash
/audit-baseline example.com --compare --baseline-id 1001
```

**Salida (stable):**
```
📊 BASELINE COMPARISON REPORT
   Current Audit: 457
   Baseline: 1001 (captured 2026-07-15)
   Target: example.com
   
   STATUS: ✅ STABLE
   
   Risk Score:
   - Baseline: 45.3
   - Current:  44.8
   - Delta:    -0.5 (IMPROVED)
   
   Findings:
   - Baseline: 5 findings
   - Current:  4 findings
   - Delta:    -1 (RESOLVED)
   
   Changes:
   - New findings:      0
   - Resolved:          1 (Old: "Weak SSH Cipher")
   - Severity changes:  0
   
   Recommendation: No action needed. Security posture stable.
```

### Ejemplo 3: Comparar vs baseline (con drift/deterioro)

**CLI:**
```bash
/audit-baseline example.com --compare
```

**Salida (degraded):**
```
📊 BASELINE COMPARISON REPORT
   Current Audit: 458
   Baseline: 1001 (captured 2026-07-15)
   Target: example.com
   
   STATUS: ⚠️  DEGRADED
   
   Risk Score:
   - Baseline: 45.3
   - Current:  68.9
   - Delta:    +23.6 (⚠️  SIGNIFICANT DETERIORATION)
   
   Findings:
   - Baseline: 5 findings
   - Current:  9 findings
   - Delta:    +4 (NEW ISSUES)
   
   🚨 New Critical Issues:
   1. Finding #456: "RDP Port 3389 Open" [CRITICAL]
      - Detected: 2026-07-29 16:05:00
      - Severity: CRITICAL
      - Action: Investigate immediately
   
   2. Finding #457: "SSL Certificate Expired" [CRITICAL]
      - Expired: 2026-07-20
      - Impact: HTTPS unavailable
      - Action: Renew certificate immediately
   
   📍 Severity Changes:
   - Finding #123 "Weak Cipher": HIGH → CRITICAL
     Reason: Certificate expiration now affects availability
   
   ✅ Resolved Issues:
   - Finding #111 "UDP DNS Port": RESOLVED
   
   Recommendations:
   1. [URGENT] Renew SSL certificate
   2. [URGENT] Close RDP port or restrict access
   3. Investigate what changed since baseline
   4. Update firewall rules to match baseline configuration
```

---

## ✅ ACCEPTANCE CRITERIA

### AC1: Captura de baseline exitosa
**Given** audit completado sin errores
**When** `/audit-baseline example.com --capture`
**Then**
- ✅ Registro creado en audit_baselines
- ✅ baseline_id retornado
- ✅ findings_snapshot contiene array de todos los findings
- ✅ risk_score capturado
- ✅ captured_at es timestamp ISO 8601

### AC2: Comparación sin drift
**Given** audit idéntico a baseline
**When** `/audit-baseline example.com --compare`
**Then**
- ✅ risk_score_delta ≈ 0 (±1.0)
- ✅ risk_trend = "stable"
- ✅ findings_delta = 0
- ✅ changes.new_findings = [] vacío

### AC3: Detección de nuevo finding
**Given** baseline con 5 findings, audit actual con 6
**When** Comparar
**Then**
- ✅ findings_delta = 1
- ✅ new_findings array contiene finding nuevo
- ✅ new_finding incluye: title, severity, check_id
- ✅ risk_score_delta > 0 (deterioro)

### AC4: Detección de resolved finding
**Given** baseline con finding X, audit actual sin finding X
**When** Comparar
**Then**
- ✅ resolved_findings contiene X
- ✅ findings_delta = -1
- ✅ risk_score_delta < 0 (mejora)

### AC5: Detección de severity change
**Given** finding que cambió de HIGH a CRITICAL
**When** Comparar
**Then**
- ✅ severity_changes array contiene cambio
- ✅ Incluye: old_severity, new_severity, reason
- ✅ risk_score_delta > 0

### AC6: Listar baselines disponibles
**Given** múltiples baselines para target
**When** `/audit-baseline example.com --list`
**Then**
- ✅ Retorna array de baselines ordenados DESC por captured_at
- ✅ Cada entry: baseline_id, captured_at, findings_count, risk_score
- ✅ Puedo identificar cuál usar con --baseline-id

### AC7: Filtrar por rango de días
**Given** 10 baselines desde hace 60 días
**When** `/audit-baseline example.com --list --days 30`
**Then**
- ✅ Solo retorna baselines de últimos 30 días
- ✅ Baselines más antiguas filtradas

---

## ⚠️ ERROR HANDLING

| Error | Caso |
|-------|------|
| `no_baselines_found` | Cuando --compare pero no hay baseline previo |
| `audit_not_found` | audit_id inválido |
| `baseline_not_found` | baseline_id no existe |
| `same_audit_as_baseline` | Intentar comparar audit vs sí mismo |

---

## 📦 INTEGRACIÓN

**Upstream (usa):**
- ← auditoria/core/engine.AuditEngine
- ← auditoria/storage/database.DatabaseManager

**Downstream (usado por):**
- → compliance automation: alertas de drift
- → trend reporting: detección de patrones

---

## 🚀 IMPLEMENTACIÓN

**Ubicación:** `.claude/skills/audit-baseline.md`

**Lógica:** `auditoria/skills/audit_baseline.py`

**Tests:** `tests/spec_6_acceptance.py`

---

**Versión:** 1.0 | **Estado:** Draft — Ready for implementation
