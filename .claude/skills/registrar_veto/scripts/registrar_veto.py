#!/usr/bin/env python3
"""scripts/registrar_veto.py — único canal de escritura de VERIFICADOR
(T-022/T-024, soporte de REQ-B-03).

Anexa RECHAZO/DECISION a LEDGER.md (nunca HALLAZGO/GATE/SUPERSEDE).

Opcionalmente, si se pasa --check-id y --estado-propuesto, actualiza el
campo "estado" del candidato en normalizado/candidatos.json -- pero con
una asimetría deliberada (Anexo Técnico U3 §2, "Dónde está el humano"):
OBSERVADO e INCONCLUSO son autoridad plena de VERIFICADOR y se escriben
tal cual; VALIDADO NUNCA se escribe literal -- este script solo puede
escribir "VALIDADO_PROPUESTO", porque "el sistema puede proponer VALIDADO;
solo un humano ... puede confirmarlo" (Anexo §2). La transición final a
"VALIDADO" ocurre exclusivamente al firmar G3 (harness/orquestador.py
--sign-gate G3), nunca desde este script.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
LEDGER_PATH = REPO_ROOT / "LEDGER.md"
CANDIDATOS_PATH = REPO_ROOT / "normalizado" / "candidatos.json"

TIPOS_PERMITIDOS = ("RECHAZO", "DECISION")
ESTADOS_QUE_VERIFICADOR_PUEDE_ESCRIBIR = {
    "VALIDADO": "VALIDADO_PROPUESTO",  # nunca el literal final -- requiere firma humana en G3
    "OBSERVADO": "OBSERVADO",
    "INCONCLUSO": "INCONCLUSO",
}


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

    # newline="" evita traducción "\n" -> "\r\n" en Windows (bug real
    # encontrado en T-014 sobre evidencias/manifest.sha256, ver LEDGER.md).
    with LEDGER_PATH.open("a", encoding="utf-8", newline="") as f:
        f.write(linea)

    return linea.rstrip("\n")


def _actualizar_estado_candidato(check_id: str, estado_propuesto: str) -> str:
    if estado_propuesto not in ESTADOS_QUE_VERIFICADOR_PUEDE_ESCRIBIR:
        raise ValueError(f"estado-propuesto {estado_propuesto!r} inválido; debe ser uno de {list(ESTADOS_QUE_VERIFICADOR_PUEDE_ESCRIBIR)}")
    estado_a_escribir = ESTADOS_QUE_VERIFICADOR_PUEDE_ESCRIBIR[estado_propuesto]

    if not CANDIDATOS_PATH.exists():
        raise ValueError(f"no existe {CANDIDATOS_PATH}")

    lineas = CANDIDATOS_PATH.read_text(encoding="utf-8").splitlines()
    encontrado = False
    nuevas_lineas = []
    for linea in lineas:
        if not linea.strip():
            continue
        registro = json.loads(linea)
        if registro.get("check_id") == check_id:
            registro["estado"] = estado_a_escribir
            encontrado = True
        nuevas_lineas.append(json.dumps(registro, ensure_ascii=False))

    if not encontrado:
        raise ValueError(f"check_id {check_id!r} no existe en {CANDIDATOS_PATH}")

    with CANDIDATOS_PATH.open("w", encoding="utf-8", newline="") as f:
        f.write("\n".join(nuevas_lineas) + "\n")

    return estado_a_escribir


def main() -> int:
    parser = argparse.ArgumentParser(description="Registra un veto o decisión de VERIFICADOR en LEDGER.md")
    parser.add_argument("--tipo", required=True, choices=TIPOS_PERMITIDOS)
    parser.add_argument("--resumen", required=True, help="Resumen en una línea, debe citar el evidence_id que sostiene el veto/decisión")
    parser.add_argument("--ref", required=True, help="Referencia, p. ej. ev:manifest.sha256 o gate:G3")
    parser.add_argument("--actor", default="VERIFICADOR")
    parser.add_argument("--check-id", help="Si se provee junto con --estado-propuesto, actualiza el estado del candidato")
    parser.add_argument("--estado-propuesto", choices=list(ESTADOS_QUE_VERIFICADOR_PUEDE_ESCRIBIR), help="VALIDADO se escribe como VALIDADO_PROPUESTO -- nunca el literal final, eso requiere firma humana en G3")
    args = parser.parse_args()

    try:
        linea = registrar(args.tipo, args.resumen, args.ref, args.actor)
        if args.check_id and args.estado_propuesto:
            estado_escrito = _actualizar_estado_candidato(args.check_id, args.estado_propuesto)
            print(f"Estado de {args.check_id} actualizado a {estado_escrito!r} en {CANDIDATOS_PATH}")
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    print(linea)
    return 0


if __name__ == "__main__":
    sys.exit(main())
