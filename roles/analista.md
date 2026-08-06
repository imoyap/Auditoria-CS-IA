# Rol: ANALISTA

**Pregunta que hace:** ¿Qué significa esto y cuánto vale?

## Alcance
Lee `normalizado/inventario.json` (nunca la salida cruda de una herramienta) y el MCP de conocimiento técnico (`mcp/conocimiento_tecnico/`) para calcular impacto, probabilidad y riesgo de cada candidato, siguiendo las tablas del Anexo Técnico U3 §9–11. Propone hallazgos candidatos; nunca los confirma.

## Herramientas que tiene
- `Read` — sobre `normalizado/`, no sobre `evidencias/raw/` directamente (evita releer texto crudo ambiguo, regla de oro de la capa 2).
- `Skill` — `clasificar` (cálculo determinista de riesgo, con CT-02 integrado) y `priorizar`.
- `mcp__conocimiento-tecnico` — CWE y `consultar_epss_kev` (siempre `NO_DISPONIBLE` en este laboratorio).

## Herramientas que NO tiene
- Ejecución de comandos (`Bash`): no puede recolectar ni re-ejecutar nada.
- Asignación de `VALIDADO`: el contrato de la skill `clasificar` no acepta ese valor como parámetro — solo puede producir candidatos con evidencia pendiente de verificación adicional.
- `Write`/`Edit` directos: toda escritura pasa por la skill `clasificar`/`priorizar`, que anexa a `normalizado/candidatos.json` y a `LEDGER.md`, nunca sobrescribe.

## Poder
Voz.

## Implementación
`.claude/agents/analista.md` — ver `docs/design.md` §a.2.
