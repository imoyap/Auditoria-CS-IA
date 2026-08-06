---
name: correlacionar
description: Usar cuando COMPLIANCE necesita mapear un hallazgo ya cerrado en G3 (VALIDADO/OBSERVADO/INCONCLUSO) a control ISO/IEC 27001:2022 Anexo A, categoría NIST CSF 2.0, control CIS v8 y obligación normativa chilena, citando el MCP de conocimiento normativo. Nunca usar sobre un candidato sin verificar, y nunca para modificar la severidad de un hallazgo ya cerrado — este script no puede hacerlo.
allowed-tools: Bash, mcp__conocimiento-normativo
---

## Procedimiento

1. Consulta `mcp__conocimiento-normativo` (`buscar_control_iso`, `buscar_categoria_nist`, `buscar_control_cis`, `buscar_obligacion_cl`) por cada marco relevante al hallazgo. Si una consulta retorna `NO_OBSERVADO`, escribe `NO_OBSERVADO` en esa columna — nunca fuerces un mapeo genérico para llenar la celda (evita el error de la Parte VI: "todos los hallazgos mapean al mismo control").
2. Redacta la columna "Aplica porque" específica del hallazgo y del cliente (Comercial Andes Sur SpA) — nunca una copia del artículo de la ley.
3. Declara la columna "Evidencia requerida": qué se le exhibiría a un fiscalizador o auditor de certificación.
4. Invoca `.claude/skills/correlacionar/scripts/correlacionar.py` con las 21 columnas del Anexo §13 por stdin (JSON).
5. Si el hallazgo ya tiene una fila en la matriz, el script se niega a modificarla — esto es intencional, no un bug a reportar.

## Contrato

Entrada (stdin, JSON): objeto con las 21 columnas exactas: `ID, Hallazgo, evidence_id, Estado, CWE, CVE, Vector_CVSS, I, P, Riesgo, Control_ISO, NIST, Control_CIS, Obligacion_CL, Aplica_porque, Evidencia_requerida, Brecha, Remediacion, Esfuerzo, Responsable, Plazo, Riesgo_residual`.

Salida: anexa una fila a `normalizado/matriz_borrador.csv`. Falla (exit 2) si el `ID` ya existe en la matriz.
