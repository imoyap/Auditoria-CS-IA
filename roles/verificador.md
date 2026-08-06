# Rol: VERIFICADOR

**Pregunta que hace:** ¿La evidencia demuestra lo que dice demostrar?

## Alcance
Lee todo el repositorio (evidencia cruda, candidatos, matriz, reporte) para confirmar o vetar cada hallazgo candidato de ANALISTA. Un hallazgo pasa a VALIDADO solo con verificación adicional capturada (no solo el indicio original); si la verificación falla por condición de red, el estado máximo es INCONCLUSO (CT-06).

## Herramientas que tiene
- `Read` — sin restricción de alcance, sobre todo el repositorio.
- `Skill` — únicamente `registrar_veto`, el único canal de escritura de este rol.

## Herramientas que NO tiene
- **Escritura arbitraria.** No tiene `Write` ni `Edit` en absoluto. `Bash` está restringido por el hook a una única invocación permitida, `.claude/skills/registrar_veto/scripts/registrar_veto.py` — cualquier otro comando (`ls`, `cat`, intentar tocar un archivo por otra vía, etc.) se rechaza. La separación no es una promesa del system prompt: el runtime de Claude Code rechaza cualquier intento — ver el hook de `docs/design.md` §a.3. Un intento real queda registrado en `LEDGER.md` como `RECHAZO` (evidencia para REQ-B-03 y REQ-H-01; ver también la corrección real de T-013 en `LDG-044`/`LDG-045` — el diseño original no le daba `Bash` en absoluto, lo que le impedía ejecutar su propio script de veto).
- No puede escribir `VALIDADO` directamente en ningún archivo: la skill `registrar_veto` solo admite entradas `RECHAZO`/`DECISION`, nunca ese estado.

## Poder
Veto de cierre. Un veto se levanta con evidencia, no con insistencia (Anexo §4).

## Implementación
`.claude/agents/verificador.md` — ver `docs/design.md` §a.2 y §a.3 (hook `PreToolUse`).
