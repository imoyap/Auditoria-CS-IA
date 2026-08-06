---
name: priorizar
description: Usar cuando hay hallazgos ya correlacionados con riesgo residual calculado y hace falta ordenarlos y asignarles un plazo de referencia de seguimiento según la banda del Anexo Técnico U3 §11 — nunca un plazo elegido a criterio libre.
allowed-tools: Bash
---

Ordena por `riesgo_residual` descendente (los de mayor riesgo primero) y asigna `plazo_referencia` por banda (Bajo→ciclo anual, Medio→90 días, Alto→30 días, Crítico→7 días, Inaceptable→24-48 horas). Es la SLA de seguimiento, no reemplaza un plazo de remediación más estricto que el equipo ya haya elegido en la matriz de correlación.

## Contrato

Entrada (stdin, JSON): `{"hallazgos": [{"check_id": "H-01", "riesgo_residual": 4, ...}, ...]}`
Salida: la misma lista, ordenada descendente por `riesgo_residual`, con el campo `plazo_referencia` agregado a cada elemento.
