#!/usr/bin/env python3
"""harness/controles/ct04_remediacion.py — CT-04: Remediación aplicable
(T-031, REQ-D-07, REQ-G-04).

La remediación no puede apuntar a la versión vulnerable ni a un
componente inexistente. Verifica que la versión objetivo de la
remediación sea distinta de la versión instalada (evidenciada).

Error de CertEngine que previene (Anexo Técnico U3 §7): remediación que
recomendaba la misma versión afectada.
"""

from __future__ import annotations

import argparse
import sys


def verificar(version_instalada: str, version_objetivo: str) -> tuple[bool, str]:
    a = version_instalada.strip().lower()
    b = version_objetivo.strip().lower()

    if not b:
        return False, "La remediación no declara una versión objetivo -- no es aplicable"

    if a == b:
        return False, (
            f"La remediación recomienda la misma versión instalada/vulnerable "
            f"({version_instalada!r}) -- remediación no aplicable (CT-04)"
        )

    return True, f"Versión objetivo ({version_objetivo!r}) distinta de la instalada ({version_instalada!r})"


def main() -> int:
    parser = argparse.ArgumentParser(description="CT-04: la remediación no puede apuntar a la versión vulnerable")
    parser.add_argument("--version-instalada", required=True)
    parser.add_argument("--version-objetivo-remediacion", required=True)
    args = parser.parse_args()

    ok, detalle = verificar(args.version_instalada, args.version_objetivo_remediacion)
    print(detalle, file=sys.stdout if ok else sys.stderr)
    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main())
