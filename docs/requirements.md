# requirements.md — Especificación formal (Fase 1)

**Fuente de verdad:** `docs/anexo_tecnico_u3.md`, `docs/rubrica_evaluacion_u3.md`, `docs/GAP_ANALYSIS.md`.
**Decisiones previas registradas en `LEDGER.md`:** `LDG-001` (reutilización de `auditoria/` por capa) y `LDG-002` (IP objetivo real = `192.168.56.117`).
**Método:** un requisito por brecha detectada en la Fase 0. Ningún requisito de esta fase incluye código — solo condición de aceptación verificable.

Orden de prioridad (mayor peso / mayor riesgo de reprobación automática primero): **D → F → G → B → E → C → A → H**.

Convención de ID: `REQ-<criterio>-<correlativo>` (p. ej. `REQ-D-01`). El campo **Criterio de aceptación** cita textualmente la condición de la banda más alta de ese criterio en la rúbrica; donde no fue posible convertir la banda en una condición verificable sin inventar contenido ausente del Anexo, se marca explícitamente como **SUPOSICIÓN PENDIENTE** en vez de inventarse.

---

## D — Evidencia, trazabilidad y controles anti-alucinación (14 pts)

### REQ-D-01 — Cadena de evidencia con `evidence_id`, hash y timestamp
**Criterio de rúbrica:** D — Evidencia, trazabilidad y controles anti-alucinación
**Banda objetivo:** 13–14/14
**Descripción:** Todo hallazgo del reporte final debe portar un `evidence_id` que resuelva a un artefacto crudo concreto en `evidencias/raw/`, con su hash SHA-256 y timestamp de captura.
**Criterio de aceptación (verificable):** "Cada afirmación del reporte final es trazable a un `evidence_id` con artefacto crudo, hash y timestamp" (rúbrica D, banda 13–14). Condición binaria: ningún hallazgo en `reporte/reporte_final.md` carece de campo `evidence_id`; cada `evidence_id` referenciado existe físicamente en `evidencias/raw/` y su hash coincide con el registrado en `evidencias/manifest.sha256`.
**Evidencia que lo demuestra:** `evidencias/manifest.sha256`, script validador que recorre `reporte/reporte_final.md` y falla si encuentra una afirmación sin `evidence_id` resoluble.
**Dependencias:** REQ-D-02 (manifiesto). Reutiliza como antecedente `auditoria/checks/base.py`/`registry.py` (contrato `run()` → estructura tipada), pero requiere separar la captura cruda de la interpretación (ver GAP_ANALYSIS §1.1, capas 1–2).

### REQ-D-02 — Manifiesto de evidencias verificable
**Criterio de rúbrica:** D
**Banda objetivo:** 13–14/14
**Descripción:** Existe `evidencias/manifest.sha256` que lista cada artefacto crudo con su hash; el manifiesto se puede re-verificar (recalcular hash y comparar) en cualquier momento posterior.
**Criterio de aceptación (verificable):** "El manifiesto de evidencias verifica" (rúbrica D, banda 13–14). Condición binaria: ejecutar la verificación del manifiesto sobre `evidencias/raw/` produce cero discrepancias.
**Evidencia que lo demuestra:** `evidencias/manifest.sha256` + script/comando de verificación y su salida capturada.
**Dependencias:** ninguna (requisito base de la capa 1).

### REQ-D-03 — Estados VALIDADO / OBSERVADO / INCONCLUSO usados con rigor
**Criterio de rúbrica:** D
**Banda objetivo:** 13–14/14
**Descripción:** Reemplaza el vocabulario actual de `specs/finding.schema.json` (`unreviewed/accepted/rejected/disputed/verified`, líneas 83–88) por el tri-estado exigido por el Anexo. `VALIDADO` solo se asigna cuando existe verificación adicional capturada, no solo el indicio de una herramienta de recolección.
**Criterio de aceptación (verificable):** "Los estados VALIDADO / OBSERVADO / INCONCLUSO se usan con rigor y el estado VALIDADO tiene respaldo de verificación adicional, no solo de nmap" (rúbrica D, banda 13–14). Condición binaria: ningún hallazgo en estado VALIDADO carece de un segundo artefacto de evidencia (distinto del primero) referenciado en su `evidence_id`.
**Evidencia que lo demuestra:** esquema de hallazgo actualizado + al menos un caso real en `LEDGER.md` donde un hallazgo pasa de OBSERVADO a VALIDADO citando el artefacto adicional.
**Dependencias:** REQ-D-01. Sustituye el campo `validation.state` de `specs/finding.schema.json`.

### REQ-D-04 — CT-01: Trazabilidad obligatoria (validador ejecutable)
**Criterio de rúbrica:** D
**Banda objetivo:** 13–14/14 (exige "al menos tres [controles] se demuestran atrapando un caso real")
**Descripción:** Validador que rechaza el reporte final si alguna afirmación carece de `evidence_id`.
**Criterio de aceptación (verificable):** El validador, ejecutado contra un reporte con al menos una afirmación sin `evidence_id` inyectada deliberadamente en una prueba, la detecta y bloquea la generación; ejecutado contra el reporte real, pasa sin rechazos.
**Evidencia que lo demuestra:** `harness/controles/ct01_trazabilidad.*` + registro de al menos una ejecución que atrapó un caso real (o de prueba) en `LEDGER.md` como `RECHAZO`.
**Dependencias:** REQ-D-01.

### REQ-D-05 — CT-02: Prohibición de inferencia de servicio (validador ejecutable)
**Criterio de rúbrica:** D
**Banda objetivo:** 13–14/14
**Descripción:** Antes de admitir un hallazgo que declare un producto/versión, el validador busca la cadena literal en `evidencias/raw/`. Si no aparece, el hallazgo se rechaza o degrada.
**Criterio de aceptación (verificable):** Búsqueda literal automática de la cadena declarada (p. ej. nombre de producto) en el conjunto de artefactos crudos referenciados por el `evidence_id` del hallazgo; ausencia de la cadena ⇒ `RECHAZO` registrado en el ledger, no publicación en el reporte.
**Evidencia que lo demuestra:** `harness/controles/ct02_inferencia.*`; ejemplo del propio Anexo (§6, `LDG-019`) como caso de referencia para el diseño de la prueba.
**Dependencias:** REQ-D-01, REQ-D-02.

### REQ-D-06 — CT-03: Coherencia de severidad (validador ejecutable)
**Criterio de rúbrica:** D
**Banda objetivo:** 13–14/14
**Descripción:** Comparación automática de la severidad de un mismo hallazgo entre la matriz de correlación, la tabla resumen y su ficha de detalle en el reporte.
**Criterio de aceptación (verificable):** El validador recorre las tres vistas por `check_id`/hallazgo y falla si encuentra más de un valor de severidad para el mismo ID.
**Evidencia que lo demuestra:** `harness/controles/ct03_severidad.*`.
**Dependencias:** REQ-F-01 (matriz de correlación), REQ-D-01.

### REQ-D-07 — CT-04: Remediación aplicable (validador ejecutable)
**Criterio de rúbrica:** D
**Banda objetivo:** 13–14/14
**Descripción:** La remediación propuesta para un hallazgo no puede apuntar a la misma versión vulnerable identificada en la evidencia.
**Criterio de aceptación (verificable):** Comparación automática: versión objetivo mencionada en el campo de remediación ≠ versión instalada citada en la evidencia del hallazgo. Discrepancia ⇒ rechazo del reporte.
**Evidencia que lo demuestra:** `harness/controles/ct04_remediacion.*`.
**Dependencias:** REQ-D-01.

### REQ-D-08 — CT-05: Consistencia numérica (resumen por agregación)
**Criterio de rúbrica:** D
**Banda objetivo:** 13–14/14
**Descripción:** El resumen ejecutivo y cualquier conteo del reporte se calculan por agregación programática sobre los datos verificados, nunca se redactan a mano.
**Criterio de aceptación (verificable):** Los números del resumen ejecutivo se regeneran ejecutando la agregación sobre `normalizado/` + hallazgos, y coinciden exactamente con lo publicado; no existe ningún número en el resumen que no provenga de ese cálculo.
**Evidencia que lo demuestra:** función/script de agregación + su salida comparada byte a byte con el resumen publicado.
**Dependencias:** REQ-D-01. Relacionado con REQ-G-02.

### REQ-D-09 — CT-06: Estado condicionado por la red
**Criterio de rúbrica:** D
**Banda objetivo:** 13–14/14
**Descripción:** Si el intento de verificación adicional de un hallazgo falla por condición de red (NAT, segmentación, timeout), el estado máximo alcanzable es INCONCLUSO, nunca VALIDADO ni OBSERVADO con apariencia de confirmado.
**Criterio de aceptación (verificable):** Regla ejecutable: todo hallazgo cuyo log de verificación registre un fallo de conectividad tiene `estado == INCONCLUSO`; el validador rechaza cualquier excepción a esta regla.
**Evidencia que lo demuestra:** `harness/controles/ct06_red.*` + caso de prueba con fallo de red simulado.
**Dependencias:** REQ-D-03.

### REQ-D-10 — CT-07: Cero dato sintético (marcadores `NO_OBSERVADO` / `NO_DISPONIBLE`)
**Criterio de rúbrica:** D
**Banda objetivo:** 13–14/14
**Descripción:** Cuando un dato no existe (p. ej. EPSS/KEV sin conectividad, o un aspecto fuera del alcance autorizado de verificar), se declara explícitamente como `NO_OBSERVADO` (hallazgo) o `NO_DISPONIBLE` (factor de riesgo, ver Anexo §10 nota de laboratorio) con fecha y justificación — nunca se omite ni se rellena con un valor supuesto.
**Criterio de aceptación (verificable):** "Las ausencias se registran, no se rellenan" (rúbrica D, banda 13–14). Ningún campo obligatorio del schema de hallazgo o de la matriz de riesgo queda vacío o con valor por defecto no declarado; todo campo no verificable tiene el marcador correspondiente y su justificación.
**Evidencia que lo demuestra:** al menos un hallazgo real con `NO_OBSERVADO` (equivalente al "Ejemplo 3" del Anexo §15) y al menos un factor de riesgo con `NO_DISPONIBLE` justificado.
**Dependencias:** REQ-E-03 (factores de probabilidad). Antecedente reutilizable con reestructuración: guardrails de `specs/ai-policy.yaml` (líneas 87–116) — ver GAP_ANALYSIS §1.1.

---

## F — Correlación normativa y de cumplimiento (14 pts)

### REQ-F-01 — Matriz de correlación con columnas mínimas del Anexo §13
**Criterio de rúbrica:** F
**Banda objetivo:** 13–14/14
**Descripción:** `reporte/matriz_correlacion.csv` con una fila por hallazgo y, como mínimo, las columnas listadas en el Anexo §13 (ID, Hallazgo, evidence_id, Estado, CWE, CVE, Vector CVSS, I, P, Riesgo, Control ISO, NIST, CIS, Obligación CL, Aplica porque, Evidencia requerida, Brecha, Remediación, Esfuerzo, Responsable, Plazo, Riesgo residual).
**Criterio de aceptación (verificable):** El archivo existe, tiene una fila por hallazgo publicado en el reporte y contiene las 21 columnas mínimas listadas; ninguna fila tiene una columna vacía sin marcador `NO_OBSERVADO`/`NO_DISPONIBLE` justificado.
**Evidencia que lo demuestra:** `reporte/matriz_correlacion.csv`.
**Dependencias:** REQ-D-01, REQ-D-10, REQ-E-01..06 (severidad/riesgo), REQ-F-02..05 (contenido de las columnas normativas).

### REQ-F-02 — Correlación con control ISO/IEC 27001:2022 Anexo A
**Criterio de rúbrica:** F
**Banda objetivo:** 13–14/14
**Descripción:** Cada hallazgo se mapea a uno o más controles específicos del Anexo A (no genérico), citando el identificador del control (p. ej. A.8.20).
**Criterio de aceptación (verificable):** Extracto de la banda 13–14: "Cada hallazgo se correlaciona con: control ISO/IEC 27001:2022 (Anexo A)...". Condición binaria: cada fila de la matriz tiene al menos un control ISO con identificador válido del Anexo A; el mapeo no repite el mismo control para más del 50% de hallazgos sin justificación distinta por fila (evita el error frecuente "todos los hallazgos mapean al mismo control", Anexo Parte VI).
**Evidencia que lo demuestra:** `reporte/matriz_correlacion.csv`, columna Control ISO.
**Dependencias:** REQ-F-06 (corpus MCP normativo, capa 3).

### REQ-F-03 — Correlación con NIST CSF 2.0 (función/categoría)
**Criterio de rúbrica:** F
**Banda objetivo:** 13–14/14
**Descripción:** Cada hallazgo se mapea a función y categoría específica de NIST CSF 2.0 (GV, ID, PR, DE, RS, RC + subcategoría, p. ej. `PR.DS-02`).
**Criterio de aceptación (verificable):** Cada fila de la matriz tiene una categoría NIST CSF 2.0 válida (no solo el nombre del framework).
**Evidencia que lo demuestra:** `reporte/matriz_correlacion.csv`, columna NIST CSF 2.0.
**Dependencias:** REQ-F-06.

### REQ-F-04 — Correlación con CIS Controls v8
**Criterio de rúbrica:** F
**Banda objetivo:** 13–14/14
**Descripción:** Cada hallazgo se mapea a un (sub)control específico de CIS v8 (p. ej. `4.8`).
**Criterio de aceptación (verificable):** Cada fila de la matriz tiene un identificador de (sub)control CIS v8 válido.
**Evidencia que lo demuestra:** `reporte/matriz_correlacion.csv`, columna CIS v8.
**Dependencias:** REQ-F-06.

### REQ-F-05 — Implicancia bajo normativa chilena, columna "aplica porque" y "evidencia requerida"
**Criterio de rúbrica:** F
**Banda objetivo:** 13–14/14
**Descripción:** Cada hallazgo relevante cita la ley chilena aplicable (Ley 21.663, 21.719 y/o 21.459 según corresponda), con una línea "aplica porque" específica del cliente (no copia del artículo) y una columna "evidencia requerida" que un fiscalizador exhibiría (política con fecha, registro, bitácora, contrato, resultado de prueba).
**Criterio de aceptación (verificable):** "La columna 'aplica porque' explica en una línea por qué esa obligación alcanza a esta organización... Para cada control se declara la evidencia requerida..." (rúbrica F, banda 13–14). Ninguna fila usa una redacción idéntica de "aplica porque" para más de un hallazgo sin justificación específica; ninguna fila trata una obligación condicionada como prohibición absoluta (Anexo §16, "errores a evitar").
**Evidencia que lo demuestra:** `reporte/matriz_correlacion.csv`, columnas "Aplica porque" y "Evidencia requerida".
**Dependencias:** REQ-F-01, REQ-F-06.

### REQ-F-06 — Corpus normativo consultable (MCP capa 3)
**Criterio de rúbrica:** F (soporta B también)
**Banda objetivo:** 13–14/14
**Descripción:** Servidor MCP de solo lectura que expone el corpus normativo (ISO/IEC 27001:2022 Anexo A, NIST CSF 2.0, CIS v8, normativa CL) para que COMPLIANCE consulte controles específicos en vez de que el modelo los recuerde de memoria.
**Criterio de aceptación (verificable):** "Al menos un servidor MCP en uso real" (rúbrica B, banda 13–14) aplicado al dominio normativo: una consulta real al servidor por un control ISO/NIST/CIS retorna el texto/identificador correcto, verificable contra la fuente.
**Evidencia que lo demuestra:** `mcp/` (configuración del servidor) + log de al menos una consulta real registrada.
**Dependencias:** ninguna sobre `auditoria/mcp/` en contenido — ver GAP_ANALYSIS §1.1 (capa 3): el andamiaje de `auditoria/mcp/server.py` es reutilizable como plantilla de transporte, el contenido de `mcp/tools.py` no.

### REQ-F-07 — Advertencia de no-asesoría-legal
**Criterio de rúbrica:** F
**Banda objetivo:** 13–14/14
**Descripción:** Todo informe generado cierra con el texto exacto de la advertencia del Anexo §16.
**Criterio de aceptación (verificable):** "Incluye la advertencia de no-asesoría-legal" (rúbrica F, banda 13–14). El texto del informe contiene, sin modificar una palabra, el párrafo del Anexo §16 ("Este documento constituye un análisis técnico de controles de seguridad... la calificación jurídica definitiva... debe ser validada por abogado...").
**Evidencia que lo demuestra:** `reporte/reporte_final.md`, sección de cierre.
**Dependencias:** REQ-G-01 (generación autónoma del reporte).

---

## G — Reporte final generado autónomamente (10 pts; ver nota de inconsistencia de ponderación en la rúbrica, §"Tabla resumen")

### REQ-G-01 — Generación autónoma desde template canónico
**Criterio de rúbrica:** G
**Banda objetivo:** 10/10
**Descripción:** El reporte final se genera por el rol REDACTOR desde datos verificados (hallazgos + matriz), no se redacta a mano, y sigue el template canónico de la Parte V (`reporte/reporte_final.md`, `reporte_final.pdf`, `matriz_correlacion.csv`), extendido con justificación de cualquier adaptación.
**Criterio de aceptación (verificable):** "El reporte se genera desde datos verificados, no se redacta a mano. Sigue el template canónico..." (rúbrica G, banda 10). Regenerar el reporte desde los mismos datos produce un documento equivalente (mismo contenido factual); ninguna sección aparece sin origen trazable a `normalizado/`, hallazgos o matriz.
**Evidencia que lo demuestra:** script/comando de generación + dos ejecuciones sobre los mismos datos comparadas.
**Dependencias:** REQ-D-01, REQ-D-08 (agregación), REQ-F-01 (matriz). Antecedente reutilizable con reestructuración: `auditoria/core/reporter.py` + `auditoria/templates/report.html` (Jinja2) — ver GAP_ANALYSIS §1.1.

### REQ-G-02 — Resumen ejecutivo coherente numéricamente
**Criterio de rúbrica:** G
**Banda objetivo:** 10/10
**Descripción:** Resumen ejecutivo escrito para el comité de gerencia (no técnico), cuyos números coinciden exactamente con las tablas de detalle porque se calculan por agregación (REQ-D-08), no se redactan.
**Criterio de aceptación (verificable):** "Resumen ejecutivo escrito para el comité de gerencia, coherente numéricamente con las tablas de detalle" (rúbrica G, banda 10). Cada cifra del resumen ejecutivo es recalculable desde los datos y coincide.
**Evidencia que lo demuestra:** comparación automática resumen ↔ agregación (mismo validador de CT-05, REQ-D-08).
**Dependencias:** REQ-D-08.

### REQ-G-03 — Priorización de remediación con responsable, esfuerzo y plazo
**Criterio de rúbrica:** G
**Banda objetivo:** 10/10
**Descripción:** El reporte incluye una tabla de priorización de remediación con responsable nominado, esfuerzo estimado y plazo, coherente con la banda de riesgo (Anexo §11).
**Criterio de aceptación (verificable):** "Priorización de remediación con responsable, esfuerzo y plazo" (rúbrica G, banda 10). Cada hallazgo con tratamiento exigido tiene las tres columnas completas y el plazo coincide con el de referencia de su banda de riesgo (Anexo §11) o justifica la desviación.
**Evidencia que lo demuestra:** tabla de priorización en `reporte/reporte_final.md`.
**Dependencias:** REQ-E-04 (matriz 5×5), REQ-F-01. Antecedente reutilizable: campo `remediation` de `specs/finding.schema.json` (líneas 153–176, `assigned_to`/`due_date`/`status`) ya tiene la forma correcta; falta poblarlo con datos reales y ligarlo a la banda de riesgo.

### REQ-G-04 — Remediaciones concretas aplicables a la versión instalada
**Criterio de rúbrica:** G
**Banda objetivo:** 10/10
**Descripción:** Ninguna remediación recomienda la misma versión vulnerable ni un componente inexistente (control CT-04).
**Criterio de aceptación (verificable):** "Remediaciones concretas y aplicables a la versión instalada" (rúbrica G, banda 10) — condición idéntica a REQ-D-07; se referencia, no se duplica.
**Evidencia que lo demuestra:** ver REQ-D-07.
**Dependencias:** REQ-D-07.

---

## B — Arquitectura agéntica y extensión propia (14 pts)

### REQ-B-01 — Ocho capas presentes y diferenciadas
**Criterio de rúbrica:** B
**Banda objetivo:** 13–14/14
**Descripción:** Las 8 capas del Anexo §3 existen como componentes diferenciados del repositorio (no mezcladas), mapeadas a carpetas concretas según la Parte V.
**Criterio de aceptación (verificable):** "Las ocho capas están presentes y diferenciadas" (rúbrica B, banda 13–14). Cada capa tiene una carpeta/componente propio, sin que la normalización y el análisis (por ejemplo) ocurran en el mismo módulo — condición explícitamente excluida de la banda 10–12 ("normalización y análisis mezclados").
**Evidencia que lo demuestra:** estructura de repo resultante del diseño de Fase 2, verificada contra `docs/design.md`.
**Dependencias:** todos los REQ de capa (D, F, roles, skills, MCP, harness).

### REQ-B-02 — Roles con alcance, herramientas y prohibiciones declaradas por escrito
**Criterio de rúbrica:** B
**Banda objetivo:** 13–14/14
**Descripción:** Cada uno de los 5 roles tiene un archivo en `roles/` que declara su pregunta, sus herramientas permitidas y sus herramientas explícitamente prohibidas, siguiendo la tabla del Anexo §4.
**Criterio de aceptación (verificable):** Existen 5 archivos en `roles/` (uno por rol), cada uno con las tres secciones (alcance/herramientas/prohibiciones) completas.
**Evidencia que lo demuestra:** `roles/recon.md`, `roles/analista.md`, `roles/verificador.md`, `roles/compliance.md`, `roles/redactor.md`.
**Dependencias:** ninguna directa sobre `auditoria/` — ver GAP_ANALYSIS §1.1 (capa 5): `ai/analyzer.py` es antecedente de prompts, no de arquitectura de rol.

### REQ-B-03 — Separación estructural de actores (VERIFICADOR sin herramientas de escritura)
**Criterio de rúbrica:** B
**Banda objetivo:** 13–14/14
**Descripción:** La separación de actores no depende de una instrucción de system prompt: el runtime rechaza técnicamente cualquier intento del rol VERIFICADOR de invocar una herramienta de escritura, y ese rechazo queda registrado en el ledger.
**Criterio de aceptación (verificable):** "la separación de actores es estructural (al VERIFICADOR no se le entregan herramientas de escritura), no de buena fe" (rúbrica B, banda 13–14). Prueba binaria: se fuerza una llamada de escritura desde el contexto de VERIFICADOR; el mecanismo (hook `PreToolUse` o middleware de validación de tool-calls, según ruta elegida en Fase 2) la rechaza, y aparece una entrada `RECHAZO` en `LEDGER.md` con el motivo.
**Evidencia que lo demuestra:** entrada `RECHAZO` real en `LEDGER.md` producida por un intento real de la prueba (no narrada). Este mismo artefacto sirve para el criterio H (bloque de punto de control humano).
**Dependencias:** REQ-B-02. Decisión de ruta (subagentes de Claude Code vs. harness propio) pendiente para `docs/design.md` — ver GAP_ANALYSIS, "puntos aún abiertos".

### REQ-B-04 — Skills como procedimientos reutilizables e invocables
**Criterio de rúbrica:** B
**Banda objetivo:** 13–14/14
**Descripción:** Las 5 skills del Anexo (`enumerar`, `clasificar`, `correlacionar`, `redactar`, `priorizar`) existen como unidades invocables, con `description`/disparador preciso, y al menos `clasificar` se apoya en un script determinista que aplica la tabla de impacto/probabilidad (Anexo §9–10) por cálculo, no por criterio libre del modelo.
**Criterio de aceptación (verificable):** "Las skills son procedimientos reutilizables e invocables" (rúbrica B, banda 13–14). Cada skill se invoca de forma independiente y produce el mismo resultado ante la misma entrada (determinismo verificable para `clasificar`).
**Evidencia que lo demuestra:** `skills/clasificar/` con script + al menos 2 ejecuciones con el mismo resultado sobre el mismo input.
**Dependencias:** REQ-E-02, REQ-E-03 (tablas de impacto/probabilidad). Verificar contra la documentación vigente de Claude Code Skills el formato correcto antes de escribir archivos (ver GAP_ANALYSIS §1.1, capa 4 — los `.claude/skills/*.md` actuales no usan frontmatter YAML).

### REQ-B-05 — Harness con BoundedLoop (WIP=1, tope, condición de salida)
**Criterio de rúbrica:** B
**Banda objetivo:** 13–14/14
**Descripción:** El orquestador ejecuta una etapa/rol a la vez (WIP=1), con un número máximo de iteraciones y una condición de salida explícita (no un bucle indefinido).
**Criterio de aceptación (verificable):** "El harness aplica BoundedLoop con tope y condición de salida" (rúbrica B, banda 13–14). El código/config del harness declara el tope máximo y la condición de salida; una ejecución de prueba que fuerza el tope se detiene exactamente ahí, registrado en el ledger.
**Evidencia que lo demuestra:** `harness/orquestador.*` + entrada en `LEDGER.md` de una ejecución que alcanzó el tope.
**Dependencias:** ninguna reutilizable directa de `auditoria/scheduler/executor.py` (ver GAP_ANALYSIS §1.1, capa 6 — ese scheduler es re-ejecución periódica por cron, no BoundedLoop de una auditoría).

### REQ-B-06 — Al menos 3 dimensiones de extensión (D1–D8) implementadas y demostradas
**Criterio de rúbrica:** B
**Banda objetivo:** 13–14/14
**Descripción:** **Resuelto (LDG-004, `docs/PROPUESTA_RC_D_VIDEO.md` §2, aprobado sin modificaciones).** El Anexo solo nombra D2 ("rol de contradicción explícita", §4); D1, D3–D8 no aparecen en ningún documento fuente revisado (Anexo, Rúbrica, Instruccion.html, guía Rapid7). El grupo definió las 8 y **se comprometió a implementar D1, D2 y D6**: D1 = re-verificación automatizada con artefacto capturado como alternativa a la firma humana para VALIDADO (texto literal del Anexo §2: "un humano o una re-verificación automatizada con artefacto capturado puede confirmarlo"); D2 = rol de contradicción explícita (Anexo §4); D6 = motor determinista de cálculo de riesgo (script que aplica las tablas de impacto/probabilidad del Anexo §9–10, con tests que fijan el resultado esperado). D3/D4/D5/D7/D8 quedan documentadas como extensiones opcionales adicionales, no como compromiso de entrega.
**Criterio de aceptación (verificable):** "Tres o más dimensiones de extensión (D1–D8) implementadas, documentadas y demostradas en video" (rúbrica B, banda 13–14). D1 se demuestra con al menos un hallazgo VALIDADO por re-verificación automatizada (no firma humana) registrado en el ledger; D2 se demuestra con al menos una objeción real del rol de contradicción que cambie o sostenga el estado de un hallazgo; D6 se demuestra con el script de `clasificar` (REQ-B-04) pasando una suite de tests que fija el resultado esperado para combinaciones conocidas de factores del Anexo §9–10.
**Evidencia que lo demuestra:** `docs/PROPUESTA_RC_D_VIDEO.md` §2 + `LEDGER.md` `LDG-004` + (en implementación) entradas de ledger específicas por cada D demostrada + bloques 5/6 del video (REQ-H-02).
**Dependencias:** REQ-D-03 (D1), REQ-B-02 (D2), REQ-B-04/REQ-E-02/REQ-E-03 (D6).

---

## E — Clasificación de riesgo y matriz impacto × probabilidad (12 pts)

### REQ-E-01 — CVSS con vector completo por hallazgo
**Criterio de rúbrica:** E
**Banda objetivo:** 11–12/12
**Descripción:** Cada hallazgo con severidad técnica declarada incluye el vector CVSS 3.1 completo, no solo el número base.
**Criterio de aceptación (verificable):** "Distingue explícitamente severidad técnica (CVSS con vector completo)..." (rúbrica E, banda 11–12). Ningún hallazgo publica un número CVSS sin su vector (p. ej. `AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H`).
**Evidencia que lo demuestra:** ficha de hallazgo en `reporte/reporte_final.md` y columna correspondiente en la matriz.
**Dependencias:** REQ-F-06 (o fuente CVSS equivalente vía MCP).

### REQ-E-02 — Cálculo de impacto por factores declarados (Anexo §9)
**Criterio de rúbrica:** E
**Banda objetivo:** 11–12/12
**Descripción:** El impacto (escala 1–5) se calcula sumando los 5 factores de la tabla del Anexo §9 (confidencialidad, integridad, disponibilidad, datos personales, criticidad operacional), no se asigna a criterio libre.
**Criterio de aceptación (verificable):** "Impacto... se derivan de factores declarados y trazables a fuente" (rúbrica E, banda 11–12). Cada valor de impacto publicado es reproducible aplicando la tabla del Anexo §9 a los factores declarados del hallazgo.
**Evidencia que lo demuestra:** script de cálculo (candidato a vivir dentro de la skill `clasificar`, REQ-B-04) + ficha de hallazgo con los 5 factores explícitos.
**Dependencias:** ninguna sobre `auditoria/` (el schema actual solo tiene `severity` como enum fijo, sin factores).

### REQ-E-03 — Cálculo de probabilidad por factores declarados, con `NO_DISPONIBLE` donde falte EPSS/KEV (Anexo §10)
**Criterio de rúbrica:** E
**Banda objetivo:** 11–12/12
**Descripción:** La probabilidad (escala 1–5) se calcula sumando los 5 factores de la tabla del Anexo §10; si el entorno aislado no tiene EPSS/KEV offline, ese factor se declara `NO_DISPONIBLE` y se justifica el valor asignado por los factores restantes (nota de laboratorio, Anexo §10).
**Criterio de aceptación (verificable):** Cada valor de probabilidad publicado es reproducible aplicando la tabla del Anexo §10; todo factor `NO_DISPONIBLE` tiene su justificación escrita junto al hallazgo.
**Evidencia que lo demuestra:** mismo script de cálculo que REQ-E-02, extendido a probabilidad.
**Dependencias:** REQ-D-10 (marcador `NO_DISPONIBLE`).

### REQ-E-04 — Matriz 5×5 con bandas y umbral de apetito de riesgo del cliente
**Criterio de rúbrica:** E
**Banda objetivo:** 11–12/12
**Descripción:** Matriz 5×5 (Anexo §11) con las 5 bandas (Bajo/Medio/Alto/Crítico/Inaceptable) y el umbral de aceptación declarado contra el apetito de riesgo del cliente (Anexo §11, "no acepta riesgo residual ≥ 15 en activos que traten datos personales").
**Criterio de aceptación (verificable):** "La matriz 5×5 tiene bandas y umbral de aceptación declarados contra el apetito de riesgo del cliente" (rúbrica E, banda 11–12). El umbral está escrito explícitamente y cada hallazgo que lo cruza está marcado para escalamiento.
**Evidencia que lo demuestra:** sección de matriz de riesgo en `reporte/reporte_final.md`.
**Dependencias:** REQ-E-02, REQ-E-03.

### REQ-E-05 — Riesgo residual reportado junto al inherente
**Criterio de rúbrica:** E
**Banda objetivo:** 11–12/12
**Descripción:** Cada hallazgo reporta riesgo inherente y riesgo residual (recalculado suponiendo aplicado el control propuesto), no solo el inherente.
**Criterio de aceptación (verificable):** Cada fila de la matriz de correlación tiene ambas columnas (Riesgo, Riesgo residual) con valores numéricos, no vacías.
**Evidencia que lo demuestra:** `reporte/matriz_correlacion.csv`, columnas Riesgo / Riesgo residual.
**Dependencias:** REQ-E-04, REQ-G-03.

### REQ-E-06 — Divergencia CVSS/riesgo contextual justificada por escrito (>1 banda)
**Criterio de rúbrica:** E
**Banda objetivo:** 11–12/12
**Descripción:** Cuando la banda CVSS y la banda de riesgo contextual difieren en más de un nivel, el hallazgo incluye una justificación escrita siguiendo el patrón del Anexo §12 (no una frase genérica tipo "se considera menos riesgoso por el contexto").
**Criterio de aceptación (verificable):** "Cuando CVSS y riesgo contextual divergen en más de una banda, la divergencia está justificada por escrito" (rúbrica E, banda 11–12). Todo hallazgo con divergencia >1 banda tiene un párrafo de justificación que cita un hallazgo o control concreto como sustento (no una estimación), replicando el patrón del ejemplo aceptable del Anexo §12.
**Evidencia que lo demuestra:** ficha de hallazgo correspondiente en `reporte/reporte_final.md`.
**Dependencias:** REQ-E-01, REQ-E-04.

---

## C — Workflow de auditoría declarado y ejecutado (10 pts)

### REQ-C-01 — Workflow completo de 10 etapas declarado y justificado
**Criterio de rúbrica:** C
**Banda objetivo:** 10/10
**Descripción:** El workflow de 10 etapas del Anexo §2 se declara por escrito (encargo → criterio → planificación → recolección → verificación → evaluación de riesgo → correlación → reporte → comunicación → seguimiento), justificando cada etapa contra una referencia reconocida.
**Criterio de aceptación (verificable):** "Declara un workflow completo del proceso de auditoría... Justifica las etapas contra una referencia reconocida (ISO 19011, NIST SP 800-115, PTES, OSSTMM)" (rúbrica C, banda 10). El README/documento de arquitectura enumera las 10 etapas, cada una con su referencia normativa/técnica citada.
**Evidencia que lo demuestra:** `README.md` (sección de arquitectura, a reescribir) o `docs/design.md`.
**Dependencias:** ninguna directa; documento puramente descriptivo.

### REQ-C-02 — Criterio de auditoría declarado antes de ejecutar
**Criterio de rúbrica:** C
**Banda objetivo:** 10/10
**Descripción:** Antes de la primera recolección, se declara contra qué se audita: ISO/IEC 27001:2022 Anexo A + NIST CSF 2.0 + normativa chilena aplicable al cliente (Anexo §1).
**Criterio de aceptación (verificable):** "Confunde auditoría con pentest: no declara criterio contra el cual auditar" es explícitamente la banda 4–6 (a evitar); la banda 10 exige lo contrario. El criterio de auditoría existe como documento fechado *antes* de la primera entrada `HALLAZGO` en `LEDGER.md` (verificable por orden cronológico de las entradas).
**Evidencia que lo demuestra:** documento de criterio de auditoría + comparación de timestamps con el ledger.
**Dependencias:** precede a G0 (REQ-A-01).

### REQ-C-03 — El workflow ejecutado coincide con el declarado
**Criterio de rúbrica:** C
**Banda objetivo:** 10/10
**Descripción:** Cada etapa efectivamente ejecutada se puede rastrear en `LEDGER.md` en el mismo orden y con el mismo actor que declara el workflow de REQ-C-01; cualquier desviación se documenta.
**Criterio de aceptación (verificable):** "El workflow ejecutado coincide con el declarado" (rúbrica C, banda 10). Las entradas de `LEDGER.md`, ordenadas cronológicamente, siguen la secuencia de etapas declarada sin saltos no justificados.
**Evidencia que lo demuestra:** `LEDGER.md` completo al cierre del proyecto.
**Dependencias:** REQ-C-01, todos los REQ de gates.

---

## A — Alcance, autorización y reglas de compromiso del pipeline (8 pts)

### REQ-A-01 — `scope/alcance.yaml` con IP única autorizada (192.168.56.117)
**Criterio de rúbrica:** A
**Banda objetivo:** 8/8
**Descripción:** Archivo `scope/alcance.yaml` que declara el activo (Metasploitable2, representando a `SRV-ADM-01` de Comercial Andes Sur SpA — `docs/Instruccion.html` líneas 2837–2842), IP (`192.168.56.117`, LDG-002), red, ventana horaria y restricciones. Es la **única** fuente de la IP autorizada — ningún otro archivo la hardcodea.
**Criterio de aceptación (verificable):** "Declara alcance completo (activo, IP, red, ventana, restricciones) y criterio de auditoría adoptado" (rúbrica A, banda 8). `scope/alcance.yaml` existe con todos los campos; un `grep` de la IP en el resto del repo solo encuentra referencias que la leen desde este archivo (config/import), nunca un literal duplicado. El campo de respaldo del IP cita `docs/Instruccion.html` (el mecanismo "la IP que Usted vea como asignada") y adjunta una captura propia (`ifconfig`/`ip a` de la instancia de Metasploitable2 del grupo, o config del adaptador host-only) como evidencia de que `192.168.56.117` es el IP efectivamente observado — no una IP declarada sin respaldo.
**Evidencia que lo demuestra:** `scope/alcance.yaml` (a crear en la Fase de implementación) + `evidencias/raw/g0-ifconfig-metasploitable2-192.168.56.117.png` (captura real de `ifconfig` dentro de la VM Metasploitable2 del grupo, mostrando `eth0: inet 192.168.56.117/24`) + `evidencias/manifest.sha256` (hash `5118d84f...4726f105f`) + `LEDGER.md` entrada `LDG-003`.
**Dependencias:** **Resuelto.** `docs/Instruccion.html` (líneas 2738, 2840–2842) confirmó que el mecanismo de autorización de este curso es "la IP que Usted vea como asignada" en su propia instancia de Metasploitable2 — no una lista firmada por el docente con el IP de cada grupo. El grupo aportó la captura real de su entorno (`ifconfig` dentro de Metasploitable2) mostrando `192.168.56.117` en `eth0`; ya está archivada sin editar en `evidencias/raw/`, hasheada en `evidencias/manifest.sha256` y registrada en `LEDGER.md` (`LDG-003`). Lo único pendiente de la Fase de implementación es que `scope/alcance.yaml` cite esta evidencia como origen del IP autorizado — el REQ ya no está bloqueado por falta de respaldo.

### REQ-A-02 — Allowlist versionada + verificación de destino en tiempo de ejecución
**Criterio de rúbrica:** A
**Banda objetivo:** 8/8
**Descripción:** `scope/allowlist.txt` versionado con los comandos permitidos; el harness verifica en tiempo de ejecución que el destino de cualquier comando coincide con la IP de `scope/alcance.yaml`, abortando si no.
**Criterio de aceptación (verificable):** "Existe allowlist versionada y verificación de destino en tiempo de ejecución" (rúbrica A, banda 8). Una prueba negativa contra un destino no autorizado (Anexo, criterio de cierre de G0) aborta correctamente y queda registrada en `LEDGER.md` como `RECHAZO`.
**Evidencia que lo demuestra:** `scope/allowlist.txt` + entrada `RECHAZO` real en `LEDGER.md` de la prueba negativa.
**Dependencias:** REQ-A-01.

### REQ-A-03 — Declaración ética firmada por todos los integrantes
**Criterio de rúbrica:** A
**Banda objetivo:** 8/8
**Descripción:** `scope/declaracion_etica.md` firmada (nombre + fecha) por cada integrante del grupo.
**Criterio de aceptación (verificable):** "La declaración ética está firmada por todos los integrantes" (rúbrica A, banda 8). El archivo existe y tiene una firma por cada miembro declarado del grupo.
**Evidencia que lo demuestra:** `scope/declaracion_etica.md`.
**Dependencias:** ninguna.

### REQ-A-04 — Reglas de compromiso RC-1 a RC-6 implementadas y demostradas
**Criterio de rúbrica:** A
**Banda objetivo:** 8/8
**Descripción:** **Resuelto (LDG-004, `docs/PROPUESTA_RC_D_VIDEO.md` §1, aprobado sin modificaciones).** Ni `docs/anexo_tecnico_u3.md`, ni `docs/rubrica_evaluacion_u3.md`, ni `docs/Instruccion.html`, ni la guía Rapid7 de Metasploitable definían "RC-1 a RC-6" — se verificó exhaustivamente en los cuatro. El grupo las definió como decisión propia, amparada en la cláusula del Anexo Parte I ("cada grupo puede modificarlo, pero debe justificar cada modificación"), citando NIST SP 800-115/PTES/OSSTMM (ya referenciadas por el Anexo §1) y las restricciones explícitas del cliente en `docs/Instruccion.html`: RC-1 alcance exclusivo a `192.168.56.117`, RC-2 ventana de trabajo acotada, RC-3 prohibición de explotación activa/interrupción de servicio, RC-4 condición de aborto, RC-5 confidencialidad de evidencia, RC-6 escalamiento ante hallazgo crítico o incidente.
**Criterio de aceptación (verificable):** "Las seis reglas de compromiso RC-1 a RC-6 están implementadas y demostradas, no solo declaradas" (rúbrica A, banda 8). RC-1, RC-3 y RC-4 se verifican por mecanismo automático (allowlist + verificación de destino + BoundedLoop, REQ-A-02/REQ-B-05); RC-2, RC-5 y RC-6 se verifican por evidencia de cumplimiento documentada (declaración firmada + registro en ledger cuando aplique), no por un validador de software — distinción explícita en `docs/PROPUESTA_RC_D_VIDEO.md` §1, nota de diseño.
**Evidencia que lo demuestra:** `docs/PROPUESTA_RC_D_VIDEO.md` §1 + `LEDGER.md` `LDG-004` + (en implementación) `roles/`/`harness/` citando cada RC por ID.
**Dependencias:** REQ-A-01, REQ-A-02.

---

## H — Video: demostración y punto de control humano (10 pts)

### REQ-H-01 — Captura demostrable de un rechazo real del sistema agéntico
**Criterio de rúbrica:** H
**Banda objetivo:** 10/10
**Descripción:** El video debe mostrar un error concreto del propio pipeline (no cosmético) y su registro en el ledger — no basta con narrar el punto de control humano.
**Criterio de aceptación (verificable):** "El bloque del punto de control humano muestra un error concreto del sistema agéntico, la razón del rechazo y su registro en el ledger" (rúbrica H, banda 10). El artefacto de REQ-B-03 (rechazo real de VERIFICADOR intentando escribir) es el candidato natural para este bloque; se reutiliza, no se fabrica un error nuevo para la cámara.
**Evidencia que lo demuestra:** misma entrada `RECHAZO` de REQ-B-03, mostrada en pantalla durante la grabación.
**Dependencias:** REQ-B-03.

### REQ-H-02 — Estructura de seis bloques del video
**Criterio de rúbrica:** H
**Banda objetivo:** 10/10
**Descripción:** **Resuelto (LDG-004, `docs/PROPUESTA_RC_D_VIDEO.md` §3, aprobado sin modificaciones).** El Anexo solo identifica explícitamente el bloque 4 ("bloque 4 del video" = ejemplo del ledger, §6, línea 140); los otros cinco no están enumerados en ningún documento fuente revisado. El grupo definió los 6: (1) presentación e identificación de integrantes, (2) arquitectura del pipeline (8 capas/5 roles), (3) ejecución real en pantalla, (4) punto de control humano — el mismo artefacto de REQ-B-03/REQ-H-01, anclado por el Anexo, (5) reporte final y firma humana en G5, (6) cierre y autocrítica del sistema.
**Criterio de aceptación (verificable):** "Los seis bloques de la estructura exigida están presentes y en proporción" (rúbrica H, banda 10). El video contiene los 6 bloques en el orden de `docs/PROPUESTA_RC_D_VIDEO.md` §3, cada uno con tiempo no nulo; el bloque 4 muestra el rechazo real de REQ-B-03 con su entrada en `LEDGER.md` visible en pantalla; el bloque 6 reconoce explícitamente al menos una limitación real del sistema (no "nuestro agente no cometió errores", Anexo Parte VI).
**Evidencia que lo demuestra:** `docs/PROPUESTA_RC_D_VIDEO.md` §3 + `LEDGER.md` `LDG-004` + el video final (fuera del alcance de este repositorio de especificación).
**Evidencia que lo demuestra:** N/A hasta resolver la suposición pendiente.
**Dependencias:** bloqueado.

---

## Tabla de trazabilidad REQ ↔ Criterio de rúbrica ↔ Gate

| REQ | Criterio | Gate | Estado |
|---|---|---|---|
| REQ-D-01 | D | G1/G2 | Definido |
| REQ-D-02 | D | G1 | Definido |
| REQ-D-03 | D | G3 | Definido |
| REQ-D-04 | D | G5 | Definido |
| REQ-D-05 | D | G3/G5 | Definido |
| REQ-D-06 | D | G5 | Definido |
| REQ-D-07 | D | G5 | Definido |
| REQ-D-08 | D | G5 | Definido |
| REQ-D-09 | D | G3 | Definido |
| REQ-D-10 | D | G3/G5 | Definido |
| REQ-F-01 | F | G4 | Definido |
| REQ-F-02 | F | G4 | Definido |
| REQ-F-03 | F | G4 | Definido |
| REQ-F-04 | F | G4 | Definido |
| REQ-F-05 | F | G4 | Definido |
| REQ-F-06 | F (soporta B) | G4 | Definido |
| REQ-F-07 | F | G5 | Definido |
| REQ-G-01 | G | G5 | Definido |
| REQ-G-02 | G | G5 | Definido |
| REQ-G-03 | G | G5 | Definido |
| REQ-G-04 | G | G5 | Definido |
| REQ-B-01 | B | — (transversal) | Definido |
| REQ-B-02 | B | — (transversal) | Definido |
| REQ-B-03 | B | G3 (demuestra control humano) | Definido |
| REQ-B-04 | B | G3 (clasificar) | Definido |
| REQ-B-05 | B | — (transversal, todas las etapas) | Definido |
| REQ-B-06 | B | — | Resuelto (`LDG-004`) — compromiso de entrega: D1, D2, D6 |
| REQ-E-01 | E | G3 | Definido |
| REQ-E-02 | E | G3 | Definido |
| REQ-E-03 | E | G3 | Definido |
| REQ-E-04 | E | G3 | Definido |
| REQ-E-05 | E | G3/G4 | Definido |
| REQ-E-06 | E | G3 | Definido |
| REQ-C-01 | C | G0 | Definido |
| REQ-C-02 | C | G0 | Definido |
| REQ-C-03 | C | — (transversal, verificado al cierre) | Definido |
| REQ-A-01 | A | G0 | Resuelto — evidencia real capturada (`LDG-003`); falta solo escribir `scope/alcance.yaml` citándola (Fase de implementación) |
| REQ-A-02 | A | G0 | Definido (depende de REQ-A-01) |
| REQ-A-03 | A | G0 | Definido |
| REQ-A-04 | A | G0 | Resuelto (`LDG-004`) |
| REQ-H-01 | H | G3 (mismo artefacto) | Definido |
| REQ-H-02 | H | — | Resuelto (`LDG-004`) |

**Cobertura:** todos los criterios A–H tienen al menos un REQ. Los criterios I (revisión cruzada) y J (defensa oral) no generan REQ en esta fase porque dependen de entregables de otros grupos / de una instancia presencial posterior, no de brechas de este repositorio.

**Fase 1 cerrada al 100%.** Los cuatro bloqueos originales quedaron resueltos: REQ-A-01 mediante `docs/Instruccion.html` (fuente del mecanismo de IP) + captura real (`LEDGER.md` `LDG-003`); REQ-A-04, REQ-B-06 y REQ-H-02 mediante `docs/PROPUESTA_RC_D_VIDEO.md`, definición propia del grupo aprobada sin modificaciones (`LEDGER.md` `LDG-004`), después de verificar exhaustivamente que ninguno de los cuatro documentos fuente disponibles (Anexo, Rúbrica, Instruccion.html, guía Rapid7 de Metasploitable) definía "RC-1 a RC-6", el listado D1–D8 o la estructura de 6 bloques del video. Ningún contenido se inventó atribuyéndolo al Anexo — cada uno queda explícitamente marcado como decisión del grupo, con su propia referencia externa citada, conforme a la regla transversal: "si no puedes citarla, es una suposición tuya y debes marcarla como tal."

Siguiente paso: Fase 2 (`docs/design.md`).
