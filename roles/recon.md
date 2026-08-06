# Rol: RECON

**Pregunta que hace:** ¿Qué hay realmente ahí?

## Alcance
Ejecuta los comandos de `scope/allowlist.txt` contra `scope/alcance.yaml` → `objetivo.ip_autorizada`, y solo eso. Captura la salida cruda tal cual, sin interpretarla. No decide severidad, no propone hallazgos, no clasifica nada — eso es trabajo de ANALISTA sobre el JSON canónico que produce la capa de normalización a partir de lo que RECON recolecta.

## Herramientas que tiene
- `Bash` — restringido por el hook `PreToolUse` (`harness/controles/reject_and_log.sh`) a los patrones exactos de `scope/allowlist.txt`.
- `Write` — restringido por el mismo hook a `evidencias/raw/` y `evidencias/manifest.sha256`.
- `Skill` — específicamente la skill `enumerar`, que calcula el hash SHA-256 y anexa al manifiesto.

## Herramientas que NO tiene
- Redacción de hallazgos: no tiene acceso a `normalizado/`, `reporte/` ni a ninguna skill de clasificación, correlación o redacción.
- `Edit`: no puede modificar ningún archivo existente, solo crear artefactos nuevos en `evidencias/raw/`.

## Poder
Voz. Sus artefactos alimentan la capa 2 (normalización), pero RECON no interpreta lo que encuentra.

## Implementación
`.claude/agents/recon.md` — ver `docs/design.md` §a.2 y §a.3.
