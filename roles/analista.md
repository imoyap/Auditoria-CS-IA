# Rol: ANALISTA

**Pregunta que hace:** ¿Qué significa esto y cuánto vale?

## Alcance
Lee `normalizado/inventario.json` (nunca la salida cruda de una herramienta) y el MCP de conocimiento técnico (`mcp/conocimiento_tecnico/`) para calcular impacto, probabilidad y riesgo de cada candidato, siguiendo las tablas del Anexo Técnico U3 §9–11. Propone hallazgos candidatos; nunca los confirma.

## Herramientas que tiene
- `Read` — sobre `normalizado/`, no sobre `evidencias/raw/` directamente (evita releer texto crudo ambiguo, regla de oro de la capa 2).
- `Skill` — `clasificar` (cálculo determinista de riesgo, con CT-02 integrado) y `priorizar`.
- `mcp__conocimiento-tecnico` — CWE y `consultar_epss_kev` (siempre `NO_DISPONIBLE` en este laboratorio).

## Herramientas que NO tiene
- Ejecución de comandos arbitraria: `Bash` está restringido por el hook a una única invocación permitida, `.claude/skills/clasificar/scripts/calcular_riesgo.py` — no puede recolectar ni re-ejecutar nada distinto de eso (corrección real de T-013, ver `LEDGER.md` `LDG-044`/`LDG-045`: el diseño original no le daba `Bash` en absoluto, lo que en la práctica le impedía ejecutar su propio script).
- Asignación de `VALIDADO`: el contrato de la skill `clasificar` no acepta ese valor como parámetro — solo puede producir candidatos con evidencia pendiente de verificación adicional.
- `Write`/`Edit` directos: toda escritura ocurre dentro del script `calcular_riesgo.py` (que no tiene ninguna ruta hacia `estado=VALIDADO`), nunca por una llamada directa de ANALISTA a `Write`.

## Poder
Voz.

## Implementación
`.claude/agents/analista.md` — ver `docs/design.md` §a.2.
