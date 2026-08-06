#!/usr/bin/env python3
"""scripts/calcular_riesgo.py — skill `clasificar` (T-019).

Motor determinista de impacto x probabilidad = riesgo (Anexo Técnico U3
§9-11). No hay margen de criterio libre del modelo: dados los factores
declarados, el resultado es siempre el mismo (extensión D6 aprobada en
LEDGER.md LDG-004).

Cuando un factor de probabilidad es NO_DISPONIBLE (típicamente EPSS/KEV en
un laboratorio sin Internet, Anexo §10 nota de laboratorio), se EXCLUYE de
la suma -- no se cuenta como 0 -- y el resultado se basa en los factores
restantes, exactamente como en los dos ejemplos resueltos del Anexo §15.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
CANDIDATOS_PATH = REPO_ROOT / "normalizado" / "candidatos.json"  # JSONL: un objeto por línea
LEDGER_PATH = REPO_ROOT / "LEDGER.md"

FACTORES_IMPACTO = ["confidencialidad", "integridad", "disponibilidad", "datos_personales", "criticidad_operacional"]
FACTORES_PROBABILIDAD = ["exploit_publico", "epss", "kev", "autenticacion", "exposicion"]

# Tabla de bandas (Anexo §9 y §10 usan la misma tabla de suma -> banda 1-5)
BANDAS_SUMA = [
    (0, 1, 1),
    (2, 3, 2),
    (4, 5, 3),
    (6, 7, 4),
    (8, 10, 5),
]

# Matriz de riesgo 5x5 (Anexo §11)
BANDAS_RIESGO = [
    (1, 4, "Bajo"),
    (5, 9, "Medio"),
    (10, 14, "Alto"),
    (15, 19, "Crítico"),
    (20, 25, "Inaceptable"),
]


def _suma_a_banda(suma: int) -> int:
    for lo, hi, banda in BANDAS_SUMA:
        if lo <= suma <= hi:
            return banda
    raise ValueError(f"Suma {suma} fuera de rango 0-10")


def _riesgo_a_banda(valor: int) -> str:
    for lo, hi, etiqueta in BANDAS_RIESGO:
        if lo <= valor <= hi:
            return etiqueta
    raise ValueError(f"Riesgo {valor} fuera de rango 1-25")


def calcular_impacto(factores: dict) -> dict:
    faltantes = [f for f in FACTORES_IMPACTO if f not in factores]
    if faltantes:
        raise ValueError(f"Faltan factores de impacto obligatorios: {faltantes}")
    suma = sum(int(factores[f]) for f in FACTORES_IMPACTO)
    return {"suma": suma, "banda": _suma_a_banda(suma)}


def calcular_probabilidad(factores: dict) -> dict:
    faltantes = [f for f in FACTORES_PROBABILIDAD if f not in factores]
    if faltantes:
        raise ValueError(f"Faltan factores de probabilidad obligatorios: {faltantes}")

    excluidos = []
    valores = []
    for f in FACTORES_PROBABILIDAD:
        v = factores[f]
        if v == "NO_DISPONIBLE":
            excluidos.append(f)
            continue
        valores.append(int(v))

    suma = sum(valores)
    return {"suma": suma, "banda": _suma_a_banda(suma), "factores_excluidos": excluidos}


def calcular_riesgo(impacto: dict, probabilidad: dict) -> dict:
    valor = impacto["banda"] * probabilidad["banda"]
    return {"valor": valor, "banda": _riesgo_a_banda(valor)}


def _check_id_ya_existe(check_id: str) -> bool:
    if not CANDIDATOS_PATH.exists():
        return False
    for linea in CANDIDATOS_PATH.read_text(encoding="utf-8").splitlines():
        if not linea.strip():
            continue
        if json.loads(linea).get("check_id") == check_id:
            return True
    return False


def _anexar_candidato(registro: dict) -> None:
    CANDIDATOS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with CANDIDATOS_PATH.open("a", encoding="utf-8", newline="") as f:
        f.write(json.dumps(registro, ensure_ascii=False) + "\n")


def _anexar_ledger_hallazgo(check_id: str, hallazgo: str, evidence_id: str) -> None:
    ts = datetime.now().astimezone().isoformat(timespec="seconds")
    ident = f"LDG-HALLAZGO-{int(datetime.now().timestamp() * 1000)}"
    linea = f'{ts} | {ident} | HALLAZGO | ANALISTA | Propone {check_id} "{hallazgo}" desde {evidence_id} | ev:{evidence_id}\n'
    with LEDGER_PATH.open("a", encoding="utf-8", newline="") as f:
        f.write(linea)


def main() -> int:
    parser = argparse.ArgumentParser(description="Calcula impacto, probabilidad y riesgo inherente (Anexo §9-11)")
    parser.add_argument("--entrada", help="Ruta a un JSON con {impacto: {...}, probabilidad: {...}}. Si se omite, lee de stdin.")
    parser.add_argument("--check-id", help="Si se provee junto con --hallazgo y --evidence-id, persiste el candidato en normalizado/candidatos.json y registra un HALLAZGO en LEDGER.md")
    parser.add_argument("--hallazgo", help="Descripción corta del hallazgo candidato")
    parser.add_argument("--evidence-id", help="ID del artefacto en evidencias/raw/ que sostiene este candidato")
    parser.add_argument("--cwe", default="NO_OBSERVADO")
    parser.add_argument("--cve", default="NO_OBSERVADO")
    args = parser.parse_args()

    texto = open(args.entrada, encoding="utf-8").read() if args.entrada else sys.stdin.read()
    datos = json.loads(texto)

    impacto = calcular_impacto(datos["impacto"])
    probabilidad = calcular_probabilidad(datos["probabilidad"])
    riesgo = calcular_riesgo(impacto, probabilidad)
    resultado = {"impacto": impacto, "probabilidad": probabilidad, "riesgo_inherente": riesgo}

    persistir = args.check_id and args.hallazgo and args.evidence_id
    if persistir:
        if _check_id_ya_existe(args.check_id):
            print(f"ERROR: {args.check_id!r} ya tiene un candidato registrado -- este script no sobrescribe candidatos existentes", file=sys.stderr)
            return 2

        # El candidato SIEMPRE nace en estado PROPUESTO -- esta ruta de
        # código no acepta ni puede escribir VALIDADO/OBSERVADO/INCONCLUSO,
        # esos estados solo los asigna VERIFICADOR (skill registrar_veto).
        registro = {
            "check_id": args.check_id,
            "hallazgo": args.hallazgo,
            "evidence_id": args.evidence_id,
            "cwe": args.cwe,
            "cve": args.cve,
            "estado": "PROPUESTO",
            **resultado,
        }
        _anexar_candidato(registro)
        _anexar_ledger_hallazgo(args.check_id, args.hallazgo, args.evidence_id)
        resultado["persistido"] = True
        resultado["check_id"] = args.check_id

    print(json.dumps(resultado, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
