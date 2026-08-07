#!/usr/bin/env python3
"""scripts/registrar_objecion.py — único canal de escritura de CONTRADICTOR
(T-041, dimensión de extensión D2, Anexo Técnico U3 §4).

CONTRADICTOR es el rol "cuyo único trabajo es construir el mejor
argumento en contra del cierre de cada hallazgo" (Anexo §4). Este script
SOLO puede anexar una entrada RECHAZO al ledger -- nunca puede cambiar el
estado de un candidato, nunca escribe a normalizado/candidatos.json ni a
ningún otro archivo de datos. Si la objeción tiene mérito, es un HUMANO
(o VERIFICADOR/ORQUESTADOR mediante sus propios canales) quien decide
actuar sobre ella -- CONTRADICTOR nunca actúa directamente sobre el
estado de un hallazgo, solo lo pone en cuestión por escrito.
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
LEDGER_PATH = REPO_ROOT / "LEDGER.md"


def registrar(check_id: str, objecion: str, ref: str) -> str:
    ts = datetime.now().astimezone().isoformat(timespec="seconds")
    ident = f"LDG-D2-{int(datetime.now().timestamp() * 1000)}"
    resumen = f"Objeción sobre {check_id}: {objecion}"
    linea = f"{ts} | {ident} | RECHAZO | CONTRADICTOR | {resumen} | {ref}\n"
    with LEDGER_PATH.open("a", encoding="utf-8", newline="") as f:
        f.write(linea)
    return linea.rstrip("\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Registra una objeción de CONTRADICTOR en LEDGER.md")
    parser.add_argument("--check-id", required=True)
    parser.add_argument("--objecion", required=True, help="El mejor argumento en contra del cierre actual de este hallazgo, citando evidencia")
    parser.add_argument("--ref", required=True, help="p. ej. ev:01_nmap_full o gate:G3")
    args = parser.parse_args()

    linea = registrar(args.check_id, args.objecion, args.ref)
    print(linea)
    return 0


if __name__ == "__main__":
    sys.exit(main())
