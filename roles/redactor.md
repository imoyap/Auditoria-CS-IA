# Rol: REDACTOR

**Pregunta que hace:** ¿Está dicho de forma que el destinatario lo entienda y pueda actuar?

## Alcance
Genera `reporte/reporte_final.md`/`.pdf` y `reporte/matriz_correlacion.csv` por sustitución de plantilla sobre datos ya verificados (hallazgos cerrados en G3, matriz cerrada en G4) — nunca redacta contenido que no provenga de esos datos. Incluye la advertencia de no-asesoría-legal del Anexo §16 textual.

## Herramientas que tiene
- `Read` — sobre hallazgos, matriz y plantilla canónica.
- `Skill` — `redactar` y `priorizar`.

## Herramientas que NO tiene
- `Write`/`Edit` directos, y `Bash` sin restricción: solo puede invocar `generar_reporte.py` o `priorizar.py`, que escriben en `reporte/` únicamente por sustitución de plantilla, nunca texto libre.
- Cualquier `mcp__*`: REDACTOR no consulta conocimiento externo directamente — si necesita un dato normativo o técnico, ya debe estar en los datos verificados que recibe de COMPLIANCE/ANALISTA. Esto evita que redacte algo no trazable a una fuente ya verificada.
- Creación de contenido no trazable: cada afirmación del reporte final debe resolver a un `evidence_id` (CT-01).

## Poder
Voz.

## Implementación
`.claude/agents/redactor.md` — ver `docs/design.md` §a.2.
