#!/usr/bin/env python3
"""harness/controles/ct03_severidad.py — CT-03: Coherencia de severidad
(T-028, REQ-D-06).

Un mismo hallazgo debe tener la misma severidad en la matriz de
correlación, la tabla resumen y su ficha de detalle. Comparación
automática -- no por lectura manual.

Error de CertEngine que previene (Anexo Técnico U3 §7): severidades
contradictorias entre resumen y detalle.
"""

from __future__ import annotations

import json
import sys


def verificar(hallazgos: list[dict]) -> list[str]:
    """Cada hallazgo: {"check_id": str, "severidad_matriz": str,
    "severidad_tabla": str, "severidad_ficha": str}. Retorna lista de
    mensajes de error (vacía si todo consistente)."""
    errores = []
    for h in hallazgos:
        valores = {
            "matriz": h.get("severidad_matriz"),
            "tabla": h.get("severidad_tabla"),
            "ficha": h.get("severidad_ficha"),
        }
        distintos = set(valores.values())
        if len(distintos) > 1:
            errores.append(
                f"{h.get('check_id', '?')}: severidad inconsistente entre secciones -> {valores}"
            )
    return errores


def main() -> int:
    datos = json.loads(sys.stdin.read())
    errores = verificar(datos["hallazgos"])
    if errores:
        for e in errores:
            print(e, file=sys.stderr)
        return 2
    print(f"OK: {len(datos['hallazgos'])} hallazgo(s), severidad consistente en las 3 secciones")
    return 0


if __name__ == "__main__":
    sys.exit(main())
