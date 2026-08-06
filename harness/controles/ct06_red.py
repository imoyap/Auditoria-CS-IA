#!/usr/bin/env python3
"""harness/controles/ct06_red.py — CT-06: Estado condicionado por la red
(T-023, REQ-D-09).

Regla: si el intento de verificación adicional de un hallazgo falló por
una condición de red (timeout, NAT, sin ruta), el estado máximo posible es
INCONCLUSO -- sin excepción, sin importar cuán fuerte parezca el indicio
original.

Error de CertEngine que previene (Anexo Técnico U3 §7): hallazgos
bloqueados por NAT marcados "Verified".
"""

from __future__ import annotations

import argparse
import sys

MOTIVOS_RED = {"timeout", "nat", "sin_ruta", "sin-ruta", "connection_refused", "unreachable"}
ESTADOS_VALIDOS = {"VALIDADO", "OBSERVADO", "INCONCLUSO"}


def evaluar(motivo_fallo_red: str, estado_propuesto: str) -> tuple[bool, str]:
    if estado_propuesto not in ESTADOS_VALIDOS:
        return False, f"Estado propuesto {estado_propuesto!r} no es uno de {ESTADOS_VALIDOS}"

    hubo_fallo_red = bool(motivo_fallo_red) and motivo_fallo_red.strip().lower() in MOTIVOS_RED

    if hubo_fallo_red and estado_propuesto != "INCONCLUSO":
        return False, (
            f"El intento de verificación falló por condición de red ({motivo_fallo_red!r}); "
            f"el estado máximo posible es INCONCLUSO, no {estado_propuesto!r} (CT-06)"
        )

    return True, "OK" if not hubo_fallo_red else "Fallo de red respetado: estado forzado/consistente con INCONCLUSO"


def main() -> int:
    parser = argparse.ArgumentParser(description="CT-06: valida que un fallo de verificación por red no permita un estado distinto de INCONCLUSO")
    parser.add_argument("--motivo-fallo-red", default="", help="Motivo del fallo de verificación si lo hubo (timeout, nat, sin_ruta, etc.); vacío si no hubo fallo de red")
    parser.add_argument("--estado-propuesto", required=True, choices=sorted(ESTADOS_VALIDOS))
    args = parser.parse_args()

    ok, detalle = evaluar(args.motivo_fallo_red, args.estado_propuesto)
    print(detalle, file=sys.stdout if ok else sys.stderr)
    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main())
