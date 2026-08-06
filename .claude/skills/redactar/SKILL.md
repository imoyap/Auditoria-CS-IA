---
name: redactar
description: Usar cuando REDACTOR necesita generar o actualizar reporte/reporte_final.md a partir de hallazgos y matriz ya verificados en G3/G4, nunca a partir de texto libre no trazable a evidence_id.
allowed-tools: Bash
---

Genera el informe por sustitución de plantilla — el resumen ejecutivo se calcula por agregación real (mismo principio que CT-05), nunca se escribe a mano. Cierra siempre con la advertencia de no-asesoría-legal del Anexo Técnico U3 §16, copiada textual.

## Procedimiento

1. Reúne los hallazgos ya cerrados en G3 (con `evidence_id` real) y la matriz correlacionada en G4.
2. Invoca `.claude/skills/redactar/scripts/generar_reporte.py --cliente "..." --activo "..." --output reporte/reporte_final.md` con los hallazgos por stdin (JSON).
3. Verifica el resultado contra CT-01 (trazabilidad) y CT-07 (cero dato sintético) antes de dar el reporte por cerrado — ver `harness/controles/`.
4. No agregues ninguna oración al reporte que no provenga de los datos de entrada.
