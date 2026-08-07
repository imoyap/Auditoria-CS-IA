#!/usr/bin/env python3
"""harness/reverificacion_d1.py — dimensión de extensión D1 (T-040, REQ-B-06).

Anexo Técnico U3 §2: "El sistema puede proponer VALIDADO; solo un humano
O UNA RE-VERIFICACIÓN AUTOMATIZADA CON ARTEFACTO CAPTURADO puede
confirmarlo." Este script implementa esa segunda vía, alternativa a la
firma humana en G3 -- es capa determinista (como normalizar_nmap.py), no
un rol agéntico: no hay margen de criterio libre del modelo, la regla es
fija y se aplica siempre igual.

Regla de promoción a VALIDADO (misma distinción que ya aplicó VERIFICADOR
de verdad sobre datos reales en T-024, ver LEDGER.md LDG-VETO-1786020794410
vs LDG-VETO-1786020802794): se exigen al menos DOS artefactos, en líneas
DISTINTAS del mismo evidence_id, y al menos uno debe ser "conductual"
(prueba de comportamiento activo -- p. ej. un banner de shell real, una
respuesta de servicio que demuestra el hecho, no solo un número de
versión). Dos artefactos de tipo "deteccion" (dos banners de versión, sin
ninguno conductual) NUNCA alcanzan VALIDADO por esta vía -- es exactamente
el caso vsftpd/distccd del Ejemplo 2 del Anexo §15, y exactamente por qué
H-02/H-04 de esta auditoría real permanecen en OBSERVADO: no existe un
segundo artefacto conductual capturable sin explotación activa (RC-3).

Este script NUNCA opera sobre normalizado/candidatos.json por defecto --
requiere --candidatos-path explícito, precisamente para que una prueba de
mecanismo no pueda tocar por accidente un hallazgo real de la auditoría.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

if hasattr(sys.stdin, "reconfigure"):
    sys.stdin.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent
LEDGER_PATH = REPO_ROOT / "LEDGER.md"

TIPOS_VALIDOS = {"deteccion", "conductual"}


def evaluar(evidence_id: str, artefactos: list[dict]) -> tuple[bool, str]:
    if len(artefactos) < 2:
        return False, "Se requieren al menos 2 artefactos independientes; se recibió menos de 2"

    for a in artefactos:
        if a.get("tipo") not in TIPOS_VALIDOS:
            return False, f"Artefacto con tipo inválido {a.get('tipo')!r}; debe ser uno de {TIPOS_VALIDOS}"

    lineas = [a["linea"] for a in artefactos]
    if len(set(lineas)) < len(lineas):
        return False, f"Artefactos no son independientes: líneas repetidas {lineas}"

    tipos = {a["tipo"] for a in artefactos}
    if "conductual" not in tipos:
        return False, (
            "Todos los artefactos son de tipo 'deteccion' (p. ej. banners de versión); "
            "sin al menos un artefacto 'conductual' (prueba de comportamiento activo) "
            "esto es exactamente el caso vsftpd/distccd del Anexo §15 Ejemplo 2 -- "
            "permanece en OBSERVADO, nunca VALIDADO por esta vía sin explotación activa (RC-3)"
        )

    return True, f"{len(artefactos)} artefactos independientes en líneas distintas de {evidence_id!r}, incluye al menos uno conductual"


def _anexar_ledger(tipo: str, resumen: str, ref: str) -> None:
    ts = datetime.now().astimezone().isoformat(timespec="seconds")
    ident = f"LDG-D1-{int(datetime.now().timestamp() * 1000)}"
    linea = f"{ts} | {ident} | {tipo} | SISTEMA-D1 | {resumen} | {ref}\n"
    with LEDGER_PATH.open("a", encoding="utf-8", newline="") as f:
        f.write(linea)


def _actualizar_candidato(candidatos_path: Path, check_id: str) -> None:
    lineas = candidatos_path.read_text(encoding="utf-8").splitlines()
    encontrado = False
    nuevas = []
    for linea in lineas:
        if not linea.strip():
            continue
        registro = json.loads(linea)
        if registro.get("check_id") == check_id:
            registro["estado"] = "VALIDADO"
            registro["validado_por"] = "D1-reverificacion_automatizada"
            encontrado = True
        nuevas.append(json.dumps(registro, ensure_ascii=False))
    if not encontrado:
        raise ValueError(f"check_id {check_id!r} no existe en {candidatos_path}")
    with candidatos_path.open("w", encoding="utf-8", newline="") as f:
        f.write("\n".join(nuevas) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="D1: re-verificación automatizada con artefacto capturado (Anexo §2)")
    parser.add_argument("--candidatos-path", required=True, help="Ruta explícita al JSONL de candidatos a actualizar -- nunca un default implícito")
    args = parser.parse_args()

    datos = json.loads(sys.stdin.read())
    check_id = datos["check_id"]
    evidence_id = datos["evidence_id"]
    artefactos = datos["artefactos"]

    ok, detalle = evaluar(evidence_id, artefactos)
    ref = f"ev:{evidence_id}"

    if not ok:
        print(f"RECHAZADO: {detalle}", file=sys.stderr)
        _anexar_ledger("RECHAZO", f"{check_id}: {detalle}", ref)
        return 2

    candidatos_path = Path(args.candidatos_path)
    _actualizar_candidato(candidatos_path, check_id)
    print(f"VALIDADO (D1, re-verificación automatizada, sin firma humana): {check_id} -- {detalle}")
    _anexar_ledger(
        "DECISION",
        f"{check_id} promovido a VALIDADO por re-verificación automatizada (D1, Anexo §2) -- {detalle}. "
        f"NO fue una firma humana la que causó esta transición.",
        ref,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
