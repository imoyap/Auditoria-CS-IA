# Auditoria-CS-IA

## Pipeline de auditoría agéntica — Unidad 3 (Diplomado en Ciberseguridad)

📄 **[Ver el informe final de la auditoría (HTML)](https://mcarreral.github.io/Auditoria-CS-IA/reporte/reporte_final.html)** — reporte completo con los 4 hallazgos reales, controles ISO/NIST/CIS y advertencia legal, publicado con GitHub Pages.

🎥 **[Ver el video de la Actividad de Cierre](https://1drv.ms/v/c/abc93e6c38f5fac8/IQDdZAsU8epKQrE3wCag65zFAeSjwllu6j_XBEnnN9O52BY?e=RtbSZF)** — grabación con la presentación del equipo, arquitectura del pipeline, ejecución real y punto de control humano (T-043).

Este repositorio contiene, además del framework genérico descrito más abajo, el pipeline de auditoría agéntica de 5 roles construido para la Actividad de Cierre de la Unidad 3 (`docs/anexo_tecnico_u3.md`, `docs/rubrica_evaluacion_u3.md`). El detalle completo de diseño, requisitos y decisiones vive en `docs/`:

- `docs/GAP_ANALYSIS.md` (Fase 0) — inventario contra el Anexo Técnico.
- `docs/requirements.md` (Fase 1) — 40 REQ trazados a criterios de rúbrica.
- `docs/design.md` (Fase 2) — arquitectura de roles, skills, harness, MCP y controles CT-01–07.
- `docs/tasks.md` (Fase 3/4) — plan de tareas y su estado real de ejecución.
- `docs/PROPUESTA_RC_D_VIDEO.md` — reglas de compromiso RC-1–6, dimensiones de extensión D1–D8, estructura del video (definición propia del grupo, aprobada en `LEDGER.md` `LDG-004`).
- `LEDGER.md` — bitácora append-only de todas las decisiones, gates y rechazos, desde la Fase 0.

### Workflow de auditoría declarado (10 etapas)

No es solo una cadena de herramientas: es el proceso de auditoría del Anexo Técnico U3 §2, justificado contra referencias reconocidas de proceso (ISO 19011:2018, ISO/IEC 27007, ISACA ITAF) y de técnica (NIST SP 800-115, OSSTMM 3, PTES, OWASP WSTG) — Anexo §1.

| # | Etapa | Actor | Gate | Firma humana |
|---|---|---|---|---|
| 0 | Encargo y autorización | Humano | G0 | **Obligatoria** |
| 1 | Definición del criterio de auditoría | Humano + COMPLIANCE | G0 | **Obligatoria** |
| 2 | Planificación | SPEC / Humano | — | — |
| 3 | Recolección de evidencia | RECON | G1 | — |
| 4 | Normalización e inventario | Determinista (sin LLM) | G2 | — |
| 5 | Análisis y verificación | ANALISTA → VERIFICADOR | G3 | **Obligatoria** |
| 6 | Evaluación de riesgo | ANALISTA + Humano | G3 | **Obligatoria** |
| 7 | Correlación normativa | COMPLIANCE | G4 | — |
| 8 | Reporte | REDACTOR | G5 | **Obligatoria** |
| 9 | Comunicación, remediación y seguimiento | Humano | — | — |

Justificación de las etapas contra las referencias del Anexo §1:
- **Etapas 0–2** (encargo, criterio, planificación) responden a ISO 19011:2018 (gestión de un programa de auditoría) y a la fase de pre-engagement de PTES/NIST SP 800-115 — nada se ejecuta sin alcance y criterio declarados por escrito.
- **Etapa 3** (recolección) sigue la disciplina de captura de evidencia de NIST SP 800-115 y OSSTMM 3 (hash + timestamp de cada artefacto, `scope/allowlist.txt` como límite operativo).
- **Etapa 4** (normalización) es la capa 2 de la arquitectura (`docs/design.md`) — parsers deterministas, nunca el LLM leyendo salida cruda.
- **Etapas 5–6** (análisis, verificación, riesgo) separan estructuralmente propuesta (ANALISTA) de confirmación (VERIFICADOR), con la matriz impacto×probabilidad de ISO 31000/ISO 27005/NIST SP 800-30 citada en el Anexo §14.
- **Etapa 7** (correlación) usa ISO/IEC 27001:2022 Anexo A, NIST CSF 2.0 y CIS v8 (Anexo §14) vía `mcp/conocimiento_normativo`.
- **Etapa 8** (reporte) sigue el template canónico del Anexo Parte V, generado por la skill `redactar`.
- **Etapa 9** (seguimiento) es responsabilidad humana, fuera del alcance de este repositorio hasta el retest.

**Criterio de auditoría** (Etapa 1, declarado por escrito antes de cualquier hallazgo real): ISO/IEC 27001:2022 Anexo A + NIST CSF 2.0 + normativa chilena aplicable (Leyes 21.663, 21.719, 21.459) — ver `scope/alcance.yaml` campo `criterio_de_auditoria`, declarado en la Fase de implementación T-002 (`LEDGER.md` `LDG-006`, commit `298020b`), antes de cualquier entrada de hallazgo real sobre el objetivo (que solo puede ocurrir desde la etapa 3 en adelante, con G0 ya firmado).

**Coincidencia workflow declarado ↔ ejecutado:** verificable en cualquier momento recorriendo `LEDGER.md` cronológicamente — cada entrada cita la tarea (`T-XXX`) y el `REQ-XXX` que avanza, en el mismo orden de bloques que `docs/tasks.md` declara.

**Verificación real al cierre (T-039, `LEDGER.md` `LDG-066`):** con el workflow completo (los 3 gates de firma humana obligatoria — G0, G3, G5 — cerrados), se recorrió `LEDGER.md` cronológicamente y se comparó contra la tabla de 10 etapas de arriba:

| Timestamp real | Hito | Etapa declarada |
|---|---|---|
| 00:58:02 | G0 firmado | 0–1 |
| 08:28:55 | RECON captura evidencia real (T-013) | 3 |
| 08:34:06 | G1 cerrado | 3 (gate) |
| 08:36:09 | G2 cerrado (normalización determinista) | 4 |
| 08:44:50 | ANALISTA propone candidatos (T-021) | 5 |
| 08:59:17 | VERIFICADOR confirma/veta (T-024/025) | 5 |
| 09:04:41 | Gap real de vector CVSS corregido (T-024b) | 6 |
| 09:08:25 | G3 firmado | 5–6 (gate) |
| 09:22:53 | COMPLIANCE correlaciona (T-027) | 7 |
| 09:24:08 | G4 cerrado | 7 (gate) |
| 09:38:26 | REDACTOR genera el informe (T-034) | 8 |
| 09:39:55 | CT-01/CT-07 verificados sobre el informe final (T-035) | 8 |
| 09:42:44 | G5 firmado | 8 (gate) |

Orden monótono sin excepción: ninguna etapa se ejecutó antes de que la etapa o gate anterior cerrara; ningún hallazgo real (`H-01`..`H-04`) aparece antes de G1 (captura de evidencia); ningún gate se firmó antes del trabajo real de su etapa. El único salto de tiempo real (G0 a las 00:58 frente a T-013 a las 08:28, ~7,5 h) no es una desviación de etapa: corresponde a dos cambios de ventana de trabajo ya registrados como entradas `SUPERSEDE` explícitas (`LDG-043`, `LDG-046`), nunca una edición silenciosa del alcance.

> **Nota de nomenclatura:** las entradas tipo `HALLAZGO` que aparecen en `LEDGER.md` durante la Fase 4 (`LDG-007`, `LDG-014`, `LDG-017`, etc.) son hallazgos de **construcción del propio pipeline** (bugs encontrados y corregidos al probar cada script), no hallazgos de auditoría sobre `192.168.56.117` — esos, siguiendo el workflow declarado arriba, solo pueden empezar a existir desde la etapa 3 en adelante, con G0 ya firmado y dentro de la ventana de trabajo real (`scope/alcance.yaml`).

---

## 🚀 Características

### Core
- **Auditoría Autónoma** — Ejecución programada sin intervención manual
- **IA Integrada** — Análisis inteligente con Claude API
- **Arquitectura Extensible** — Añade nuevos módulos heredando de `BaseCheck`
- **5 módulos integrados** — sistema, red, SSL/TLS, filesystem y secretos

### API & Integración
- **REST API** — 18 endpoints para control y webhooks
- **MCP Server** — 9 herramientas para integración con Claude
- **Claude Code Skills** — Integración nativa con herramientas de Claude

### Almacenamiento & Reportes
- **SQLite Persistencia** — Histórico completo de auditorías
- **Reportes Multi-formato** — JSON, HTML, Markdown y consola (Rich)
- **Puntuación de Riesgo** — Calculada por severidad de hallazgos
- **Trazabilidad Completa** — Cada hallazgo con timestamp y metadata

### DevOps
- **Docker & Compose** — Stack local con PostgreSQL, Prometheus, Grafana
- **Kubernetes Ready** — Manifests para producción
- **Monitoreo** — Integración con Prometheus + Grafana
- **CI/CD** — GitHub Actions scaffolding

## 📦 Stack Técnico

- **Python 3.10+** — Flask, APScheduler, SQLAlchemy
- **Claude API** — Análisis inteligente y procesamiento de hallazgos
- **Base de Datos** — SQLite (dev) / PostgreSQL (prod)
- **Contenedores** — Docker & Kubernetes
- **Monitoreo** — Prometheus + Grafana
- **CI/CD** — GitHub Actions

## ⚡ Inicio Rápido

```bash
# Clonar
git clone https://github.com/cherrera0001/Auditoria-CS-IA.git
cd Auditoria-CS-IA

# Instalar
make install

# Ejecutar
docker-compose up -d

# Ver documentación
cat docs/README.md
```

## 📚 Documentación

```
docs/
├── guides/              → Guías de usuario
├── architecture/        → Diseño técnico
├── operations/          → Deployment y monitoreo
├── development/         → Setup para desarrolladores
├── advanced/            → Temas avanzados
└── reference/           → Especificaciones y FAQs
```

Documentación completa en `docs/README.md`

## 💻 Uso

### CLI
```bash
# Auditoría completa
auditoria audit

# Auditar dominio
auditoria audit --target example.com --modules network ssl

# Buscar secretos
auditoria audit --scan-path ./proyecto --modules secrets

# Exportar informes
auditoria audit --output-json report.json --output-html report.html
```

### REST API
```bash
# Iniciar servidor
python scripts/run_api.py --port 5000

# Ejecutar auditoría
curl -X POST http://localhost:5000/api/audit \
  -H "Content-Type: application/json" \
  -d '{"modules": ["system", "network"]}'
```

### MCP Integration
```python
from auditoria.mcp.server import MCPAuditServer

server = MCPAuditServer()
await server.start()
```

## 🧩 Módulos de Auditoría

| Módulo       | Categoría | Descripción |
|-------------|-----------|------------|
| `system`    | sistema   | Firewall, antivirus, privilegios, SO |
| `network`   | red       | DNS, puertos, conectividad |
| `ssl`       | cifrado   | Certificados, TLS, expiración |
| `filesystem`| archivos  | Permisos inseguros, archivos sensibles |
| `secrets`   | secretos  | Credenciales en código, tokens |

## 🔧 Crear Módulo Personalizado

```python
from auditoria.checks.base import BaseCheck
from auditoria.checks.registry import register_check
from auditoria.core.models import Finding, Severity

@register_check
class MiCheck(BaseCheck):
    name = "mi-check"
    category = "custom"
    description = "Mi verificación"

    def run(self) -> list[Finding]:
        return [Finding(...)]
```

Registra en `auditoria/checks/__init__.py`

## Módulos de auditoría

| Módulo       | Categoría | Descripción                                      |
|-------------|-----------|--------------------------------------------------|
| `system`    | sistema   | Firewall, antivirus, privilegios, info del SO    |
| `network`   | red       | DNS, escaneo de puertos comunes                  |
| `ssl`       | cifrado   | Certificados, expiración, protocolos TLS         |
| `filesystem`| archivos  | Archivos sensibles con permisos inseguros        |
| `secrets`   | secretos  | Detección de credenciales en código fuente       |

## Crear un módulo personalizado

```python
from auditoria.checks.base import BaseCheck
from auditoria.checks.registry import register_check
from auditoria.core.models import Finding, Severity, Status

@register_check
class MiCheck(BaseCheck):
    name = "mi-check"
    category = "custom"
    description = "Mi verificación personalizada"

    def run(self) -> list[Finding]:
        return [
            Finding(
                check_id="CUSTOM-001",
                title="Ejemplo",
                description="Descripción del hallazgo",
                severity=Severity.MEDIUM,
                status=Status.WARN,
                recommendation="Acción recomendada",
            )
        ]
```

Importa el módulo en `auditoria/checks/__init__.py` para registrarlo.

## Estructura del proyecto

```
Auditoria-CS-IA/
├── auditoria/
│   ├── cli.py              # Interfaz de línea de comandos
│   ├── core/
│   │   ├── engine.py       # Motor de ejecución
│   │   ├── models.py       # Modelos de datos
│   │   └── reporter.py     # Generadores de informes
│   ├── checks/
│   │   ├── base.py         # Clase base BaseCheck
│   │   ├── registry.py     # Registro de módulos
│   │   ├── system.py
│   │   ├── network.py
│   │   ├── ssl_tls.py
│   │   ├── filesystem.py
│   │   └── secrets.py
│   └── templates/
│       └── report.html
├── tests/
├── pyproject.toml
└── requirements.txt
```

## Códigos de salida

| Código | Significado                          |
|--------|--------------------------------------|
| 0      | Sin hallazgos críticos ni altos      |
| 1      | Hallazgos de severidad alta          |
| 2      | Hallazgos de severidad crítica       |

## Tests

```bash
pip install -e ".[dev]"
pytest
```

## Licencia

MIT
