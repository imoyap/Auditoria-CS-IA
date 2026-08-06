#!/usr/bin/env python3
"""scripts/correlacionar.py — skill `correlacionar` (T-026, REQ-F-01..05).

Anexa una fila a normalizado/matriz_borrador.csv con las columnas mínimas
del Anexo Técnico U3 §13. Una vez que un check_id tiene fila, esta fila es
inmutable para este script -- no existe una ruta de código para modificar
una fila ya escrita, así que COMPLIANCE no puede alterar la severidad de
un hallazgo que ANALISTA/VERIFICADOR ya cerraron (Anexo §4: "Herramientas
que NO tiene: Modificación de severidades").

Los valores de los controles ISO/NIST/CIS/CL deben venir de una consulta
real al MCP de conocimiento normativo (mcp/conocimiento_normativo) hecha
por el rol COMPLIANCE antes de invocar este script -- este script no
consulta el corpus, solo persiste lo ya decidido con su fuente.
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

if hasattr(sys.stdin, "reconfigure"):
    sys.stdin.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parents[4]
MATRIZ_PATH = REPO_ROOT / "normalizado" / "matriz_borrador.csv"

COLUMNAS = [
    "ID", "Hallazgo", "evidence_id", "Estado", "CWE", "CVE", "Vector_CVSS", "I", "P", "Riesgo",
    "Control_ISO", "NIST", "Control_CIS", "Obligacion_CL", "Aplica_porque", "Evidencia_requerida",
    "Brecha", "Remediacion", "Esfuerzo", "Responsable", "Plazo", "Riesgo_residual",
]


def _leer_existentes() -> dict[str, dict]:
    if not MATRIZ_PATH.exists():
        return {}
    with MATRIZ_PATH.open(encoding="utf-8", newline="") as f:
        return {fila["ID"]: fila for fila in csv.DictReader(f)}


def correlacionar(fila: dict) -> tuple[bool, str]:
    faltantes = [c for c in COLUMNAS if c not in fila]
    if faltantes:
        return False, f"Faltan columnas obligatorias: {faltantes}"

    existentes = _leer_existentes()
    if fila["ID"] in existentes:
        return False, (
            f"El hallazgo {fila['ID']!r} ya tiene una fila en la matriz -- este script no modifica "
            f"filas existentes (protege contra alteración de severidad ya cerrada, Anexo §4)"
        )

    escribir_encabezado = not MATRIZ_PATH.exists()
    MATRIZ_PATH.parent.mkdir(parents=True, exist_ok=True)
    with MATRIZ_PATH.open("a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNAS)
        if escribir_encabezado:
            writer.writeheader()
        writer.writerow(fila)

    return True, f"Fila anexada para {fila['ID']!r}"


def main() -> int:
    fila = json.loads(sys.stdin.read())
    ok, detalle = correlacionar(fila)
    print(detalle, file=sys.stdout if ok else sys.stderr)
    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main())
