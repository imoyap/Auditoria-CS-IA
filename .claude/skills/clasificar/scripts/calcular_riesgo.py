#!/usr/bin/env python3
"""scripts/calcular_riesgo.py — skill `clasificar` (T-019).

Motor determinista de impacto x probabilidad = riesgo (Anexo Técnico U3
§9-11). No hay margen de criterio libre del modelo: dados los factores
declarados, el resultado es siempre el mismo (extensión D6 aprobada en
LEDGER.md LDG-004).

Cuando un factor de probabilidad es NO_DISPONIBLE (típicamente EPSS/KEV en
un laboratorio sin Internet, Anexo §10 nota de laboratorio), se EXCLUYE de
la suma -- no se cuenta como 0 -- y el resultado se basa en los factores
restantes, exactamente como en los dos ejemplos resueltos del Anexo §15.
"""

from __future__ import annotations

import argparse
import json
import sys

FACTORES_IMPACTO = ["confidencialidad", "integridad", "disponibilidad", "datos_personales", "criticidad_operacional"]
FACTORES_PROBABILIDAD = ["exploit_publico", "epss", "kev", "autenticacion", "exposicion"]

# Tabla de bandas (Anexo §9 y §10 usan la misma tabla de suma -> banda 1-5)
BANDAS_SUMA = [
    (0, 1, 1),
    (2, 3, 2),
    (4, 5, 3),
    (6, 7, 4),
    (8, 10, 5),
]

# Matriz de riesgo 5x5 (Anexo §11)
BANDAS_RIESGO = [
    (1, 4, "Bajo"),
    (5, 9, "Medio"),
    (10, 14, "Alto"),
    (15, 19, "Crítico"),
    (20, 25, "Inaceptable"),
]


def _suma_a_banda(suma: int) -> int:
    for lo, hi, banda in BANDAS_SUMA:
        if lo <= suma <= hi:
            return banda
    raise ValueError(f"Suma {suma} fuera de rango 0-10")


def _riesgo_a_banda(valor: int) -> str:
    for lo, hi, etiqueta in BANDAS_RIESGO:
        if lo <= valor <= hi:
            return etiqueta
    raise ValueError(f"Riesgo {valor} fuera de rango 1-25")


def calcular_impacto(factores: dict) -> dict:
    faltantes = [f for f in FACTORES_IMPACTO if f not in factores]
    if faltantes:
        raise ValueError(f"Faltan factores de impacto obligatorios: {faltantes}")
    suma = sum(int(factores[f]) for f in FACTORES_IMPACTO)
    return {"suma": suma, "banda": _suma_a_banda(suma)}


def calcular_probabilidad(factores: dict) -> dict:
    faltantes = [f for f in FACTORES_PROBABILIDAD if f not in factores]
    if faltantes:
        raise ValueError(f"Faltan factores de probabilidad obligatorios: {faltantes}")

    excluidos = []
    valores = []
    for f in FACTORES_PROBABILIDAD:
        v = factores[f]
        if v == "NO_DISPONIBLE":
            excluidos.append(f)
            continue
        valores.append(int(v))

    suma = sum(valores)
    return {"suma": suma, "banda": _suma_a_banda(suma), "factores_excluidos": excluidos}


def calcular_riesgo(impacto: dict, probabilidad: dict) -> dict:
    valor = impacto["banda"] * probabilidad["banda"]
    return {"valor": valor, "banda": _riesgo_a_banda(valor)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Calcula impacto, probabilidad y riesgo inherente (Anexo §9-11)")
    parser.add_argument("--entrada", help="Ruta a un JSON con {impacto: {...}, probabilidad: {...}}. Si se omite, lee de stdin.")
    args = parser.parse_args()

    texto = open(args.entrada, encoding="utf-8").read() if args.entrada else sys.stdin.read()
    datos = json.loads(texto)

    impacto = calcular_impacto(datos["impacto"])
    probabilidad = calcular_probabilidad(datos["probabilidad"])
    riesgo = calcular_riesgo(impacto, probabilidad)

    print(json.dumps({"impacto": impacto, "probabilidad": probabilidad, "riesgo_inherente": riesgo}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
