#!/usr/bin/env python3
"""harness/controles/ct01_trazabilidad.py — CT-01: Trazabilidad obligatoria
(T-035, REQ-D-04).

Toda afirmación del reporte lleva evidence_id, y ese evidence_id debe
resolver a un artefacto real listado en evidencias/manifest.sha256 --
no basta con que el campo exista, tiene que apuntar a algo verificable.

Error de CertEngine que previene (Anexo Técnico U3 §7): hallazgos sin
respaldo.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

if hasattr(sys.stdin, "reconfigure"):
    sys.stdin.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = REPO_ROOT / "evidencias" / "manifest.sha256"


def _cargar_manifiesto() -> set[str]:
    """Retorna el conjunto de rutas de artefacto (p. ej.
    'evidencias/raw/04_nmap_sv.txt') listadas en el manifiesto."""
    if not MANIFEST_PATH.exists():
        return set()
    rutas = set()
    for linea in MANIFEST_PATH.read_text(encoding="utf-8").splitlines():
        if not linea.strip():
            continue
        _hash, _, ruta = linea.partition("*")
        rutas.add(ruta.strip())
    return rutas


def verificar(afirmaciones: list[dict]) -> list[str]:
    rutas_manifiesto = _cargar_manifiesto()
    # evidence_id es el nombre del artefacto sin extensión -- la extensión
    # real varía (.txt para salida de comandos, .png para capturas, etc.),
    # así que se compara por stem, no asumiendo una extensión fija (bug
    # real encontrado probando este script con la captura de G0, que es
    # .png, no .txt).
    stems_manifiesto = {Path(r).stem for r in rutas_manifiesto}

    errores = []
    for a in afirmaciones:
        evidence_id = a.get("evidence_id")
        if not evidence_id:
            errores.append(f"Afirmación sin evidence_id: {a.get('afirmacion', '?')!r}")
            continue
        if evidence_id not in stems_manifiesto:
            errores.append(
                f"evidence_id {evidence_id!r} no resuelve a ningún artefacto en evidencias/manifest.sha256 "
                f"(afirmación: {a.get('afirmacion', '?')!r})"
            )
    return errores


def main() -> int:
    datos = json.loads(sys.stdin.read())
    errores = verificar(datos["afirmaciones"])
    if errores:
        for e in errores:
            print(e, file=sys.stderr)
        return 2
    print(f"OK: {len(datos['afirmaciones'])} afirmación(es), todas trazables a un artefacto real")
    return 0


if __name__ == "__main__":
    sys.exit(main())
