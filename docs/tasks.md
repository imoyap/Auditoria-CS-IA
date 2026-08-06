# tasks.md — Plan de tareas (Fase 3)

**Fuente:** `docs/design.md`, `docs/requirements.md`.
**Regla de orden:** las tareas están numeradas por **dependencia real de construcción** (nada puede ejecutarse sin `scope/alcance.yaml`; ningún hallazgo puede clasificarse sin evidencia cruda; ningún reporte puede redactarse sin hallazgos cerrados). Dentro de cada bloque que no tiene una dependencia técnica estricta entre sí, se respeta la prioridad de puntaje del prompt original: **D → F → G → B → E → C → A → H**. Donde una tarea de bajo peso en rúbrica (p. ej. A) es un prerequisito estructural de una de alto peso (p. ej. D no puede empezar sin G0), se anota explícitamente — el peso de puntaje no cambia el orden de construcción.

**Estado:** Fase 4 (BoundedLoop) en curso, WIP=1. Progreso registrado abajo; toda tarea no listada como cerrada sigue `pendiente`. Marcar una tarea como cerrada sin su condición de "hecho" verificada es exactamente el tipo de reconstrucción de trazabilidad que la Parte VI del Anexo señala como error.

### Progreso

| Tarea | Estado | Ledger |
|---|---|---|
| T-001 | **Cerrada** — 12 carpetas creadas, cada una con ≥1 archivo real; verificado con `find` | `LDG-005` |
| T-002 | **Cerrada** — `scope/alcance.yaml` parsea como YAML válido, sin literales de IP duplicados en el resto del repo | `LDG-006` |
| T-003 | **Cerrada** — 8 patrones regex válidos en `scope/allowlist.txt`, sin IP literal; repositorio git inicializado y versionado (commit `298020b`) | `LDG-007..LDG-010` |
| T-004 | **Cerrada** — `scope/declaracion_etica.md` firmado por Mauricio Carrera (único integrante confirmado) | `LDG-011` |
| T-005 | **Cerrada** — ya satisfecha por T-002 (RC-1..RC-6 en `scope/alcance.yaml` con fuente citada); verificación formal aparte | `LDG-012` |
| T-006 | **Cerrada** — 5 archivos `roles/*.md`, cada uno con las 3 secciones exigidas | `LDG-013` |
| T-007 | **Cerrada** — 5 subagentes `.claude/agents/*.md` con `tools`/`disallowedTools` verificados estática y dinámicamente (`claude -p --agent verificador` confirmó el rechazo real de Bash) | `LDG-014`, `LDG-015` |
| T-008 | **Cerrada** — `harness/controles/reject_and_log.sh` probado con 4 payloads reales (3 rechazos + 1 permiso), cada rechazo generó una entrada real en `LEDGER.md` | `LDG-016` |
| T-009 | **Cerrada** — `harness/orquestador.py` probado en 3 escenarios reales: tope de reintentos real (etapa 0 falla porque `ventana_de_trabajo` sigue sin definir), `--continue` se niega a avanzar, `--sign-gate` probado con gate desechable | `LDG-017`, `LDG-018` |
| (ventana real) | `scope/alcance.yaml.ventana_de_trabajo` actualizada con fecha real confirmada por el usuario (2026-08-07 10:00–12:00); etapa 0 del harness ahora pasa de verdad y se detiene esperando G0 | `LDG-020` |
| T-010 | **Cerrada** — `gates/G0.md` con los 7 campos del formato exacto, evidencia real, prueba negativa contra `192.168.56.101` incluida, Firma humana en `[PENDIENTE]` | `LDG-021` |
| **T-011** | **Cerrada — G0 FIRMADO** por Mauricio Carrera (2026-08-06), confirmado explícitamente antes de ejecutar `--sign-gate`. **Bloque 0 completo (T-001..T-011).** | `LDG-022` |
| T-012 | **Cerrada** — skill `enumerar` probada con artefacto de prueba (eliminado después); hash/manifiesto verificados, no-sobrescritura verificada. Sin tocar el objetivo — la ejecución real espera la ventana de mañana | `LDG-023`, `LDG-024` |
| T-017 | **Cerrada** — `mcp/conocimiento_tecnico` verificado con protocolo MCP real vía `claude -p --mcp-config`, no solo en Python | `LDG-025`, `LDG-026` |
| T-018 | **Cerrada** — `mcp/conocimiento_normativo` (corpus tomado del Anexo §14-15) verificado con protocolo MCP real, incluido el caso NO_OBSERVADO | `LDG-027` |
| T-019 | **Cerrada** — skill `clasificar` (motor D6): 12/12 verificaciones exactas contra los 2 ejemplos numéricos del Anexo §15; falla explícita ante factor faltante | `LDG-028` |
| T-020 | **Cerrada** — CT-02 probado reproduciendo el ejemplo literal del Anexo §6 (wordpress no encontrado → rechazo) | `LDG-029` |
| T-022 | **Cerrada** — skill `registrar_veto` probada: RECHAZO válido se anexa, `--tipo HALLAZGO` rechazado por argparse | `LDG-030`, `LDG-031` |
| T-023 | **Cerrada** — CT-06 probado en 3 casos (fallo de red+VALIDADO→rechazo, fallo de red+INCONCLUSO→permite, sin fallo+VALIDADO→permite) | `LDG-032` |
| T-028 | **Cerrada** — CT-03 probado: consistente→OK, divergente→rechazo citando check_id y valores | `LDG-033` |
| T-031 | **Cerrada** — CT-04 probado reproduciendo el error real de CertEngine (misma versión) → rechazo; versión distinta → permite | `LDG-034` |
| T-032 | **Cerrada** — CT-05 lógica verificada (consistente/discrepante); hallazgo de entorno documentado (encoding de acentos en pipes de git-bash) | `LDG-035`, `LDG-036` |
| T-035 | **Cerrada** — CT-01 y CT-07, ambos con 3 casos reales cada uno; CT-01 probado con la evidencia real de G0 (no ficticia) | `LDG-037`, `LDG-038` |
| T-026 | **Cerrada** — skill `correlacionar` probada con el Ejemplo 1 del Anexo (Telnet); reintento sobre mismo ID rechazado (protege severidad) | `LDG-039` |
| T-030 | **Cerrada** — skill `priorizar` probada con los riesgos residuales exactos de los 2 ejemplos del Anexo (orden y plazo correctos) | `LDG-040` |
| T-033 | **Cerrada** — skill `redactar`: determinismo verificado (diff vacío), advertencia legal comparada programáticamente contra el Anexo (coincide exacto) | `LDG-041` |
| T-037, T-038 | **Cerradas** — workflow de 10 etapas documentado en README.md con justificación normativa; criterio de auditoría verificado anterior al primer HALLAZGO real | `LDG-042` |
| **T-013** | **Cerrada — EJECUCIÓN REAL contra 192.168.56.117.** RECON ejecutó nmap real (30 puertos abiertos, incluye vsftpd 2.3.4 y Telnet — los mismos casos del Anexo §15, ahora con evidencia real). Encontró y forzó la corrección de 2 bugs arquitectónicos reales en el camino (Bash ausente para 4 roles; filtro de metacaracteres bloqueaba heredocs legítimos) | `LDG-044` a `LDG-049` |
| **T-014** | **G1 CERRADO.** Bug real encontrado y corregido en el camino: Python en Windows corrompía manifest.sha256 con \r colgantes (newline="" agregado a 3 scripts) | `LDG-050`, `LDG-051` |
| **T-015** | **G2 CERRADO.** `normalizado/inventario.json` real: 30 servicios, 0 sin línea de origen, verificado cruzado contra el crudo (vsftpd línea 6, telnet línea 10) | `LDG-052` |
| **T-021** | **4 candidatos reales propuestos por ANALISTA** (H-01 bindshell, H-02 vsftpd/CVE-2011-2523, H-03 UnrealIRCd/CVE-2010-2075, H-04 distccd/CVE-2004-2687), CWE vía MCP real, todos en estado PROPUESTO | `LDG-053`, `LDG-054` |
| **T-024, T-025** | **VERIFICADOR real revisó los 4 candidatos citando línea de origen**: H-01 bindshell → `VALIDADO_PROPUESTO` (dos artefactos independientes, L38+L39, sin explotación); H-02 vsftpd 2.3.4 → `OBSERVADO` (veto explícito a la elevación, coincide con Ejemplo 2 del Anexo §15); H-03 UnrealIRCd → `INCONCLUSO` (veto por CT-02: versión no confirmada en evidencia, CVE no sostenible); H-04 distccd → `OBSERVADO` (artefacto único, sin segunda sonda). Bug real encontrado y corregido antes de la invocación: `registrar_veto.py` no actualizaba `estado` en `candidatos.json`. Persistencia verificada exacta. **T-025 (cierre de G3) queda pendiente de firma humana** — H-01 permanece en `VALIDADO_PROPUESTO`, no se auto-firma | `LDG-055`, `LDG-056` |
| **T-024b** | **Gap real corregido**: G3 exige "vector CVSS completo" y ningún script lo producía. Construido `corpus_cvss.json` citando NVD real (CVE-2011-2523 v3.1, CVE-2004-2687 v2.0 — NVD no publica v3.1 para éste, no se inventó equivalencia), tool `buscar_cvss` agregada al MCP y probada vía protocolo real (3 casos, incluido CVE inexistente → `NO_OBSERVADO`). `candidatos.json` actualizado: H-02/H-04 con vector real, H-01/H-03 en `NO_OBSERVADO` justificado (sin CVE numerado / CVE vetado por CT-02) | `LDG-057`, `LDG-058` |
| **T-025** | **G3 FIRMADO** por Mauricio Carrera (2026-08-06), confirmado explícitamente antes de ejecutar `--sign-gate`. Gap real encontrado y corregido en el camino: `cmd_sign_gate` no tenía ninguna ruta de código que promoviera `VALIDADO_PROPUESTO` a `VALIDADO` literal — se agregó `_promover_validado_propuesto()`, la única función de todo el pipeline que puede escribir ese literal, y solo se ejecuta como consecuencia directa de la firma humana. Probada en copia desechable antes de usarla sobre datos reales. H-01 quedó `VALIDADO` (único), H-02/H-04 `OBSERVADO`, H-03 `INCONCLUSO` — verificado exacto contra `normalizado/candidatos.json`. **Bloque de clasificación (T-021, T-024, T-024b, T-025) completo.** | `LDG-HARNESS` (firma + promoción, ver últimas 2 líneas de `LEDGER.md`) |
| **T-027** | **COMPLIANCE real correlacionó los 4 hallazgos de G3** contra ISO 27001 Anexo A / NIST CSF 2.0 / CIS v8 / normativa CL, consultando `mcp__conocimiento-normativo` de verdad (controles citados verificados uno a uno contra `corpus_normativo.json`, ninguno inventado). H-03 (INCONCLUSO) siguió la regla de `LDG-059`: sin remediación ni plazo sobre un hallazgo no confirmado, solo una recomendación de ampliar el alcance. `normalizado/matriz_borrador.csv`: 4 filas, 22 columnas (coincide exacto con la tabla literal del Anexo §13), cero celdas vacías sin marcador | `LDG-059`, `LDG-060` |
| **T-029** | **G4 CERRADO** (APPROVE, sin firma humana — Anexo §2 solo exige firma en G0/G3/G5). Los 4 hallazgos tienen Control_ISO/NIST/Control_CIS/Aplica_porque no vacíos, cada uno con Evidencia_requerida declarada; sin mapeo repetido sin justificación distinta (evita el error de la Parte VI del Anexo). **Bloque de correlación normativa (T-026, T-027, T-029) completo.** | `LDG-061` |
| **T-034** | **REDACTOR real produjo `reporte/reporte_final.md` y `reporte/matriz_correlacion.csv`.** Dos bugs reales encontrados y corregidos antes de invocar (revisión de código, no ejecución): severidad "Crítica" nunca se contaba por la í acentuada rompiendo el prefijo ASCII; y ningún script producía `matriz_correlacion.csv` (REDACTOR no tiene `Write` ni `cp`). Verificado independientemente: resumen ejecutivo 4 hallazgos con bandas consistentes (suma = Total), advertencia legal coincide byte a byte con el Anexo §16, matriz con `Plazo_referencia` real (90 días para los 3 confirmados, `NO_OBSERVADO` para H-03) | `LDG-062`, `LDG-063`, `LDG-064` |
| **T-035** | **CT-01 y CT-07 ejecutados sobre el reporte real de T-034** (distinto de la prueba genérica anterior con datos ficticios). CT-01: 4 afirmaciones, todas con `evidence_id=01_nmap_full`, las 4 resuelven contra `evidencias/manifest.sha256` → exit 0. CT-07: 4 filas de `matriz_correlacion.csv` (23 columnas cada una), cero campos vacíos sin marcador → exit 0 en las 4 | `LDG-065` |

---

## Bloque 0 — Gobernanza mínima (prerequisito de todo; G0 no cierra sin esto)

| ID | Tarea | REQ | Condición de "hecho" verificable |
|---|---|---|---|
| T-001 | Crear la estructura de carpetas de la Parte V del Anexo (`scope/`, `roles/`, `.claude/agents/`, `.claude/skills/`, `mcp/`, `harness/`, `evidencias/`, `normalizado/`, `gates/`, `reporte/`) | REQ-B-01 | `find` sobre el repo muestra las 10 carpetas; ninguna está vacía de un archivo placeholder mínimo (`.gitkeep` o README de la carpeta) |
| T-002 | Escribir `scope/alcance.yaml` con activo (Metasploitable2/`SRV-ADM-01`), IP `192.168.56.117`, ventana horaria, restricciones (sin explotación activa/interrupción de servicio), y campo de respaldo citando `docs/Instruccion.html` + `evidencias/raw/g0-ifconfig-metasploitable2-192.168.56.117.png` | REQ-A-01 | El archivo existe y parsea como YAML válido; `grep -r "192.168.56.117"` en el resto del repo solo encuentra referencias que importan/leen este archivo, ningún literal duplicado |
| T-003 | Escribir `scope/allowlist.txt` versionado con los comandos permitidos (`nmap`, `nc`, `curl`, `nikto` con flags fijos, no destructivos) | REQ-A-02 | El archivo existe versionado en git; el harness (T-008) lo lee para validar cada comando de RECON |
| T-004 | Escribir `scope/declaracion_etica.md` y recolectar firma (nombre + fecha) de cada integrante | REQ-A-03 | El archivo tiene una firma por cada integrante declarado del grupo |
| T-005 | Trasladar RC-1 a RC-6 (`docs/PROPUESTA_RC_D_VIDEO.md` §1, aprobadas en `LDG-004`) a `scope/alcance.yaml` como campo `reglas_de_compromiso`, cada una con su ID | REQ-A-04 | Las 6 reglas aparecen en `scope/alcance.yaml` citando la fuente (NIST SP 800-115/PTES/OSSTMM) de `docs/PROPUESTA_RC_D_VIDEO.md` §1 |
| T-006 | Escribir `roles/<rol>.md` (5 archivos) documentando en lenguaje humano el alcance, herramientas y prohibiciones de cada rol, según la tabla de `docs/design.md` §a.2 | REQ-B-02 | Existen los 5 archivos, cada uno con las 3 secciones completas |
| T-007 | Escribir `.claude/agents/<rol>.md` (5 subagentes) con `tools`/`disallowedTools` exactos de `docs/design.md` §a.2 | REQ-B-02, REQ-B-03 | Un intento de invocar `Bash` desde el contexto de `analista`, `verificador`, `compliance` o `redactor` falla con el error de Claude Code ("agent would be spawned with zero tools" o rechazo en ejecución), no con una instrucción de system prompt ignorable |
| T-008 | Escribir `harness/controles/reject_and_log.sh` (hook `PreToolUse`) y cablearlo en el frontmatter `hooks:` de cada subagente de escritura restringida | REQ-B-03 | Forzar una llamada de escritura desde `verificador` produce una entrada `RECHAZO` real en `LEDGER.md` con `ref:hook`, y la operación no se ejecuta (código de salida 2 confirmado en el log del hook) |
| T-009 | Escribir `harness/orquestador.py`: BoundedLoop WIP=1, tope de 30 iteraciones, condición de salida, mecanismo `--sign-gate`/`--continue` de `docs/design.md` | REQ-B-05 | Una ejecución de prueba que fuerza el tope de reintentos en una etapa se detiene exactamente ahí y queda registrada en `LEDGER.md`; `orquestador.py --continue` antes de firmar un gate vuelve a detenerse en la misma etapa sin avanzar |
| T-010 | Escribir `gates/G0.md` con el criterio de cierre del Anexo §5 y la evidencia de T-002/T-003/T-004/T-005 | REQ-A-01, REQ-A-02, REQ-A-03, REQ-A-04 | El archivo sigue el formato exacto del Anexo §5; el campo `Firma humana` está en `[PENDIENTE]` hasta que un humano lo firme explícitamente |
| **T-011** | **Cerrar G0**: firma humana real sobre `gates/G0.md`, veredicto declarado | REQ-A-01..04 (gate) | `gates/G0.md` tiene `Firma humana: [nombre, fecha]` real (no `[PENDIENTE]`) y una entrada `GATE` en `LEDGER.md` referenciándolo. **Bloqueante: ninguna tarea del Bloque 1 en adelante que implique ejecutar comandos contra `192.168.56.117` puede iniciar antes de este cierre** |

---

## Bloque 1 — Recolección y normalización (capas 1–2; prerequisito de D)

| ID | Tarea | REQ | Condición de "hecho" verificable |
|---|---|---|---|
| T-012 | Escribir `.claude/skills/enumerar/SKILL.md` + `scripts/registrar_evidencia.py` (captura cruda → hash → `evidencias/manifest.sha256`) | REQ-D-01, REQ-D-02 | Ejecutar el script sobre una salida de prueba produce un archivo en `evidencias/raw/` cuyo hash coincide con la línea añadida al manifiesto |
| T-013 | RECON ejecuta la recolección real contra `192.168.56.117` con los comandos de `scope/allowlist.txt` (tras G0 cerrado) | REQ-D-01, REQ-D-02 | `evidencias/raw/` contiene artefactos crudos reales de esta ejecución (no de `localhost`, ver `docs/GAP_ANALYSIS.md` §0.2); `evidencias/manifest.sha256` verifica sin discrepancias |
| **T-014** | **Cerrar G1**: verificación de que todo artefacto tiene hash+timestamp y no hay comandos fuera de allowlist en el log | REQ-D-01, REQ-D-02 (gate) | `gates/G1.md` cerrado con veredicto y evidencia; una prueba negativa contra un IP distinto de `192.168.56.117` (p. ej. `192.168.56.101`, el ejemplo de plantilla) aborta y queda como `RECHAZO` en el ledger, demostrando el criterio de cierre |
| T-015 | Generar `normalizado/inventario.json` (JSON canónico) desde `evidencias/raw/`, con puntero a la línea de origen de cada servicio | — (soporte de D vía G2) | Cada servicio del JSON apunta a una línea de un artefacto crudo real; cero servicios sin origen (criterio de cierre G2, Anexo §5) |
| **T-016** | **Cerrar G2** | — (gate) | `gates/G2.md` cerrado con veredicto |

---

## Bloque 2 — Conocimiento (MCP) y skills de análisis/correlación/reporte (soporte de D, E, F, G — prioridad de puntaje)

| ID | Tarea | REQ | Condición de "hecho" verificable |
|---|---|---|---|
| T-017 | Construir `mcp/conocimiento_tecnico/` (corpus CWE offline + tool `consultar_epss_kev` que siempre retorna `NO_DISPONIBLE` con justificación) | REQ-E-01, REQ-D-10 (soporte) | Una consulta real al servidor por un CWE conocido retorna el identificador correcto; una consulta de EPSS/KEV retorna el marcador `NO_DISPONIBLE`, nunca un valor inventado |
| T-018 | Construir `mcp/conocimiento_normativo/` (corpus ISO 27001:2022 Anexo A, NIST CSF 2.0, CIS v8, normativa CL) | REQ-F-06 | Una consulta real por un control ISO/NIST/CIS retorna el identificador correcto verificable contra la fuente; ausencia de coincidencia retorna `NO_OBSERVADO`, no una aproximación |
| **T-019** | Escribir `.claude/skills/clasificar/SKILL.md` + `scripts/calcular_riesgo.py` (tablas Anexo §9–11) | REQ-E-02, REQ-E-03, REQ-E-04, REQ-B-04, D6 (`LDG-004`) | Suite de tests fija el resultado esperado para al menos 3 combinaciones de factores conocidas del Anexo (los 3 ejemplos de §15); el script las reproduce exactamente |
| T-020 | Escribir CT-02 (`harness/controles/ct02_inferencia.py`) e integrarlo como paso obligatorio dentro de `clasificar` antes de admitir un candidato | REQ-D-05 | Un candidato cuyo producto/versión no aparece literalmente en el artefacto crudo referenciado es rechazado automáticamente, con entrada `RECHAZO` en el ledger citando la ausencia de la cadena |
| T-021 | ANALISTA ejecuta `clasificar` sobre `normalizado/inventario.json`, produce candidatos en `normalizado/candidatos.json` | REQ-D-03 (base) | Cada candidato tiene entrada `HALLAZGO` en `LEDGER.md` con `evidence_id`; ninguno tiene `estado=VALIDADO` en este punto (el schema del candidato no acepta ese valor todavía) |
| T-022 | Escribir `.claude/skills/registrar_veto/SKILL.md` (único canal de escritura de VERIFICADOR) | REQ-B-03 (soporte) | El script solo acepta escribir entradas `RECHAZO`/`DECISION`; un intento de pasarle `estado=VALIDADO` como parámetro falla en el propio script, no solo en el prompt |
| T-023 | Escribir CT-06 (`ct06_red.py`) e integrarlo en la verificación adicional de VERIFICADOR | REQ-D-09 | Un caso de prueba con fallo de conectividad simulado produce `estado=INCONCLUSO` sin excepción, incluso si el intento original sugería algo distinto |
| T-024 | VERIFICADOR revisa cada candidato de T-021: confirma con verificación adicional capturada (no solo el indicio original) → VALIDADO / OBSERVADO / INCONCLUSO | REQ-D-03 | Todo hallazgo en VALIDADO tiene un segundo `evidence_id` (distinto del original) referenciado; ver ejemplo de referencia del Anexo §15 (Telnet=VALIDADO con `nc`, vsftpd=OBSERVADO sin explotación) |
| T-024b | Corregir gap real encontrado en revisión de G3 (`LDG-057`): construir `mcp/conocimiento_tecnico/corpus_cvss.json` citando NVD para los CVE en juego, agregar tool `buscar_cvss` al MCP, y persistir `Vector_CVSS` en cada candidato de `normalizado/candidatos.json` | REQ-E-01 | Cada candidato con CVE sostenido por evidencia tiene vector CVSS 3.1 completo con fuente citada (NVD); el candidato con CVE vetado por VERIFICADOR (H-03, CT-02) tiene `Vector_CVSS=NO_OBSERVADO` explícito, no un vector inventado |
| **T-025** | **Cerrar G3**: firma humana sobre cada VALIDADO | REQ-D-03 (gate) | `gates/G3.md` cerrado; cada hallazgo VALIDADO tiene su propia línea de firma humana o referencia a la firma general del gate, según se defina en el gate |
| T-026 | Escribir `.claude/skills/correlacionar/SKILL.md`, consumiendo `mcp/conocimiento_normativo` | REQ-F-02, REQ-F-03, REQ-F-04, REQ-F-05 | Para una muestra de hallazgos cerrados, ningún mapeo repite el mismo control ISO para más del 50% sin justificación distinta (evita el error de la Parte VI, "todos los hallazgos mapean al mismo control") |
| T-027 | COMPLIANCE ejecuta `correlacionar` sobre los hallazgos de G3, produce `normalizado/matriz_borrador.csv` con las 21 columnas mínimas del Anexo §13 | REQ-F-01 | El CSV existe con una fila por hallazgo y las 21 columnas; ninguna columna vacía sin marcador `NO_OBSERVADO`/`NO_DISPONIBLE` justificado |
| T-028 | Escribir CT-03 (`ct03_severidad.py`) | REQ-D-06 | Un caso de prueba con severidad divergente entre matriz/tabla/ficha es detectado y rechazado |
| **T-029** | **Cerrar G4** | REQ-F-01..05 (gate) | `gates/G4.md` cerrado; cada hallazgo tiene al menos un control ISO, una categoría NIST, un control CIS y la línea "aplica porque" (criterio de cierre literal del Anexo §5) |
| T-030 | Escribir `.claude/skills/priorizar/SKILL.md` (ordena por riesgo residual, asigna plazo por banda del Anexo §11) | REQ-G-03 | La tabla de priorización resultante asigna el plazo de referencia correcto (30/90/7/24-48h según banda) a cada hallazgo de prueba |
| T-031 | Escribir CT-04 (`ct04_remediacion.py`) | REQ-D-07, REQ-G-04 | Una remediación de prueba que recomienda la misma versión vulnerable es rechazada |
| T-032 | Escribir CT-05 (`ct05_consistencia.py`) | REQ-D-08, REQ-G-02 | El resumen ejecutivo recalculado por agregación coincide byte a byte con el publicado; una discrepancia inyectada de prueba es detectada |
| T-033 | Escribir `.claude/skills/redactar/SKILL.md` + `scripts/generar_reporte.py` (template canónico Parte V + advertencia legal §16 textual) | REQ-G-01, REQ-F-07 | Dos ejecuciones del script sobre los mismos datos producen contenido factual equivalente; el reporte generado contiene, sin modificar una palabra, el párrafo de advertencia legal del Anexo §16 |
| T-034 | REDACTOR ejecuta `redactar` + `priorizar`, produce `reporte/reporte_final.md` y `reporte/matriz_correlacion.csv` | REQ-G-01, REQ-G-02, REQ-G-03, REQ-G-04 | Los archivos existen y pasan T-035 (CT-01/CT-07 finales) sin rechazos |
| T-035 | Escribir CT-01 (`ct01_trazabilidad.py`) y CT-07 (`ct07_dato_sintetico.py`), ejecutarlos sobre el reporte de T-034 | REQ-D-04, REQ-D-10 | Cero afirmaciones sin `evidence_id`; cero campos vacíos sin marcador justificado — ambos validadores retornan código de salida 0 |
| **T-036** | **Cerrar G5**: los 7 controles CT-01..07 pasan, firma humana del informe | REQ-D-04..10, REQ-G-01..04 (gate) | `gates/G5.md` cerrado con los 7 resultados de validador adjuntos y firma humana real |

---

## Bloque 3 — Workflow declarado, extensiones D, y demostración (C, B-extensiones, H)

| ID | Tarea | REQ | Condición de "hecho" verificable |
|---|---|---|---|
| T-037 | Documentar el workflow de 10 etapas en `README.md`, justificando cada etapa contra ISO 19011/NIST SP 800-115/PTES/OSSTMM, señalando dónde actúa cada rol y dónde firma el humano | REQ-C-01 | El documento enumera las 10 etapas con su referencia citada y el rol/gate correspondiente |
| T-038 | Declarar por escrito el criterio de auditoría (ISO 27001 Anexo A + NIST CSF 2.0 + normativa CL) con fecha anterior a la primera entrada `HALLAZGO` del ledger | REQ-C-02 | El documento de criterio tiene timestamp/fecha anterior a `LDG` del primer `HALLAZGO` en `LEDGER.md` |
| T-039 | Verificar al cierre que la secuencia de `LEDGER.md` coincide con el workflow declarado en T-037, documentar cualquier desviación | REQ-C-03 | Recorrido cronológico del ledger sin saltos de etapa no justificados |
| T-040 | Implementar y demostrar **D1** (re-verificación automatizada con artefacto capturado como alternativa a firma humana para VALIDADO) | REQ-B-06 (D1) | Al menos un hallazgo pasa a VALIDADO por re-verificación automatizada (no firma humana directa), registrado en el ledger |
| T-041 | Implementar y demostrar **D2** (rol de contradicción explícita) | REQ-B-06 (D2) | Al menos una objeción real de este rol cambia o sostiene el estado de un hallazgo, registrada en el ledger |
| T-042 | D6 ya construido en T-019 — documentar su demostración explícita para video | REQ-B-06 (D6) | La suite de tests de T-019 se referencia como evidencia de D6 en el guion del video |
| T-043 | Grabar el video según los 6 bloques de `docs/PROPUESTA_RC_D_VIDEO.md` §3, usando el rechazo de T-008 como bloque 4 | REQ-H-01, REQ-H-02 | Los 6 bloques están presentes y en proporción; el bloque 4 muestra el rechazo real (no narrado) y su entrada en `LEDGER.md`; el bloque 6 reconoce al menos una limitación real del sistema |

---

## Resumen de dependencias críticas

```
T-001..T-011 (Bloque 0, gobernanza)
        │  G0 cerrado (T-011) es prerequisito de TODA ejecución contra 192.168.56.117
        ▼
T-012..T-016 (Bloque 1, recolección/normalización — G1, G2)
        ▼
T-017..T-036 (Bloque 2, análisis/riesgo/correlación/reporte — G3, G4, G5)
        ▼
T-037..T-043 (Bloque 3, workflow declarado, extensiones D, video)
```

Los controles CT-01 a CT-07 (T-020, T-023, T-028, T-031, T-032, T-035) se intercalan dentro del Bloque 2, en el punto exacto del ciclo donde el Anexo exige que actúen — no se agrupan al final como una tarea de "calidad" tardía, precisamente para evitar el error de la Parte VI de tratar la gobernanza como papeleo.

**Siguiente paso:** Fase 4 — ejecutar este plan en el BoundedLoop (WIP=1), empezando por T-001.
