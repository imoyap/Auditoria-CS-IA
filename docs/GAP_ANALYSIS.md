# GAP_ANALYSIS.md — Auditoria-CS-IA vs. Anexo Técnico U3 / Rúbrica U3

**Fecha:** 2026-08-03
**Fuente de verdad:** `docs/anexo_tecnico_u3.md` (v1.0) y `docs/rubrica_evaluacion_u3.md` (v1.0)
**Método:** inspección directa del repositorio (lectura de archivos, `find` sobre rutas esperadas). Sin ejecución de pipeline, sin generación de evidencia.
**Alcance de este documento:** solo diagnóstico (Fase 0). No contiene propuestas de solución.

---

## 0. Hallazgo de encuadre (léase antes que las tablas)

El repositorio actual (`Auditoria-CS-IA`) es un **framework de auditoría continua de cumplimiento genérico**, escrito en Python: un CLI (`auditoria/cli.py`), un motor de checks deterministas (`system`, `network`, `ssl`, `filesystem`, `secrets`), una API REST (Flask), un servidor MCP que expone *herramientas de ejecución* (`execute_audit`, `get_audit_history`, etc.), persistencia SQLite, scheduler y webhooks. Es un proyecto real, con specs propias (`specs/`), gates de calidad de software propios (`quality/gates-final.yaml`) y una política de uso de IA propia (`specs/ai-policy.yaml`).

Ese proyecto **no es una instancia de la arquitectura exigida por el Anexo Técnico U3**. No comparte target (`192.168.56.101`), no comparte el modelo de 5 roles con separación estructural, no comparte el concepto de gate con firma humana (sus "gates" G0–G10 son gates de calidad de *este* software, no del *proceso de auditoría*), y no tiene ninguno de los artefactos de gobernanza exigidos (ledger, scope firmado, allowlist, evidencias crudas con hash, JSON normalizado, matriz de correlación normativa).

Esto no es una crítica al proyecto existente — es simplemente una constatación: **la brecha no es de "completar algunos módulos", es de construir, dentro del mismo repositorio, un sistema distinto que cumpla el encargo de U3**, decidiendo explícitamente qué partes del código/infra existente se reutilizan (p. ej. el patrón de checks deterministas, SQLite, Jinja2 para reportes) y qué se construye desde cero (roles, harness, gates, ledger, MCP de conocimiento, correlación normativa).

Ninguna condición de reprobación automática está activada hoy: no se ha ejecutado nada contra ningún IP, no hay hallazgos fabricados, no hay ledger reconstruido — porque **nada de eso existe todavía**.

### 0.1 Corrección de alcance — IP objetivo real (LDG-002)

La primera versión de este documento señalaba que `192.168.56.101` no aparece en ningún archivo del repositorio y lo trataba como una brecha de alcance. Esa lectura queda corregida: **`192.168.56.101` es el IP de ejemplo de la plantilla del Anexo Técnico U3** (aparece en el diagrama de arquitectura, en la tabla de reprobación automática y en la banda 0 del criterio A de la rúbrica como ilustración del formato exigido, no como el IP asignado a este grupo). `docs/anexo_tecnico_u3.md` y `docs/rubrica_evaluacion_u3.md` no se editan — son transcripción fiel de los documentos oficiales del curso.

**El IP objetivo real y autorizado de este grupo es `192.168.56.117`** (decisión registrada en `LEDGER.md`, entrada `LDG-002`). La ausencia de `.101` en el repo no es una brecha; la brecha real — que sigue vigente — es que **`192.168.56.117` tampoco aparece todavía en ningún artefacto propio del proyecto**: no existe `scope/alcance.yaml` que lo declare, y por lo tanto no hay allowlist, ni criterio de cierre de G0, ni ningún rol o script que pueda leerlo. Cuando se cree `scope/alcance.yaml` en la Fase de implementación, será la **única fuente** del IP autorizado — ningún otro archivo (`roles/`, `harness/`, `gates/`) debe hardcodearlo.

**Fuente adicional revisada — `docs/Instruccion.html`.** Es la página del "Actividad de Cierre Unidad 3" del aula virtual del curso (Moodle), de la cual se descargan como adjuntos los mismos dos PDF ya transcritos (`Anexo técnico U3.pdf`, `11 Rúbrica de Evaluación U3 (100 puntos).pdf`; ver líneas 2870 del HTML). Su cuerpo introductorio (secciones "1. Situación" y "2. El encargo", líneas 2742–2869) agrega contexto que no estaba en la copia de los PDF transcritos y que es relevante para el alcance:

- **El activo de laboratorio es específicamente Metasploitable2**, no un host de red genérico: *"Objetivo de laboratorio: Metasploitable2 (mismo target)"* (línea 2738) y *"En el laboratorio, este activo está representado por Metasploitable2 y la dirección ip que Usted vea como asignada, como ejemplo 192.168.56.101"* (línea 2840–2842).
- **El mecanismo real de asignación de IP es "la que Usted vea como asignada"**, no una lista fija publicada por el docente — cada estudiante/grupo observa el IP de su propia instancia de Metasploitable2 en su entorno de laboratorio (típicamente vía `ifconfig`/`ip a` dentro de la VM, o la asignación DHCP del adaptador host-only de VirtualBox). `192.168.56.101` es, otra vez, solo el ejemplo del enunciado — consistente con lo ya concluido a partir del Anexo. El texto **no lista IPs por grupo** en ningún punto (se verificó con búsqueda exhaustiva de `56.117`, `56.101` y variantes: la única ocurrencia de un IP `192.168.56.x` en todo el archivo es el ejemplo de la línea 2842).
- El cliente ficticio (Comercial Andes Sur SpA, Chillán, 140 trabajadores, datos personales y datos sensibles de licencias médicas, no calificada OIV, sin certificaciones vigentes) coincide exactamente con el que ya aparecía citado en `docs/anexo_tecnico_u3.md` §11 — confirma que ambos documentos describen el mismo encargo, no encargos distintos.
- Se revisaron los encabezados completos del HTML (`<h1>`/`<h2>` con ancla): el documento **no contiene** una sección de "reglas de compromiso RC-1 a RC-6", ni un listado de "dimensiones de extensión D1–D8", ni una "estructura de seis bloques del video" — el cuerpo termina en la sección 2 y pasa directo a los adjuntos. Estos tres elementos, exigidos por la rúbrica en los criterios A, B y H respectivamente, **siguen sin estar disponibles en ninguno de los tres documentos fuente entregados hasta ahora** (Anexo, Rúbrica, Instruccion.html).

**Conclusión práctica para G0:** el respaldo documental que legitima `192.168.56.117` no es (ni el curso exige que sea) una lista firmada con el IP de cada grupo — es el mecanismo descrito en `docs/Instruccion.html`: "la IP que Usted vea como asignada" en su propia instancia de Metasploitable2.

**Evidencia ya capturada (2026-08-03T21:57:08-04:00, `LEDGER.md` `LDG-003`):** el grupo aportó una captura de pantalla de su propia VM ("METAEXPLOITABLE [Corriendo] - Oracle VirtualBox") ejecutando `ifconfig`, que muestra `eth0` con `inet addr:192.168.56.117 Bcast:192.168.56.255 Mask:255.255.255.0`. El archivo se copió sin editar a `evidencias/raw/g0-ifconfig-metasploitable2-192.168.56.117.png`, se hasheó (SHA-256 `5118d84f516a610057c7de49d207cc69b14ff60c6a7790e60760d164726f105f`) en `evidencias/manifest.sha256`, y quedó registrado en el ledger. Esto satisface el requisito de evidencia de REQ-A-01 (`docs/requirements.md`); lo único pendiente es que `scope/alcance.yaml`, cuando se escriba en la Fase de implementación, cite esta evidencia como origen del IP autorizado.

### 0.2 Evidencia heredada — no válida para este alcance

Antes de reutilizar cualquier evidencia existente bajo `auditoria/`, se verificó a qué objetivo corresponde. Resultado de la búsqueda (`grep` sobre campos `target`/`host`/`ip` en `evidence/` y `data/`):

| Archivo | Campo `target` encontrado | ¿Válido para este alcance (192.168.56.117)? |
|---|---|---|
| `evidence/review/audit-system-test.json:2` | `"localhost"` | No |
| `evidence/review/multi-module.json:2` | `"localhost"` | No |
| `data/audit-results/auditoria_report.json:2` | `"localhost"` | No |

Ninguno de estos tres artefactos corresponde a `192.168.56.117` ni a ningún IP de red distinto — son ejecuciones de auditoría contra el propio equipo de desarrollo (`localhost`), generadas durante la validación del framework genérico (ver `docs/CAPABILITY_MATRIX.md`). No representan evidencia de una ejecución fuera de alcance en el sentido que prohíbe la rúbrica (no hay ningún IP ajeno a `192.168.56.117` involucrado), pero tampoco son evidencia de una auditoría contra el objetivo real de este entregable.

**Tratamiento:** se dejan donde están, sin incorporarlas como evidencia de este entregable U3 y sin borrarlas (son artefactos legítimos de la validación previa del framework, útiles como antecedente técnico — ver §1.1). Ningún artefacto en `evidencias/raw/` (cuando se cree) debe apuntar a estos archivos como si fueran evidencia de la auditoría contra `.117`; eso contaminaría el manifiesto y el criterio de cierre de G1 ("no hay comandos ejecutados fuera de allowlist en el log").

---

## 1. Las ocho capas de la arquitectura de referencia (Anexo, Parte II §3)

| Capa | Estado actual | Ruta (si existe) | Brecha |
|---|---|---|---|
| 8. Control humano (gates de firma, veto, aceptación) | Ausente | — | No hay ningún punto de parada con firma humana sobre el *proceso de auditoría*. `quality/gates-final.yaml` es autoevaluación automática del propio repo (sin firma humana), no gates G0/G3/G5. |
| 6. Harness (orquestación, gates, ledger, estado, BoundedLoop) | Ausente | — | No existe `harness/`. No hay concepto de BoundedLoop, WIP=1, ni tope de iteraciones. `auditoria/core/engine.py` orquesta *checks*, no *roles* ni *gates*. |
| 5. Roles (RECON, ANALISTA, VERIFICADOR, COMPLIANCE, REDACTOR) | Ausente | — | No existe ningún actor con alcance/herramientas/prohibiciones declaradas. El "motor" es un solo componente (`AuditEngine`) que recolecta, evalúa y reporta sin separación. |
| 4. Skills (enumerar, clasificar, correlacionar, redactar, priorizar) | Distinto concepto, no equivalente | `.claude/skills/audit-api.md`, `audit-report.md`, `audit-status.md`, `quick-audit.md` | Son *comandos operativos* del CLI/API existente (arrancar la API, generar reportes del sistema actual), no los procedimientos de auditoría del Anexo. Ninguna skill implementa clasificación de riesgo por tabla I×P ni correlación normativa. |
| 3. Conocimiento (MCP: CVE/CWE/CVSS, ISO 27001, NIST CSF, corpus CL) | Ausente en el sentido exigido | `auditoria/mcp/server.py`, `auditoria/mcp/tools.py` | El MCP existente expone 9 *herramientas de ejecución* sobre la base de datos propia del proyecto (`execute_audit`, `get_trends`, `register_webhook`, etc.), no un corpus de conocimiento de solo lectura citable (CVE/CWE/CVSS, ISO/IEC 27001:2022 Anexo A, NIST CSF 2.0, normativa chilena). Es "MCP ausente o simulado" respecto de lo que pide la rúbrica en el criterio B. |
| 2. Normalización (parsers deterministas → JSON canónico) | Parcialmente análogo, no equivalente | `auditoria/checks/*.py` | Los checks producen `Finding` estructurados directamente (no parsean salida cruda de `nmap`/`nc`/`curl`/`nikto`). No existe la capa intermedia "artefacto crudo → JSON canónico con línea de origen" que exige G2. |
| 1. Recolección (nmap, nc, curl, nikto → crudo + SHA-256) | Ausente | — | No hay ejecución de herramientas de reconocimiento externas contra un objetivo de red, ni captura de artefactos crudos con hash y timestamp. Los checks del repo auditan el propio host/localhost o un dominio arbitrario, no un objetivo de red autorizado con evidencia cruda preservada. |
| Objetivo — 192.168.56.117 (solo lectura) | Ausente | — | El IP real del grupo (`192.168.56.117`, ver §0.1) no aparece en ningún archivo del repositorio. El proyecto está diseñado para "target" genérico (`localhost`, `example.com`, cualquier dominio/ruta), sin restricción de alcance a un único IP autorizado. |

### 1.1 Reutilización de `auditoria/` por capa (LDG-001)

Decisión registrada: `auditoria/` se reutiliza como base donde el diseño actual lo permite; no se reconstruye todo desde cero. Esta sección evalúa, capa por capa, si el código existente sirve tal cual, sirve con reestructuración, o no aplica — con especial atención a si su diseño actual permite la **separación estructural de roles** que exige la banda 13–14 del criterio B (si un mismo componente recolecta, analiza y clasifica en la misma pieza de código, no es reutilizable sin dividirlo).

| Capa | Módulo(s) candidato(s) en `auditoria/` | Cobertura actual | Qué falta para la banda alta | Veredicto |
|---|---|---|---|---|
| 1. Recolección | `auditoria/checks/network.py`, `system.py`, `ssl_tls.py` | Parcial. `NetworkCheck._scan_ports()` (`network.py:87-133`) escanea puertos con sockets Python nativos (`socket.connect_ex`), no invoca `nmap`/`nc`/`curl`/`nikto` como procesos externos, y no persiste salida cruda con hash — el resultado va directo a un objeto `Finding` en memoria. | (a) Reemplazar/envolver la lógica por invocación real de las herramientas de la allowlist vía `subprocess`, con `stdout`/`stderr` capturados tal cual a `evidencias/raw/` + SHA-256 antes de cualquier interpretación. (b) Sacar la asignación de severidad (`network.py:128`, `Severity.HIGH if risky else Severity.MEDIUM`) fuera de esta capa — hoy decide severidad en el mismo paso que "recolecta", que es exactamente el patrón "un solo agente hace todo" que la Parte VI señala como error. | **Reutilizable con reestructuración**, no tal cual. El patrón target/config/`ThreadPoolExecutor` es aprovechable; la mezcla recolección+clasificación no. |
| 2. Normalización | `auditoria/checks/base.py` (`BaseCheck`), `registry.py`, `core/models.py` (`Finding`) | Parcial. `BaseCheck.run()` (`base.py:22-24`) es un contrato limpio de "ejecutar y devolver hallazgos estructurados", y `Finding` (`core/models.py`) ya es un modelo tipado — es el antecedente más cercano a un "parser determinista → estructura canónica". | El contrato actual permite que `run()` interprete y clasifique en el mismo método (ver capa 1). Para servir como Capa 2 real hace falta separar "parsear artefacto crudo → JSON canónico con puntero a la línea de origen" como paso propio, sin severidad ni juicio de riesgo todavía. | **Reutilizable como base de diseño** (el contrato `BaseCheck`/`registry` es un buen punto de partida), con la separación de responsabilidades como cambio obligatorio. |
| 3. Conocimiento (MCP) | `auditoria/mcp/server.py`, `mcp/tools.py` | Ninguna en contenido. Los 9 tools de `AUDIT_TOOLS` (`mcp/tools.py:6-189`) son de *ejecución y gestión* sobre la base de datos propia del proyecto (`execute_audit`, `get_audit_history`, `register_webhook`, etc.), no de consulta a un corpus de conocimiento (CVE/CWE/CVSS, ISO 27001 Anexo A, NIST CSF 2.0, normativa CL). | Construir un servidor MCP nuevo, de solo lectura, sobre un corpus real (offline si el laboratorio no tiene Internet, declarando `NO_DISPONIBLE` donde falte EPSS/KEV). | **No reutilizable en contenido.** El *andamiaje* del servidor (`server.py` como wrapper del protocolo MCP y el estilo de definición de tools con `inputSchema`) sí es reutilizable como plantilla de cómo levantar un servidor MCP en este stack. |
| 4. Skills | `.claude/skills/audit-api.md`, `audit-report.md`, `audit-status.md`, `quick-audit.md` | Ninguna en contenido. Son comandos operativos del framework genérico (arrancar la API, generar reportes, ver estado de tareas programadas), no los procedimientos `enumerar/clasificar/correlacionar/redactar/priorizar` del Anexo. Además usan un formato sin frontmatter YAML (`# Skill: nombre` + secciones libres) — antes de reutilizar la convención hay que verificar contra la documentación vigente de Claude Code Skills si ese formato sigue siendo válido o si el spec actual exige `SKILL.md` con `name`/`description` en YAML. | Escribir las 5 skills nuevas exigidas por el Anexo, con `description` como disparador preciso (no genérico), y verificar el formato correcto contra la doc vigente antes de escribir archivos. | **No reutilizable en contenido**, pero la estructura del repositorio (`.claude/skills/`) ya existe y está en uso, lo cual reduce trabajo de plomería. |
| 5. Roles | `auditoria/ai/analyzer.py`, `ai/prompts.py` | Ninguna en el sentido de rol con permisos delimitados. `AuditAnalyzer` (`ai/analyzer.py:17-174`) hace prioritización, resumen ejecutivo y detección de patrones todo en una sola clase, con un solo cliente Anthropic y sin restricción de herramientas — es el equivalente en miniatura de "un solo agente hace todo". Además usa el modelo `claude-3-5-sonnet-20241022` (`analyzer.py:64,113,143,164`), que deberá actualizarse. | Dividir esta única clase en los 5 roles con fronteras de herramientas reales (subagentes con `tools`/`disallowedTools`, o middleware de validación si es harness propio). Los prompts de `ai/prompts.py` (`PRIORITIZE_FINDINGS`, `ANALYZE_FINDINGS`, `GENERATE_EXECUTIVE_SUMMARY`, `DETECT_PATTERNS`) son un antecedente de redacción reutilizable para los roles ANALISTA y REDACTOR, no para VERIFICADOR ni COMPLIANCE (que no tienen equivalente hoy). | **Antecedente de prompts reutilizable; arquitectura de rol, no.** Requiere separación estructural completa, no ajuste incremental. |
| 6. Harness | `auditoria/scheduler/executor.py`, `auditoria/api/server.py`, `auditoria/storage/database.py` | Ninguna como BoundedLoop. `AuditScheduler` (`scheduler/executor.py:48-171`) orquesta *re-ejecuciones periódicas por cron* de la misma auditoría completa, no un ciclo de una-etapa-a-la-vez con WIP=1 entre roles. `api/server.py` es un disparador HTTP del motor existente. `storage/database.py` (SQLite, `DatabaseManager`) sí tiene un patrón sólido de persistencia transaccional que podría indexar el ledger para consulta, pero el Anexo exige que `LEDGER.md` sea el archivo append-only fuente de verdad, no una tabla. | Construir el orquestador de roles/gates desde cero (`harness/orquestador.*`); el scheduler cron sirve más adelante para la etapa 9 (retest periódico), no para el bucle principal. Si se usa SQLite como índice de lectura del ledger, debe generarse *desde* `LEDGER.md`, nunca al revés. | **No reutilizable para el bucle principal.** `database.py` es reutilizable como índice secundario opcional; `scheduler/executor.py` es reutilizable para la etapa 9, no para el harness. |
| 8. Control humano | `quality/gates-final.yaml` | Ninguna. Es una autoevaluación automática de gates de *calidad de software de este repositorio* (tests, cobertura, integridad de código) sin campo de firma humana ni veredicto `APPROVE_WITH_FINDINGS` — todos sus 10 gates se marcan `PASS`/`BLOCKED` sin que un humano firme. | Construir `gates/G0.md`, `G3.md`, `G5.md` con el formato exacto del Anexo (§5), incluida la firma humana obligatoria. | **No reutilizable.** Es un concepto adyacente (ambos se llaman "gate") pero resuelve un problema distinto; puede servir como recordatorio de *qué se le exige a un archivo de gates para no ser papeleo*, nada más. |

**Antecedente transversal:** `specs/ai-policy.yaml` (guardrails, líneas 87–116) ya declara principios compatibles con CT-01/CT-07 — "AI cannot create findings without evidence", "Only humans can mark findings as confirmed" — pero como *política* para el enriquecimiento por IA de hallazgos ya generados por checks locales, no como validadores ejecutables mapeados a los 7 controles del Anexo. Es un punto de partida para redactar los REQ de la Fase 1 relacionados con CT-01 y CT-07, no una implementación a copiar.

## 2. Los cinco roles del concilio y su tabla de permisos (Anexo §4)

| Elemento requerido | Estado actual | Banda estimada | Brecha |
|---|---|---|---|
| Rol RECON (ejecutor allowlist, escritura en `evidencias/raw/`, sin redacción de hallazgos) | Ausente | — | No existe. `auditoria/checks/network.py` hace algo adyacente (DNS, puertos) pero como *función*, no como actor con permisos restringidos ni allowlist de comandos. |
| Rol ANALISTA (lectura de JSON canónico + MCP CVE/CWE/CVSS, sin ejecución ni asignación de VALIDADO) | Ausente | — | `auditoria/ai/analyzer.py` es lo más cercano (usa Claude para `PRIORITIZE_FINDINGS`, `ANALYZE_FINDINGS`, etc.) pero es una función de enriquecimiento sin frontera de herramientas — no hay separación estructural entre "quien analiza" y "quien podría escribir". |
| Rol VERIFICADOR (lectura de todo, **sin** herramientas de escritura, veto de cierre) | Ausente | — | No existe ningún actor cuyas herramientas estén restringidas a solo lectura por diseño del runtime (vía `tools`/`disallowedTools` o equivalente). `specs/ai-policy.yaml` declara reglas como "solo humanos confirman hallazgos" (líneas 106–116), lo cual es un principio compatible, pero está descrito como *política*, no implementado como *restricción estructural de herramientas* — es exactamente la diferencia que la rúbrica banda 13–14 del criterio B exige que no sea "de buena fe". |
| Rol COMPLIANCE (MCP normativo, sin modificar severidades) | Ausente | — | No existe. `report.schema.json:223` tiene un campo `compliance_framework` con enum `["CIS","NIST","PCI-DSS","SOC2","ISO27001"]` — nombres de marco, no controles específicos ni corpus consultable. |
| Rol REDACTOR (plantillas + datos verificados, sin contenido no trazable) | Parcialmente análogo | `auditoria/core/reporter.py`, `auditoria/templates/report.html` | Genera reportes JSON/HTML desde los `Finding` de la base de datos (trazabilidad relativa a la BD propia), pero no hay concepto de `evidence_id` ligado a artefacto crudo con hash, ni restricción de "no puede crear contenido no trazable" implementada como control. |
| Separación estructural de actores (al VERIFICADOR no se le dan herramientas de escritura) | Ausente | — | No hay ningún mecanismo — ni subagentes con `tools:` restringido, ni middleware que valide tool-calls por rol — que impida a un componente escribir. Todo corre en un solo proceso con acceso completo a la BD y al filesystem. |
| Rol opcional "contradicción explícita" (D2) | Ausente | — | No implementado; es opcional, pero no hay ninguna extensión D1–D8 de la lista del Anexo implementada tampoco. |

## 3. Workflow de 10 etapas y los 3 gates con firma humana (Anexo §2)

| Etapa Anexo | Estado actual | Brecha |
|---|---|---|
| 0. Encargo y autorización (G0) | Ausente | No hay carta de alcance, ventana, contactos ni restricciones. No hay firma humana registrada en ningún artefacto. |
| 1. Criterio de auditoría (G0) | Ausente | No hay declaración de qué normas/controles se auditan por cliente (ISO 27001 Anexo A / NIST CSF 2.0 / normativa CL). |
| 2. Planificación | Ausente como etapa distinta | El CLI permite elegir módulos (`--modules`), pero no hay "plan de pruebas" documentado con evidencia esperada por prueba. |
| 3. Recolección de evidencia (G1) | Ausente | No hay artefactos crudos con hash+timestamp ni manifiesto (`manifest.sha256`). |
| 4. Normalización e inventario (G2) | Ausente | No hay JSON canónico de activos/servicios que referencie línea de artefacto crudo. |
| 5. Análisis y verificación (G3) | Parcialmente análogo, sin separación de roles | `Finding.validation.state` usa enum `["unreviewed","accepted","rejected","disputed","verified"]` (`specs/finding.schema.json:83-88`) — vocabulario distinto del exigido `VALIDADO / OBSERVADO / INCONCLUSO`, y sin flujo ANALISTA→VERIFICADOR estructural. |
| 6. Evaluación de riesgo (G3) | Ausente | Solo existe `severity` como enum fijo (`critical/high/medium/low/info`); no hay CVSS con vector, ni factores de impacto/probabilidad, ni matriz 5×5. |
| 7. Correlación normativa (G4) | Ausente | No hay matriz hallazgo↔control↔obligación↔evidencia requerida. |
| 8. Reporte (G5) | Parcialmente análogo | Existe generación de reporte (JSON/HTML vía Jinja2), pero no usa el template canónico del Anexo (Parte V: `reporte_final.md/.pdf` + `matriz_correlacion.csv`) ni pasa por los 7 controles anti-alucinación. |
| 9. Comunicación, remediación y seguimiento | Parcialmente análogo | Existe campo `remediation` con `assigned_to`/`due_date`/`status` (`specs/finding.schema.json:153-176`), pero no hay retest diferencial ni plan con las columnas exigidas (esfuerzo, plazo, riesgo residual). |
| **G0 con firma humana** | Ausente | Ningún artefacto de "firma humana" existe en el repo. |
| **G3 con firma humana sobre VALIDADO** | Ausente | El estado `verified` en el schema no exige firma humana explícita ni artefacto de re-verificación. |
| **G5 con firma humana del informe** | Ausente | No hay mecanismo de firma sobre el informe final. |

## 4. Formato de gate, formato de ledger y los 7 controles anti-alucinación (Anexo §5–7)

| Elemento requerido | Estado actual | Ruta | Brecha |
|---|---|---|---|
| Formato `gates/GX.md` (Criterio / Evidencia presentada / Concilio / Objeciones / Veredicto / Hallazgos abiertos / Firma humana) | Distinto formato, mismo nombre "gate" | `quality/gates-final.yaml` | Son gates de *calidad de software* (repo integrity, tests unitarios, cobertura, seguridad del código) evaluados en un solo archivo YAML, sin veredicto `APPROVE_WITH_FINDINGS`, sin campo de firma humana, sin ledger asociado. No sirven como sustituto de G0–G5 del Anexo. |
| `LEDGER.md` append-only con `SUPERSEDE` | Ausente | — | No existe ningún archivo de ledger en el repositorio. |
| CT-01 Trazabilidad obligatoria (`evidence_id`) | Ausente | — | No existe el campo `evidence_id` en ningún schema. `Finding.evidence` (línea 57 de `finding.schema.json`) es un objeto/string libre, no un identificador que apunte a un artefacto crudo con hash. |
| CT-02 Prohibición de inferencia de servicio | Parcialmente presente en espíritu, no como control ejecutable | `specs/ai-policy.yaml:88-92` ("AI cannot create findings without evidence") | Es una regla de política para el enriquecimiento por IA de hallazgos ya creados por checks deterministas — no es un validador que busque la cadena literal en un artefacto crudo antes de admitir un hallazgo, porque no hay artefactos crudos. |
| CT-03 Coherencia de severidad | Ausente como control ejecutable | — | No hay comparación automática entre matriz/tabla/ficha porque no existen esas tres vistas del mismo hallazgo. |
| CT-04 Remediación aplicable (versión objetivo ≠ versión instalada) | Ausente | — | El campo `recommendation` es texto libre sin verificación de versión. |
| CT-05 Consistencia numérica (resumen por agregación) | Parcialmente presente | `auditoria/core/reporter.py` (a confirmar en Fase de diseño si agrega o redacta) | Requiere verificar en el código si el resumen se calcula por agregación real; no hay un control explícito nombrado ni testeado para esto. |
| CT-06 Estado condicionado por la red (falla de verificación → máximo INCONCLUSO) | Ausente | — | No existe el concepto de intento de verificación fallido por red que degrade el estado. |
| CT-07 Cero dato sintético (`NO_OBSERVADO`) | Ausente | — | No existe ningún marcador de ausencia de dato en los schemas. `ai-policy.yaml` no cubre el caso de datos faltantes (EPSS/KEV) porque esos conceptos no existen en el proyecto actual. |

**Nota:** `specs/ai-policy.yaml` (guardrails, sección III, líneas 87–116) contiene principios *de espíritu compatible* con CT-01/CT-07 (evidencia obligatoria, inmutabilidad de severidad por IA, confirmación humana), lo cual es un antecedente reutilizable para el diseño de Fase 2, pero hoy son reglas declaradas para un dominio distinto (enriquecimiento de hallazgos ya generados por checks locales), no los 7 controles del Anexo mapeados a errores de CertEngine.

## 5. Estructura mínima del repositorio (Anexo, Parte V)

| Ruta exigida | Estado actual | Brecha |
|---|---|---|
| `README.md` (arquitectura, decisiones, extensiones) | Existe, pero describe el proyecto genérico | `README.md` | Necesita reescritura completa para reflejar la arquitectura U3 una vez diseñada. |
| `scope/alcance.yaml` | Ausente | — | No existe carpeta `scope/`. |
| `scope/allowlist.txt` | Ausente | — | No existe. |
| `scope/declaracion_etica.md` | Ausente | — | No existe. |
| `roles/` | Ausente | — | No existe. |
| `skills/` (enumerar, clasificar, correlacionar, redactar, priorizar) | No equivalente | `.claude/skills/*.md` cubre un dominio distinto (ver §1) | — |
| `mcp/` | No equivalente | `auditoria/mcp/` cubre un dominio distinto (ver §1) | — |
| `harness/orquestador.*` | Ausente | — | No existe. |
| `harness/controles/` (CT-01..07) | Ausente | — | No existe. |
| `evidencias/raw/` | No equivalente | `evidence/` existe pero contiene evidencia de *verificación de este repositorio* (baseline, resultados e2e), no artefactos crudos de una auditoría contra 192.168.56.101 | — |
| `evidencias/manifest.sha256` | Ausente | — | No existe. |
| `normalizado/` | Ausente | — | No existe. |
| `gates/` (G0..G5) | No equivalente | `quality/gates-final.yaml` cubre gates de calidad de software (ver §4) | — |
| `LEDGER.md` | Ausente | — | No existe. |
| `reporte/reporte_final.md` / `.pdf` | No equivalente | `auditoria/templates/report.html`, `data/audit-results/*.json` | No sigue el template canónico ni la matriz de correlación exigida. |
| `reporte/matriz_correlacion.csv` | Ausente | — | No existe. |

## 6. Criterios de la rúbrica A–J: banda actual estimada

> Estimación conservadora basada en inspección de archivos, no en ejecución. Cero puntaje no es un juicio negativo sobre el proyecto existente — es la constatación de que los artefactos exigidos por el Anexo U3 aún no existen bajo ningún nombre equivalente verificable.

| Criterio | Máximo | Banda estimada hoy | Justificación (evidencia de la banda) |
|---|---|---|---|
| A — Alcance, autorización, RC-1..RC-6 | 8 | **0** | "Alcance ausente o ambiguo" — no hay IP objetivo, allowlist, ventana ni declaración ética en el repo. |
| B — Arquitectura agéntica y extensión propia | 14 | **0–5** | "No hay arquitectura: ... un script sin componente agéntico. Sin extensión propia sobre la base" — hay un motor de checks + IA de enriquecimiento, pero sin roles separados, sin MCP de conocimiento, sin harness/BoundedLoop, sin gates de proceso. |
| C — Workflow de auditoría declarado y ejecutado | 10 | **0–3** | "No hay workflow declarado. La ejecución es una secuencia improvisada" — el proyecto ejecuta checks, no un workflow de auditoría con criterio declarado. |
| D — Evidencia, trazabilidad, CT-01..07 | 14 | **0–5** | "Sin trazabilidad [equivalente]. Afirmaciones del reporte que no corresponden a ningún artefacto [crudo con hash]" — existe *algo* de evidencia (objeto `evidence` en el finding) pero no hay `evidence_id`, ni hash, ni manifiesto, ni los 7 controles. |
| E — Clasificación de riesgo I×P | 12 | **0–3** | "Sin matriz, o matriz de colores sin criterio" — solo existe un enum de severidad fijo, sin CVSS con vector ni factores de impacto/probabilidad. |
| F — Correlación normativa y de cumplimiento | 14 | **0–5** | "Sin correlación normativa" — solo existe un campo `compliance_framework` con el nombre del marco, sin controles específicos, sin "aplica porque", sin evidencia requerida. |
| G — Reporte final generado autónomamente | 10 | **4–6** | Hay generación automática real de reportes desde datos (JSON/HTML vía Jinja2) — eso es un antecedente aprovechable — pero no sigue el template canónico del Anexo, no tiene resumen ejecutivo por agregación verificada, ni prioriza con responsable/esfuerzo/plazo en el formato exigido. |
| H — Video: demostración y punto de control humano | 10 | **No verificable** | No existe grabación en el repositorio; no corresponde estimar banda sin el artefacto. |
| I — Revisión cruzada producida | 4 | **No aplica aún** | Depende de recibir el reporte de otro grupo; etapa posterior del curso. |
| J — Defensa oral | 4 | **No aplica aún** | Evaluación presencial posterior. |

**Puntaje estimado hoy (A+B+C+D+E+F+G, sin H/I/J):** aproximadamente **4 a 27 de 86** puntos posibles en esos siete criterios — la mayor parte del pipeline exigido está por construir.

---

## 7. Cierre de Fase 0

Este documento es diagnóstico únicamente. No se ha propuesto ninguna solución de diseño ni se ha escrito código. Antes de avanzar a la Fase 1 (`docs/requirements.md`), se espera confirmación explícita del usuario — salvo instrucción de "continúa sin pausas".

**Decisiones ya tomadas (registradas en `LEDGER.md`):**

1. ~~¿Se reutiliza `auditoria/` o se construye en paralelo?~~ — **Resuelto (LDG-001):** se reutiliza donde el diseño actual lo permite; detalle por capa en §1.1.
2. ~~¿Cuál es el IP objetivo real?~~ — **Resuelto (LDG-002):** `192.168.56.117`; detalle en §0.1.

**Puntos aún abiertos antes o durante la Fase 1:**

1. **Ruta de aislamiento estructural de roles (Fase 2a del prompt):** subagentes de Claude Code vs. harness propio contra la API — es la decisión de mayor impacto en el criterio B (14 pts) y se resuelve en `docs/design.md` (Fase 2), no aquí. La Fase 1 puede redactar el REQ correspondiente sin fijar la ruta todavía, dejándola como decisión de diseño explícita.
2. **Respaldo escrito de la autorización sobre `192.168.56.117`.** El Anexo (Parte I, etapa 0) exige que G0 cierre solo si "existe scope firmado con IP autorizada". La instrucción de este chat confirma el IP, pero no constituye por sí sola el respaldo documental (correo o documento del docente) que un `alcance.yaml` firmado debería poder citar como origen de la autorización. Mientras ese respaldo no se identifique explícitamente, el REQ de scope (Fase 1) queda redactado pero **G0 no puede declararse cerrable** — esto se le preguntó directamente al usuario antes de continuar a la Fase 1, conforme a la instrucción de detenerse si no hay forma de confirmarlo por escrito.
