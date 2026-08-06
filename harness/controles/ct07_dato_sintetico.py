#!/usr/bin/env python3
"""harness/controles/ct07_dato_sintetico.py — CT-07: Cero dato sintético
(T-035, REQ-D-10).

Si un dato no existe, la ausencia se mide, se fecha y se muestra como
hallazgo -- nunca se rellena. Todo campo obligatorio debe tener un valor
real o el marcador explícito NO_OBSERVADO / NO_DISPONIBLE, nunca quedar
vacío, en None, o con un valor por defecto no declarado como tal.

Error de CertEngine que previene (Anexo Técnico U3 §7): informe simétrico
y completo sobre datos incompletos.
"""

from __future__ import annotations

import json
import sys

if hasattr(sys.stdin, "reconfigure"):
    sys.stdin.reconfigure(encoding="utf-8")

MARCADORES_VALIDOS = {"NO_OBSERVADO", "NO_DISPONIBLE"}


def verificar(registro: dict, campos_obligatorios: list[str]) -> list[str]:
    errores = []
    for campo in campos_obligatorios:
        valor = registro.get(campo, None)
        vacio = valor is None or (isinstance(valor, str) and valor.strip() == "")
        if vacio:
            errores.append(
                f"Campo obligatorio {campo!r} está vacío sin marcador NO_OBSERVADO/NO_DISPONIBLE (CT-07)"
            )
    return errores


def main() -> int:
    datos = json.loads(sys.stdin.read())
    errores = verificar(datos["registro"], datos["campos_obligatorios"])
    if errores:
        for e in errores:
            print(e, file=sys.stderr)
        return 2
    print(f"OK: {len(datos['campos_obligatorios'])} campo(s) obligatorio(s), ninguno vacío sin marcador")
    return 0


if __name__ == "__main__":
    sys.exit(main())
