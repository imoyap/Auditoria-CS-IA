#!/usr/bin/env python3
"""scripts/registrar_evidencia.py — skill `enumerar` (T-012, REQ-D-01, REQ-D-02).

Lee salida cruda por stdin, la escribe SIN editar a evidencias/raw/<nombre>.txt,
calcula su SHA-256 real y anexa la línea al manifiesto. No interpreta el
contenido — esa es la regla de oro de la capa 2 (Anexo Técnico U3 §3): el
modelo nunca lee la terminal directamente, siempre lee el artefacto ya
capturado y su hash verificable.

Un artefacto nunca se sobrescribe: si <nombre>.txt ya existe, el script falla
en vez de aceptar una segunda versión silenciosa del mismo nombre.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
RAW_DIR = REPO_ROOT / "evidencias" / "raw"
MANIFEST_PATH = REPO_ROOT / "evidencias" / "manifest.sha256"


def main() -> int:
    parser = argparse.ArgumentParser(description="Registra un artefacto de evidencia cruda con hash y timestamp")
    parser.add_argument("--nombre", required=True, help="Nombre del artefacto, sin extensión (p. ej. 01_nmap_sv)")
    parser.add_argument("--comando", required=True, help="Comando textual que produjo esta salida (metadato, no se ejecuta aquí)")
    args = parser.parse_args()

    if "/" in args.nombre or "\\" in args.nombre or ".." in args.nombre:
        print(f"ERROR: nombre inválido (sin rutas): {args.nombre!r}", file=sys.stderr)
        return 1

    destino = RAW_DIR / f"{args.nombre}.txt"
    if destino.exists():
        print(f"ERROR: {destino} ya existe — un artefacto de evidencia nunca se sobrescribe", file=sys.stderr)
        return 1

    contenido_crudo = sys.stdin.buffer.read()

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    destino.write_bytes(contenido_crudo)

    sha256 = hashlib.sha256(contenido_crudo).hexdigest()
    ruta_relativa = destino.relative_to(REPO_ROOT).as_posix()

    # newline="" evita que Python traduzca "\n" a "\r\n" en modo texto de
    # Windows -- bug real encontrado verificando el manifiesto en T-014
    # (sha256sum -c fallaba por un \r colgante en la línea nueva).
    with MANIFEST_PATH.open("a", encoding="utf-8", newline="") as f:
        f.write(f"{sha256} *{ruta_relativa}\n")

    timestamp = datetime.now().astimezone().isoformat(timespec="seconds")
    salida = {
        "artefacto": ruta_relativa,
        "sha256": sha256,
        "timestamp": timestamp,
        "comando": args.comando,
    }
    print(json.dumps(salida, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
