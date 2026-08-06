#!/usr/bin/env python3
"""scripts/generar_reporte.py — skill `redactar` (T-033, REQ-G-01, REQ-F-07).

Genera el reporte final por sustitución de plantilla sobre datos ya
verificados -- nunca texto libre. El resumen ejecutivo se calcula por
agregación real sobre los hallazgos recibidos (misma lógica que CT-05,
harness/controles/ct05_consistencia.py), no se redacta a mano. Cierra
siempre con la advertencia de no-asesoría-legal del Anexo Técnico U3 §16,
copiada textual -- ni una palabra distinta.

Determinismo: dos ejecuciones con los mismos datos de entrada deben
producir el mismo contenido factual (mismos números, mismas filas) --
verificado en LEDGER.md al cerrar T-033.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

if hasattr(sys.stdin, "reconfigure"):
    sys.stdin.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parents[4]

# Copiado textual del Anexo Técnico U3 §16 -- no modificar ni una palabra.
ADVERTENCIA_LEGAL = (
    "Este documento constituye un análisis técnico de controles de seguridad y su "
    "correspondencia con obligaciones normativas. No sustituye asesoría legal. La "
    "calificación jurídica definitiva de la organización, sus roles y sus obligaciones "
    "debe ser validada por abogado. La normativa chilena de ciberseguridad y protección "
    "de datos se encuentra en despliegue por etapas; los criterios sujetos a reglamento "
    "pendiente se señalan como tales."
)

PREFIJOS_SEVERIDAD = {"crit": "Crítica", "alt": "Alta", "med": "Media", "baj": "Baja"}


def _severidad_canonica(valor: str) -> str:
    v = valor.strip().lower()
    for prefijo, canonica in PREFIJOS_SEVERIDAD.items():
        if v.startswith(prefijo):
            return canonica
    return "Desconocida"


def calcular_resumen(hallazgos: list[dict]) -> dict:
    """Agregación real -- CT-05 aplicado dentro del propio generador, no
    solo como validador externo posterior."""
    conteo = {"Crítica": 0, "Alta": 0, "Media": 0, "Baja": 0}
    for h in hallazgos:
        sev = _severidad_canonica(h["severidad"])
        if sev in conteo:
            conteo[sev] += 1
    conteo["Total"] = len(hallazgos)
    return conteo


def generar_markdown(hallazgos: list[dict], cliente: str, activo: str) -> str:
    resumen = calcular_resumen(hallazgos)

    filas = "\n".join(
        f"| {h['check_id']} | {h['hallazgo']} | {_severidad_canonica(h['severidad'])} | {h['estado']} | {h['evidence_id']} |"
        for h in hallazgos
    )

    return f"""# Reporte Final de Auditoría — {cliente}

**Activo evaluado:** {activo}

## Resumen Ejecutivo

Total de hallazgos: {resumen['Total']} (Crítica: {resumen['Crítica']}, Alta: {resumen['Alta']}, Media: {resumen['Media']}, Baja: {resumen['Baja']})

*Estas cifras se calculan por agregación directa sobre los hallazgos verificados, no se redactan a mano (control CT-05).*

## Hallazgos

| ID | Hallazgo | Severidad | Estado | evidence_id |
|---|---|---|---|---|
{filas}

## Advertencia

{ADVERTENCIA_LEGAL}
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Genera el reporte final por sustitución de plantilla")
    parser.add_argument("--cliente", required=True)
    parser.add_argument("--activo", required=True)
    parser.add_argument("--output", required=True, help="Ruta de salida del .md")
    args = parser.parse_args()

    datos = json.loads(sys.stdin.read())
    contenido = generar_markdown(datos["hallazgos"], args.cliente, args.activo)

    salida = Path(args.output)
    salida.parent.mkdir(parents=True, exist_ok=True)
    salida.write_text(contenido, encoding="utf-8")

    print(f"Reporte generado: {salida}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
