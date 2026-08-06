#!/usr/bin/env python3
"""harness/controles/ct02_inferencia.py — CT-02: Prohibición de inferencia de
servicio (T-020, REQ-D-05).

No se declara un producto/versión que no aparezca literalmente en un
artefacto crudo de evidencias/raw/. Búsqueda de cadena exacta (substring,
no difusa) -- si la cadena no está, el candidato se rechaza, sin importar
cuán probable parezca la inferencia.

Error de CertEngine que previene (Anexo Técnico U3 §7): hallazgo de CMS y
de registro SPF fabricados a partir de indicios indirectos, no de la
cadena real presente en la evidencia.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = REPO_ROOT / "evidencias" / "raw"


def verificar_cadena_literal(cadena: str, evidence_id: str) -> tuple[bool, str]:
    """evidence_id es el nombre del artefacto sin extensión, tal como lo
    escribe scripts/registrar_evidencia.py (evidencias/raw/<evidence_id>.txt)."""
    archivo = RAW_DIR / f"{evidence_id}.txt"
    if not archivo.exists():
        return False, f"No existe el artefacto evidencias/raw/{evidence_id}.txt"

    contenido = archivo.read_text(encoding="utf-8", errors="replace")
    if cadena in contenido:
        return True, f"Cadena {cadena!r} encontrada literalmente en evidencias/raw/{evidence_id}.txt"
    return False, f"Cadena {cadena!r} NO aparece literalmente en evidencias/raw/{evidence_id}.txt — inferencia no sostenida"


def main() -> int:
    parser = argparse.ArgumentParser(description="CT-02: verifica que una cadena de producto/versión aparezca literalmente en la evidencia cruda")
    parser.add_argument("--cadena", required=True, help="Cadena literal a buscar (p. ej. nombre de producto o versión)")
    parser.add_argument("--evidence-id", required=True, help="ID del artefacto en evidencias/raw/ (sin extensión)")
    args = parser.parse_args()

    ok, detalle = verificar_cadena_literal(args.cadena, args.evidence_id)
    print(detalle, file=sys.stdout if ok else sys.stderr)
    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main())
