---
name: registrar_veto
description: Usar cuando VERIFICADOR necesita vetar un hallazgo candidato o registrar una decisión sobre su estado, citando el evidence_id que sostiene el veto. Es el único canal de escritura de VERIFICADOR — no usar para intentar asignar VALIDADO a un hallazgo, este script no tiene esa capacidad.
allowed-tools: Bash
---

Único canal de mutación de VERIFICADOR (`docs/design.md` §a.2). Solo puede anexar entradas `RECHAZO` o `DECISION` a `LEDGER.md` — nunca toca `normalizado/candidatos.json` ni ningún registro de estado de hallazgos, así que no existe una ruta de código por la que este script pueda escribir `VALIDADO`.

## Procedimiento

1. Cuando VERIFICADOR decide vetar un candidato, invoca:
   ```
   .claude/skills/registrar_veto/scripts/registrar_veto.py --tipo RECHAZO --resumen "Veto a H-XX: <motivo citando evidence_id>" --ref "ev:<evidence_id>"
   ```
2. Cuando VERIFICADOR sostiene una decisión (p. ej. confirma por qué algo queda INCONCLUSO), usa `--tipo DECISION`.
3. Un veto siempre cita el `evidence_id` (o la ausencia de uno) que lo sostiene — nunca "insistencia" sin evidencia (Anexo Técnico U3 §4).
