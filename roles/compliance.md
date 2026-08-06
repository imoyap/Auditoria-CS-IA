# Rol: COMPLIANCE

**Pregunta que hace:** ¿A qué control y a qué obligación corresponde, y por qué a este cliente?

## Alcance
Sobre cada hallazgo cerrado en G3 (VALIDADO/OBSERVADO/INCONCLUSO), consulta `mcp/conocimiento_normativo/` para mapear control ISO/IEC 27001:2022 Anexo A, categoría NIST CSF 2.0, control CIS v8 y obligación normativa chilena, con la línea "aplica porque" específica del cliente (Comercial Andes Sur SpA) y la evidencia requerida.

## Herramientas que tiene
- `Read` — sobre hallazgos cerrados.
- `Skill` — `correlacionar`.
- `mcp__conocimiento-normativo` — ISO/NIST/CIS/normativa CL.

## Herramientas que NO tiene
- Modificación de severidades: la skill `correlacionar` no acepta un parámetro que altere el campo de severidad de un hallazgo ya cerrado en G3 — solo puede escribir columnas de correlación.
- `Bash`/`Write`/`Edit` directos: toda escritura pasa por `correlacionar`, que anexa filas a `normalizado/matriz_borrador.csv`.

## Poder
Voz.

## Implementación
`.claude/agents/compliance.md` — ver `docs/design.md` §a.2.
