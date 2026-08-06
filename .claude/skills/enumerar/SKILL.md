---
name: enumerar
description: Usar cuando RECON acaba de ejecutar un comando de scope/allowlist.txt y necesita capturar su salida cruda como evidencia con hash y timestamp, antes de que cualquier otro rol la interprete. No usar para analizar, clasificar o resumir el contenido — eso es trabajo de ANALISTA sobre normalizado/, nunca de esta skill.
allowed-tools: Bash
---

Capa 1 (recolección), procedimiento determinista — no hay interpretación posible en esta skill.

## Procedimiento

1. Ejecuta el comando permitido de `scope/allowlist.txt` y captura su salida (stdout + stderr) tal cual, sin editarla ni resumirla.
2. Invoca `.claude/skills/enumerar/scripts/registrar_evidencia.py --nombre <NOMBRE_DESCRIPTIVO> --comando "<comando ejecutado>"`, pasando la salida cruda por stdin.
3. El script escribe el artefacto en `evidencias/raw/<NOMBRE_DESCRIPTIVO>.txt`, calcula su SHA-256 y anexa la línea correspondiente a `evidencias/manifest.sha256`. No lo hagas a mano — el hash calculado por el script es la fuente de verdad, no uno recalculado o copiado por el modelo.
4. Reporta únicamente la ruta del artefacto y su hash. No describas ni interpretes lo que dice el contenido — esa es la frontera con la capa de normalización (capa 2) y con el rol ANALISTA.

## Contrato del script

```
registrar_evidencia.py --nombre <nombre_sin_extension> --comando "<comando textual>" < salida_cruda
```

Salida: JSON de una línea `{"artefacto": "evidencias/raw/<nombre>.txt", "sha256": "<hash>", "timestamp": "<ISO-8601>"}`. Falla (exit != 0) si `<nombre>.txt` ya existe — un artefacto de evidencia nunca se sobrescribe.
