#!/usr/bin/env python3
"""scripts/priorizar.py — skill `priorizar` (T-030, REQ-G-03).

Ordena hallazgos por riesgo RESIDUAL descendente y asigna el plazo de
referencia según la banda de la matriz 5x5 (Anexo Técnico U3 §11) -- no
un plazo arbitrario. El "plazo de referencia" es la SLA de seguimiento
por banda de riesgo; un plazo de remediación más estricto elegido por el
equipo (columna "Plazo" de la matriz de correlación) es una decisión
aparte y puede ser más corto, nunca más largo que esta referencia.
"""

from __future__ import annotations

import json
import sys

if hasattr(sys.stdin, "reconfigure"):
    sys.stdin.reconfigure(encoding="utf-8")

BANDAS_PLAZO = [
    (1, 4, "Ciclo anual"),
    (5, 9, "90 días"),
    (10, 14, "30 días"),
    (15, 19, "7 días"),
    (20, 25, "24 - 48 horas"),
]


def plazo_referencia(riesgo_residual: int) -> str:
    for lo, hi, plazo in BANDAS_PLAZO:
        if lo <= riesgo_residual <= hi:
            return plazo
    raise ValueError(f"Riesgo residual {riesgo_residual} fuera de rango 1-25")


def priorizar(hallazgos: list[dict]) -> list[dict]:
    anotados = []
    for h in hallazgos:
        h2 = dict(h)
        h2["plazo_referencia"] = plazo_referencia(int(h["riesgo_residual"]))
        anotados.append(h2)
    return sorted(anotados, key=lambda h: h["riesgo_residual"], reverse=True)


def main() -> int:
    datos = json.loads(sys.stdin.read())
    resultado = priorizar(datos["hallazgos"])
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
