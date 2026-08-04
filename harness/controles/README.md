# harness/controles/

Los 7 controles anti-alucinación (Anexo Técnico U3 §7), cada uno como script ejecutable, no como mención en un documento:

| Script | Se ejecuta antes de | REQ |
|---|---|---|
| `ct01_trazabilidad.py` | G5 | REQ-D-04 |
| `ct02_inferencia.py` | admisión de cada candidato (dentro de `clasificar`) | REQ-D-05 |
| `ct03_severidad.py` | G4/G5 | REQ-D-06 |
| `ct04_remediacion.py` | G5 | REQ-D-07 |
| `ct05_consistencia.py` | G5 | REQ-D-08 |
| `ct06_red.py` | verificación adicional de VERIFICADOR | REQ-D-09 |
| `ct07_dato_sintetico.py` | G3, G4, G5 | REQ-D-10 |
| `reject_and_log.sh` | hook `PreToolUse` de cada subagente con escritura restringida | REQ-B-03 |

Ver `docs/design.md`, tabla de controles CT-01..07, y `docs/tasks.md` T-008, T-020, T-023, T-028, T-031, T-032, T-035.
