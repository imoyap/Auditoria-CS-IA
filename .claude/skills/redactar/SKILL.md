---
name: redactar
description: Usar cuando REDACTOR necesita generar o actualizar reporte/reporte_final.md a partir de hallazgos y matriz ya verificados en G3/G4, nunca a partir de texto libre no trazable a evidence_id.
allowed-tools: Bash
---

Genera el informe por sustitución de plantilla — el resumen ejecutivo se calcula por agregación real (mismo principio que CT-05), nunca se escribe a mano. Cierra siempre con la advertencia de no-asesoría-legal del Anexo Técnico U3 §16, copiada textual.

## Procedimiento

1. Reúne los hallazgos ya cerrados en G3 (con `evidence_id` real) y la matriz correlacionada en G4 (`normalizado/matriz_borrador.csv`).
2. Para cada hallazgo con `Riesgo_residual` numérico (VALIDADO/OBSERVADO), invoca `.claude/skills/priorizar/scripts/priorizar.py` por stdin (JSON `{"hallazgos": [...]}`) para obtener `plazo_referencia` por banda (Anexo §11). Un hallazgo con `Riesgo_residual=NO_OBSERVADO` (p. ej. INCONCLUSO) no se le pasa a `priorizar.py` — no tiene banda que calcular.
3. Invoca `.claude/skills/redactar/scripts/generar_reporte.py --cliente "..." --activo "..." --output reporte/reporte_final.md --matriz-entrada normalizado/matriz_borrador.csv --matriz-salida reporte/matriz_correlacion.csv` con un único JSON por stdin: `{"hallazgos": [...], "plazos_referencia": {"check_id": "plazo o NO_OBSERVADO", ...}}`. Esta única invocación genera ambos archivos: `reporte_final.md` y `reporte/matriz_correlacion.csv` (la matriz de G4 con la columna `Plazo_referencia` agregada).
4. Verifica el resultado contra CT-01 (trazabilidad) y CT-07 (cero dato sintético) antes de dar el reporte por cerrado — ver `harness/controles/`.
5. No agregues ninguna oración al reporte que no provenga de los datos de entrada.
