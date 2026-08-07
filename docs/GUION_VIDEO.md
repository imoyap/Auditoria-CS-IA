# Guion del video — T-043

Estructura de 6 bloques aprobada en `docs/PROPUESTA_RC_D_VIDEO.md` §3 (`LEDGER.md` `LDG-004`). Cada bloque cita el artefacto real exacto a mostrar en pantalla — nada de lo listado aquí es hipotético, todo existe ya en el repositorio y puede grabarse tal cual.

**Regla de grabación (Anexo Parte VI / rúbrica H banda 10):** terminal legible, ejecución real en pantalla, cortes anunciados en voz si los hay. No narrar "no cometimos errores" — el bloque 6 exige lo contrario.

---

## Bloque 1 — Presentación (banda 10, "todos los integrantes intervienen y se identifican")

- Cada integrante del grupo se identifica por nombre.
- Resumir el encargo en 1-2 frases: cliente ficticio "Comercial Andes Sur SpA", activo `SRV-ADM-01` (Metasploitable2, `192.168.56.117`), restricciones (ventana de trabajo acotada, sin explotación activa — RC-3).
- Mostrar en pantalla: `scope/alcance.yaml` (sección `objetivo` y `reglas_de_compromiso`).

## Bloque 2 — Arquitectura (criterio B, separación estructural de roles)

- Mostrar la tabla de 10 etapas de `README.md` (sección "Workflow de auditoría declarado").
- Mostrar `.claude/agents/verificador.md`: señalar en voz que `tools:` no incluye `Write` ni `Edit`, y que el hook (`hooks.PreToolUse`) restringe su único `Bash` permitido a un solo script.
- **Evidencia de D6** (motor determinista de riesgo, sin margen de criterio libre del modelo): ejecutar en vivo
  ```
  python3 .claude/skills/clasificar/scripts/test_calcular_riesgo.py
  ```
  y mostrar las 12/12 verificaciones OK reproduciendo los 2 ejemplos numéricos del Anexo §15 (re-confirmado real el 2026-08-07, `LEDGER.md` `LDG-069`).
- Mencionar D1 (`harness/reverificacion_d1.py`) y D2 (rol `CONTRADICTOR`, `.claude/agents/contradictor.md`) como las otras 2 extensiones construidas — se muestran en detalle más abajo si el tiempo alcanza, o se referencian con su LDG.

## Bloque 3 — Ejecución real en pantalla (banda 10, "terminal legible, sin cortes que oculten fallos")

Mostrar, en este orden, con el ledger visible en paralelo (`tail -f LEDGER.md` en otra terminal o revisado justo después de cada paso):

1. **Recolección real:** `evidencias/raw/01_nmap_full.txt` (hash en `evidencias/manifest.sha256`) — la captura real contra `192.168.56.117`, 30 puertos abiertos.
2. **Normalización determinista:** `normalizado/inventario.json` — señalar que cada servicio tiene `linea_origen` (capa 2, sin LLM).
3. **Análisis → verificación:** `normalizado/candidatos.json` — mostrar los 4 estados finales (H-01 `VALIDADO`, H-02/H-04 `OBSERVADO`, H-03 `INCONCLUSO`) y citar en voz por qué H-02 no es `VALIDADO` (Ejemplo 2 del Anexo, banner de versión ≠ backdoor disparado).

## Bloque 4 — Punto de control humano (ancla explícita del Anexo §6; banda 10, "muestra un error concreto, la razón del rechazo, su registro en el ledger")

Reproducir en vivo el caso real de T-008 (`LEDGER.md`, líneas con `LDG-015`/`LDG-016`, timestamp real `2026-08-06T00:40:05` a `00:40:27`):

- Mostrar el intento real: VERIFICADOR tratando de usar `Write` (fuera de su tabla de permisos).
- Mostrar el rechazo real en `LEDGER.md`: la línea `RECHAZO | VERIFICADOR | Intento de uso de herramienta fuera de tabla de permisos: Write | ref:hook`.
- Explicar en voz: esto no es un mensaje de error decorativo — es el runtime de Claude Code rechazando la herramienta antes de ejecutarla, porque `disallowedTools` en `.claude/agents/verificador.md` no incluye `Write`.
- **Alternativa igual de válida si se prefiere algo más reciente:** el rechazo real de un comando fuera del patrón permitido de COMPLIANCE durante T-027 (`LEDGER.md`, buscar `LDG-HOOK` con actor `COMPLIANCE`, 2026-08-06 ~09:16) — un intento de `ls`/`cd &&` real, rechazado en vivo mientras el agente trabajaba.

## Bloque 5 — Reporte final (criterio G, banda 10, "se demuestra el punto donde se detiene y pide firma humana")

- Mostrar `reporte/reporte_final.md` generado (resumen ejecutivo con agregación real, advertencia legal del Anexo §16 copiada textual).
- Mostrar `reporte/matriz_correlacion.csv` (22 columnas de G4 + `Plazo_referencia`).
- **Momento clave a filmar en vivo:** el mecanismo de firma de gate deteniéndose. Se puede reproducir con un gate desechable, o mostrar directamente `gates/G5.md` con la firma ya puesta y explicar en voz que antes de esa línea el archivo tenía `**Firma humana:** [PENDIENTE]` y el sistema **nunca** la completa por sí mismo — solo `harness/orquestador.py --sign-gate G5 --by "<nombre>" --date "<fecha>"`, ejecutado por un humano, la reemplaza. Mostrar el comando real ejecutándose.

## Bloque 6 — Cierre y autocrítica (Anexo Parte VI: "nuestro agente no cometió errores" → banda 0-2; se exige lo opuesto)

Limitaciones reales a reconocer (no inventar otras, no minimizar estas):

- **H-03 quedó INCONCLUSO**, no porque el sistema fallara, sino porque la evidencia real nunca mostró la versión de UnrealIRCd — el sistema se negó a inventar una atribución de CVE sin sostén (CT-02). Esto es una limitación real de lo que se pudo verificar dentro del alcance autorizado (RC-3 prohíbe una sonda más agresiva).
- **Bugs reales de construcción** encontrados durante el proyecto, no ocultados: el diseño original de permisos de `Bash` por rol era inviable (tuvo que rediseñarse en T-013, ver `docs/design.md` nota de diseño); un bug de acentos hizo que "Crítica" nunca se contara en el resumen ejecutivo hasta T-034 (`LDG-062`); `candidatos.json` retuvo un dato residual de riesgo sobre H-03 que CONTRADICTOR (D2) tuvo que señalar antes de que se corrigiera (`LDG-068`).
- **D1 no pudo aplicarse a ningún hallazgo real de esta auditoría** (solo a un candidato de prueba) porque, dentro de RC-3, ninguno de los 4 hallazgos calificaba genuinamente para la vía automatizada sin firma humana — una limitación honesta del alcance, no del mecanismo.
- Cerrar reconociendo que la ventana de trabajo real tuvo que extenderse dos veces durante la ejecución (`LDG-043`, `LDG-046`) porque el trabajo tomó más tiempo del planeado inicialmente.

---

**Trazabilidad de este guion:** cada afirmación cita un archivo real o una entrada de `LEDGER.md` existente al momento de escribir este documento (2026-08-07). Ninguna cifra ni cita aquí es hipotética.
