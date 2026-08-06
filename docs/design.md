# design.md — Diseño de arquitectura (Fase 2)

**Fuente de verdad:** `docs/anexo_tecnico_u3.md`, `docs/rubrica_evaluacion_u3.md`, `docs/requirements.md`, `docs/PROPUESTA_RC_D_VIDEO.md`, `LEDGER.md`.
**Estado:** diseño únicamente — sin código de implementación. Cada decisión cita el REQ que resuelve y, cuando corresponde, la sección del Anexo o la documentación externa verificada.
**Verificación de sintaxis externa:** antes de diseñar la Parte a) y b), se verificó la sintaxis vigente de subagentes y skills de Claude Code contra `https://code.claude.com/docs/en/sub-agents` y `https://code.claude.com/docs/en/skills` (consultados el 2026-08-03). Las citas de campos de frontmatter en este documento provienen de esa verificación, no de memoria.

---

## a) Roles → mecanismo de aislamiento estructural

### a.1 Comparación de rutas

| Ruta | Cómo logra separación estructural | Verificado hoy |
|---|---|---|
| **Subagentes de Claude Code** (`.claude/agents/*.md`) | Cada archivo declara `tools` (allowlist) y/o `disallowedTools` (denylist) en YAML frontmatter. El runtime resuelve el pool de herramientas *antes* de que el subagente pueda invocar nada: "If no entry in the list resolves to a tool, the subagent usually fails to launch" — no es una instrucción que el modelo pueda ignorar. | Confirmado en `sub-agents` doc: `tools`/`disallowedTools` son campos soportados; `disallowedTools` se aplica primero y luego `tools` se resuelve contra el pool restante. |
| **Harness propio contra la API de Anthropic** | El harness arma el array `tools` de cada llamada `messages.create()` según el rol; si el rol no está en el array, la API no puede invocarla. | Válido en principio, pero exige reimplementar todo el ciclo de conversación, memoria y reintentos que Claude Code ya resuelve — mayor superficie de bugs propios en el propio mecanismo de aislamiento que se está intentando demostrar como confiable. |

**Decisión (resuelve REQ-B-03):** **Ruta combinada** — subagentes de Claude Code como mecanismo primario de aislamiento (porque el runtime ya impone el límite, no un harness que el propio grupo escribió y podría tener un bug), más un **harness propio ligero en Python** (reutilizando el patrón de `auditoria/core/engine.py` y `auditoria/scheduler/executor.py` como antecedente de orquestación — ver `docs/GAP_ANALYSIS.md` §1.1) que invoca cada subagente vía Claude Code en **modo headless** (`claude -p`), controla el `BoundedLoop`, escribe el ledger, y aplica las pausas de gate. El harness no es el mecanismo de aislamiento de herramientas — Claude Code lo es — el harness es el mecanismo de secuenciación y gobierno.

Justificación: el Anexo exige que el harness gobierne "orquestación, gates, ledger, estado, BoundedLoop" (capa 6) — eso es responsabilidad de secuenciación, no de aislamiento de herramientas. Mezclar ambas responsabilidades en el mismo componente sería repetir el antipatrón de la Parte VI ("un solo agente hace todo"), aplicado esta vez al harness. Separarlas dos veces —roles aislados por Claude Code, secuencia gobernada por un harness propio— es más verificable: cada mitad se prueba con un caso de fallo distinto (REQ-B-03: intento de escritura de VERIFICADOR → rechazo del runtime; REQ-B-05: tope de iteraciones → detención del harness).

### a.2 Superficie de herramientas por rol

Refinamiento sobre la tabla del Anexo §4: en vez de dar a cada rol acceso crudo a `Write`/`Edit`/`Bash` y confiar en la disciplina del rol, **la única superficie de escritura de cualquier rol (salvo RECON) es una skill del proyecto** — un script determinista que impone sus propias invariantes (p. ej. "nunca escribas estado=VALIDADO", "solo puedes anexar, nunca sobrescribir"). Esto añade una segunda barrera estructural por debajo del campo `tools`: aunque `tools` se mal-configurara, el script de la skill sigue rechazando la operación indebida en su propio código.

| Rol | `tools` (allowlist) | `disallowedTools` | Superficie de escritura real | Resuelve |
|---|---|---|---|---|
| **RECON** | `Read`, `Bash`, `Write`, `Skill` | `Edit` | `Bash` validado por el hook contra `scope/allowlist.txt` (comandos de red) **o** contra la invocación exacta de `.claude/skills/enumerar/scripts/registrar_evidencia.py`; `Write` solo bajo `evidencias/raw/` y `evidencias/manifest.sha256` | REQ-A-02, REQ-D-01, REQ-D-02 |
| **ANALISTA** | `Read`, `Bash`, `Skill`, `mcp__conocimiento-tecnico` | `Write`, `Edit` | `Bash` restringido por el hook a la invocación exacta de `.claude/skills/clasificar/scripts/calcular_riesgo.py` — el script no acepta un parámetro `estado=VALIDADO`, esa transición no existe en su contrato | REQ-D-03, REQ-E-01..06, REQ-B-04 |
| **VERIFICADOR** | `Read`, `Bash`, `Skill` | `Write`, `Edit` | `Bash` restringido por el hook a la invocación exacta de `.claude/skills/registrar_veto/scripts/registrar_veto.py`, que únicamente puede anexar entradas `RECHAZO` o `DECISION` a `LEDGER.md` — nunca puede escribir `VALIDADO` | REQ-B-03, REQ-H-01 |
| **COMPLIANCE** | `Read`, `Bash`, `Skill`, `mcp__conocimiento-normativo` | `Write`, `Edit` | `Bash` restringido por el hook a `.claude/skills/correlacionar/scripts/correlacionar.py`, que anexa filas a `normalizado/matriz_borrador.csv` y rechaza cualquier intento de modificar una fila ya existente | REQ-F-01..07 |
| **REDACTOR** | `Read`, `Bash`, `Skill` | `Write`, `Edit`, `mcp__*` | `Bash` restringido por el hook a `.claude/skills/redactar/scripts/generar_reporte.py` o `.claude/skills/priorizar/scripts/priorizar.py`, que escriben `reporte/` solo por sustitución de plantilla sobre datos ya en estado VALIDADO/OBSERVADO/INCONCLUSO | REQ-G-01..04 |

**Nota de diseño (corregida en T-013, ver `LEDGER.md` `LDG-044`/`LDG-045`):** la versión original de esta tabla no daba `Bash` a ningún rol salvo RECON — lo cual, verificado ejecutando RECON de verdad contra el objetivo, resultó impedirle también a él completar su propio ciclo de captura de evidencia (el hook rechazaba la invocación de `registrar_evidencia.py` por no estar en `scope/allowlist.txt`), y habría impedido lo mismo a los otros 4 roles con sus propios scripts. La corrección real: **todo rol recibe `Bash`, pero el hook lo restringe a exactamente una invocación permitida — el script de su propia skill.** Esto sigue satisfaciendo la banda 13–14 del criterio B ("al VERIFICADOR no se le entregan herramientas de escritura"): `Bash` no es una herramienta de escritura genérica aquí, es un canal reducido a una única operación determinista sin ruta hacia `VALIDADO` ni hacia ningún archivo fuera del alcance de esa operación — verificado en vivo (`claude -p --agent verificador`) que `ls` sigue rechazándose.

### a.3 Hook `PreToolUse` — verificación y rechazo registrado

Diseño del hook (Bash/PowerShell script), scopeado por rol en el campo `hooks:` del frontmatter de cada subagente (confirmado como campo soportado: "Lifecycle hooks scoped to this subagent"):

```yaml
# .claude/agents/verificador.md (fragmento de frontmatter)
hooks:
  PreToolUse:
    - matcher: "Write|Edit|Bash"
      hooks:
        - type: command
          command: "./harness/controles/reject_and_log.sh VERIFICADOR"
```

Comportamiento del script (diseño, sin código todavía — implementación en Fase 4):
1. Recibe el evento `PreToolUse` como JSON por stdin (nombre de herramienta + argumentos).
2. Si la herramienta invocada no pertenece a la superficie de escritura declarada en a.2 para ese rol, construye la línea de ledger `[ISO-8601] | [ID autogenerado] | RECHAZO | [ROL] | Intento de uso de herramienta fuera de tabla de permisos: [tool] | ref:hook` y la anexa a `LEDGER.md`.
3. Sale con código 2 (bloquea la operación — comportamiento confirmado en la documentación de hooks: "exits with code 2 to block write operations").

Este es el artefacto que resuelve **REQ-B-03** y sirve simultáneamente de evidencia demostrable para **REQ-H-01** (bloque 4 del video) — un rechazo real, no narrado.

---

## b) Skills → procedimientos reutilizables e invocables

Confirmado contra `skills` doc: cada skill es una carpeta `.claude/skills/<nombre>/SKILL.md`, frontmatter YAML con `name` y `description` (obligatorios — `description` es el disparador y debe describir *cuándo* se activa, no ser genérica), más campos opcionales `allowed-tools`, `disallowed-tools`, `disable-model-invocation` (para forzar invocación manual `/nombre` en vez de automática), `context: fork` (ejecuta en subagente propio). Archivos de soporte (scripts, plantillas, ejemplos) viven junto a `SKILL.md` en el mismo directorio.

| Skill | Ruta | `description` (disparador) | Contenido determinista |
|---|---|---|---|
| `enumerar` | `.claude/skills/enumerar/SKILL.md` | "Usar cuando RECON necesita traducir el resultado de un comando de la allowlist en un artefacto crudo con hash y timestamp antes de cualquier interpretación." | `scripts/registrar_evidencia.py`: recibe stdout/stderr crudo + comando ejecutado, calcula SHA-256, escribe a `evidencias/raw/`, anexa línea a `evidencias/manifest.sha256`. No interpreta el contenido. |
| `clasificar` | `.claude/skills/clasificar/SKILL.md` | "Usar cuando ANALISTA tiene un hallazgo candidato y necesita calcular impacto, probabilidad y riesgo I×P siguiendo las tablas del Anexo §9–11, nunca por criterio libre." | `scripts/calcular_riesgo.py`: entrada JSON con los 5 factores de impacto y los 5 de probabilidad (Anexo §9–10, incluido `NO_DISPONIBLE`); salida determinista: impacto 1–5, probabilidad 1–5, riesgo inherente = impacto × probabilidad, banda (Anexo §11). Resuelve REQ-E-02, REQ-E-03, REQ-E-04, y es la base de la extensión **D6** aprobada (`LDG-004`). |
| `correlacionar` | `.claude/skills/correlacionar/SKILL.md` | "Usar cuando COMPLIANCE necesita mapear un hallazgo ya clasificado a control ISO/IEC 27001:2022 Anexo A, categoría NIST CSF 2.0, control CIS v8 y obligación normativa chilena, citando el MCP normativo." | Consulta `mcp__conocimiento-normativo` (b.4) por cada marco; nunca inventa un ID de control — si la consulta no retorna coincidencia, escribe `NO_OBSERVADO` en esa columna en vez de forzar un mapeo. Resuelve REQ-F-02..05. |
| `redactar` | `.claude/skills/redactar/SKILL.md` | "Usar cuando REDACTOR necesita generar o actualizar el reporte final a partir de hallazgos y matriz ya verificados, nunca a partir de texto libre." | `scripts/generar_reporte.py`: sustitución de plantilla canónica (Parte V) + agregación numérica para el resumen ejecutivo (CT-05, REQ-D-08). Resuelve REQ-G-01, REQ-G-02. |
| `priorizar` | `.claude/skills/priorizar/SKILL.md` | "Usar cuando se necesita ordenar hallazgos por banda de riesgo, con responsable, esfuerzo y plazo, siguiendo los plazos de referencia del Anexo §11." | Ordena por riesgo residual descendente; asigna plazo por banda tal como la tabla del Anexo §11 (no un plazo arbitrario). Resuelve REQ-G-03. |

**Skill adicional necesaria, no listada en el Anexo:** `registrar_veto` (usada por VERIFICADOR, ver a.2) — `disable-model-invocation: false` (VERIFICADOR la invoca según su propio juicio, no bajo demanda del usuario), `allowed-tools` vacío (el script en sí hace el único `Write` permitido, no el modelo).

---

## Mapeo de las 8 capas a carpetas del repositorio

Se usa literalmente la estructura de la Parte V del Anexo, sin modificarla:

```
Auditoria-CS-IA/
├── README.md
├── scope/
│   ├── alcance.yaml           # capa 8 (insumo) — IP 192.168.56.117, ventana, RC-1..6
│   ├── allowlist.txt          # capa 1 (control)
│   └── declaracion_etica.md
├── roles/                     # documentación humana-legible de cada rol (capa 5)
│   ├── recon.md  analista.md  verificador.md  compliance.md  redactor.md
├── .claude/agents/            # capa 5 — implementación ejecutable de los roles
│   ├── recon.md  analista.md  verificador.md  compliance.md  redactor.md
├── .claude/skills/            # capa 4
│   ├── enumerar/  clasificar/  correlacionar/  redactar/  priorizar/  registrar_veto/
├── mcp/                       # capa 3
│   ├── conocimiento_tecnico/   (CVE/CWE/CVSS)
│   ├── conocimiento_normativo/ (ISO/NIST/CIS/CL)
│   └── config.json
├── harness/                   # capa 6
│   ├── orquestador.py
│   └── controles/              # CT-01..CT-07 (ver sección más abajo)
├── evidencias/                # capa 1 (salida)
│   ├── raw/
│   └── manifest.sha256
├── normalizado/                # capa 2
│   ├── inventario.json  candidatos.json  matriz_borrador.csv
├── gates/                      # capa 8 (artefacto)
│   ├── G0.md  G1.md  G2.md  G3.md  G4.md  G5.md
├── LEDGER.md                   # capa 6 (artefacto)
└── reporte/
    ├── reporte_final.md  reporte_final.pdf  matriz_correlacion.csv
```

`auditoria/` (el framework genérico existente) se mantiene aparte, fuera de este árbol U3, y se referencia puntualmente desde el harness donde `docs/GAP_ANALYSIS.md` §1.1 lo marcó reutilizable (p. ej. el patrón `BaseCheck`/`registry` como inspiración de contrato, `storage/database.py` como índice de lectura opcional del ledger) — nunca como dependencia dura, para no mezclar los dos sistemas.

---

## Servidor(es) MCP de capa 3 (conocimiento)

Resuelve REQ-F-06. Dos servidores MCP de solo lectura, ambos con corpus **offline** (el laboratorio no tiene acceso a Internet — Anexo §10, nota de laboratorio):

**`mcp/conocimiento_normativo/`** — corpus estático empaquetado en el repo:
- `iso27001_2022_anexoA.json` — los 93 controles con ID, tema, nombre corto.
- `nist_csf_2.json` — funciones/categorías GV/ID/PR/DE/RS/RC.
- `cis_v8.json` — controles y sub-controles IG1/IG2/IG3.
- `normativa_cl.json` — artículos relevantes de Ley 21.663, 21.719, 21.459 (solo los citables para el tipo de hallazgo esperado en Metasploitable2, no el cuerpo legal completo).

Tools expuestas: `buscar_control_iso(id_o_texto)`, `buscar_categoria_nist(id_o_texto)`, `buscar_control_cis(id_o_texto)`, `buscar_obligacion_cl(tema)`. Cada una retorna coincidencia exacta o `NO_OBSERVADO` — nunca aproxima ni inventa un ID.

**`mcp/conocimiento_tecnico/`** — corpus estático:
- Subconjunto de CWE relevante a los servicios esperados en Metasploitable2 (CWE-319, CWE-912, CWE-798, CWE-287, CWE-778, etc.).
- Tool `consultar_epss_kev(cve)` que **siempre** retorna `{"disponible": false, "razon": "entorno de laboratorio aislado, sin acceso a Internet"}` — la ausencia se declara por diseño del propio servidor, no por omisión del modelo. Esto es la implementación estructural de la nota de laboratorio del Anexo §10 y del control CT-07 (REQ-D-10, REQ-E-03): el modelo nunca tiene la opción de "adivinar" un EPSS porque la herramienta que lo serviría no existe para eso.

---

## Diseño del harness/orquestador (BoundedLoop)

Resuelve REQ-B-05. Script en Python (`harness/orquestador.py`), reutilizando como antecedente de orquestación `auditoria/core/engine.py` (ver GAP_ANALYSIS §1.1) pero sin heredar su mezcla recolección+clasificación.

**Ciclo (WIP=1):**

```
etapas = [0,1,2,3,4,5,6,7,8,9]   # Anexo §2
tope_reintentos_por_etapa = 3
max_iteraciones = len(etapas) * tope_reintentos_por_etapa   # 30, explícito en config

for etapa in etapas:
    intentos = 0
    while intentos < tope_reintentos_por_etapa:
        resultado = invocar_subagente_de_la_etapa(etapa)   # `claude -p` con el .claude/agents/*.md del rol correspondiente
        if resultado.ok:
            LEDGER.append(...)
            break
        else:
            intentos += 1
            LEDGER.append(RECHAZO, motivo=resultado.error)
    else:
        detener_loop("tope de reintentos alcanzado en etapa %s" % etapa)  # condición de salida

    if etapa in (0, 5, 8):   # etapas con gate obligatorio G0, G3, G5
        pausar_para_firma_humana(gate_correspondiente)
```

**Pausa real, no informativa (resuelve la exigencia explícita de "no un log informativo"):** al llegar a una etapa con gate obligatorio, el harness escribe `gates/GX.md` con el criterio y la evidencia ya completos pero `**Firma humana:** [PENDIENTE]`, y **termina el proceso** (`sys.exit`, no un `sleep` ni un `input()` que pueda saltarse con un timeout). El harness no vuelve a ejecutar la etapa siguiente hasta que se le invoque explícitamente con `orquestador.py --sign-gate G0 --by "Nombre Apellido" --date "2026-08-10"`, comando que reemplaza `[PENDIENTE]` por el valor real en `gates/GX.md` y recién entonces permite que la siguiente invocación de `orquestador.py --continue` avance. Sin ese archivo modificado, `--continue` vuelve a detenerse en la misma etapa.

**Condición de salida del loop:** todas las etapas completas y `G5` firmado, **o** tope de reintentos alcanzado en cualquier etapa sin resolución, **o** un gate cerrado con veredicto `REJECT` sin apelación.

---

## Formato exacto de `gates/GX.md` y `LEDGER.md`

Copiados literalmente del Anexo §5 y §6 — no se aproximan:

```markdown
## Gate [ID] — [nombre]
**Criterio:** [condición verificable, redactada ANTES de empezar]
**Evidencia presentada:** [artefacto, ubicación, cómo verificarlo]
**Concilio:** [roles convocados]
**Objeciones:** [texto de cada objeción y cómo se resolvió, o "abierta"]
**Veredicto:** APPROVE | APPROVE_WITH_FINDINGS | REJECT
**Hallazgos abiertos:** [con ID]
**Firma humana:** [nombre, fecha] (obligatoria en G0, G3 y G5)
```

```
[ISO-8601] | [ID] | [DECISION|GATE|HALLAZGO|SUPERSEDE|RECHAZO] | [actor] | [resumen en una línea] | [ref]
```

`LEDGER.md` ya sigue este formato desde `LDG-001` (ver el archivo en la raíz del repo) — el diseño no cambia nada, solo formaliza que el harness y los hooks escriben exactamente en este formato, nunca en uno aproximado.

---

## Diseño de los 7 controles anti-alucinación (CT-01 a CT-07)

Cada uno como script en `harness/controles/`, ejecutado por el harness antes de cerrar el gate correspondiente (no bajo demanda manual):

| ID | Script | Se ejecuta antes de | Lógica (determinista) | Error de CertEngine que previene |
|---|---|---|---|---|
| CT-01 | `ct01_trazabilidad.py` | G5 | Recorre `reporte/reporte_final.md`; para cada afirmación con formato de hallazgo, exige un `evidence_id` que resuelva en `evidencias/manifest.sha256` | Hallazgos sin respaldo |
| CT-02 | `ct02_inferencia.py` | admisión de cada candidato (dentro de la skill `clasificar`) | Búsqueda literal (`grep` exacto, no fuzzy) de la cadena del producto/versión declarado en los archivos de `evidencias/raw/` referenciados por el `evidence_id` | Hallazgo de CMS/SPF fabricado |
| CT-03 | `ct03_severidad.py` | G5 | Compara el valor de severidad del mismo `check_id` entre `reporte/matriz_correlacion.csv`, la tabla resumen y la ficha de detalle del reporte | Severidades contradictorias |
| CT-04 | `ct04_remediacion.py` | G5 | Compara el campo "versión objetivo" de la remediación contra el campo "versión instalada" de la evidencia; iguales ⇒ rechazo | Remediación que recomendaba la versión afectada |
| CT-05 | `ct05_consistencia.py` | G5 | Recalcula el resumen ejecutivo por agregación sobre `normalizado/` + hallazgos y lo compara byte a byte con lo publicado | Cifras divergentes entre secciones |
| CT-06 | `ct06_red.py` | cierre de cada hallazgo (dentro de `clasificar`/`registrar_veto`) | Si el log de verificación adicional registra timeout/NAT/sin-ruta, fuerza `estado = INCONCLUSO` sin excepción | Hallazgos bloqueados por NAT marcados "Verified" |
| CT-07 | `ct07_dato_sintetico.py` | G3, G4, G5 | Ningún campo obligatorio del schema de hallazgo o de la matriz puede quedar vacío: debe tener valor real o el marcador `NO_OBSERVADO`/`NO_DISPONIBLE` con justificación no vacía | Informe simétrico sobre datos incompletos |

**Punto de conexión con el harness:** el orquestador no cierra `gates/G3.md`, `G4.md` ni `G5.md` si alguno de los validadores correspondientes retorna código de salida distinto de 0 — el fallo se anexa al ledger como `RECHAZO` y el loop propone la corrección mínima como sub-tarea, tal como exige el paso 5 del ciclo de la Fase 4 del prompt original.

---

## Trazabilidad de esta fase

Este diseño resuelve, sin dejar pendientes de suposición: REQ-B-01 a REQ-B-06 (arquitectura), REQ-D-01/02/04-10 (evidencia y CT-01-07 como validadores concretos), REQ-E-02/03 (skill `clasificar`), REQ-F-06 (MCP normativo), REQ-G-01 (skill `redactar`). Los REQ de contenido puro (qué dice cada control ISO específico, qué ley aplica a cada hallazgo) no se resuelven aquí — son trabajo de ejecución (Fase 4), no de diseño.

**Siguiente paso:** Fase 3 — `docs/tasks.md`, descomponiendo este diseño en tareas T-001…, ordenadas por dependencia real (el ledger y el formato de gate ya existen; lo primero en construirse debe ser `scope/alcance.yaml` + `allowlist.txt`, porque G0 es la primera pausa obligatoria y nada más puede cerrar sin ella).
