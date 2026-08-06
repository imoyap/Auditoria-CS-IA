---
name: clasificar
description: Usar cuando ANALISTA tiene un hallazgo candidato con sus factores de impacto y probabilidad declarados, y necesita calcular impacto (1-5), probabilidad (1-5) y riesgo inherente (1-25) siguiendo las tablas del Anexo Técnico U3 §9-11. Nunca usar para asignar un riesgo por criterio libre — si faltan factores, el script falla en vez de adivinar.
allowed-tools: Bash
---

Capa de análisis, motor determinista (extensión **D6**, `LEDGER.md` `LDG-004`) — el resultado no depende del criterio del modelo, depende solo de los factores que declares.

## Procedimiento

1. Declara los 5 factores de impacto (`confidencialidad`, `integridad`, `disponibilidad`, `datos_personales`, `criticidad_operacional`, cada uno 0/1/2 según el Anexo §9) y los 5 de probabilidad (`exploit_publico`, `epss`, `kev`, `autenticacion`, `exposicion`, cada uno 0/1/2, o `"NO_DISPONIBLE"` para `epss`/`kev` si el laboratorio no tiene esa fuente — Anexo §10, nota de laboratorio).
2. Invoca `.claude/skills/clasificar/scripts/calcular_riesgo.py` con ese JSON por stdin.
3. El script calcula impacto, probabilidad (excluyendo del promedio cualquier factor `NO_DISPONIBLE`, nunca tratándolo como 0) y riesgo inherente = impacto × probabilidad, con su banda (Bajo/Medio/Alto/Crítico/Inaceptable).
4. Si algún factor obligatorio falta, el script falla (no calcula con un valor supuesto) — vuelve a ANALISTA y complétalo o decláralo `NO_DISPONIBLE` explícitamente.

## Contrato

Entrada (stdin, JSON):
```json
{"impacto": {"confidencialidad": 2, "integridad": 1, "disponibilidad": 0, "datos_personales": 1, "criticidad_operacional": 2},
 "probabilidad": {"exploit_publico": 0, "epss": "NO_DISPONIBLE", "kev": 0, "autenticacion": 2, "exposicion": 1}}
```

Salida: JSON con `impacto.banda`, `probabilidad.banda`, `probabilidad.factores_excluidos`, `riesgo_inherente.valor` y `riesgo_inherente.banda`.

Verificado contra los 2 ejemplos numéricos completos del Anexo §15 (Telnet y vsftpd) en `.claude/skills/clasificar/scripts/test_calcular_riesgo.py`.
