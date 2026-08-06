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
import unicodedata
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


def _sin_acentos(texto: str) -> str:
    """Bug real encontrado en T-034 (LEDGER.md): "Crítica".lower().startswith("crit")
    es False -- la í acentuada rompe la comparación con el prefijo ASCII "crit",
    así que ninguna severidad "Crítica" real se contaba nunca. Se normaliza
    quitando diacríticos antes de comparar (NFKD + descarte de marcas combinantes)."""
    return "".join(c for c in unicodedata.normalize("NFKD", texto) if not unicodedata.combining(c))


def _severidad_canonica(valor: str) -> str:
    v = _sin_acentos(valor.strip().lower())
    for prefijo, canonica in PREFIJOS_SEVERIDAD.items():
        if v.startswith(prefijo):
            return canonica
    return "NO_OBSERVADO"


def calcular_resumen(hallazgos: list[dict]) -> dict:
    """Agregación real -- CT-05 aplicado dentro del propio generador, no
    solo como validador externo posterior.

    "Desconocida" (severidad NO_OBSERVADO/no confirmada, típicamente un
    hallazgo INCONCLUSO) se cuenta explícitamente en vez de omitirse --
    omitirla dejaría Total > suma de las 4 bandas conocidas, una
    inconsistencia numérica que CT-05 existe justamente para atrapar
    (bug real encontrado en T-034 antes de invocar REDACTOR, ver LEDGER.md)."""
    conteo = {"Crítica": 0, "Alta": 0, "Media": 0, "Baja": 0, "NO_OBSERVADO": 0}
    for h in hallazgos:
        sev = _severidad_canonica(h["severidad"])
        conteo[sev] += 1
    conteo["Total"] = len(hallazgos)
    return conteo


def generar_markdown(hallazgos: list[dict], cliente: str, activo: str) -> str:
    resumen = calcular_resumen(hallazgos)

    filas = "\n".join(
        f"| {h['check_id']} | {h['hallazgo']} | {_severidad_canonica(h['severidad'])} | {h['estado']} | {h['evidence_id']} |"
        for h in hallazgos
    )

    # Nota deliberadamente agnóstica de estado: NO_OBSERVADO agrupa tanto un
    # hallazgo VALIDADO sin CVE/CVSS catalogado (p. ej. un backdoor a medida,
    # sin vulnerabilidad numerada que consultar) como uno INCONCLUSO sin
    # severidad asignable por falta de verificación (Anexo §15, Ejemplo 3) --
    # son razones distintas, y la tabla de "Estado" por fila ya distingue
    # cuál es cuál; el resumen no debe asumir que todos son INCONCLUSO.
    nota_desconocida = (
        f" + {resumen['NO_OBSERVADO']} sin severidad técnica asignable (sin CVE/CVSS "
        f"catalogado, o verificación aún pendiente — ver columna Estado por hallazgo)"
        if resumen["NO_OBSERVADO"] > 0 else ""
    )

    return f"""# Reporte Final de Auditoría — {cliente}

**Activo evaluado:** {activo}

## Resumen Ejecutivo

Total de hallazgos: {resumen['Total']} (Crítica: {resumen['Crítica']}, Alta: {resumen['Alta']}, Media: {resumen['Media']}, Baja: {resumen['Baja']}{nota_desconocida})

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
