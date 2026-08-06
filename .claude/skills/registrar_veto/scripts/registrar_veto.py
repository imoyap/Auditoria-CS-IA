#!/usr/bin/env python3
"""scripts/registrar_veto.py — único canal de escritura de VERIFICADOR
(T-022, soporte de REQ-B-03).

No toca normalizado/candidatos.json ni ningún otro archivo de estado de
hallazgos: la garantía de que VERIFICADOR no puede escribir VALIDADO no es
un filtro de palabras sobre el texto, es que este script *no tiene* ninguna
ruta de código que modifique el campo de estado de un hallazgo. Su único
efecto posible es anexar una línea a LEDGER.md, y solo de tipo RECHAZO o
DECISION -- HALLAZGO, GATE y SUPERSEDE no son de este rol.
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
LEDGER_PATH = REPO_ROOT / "LEDGER.md"

TIPOS_PERMITIDOS = ("RECHAZO", "DECISION")


def registrar(tipo: str, resumen: str, ref: str, actor: str = "VERIFICADOR") -> str:
    if tipo not in TIPOS_PERMITIDOS:
        raise ValueError(
            f"tipo {tipo!r} no permitido para este rol. Solo {TIPOS_PERMITIDOS} "
            f"-- VERIFICADOR no tiene canal para HALLAZGO, GATE ni SUPERSEDE, "
            f"y jamás para asignar VALIDADO directamente."
        )

    ts = datetime.now().astimezone().isoformat(timespec="seconds")
    ident = f"LDG-VETO-{int(datetime.now().timestamp() * 1000)}"
    linea = f"{ts} | {ident} | {tipo} | {actor} | {resumen} | {ref}\n"

    with LEDGER_PATH.open("a", encoding="utf-8") as f:
        f.write(linea)

    return linea.rstrip("\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Registra un veto o decisión de VERIFICADOR en LEDGER.md")
    parser.add_argument("--tipo", required=True, choices=TIPOS_PERMITIDOS)
    parser.add_argument("--resumen", required=True, help="Resumen en una línea, debe citar el evidence_id que sostiene el veto/decisión")
    parser.add_argument("--ref", required=True, help="Referencia, p. ej. ev:manifest.sha256 o gate:G3")
    parser.add_argument("--actor", default="VERIFICADOR")
    args = parser.parse_args()

    try:
        linea = registrar(args.tipo, args.resumen, args.ref, args.actor)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    print(linea)
    return 0


if __name__ == "__main__":
    sys.exit(main())
