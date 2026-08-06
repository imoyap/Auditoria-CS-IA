#!/usr/bin/env python3
"""Test determinista de calcular_riesgo.py contra los 2 ejemplos numéricos
completos del Anexo Técnico U3 §15 (Ejemplo 1 - Telnet, Ejemplo 2 - vsftpd).
El Ejemplo 3 (ausencia) no se prueba aquí porque el propio Anexo indica que
no se calcula: "sin verificación, no se asigna riesgo cuantitativo" -- no
hay un resultado numérico esperado contra el cual comparar.

Ejecutar: python calcular_riesgo.py de este mismo directorio.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from calcular_riesgo import calcular_impacto, calcular_probabilidad, calcular_riesgo

CASOS = [
    {
        "nombre": "Ejemplo 1 — Telnet expuesto (Anexo §15)",
        "impacto": {"confidencialidad": 2, "integridad": 1, "disponibilidad": 0, "datos_personales": 1, "criticidad_operacional": 2},
        "probabilidad": {"exploit_publico": 0, "epss": "NO_DISPONIBLE", "kev": 0, "autenticacion": 2, "exposicion": 1},
        "esperado": {"impacto_suma": 6, "impacto_banda": 4, "probabilidad_suma": 3, "probabilidad_banda": 2, "riesgo_valor": 8, "riesgo_banda": "Medio"},
    },
    {
        "nombre": "Ejemplo 2 — vsftpd 2.3.4 (Anexo §15)",
        "impacto": {"confidencialidad": 2, "integridad": 2, "disponibilidad": 2, "datos_personales": 1, "criticidad_operacional": 2},
        "probabilidad": {"exploit_publico": 2, "epss": "NO_DISPONIBLE", "kev": 0, "autenticacion": 2, "exposicion": 1},
        "esperado": {"impacto_suma": 9, "impacto_banda": 5, "probabilidad_suma": 5, "probabilidad_banda": 3, "riesgo_valor": 15, "riesgo_banda": "Crítico"},
    },
]


def main() -> int:
    fallos = 0
    for caso in CASOS:
        impacto = calcular_impacto(caso["impacto"])
        probabilidad = calcular_probabilidad(caso["probabilidad"])
        riesgo = calcular_riesgo(impacto, probabilidad)
        esperado = caso["esperado"]

        checks = [
            ("impacto.suma", impacto["suma"], esperado["impacto_suma"]),
            ("impacto.banda", impacto["banda"], esperado["impacto_banda"]),
            ("probabilidad.suma", probabilidad["suma"], esperado["probabilidad_suma"]),
            ("probabilidad.banda", probabilidad["banda"], esperado["probabilidad_banda"]),
            ("riesgo.valor", riesgo["valor"], esperado["riesgo_valor"]),
            ("riesgo.banda", riesgo["banda"], esperado["riesgo_banda"]),
        ]

        print(f"\n{caso['nombre']}")
        for campo, obtenido, esp in checks:
            ok = obtenido == esp
            estado = "OK" if ok else "FALLO"
            print(f"  [{estado}] {campo}: obtenido={obtenido!r} esperado={esp!r}")
            if not ok:
                fallos += 1

    print(f"\n{'TODOS LOS CASOS PASARON' if fallos == 0 else f'{fallos} verificaciones fallaron'}")
    return 1 if fallos else 0


if __name__ == "__main__":
    sys.exit(main())
