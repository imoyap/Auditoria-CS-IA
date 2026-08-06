#!/usr/bin/env python3
"""harness/controles/ct05_consistencia.py — CT-05: Consistencia numérica
(T-032, REQ-D-08, REQ-G-02).

Los conteos y cifras del resumen ejecutivo se recalculan desde los datos,
no se escriben a mano. Este validador recalcula por agregación sobre la
lista real de hallazgos y compara byte a byte (campo a campo) contra el
resumen publicado -- cualquier discrepancia se rechaza.

Error de CertEngine que previene (Anexo Técnico U3 §7): cifras divergentes
entre secciones del informe.
"""

from __future__ import annotations

import json
import sys

# En Windows, sys.stdin no siempre decodifica como UTF-8 por defecto (usa el
# codepage de la consola) -- encontrado probando este mismo script: "Crítica"
# llegaba corrompido byte a byte. Se fuerza UTF-8 explícitamente en vez de
# confiar en el default de la plataforma.
if hasattr(sys.stdin, "reconfigure"):
    sys.stdin.reconfigure(encoding="utf-8")

SEVERIDADES = ["critica", "alta", "media", "baja"]
# Match por prefijo, no por igualdad estricta: consolas Windows con
# codepage distinto de UTF-8 pueden corromper la tilde de "crítica" al
# pasar por un pipe (encontrado probando este mismo script). El prefijo
# sin acentos ("crit", "alt", "med", "baj") es estable frente a eso.
PREFIJOS = {"crit": "critica", "alt": "alta", "med": "media", "baj": "baja"}


def _normalizar_severidad(valor: str) -> str:
    v = valor.strip().lower()
    for prefijo, canonica in PREFIJOS.items():
        if v.startswith(prefijo):
            return canonica
    raise ValueError(f"Severidad no reconocida: {valor!r} (no matchea ningún prefijo conocido {list(PREFIJOS)})")


def recalcular(hallazgos: list[dict]) -> dict:
    conteo = {s: 0 for s in SEVERIDADES}
    for h in hallazgos:
        sev = _normalizar_severidad(h["severidad"])
        conteo[sev] += 1
    conteo["total"] = len(hallazgos)
    return conteo


def main() -> int:
    datos = json.loads(sys.stdin.read())
    recalculado = recalcular(datos["hallazgos"])
    publicado = datos["resumen_publicado"]

    discrepancias = [
        f"{campo}: publicado={publicado.get(campo)!r} recalculado={recalculado[campo]!r}"
        for campo in recalculado
        if publicado.get(campo) != recalculado[campo]
    ]

    if discrepancias:
        print("CT-05: el resumen publicado NO coincide con la agregación real:", file=sys.stderr)
        for d in discrepancias:
            print(f"  - {d}", file=sys.stderr)
        return 2

    print(f"OK: resumen publicado coincide con la agregación real: {recalculado}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
