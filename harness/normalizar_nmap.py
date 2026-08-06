#!/usr/bin/env python3
"""harness/normalizar_nmap.py — capa 2, normalización (T-015, criterio G2).

Parser DETERMINISTA (sin LLM) de salida de `nmap -sV`. Regla de oro de la
capa 2 (Anexo Técnico U3 §3): el modelo de lenguaje nunca lee la terminal
directamente -- lee este JSON canónico. Cada servicio queda con puntero
a la línea exacta del artefacto crudo de origen (criterio de cierre de
G2: "Cero servicios sin origen").

No interpreta versiones ni asigna severidad -- eso es trabajo de
ANALISTA (capa 5) sobre este JSON, no de esta capa.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# PORT      STATE SERVICE     VERSION
# 21/tcp    open  ftp         vsftpd 2.3.4
LINEA_PUERTO = re.compile(
    r"^(?P<puerto>\d+)/(?P<protocolo>tcp|udp)\s+"
    r"(?P<estado>\S+)\s+"
    r"(?P<servicio>\S+)\s*"
    r"(?P<version>.*)$"
)


def parsear(ruta_evidencia: Path, evidence_id: str) -> list[dict]:
    servicios = []
    lineas = ruta_evidencia.read_text(encoding="utf-8", errors="replace").splitlines()
    for numero_linea, linea in enumerate(lineas, start=1):
        m = LINEA_PUERTO.match(linea)
        if not m:
            continue
        servicios.append({
            "puerto": int(m.group("puerto")),
            "protocolo": m.group("protocolo"),
            "estado": m.group("estado"),
            "servicio": m.group("servicio"),
            "version": m.group("version").strip() or "NO_OBSERVADO",
            "evidence_id": evidence_id,
            "linea_origen": numero_linea,
        })
    return servicios


def main() -> int:
    parser = argparse.ArgumentParser(description="Normaliza salida de nmap a JSON canónico (capa 2, determinista)")
    parser.add_argument("--evidence-id", required=True, help="ID del artefacto en evidencias/raw/ (sin extensión)")
    parser.add_argument("--output", default=str(REPO_ROOT / "normalizado" / "inventario.json"))
    args = parser.parse_args()

    ruta_evidencia = REPO_ROOT / "evidencias" / "raw" / f"{args.evidence_id}.txt"
    if not ruta_evidencia.exists():
        print(f"ERROR: no existe {ruta_evidencia}", file=sys.stderr)
        return 1

    servicios = parsear(ruta_evidencia, args.evidence_id)

    sin_origen = [s for s in servicios if "linea_origen" not in s or not s["linea_origen"]]
    if sin_origen:
        print(f"ERROR: {len(sin_origen)} servicio(s) sin línea de origen -- viola criterio de cierre de G2", file=sys.stderr)
        return 2

    salida = Path(args.output)
    salida.parent.mkdir(parents=True, exist_ok=True)
    salida.write_text(json.dumps({"servicios": servicios}, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")

    print(f"OK: {len(servicios)} servicio(s) normalizados, todos con línea de origen, escritos en {salida}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
