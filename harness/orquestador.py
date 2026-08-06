#!/usr/bin/env python3
"""harness/orquestador.py — BoundedLoop del pipeline de auditoría U3 (T-009, REQ-B-05).

WIP=1: una etapa en vuelo a la vez. Tope global de iteraciones = 30
(10 etapas x 3 reintentos cada una). Las etapas cuyo gate es G0, G3 o G5
detienen el proceso de verdad (sys.exit) hasta que un humano firme
explícitamente con --sign-gate — no es un log informativo, es una parada
real del proceso: sin la firma, --continue vuelve a detenerse en el mismo
punto.

No depende de auditoria/ (el framework genérico existente) — ver
docs/GAP_ANALYSIS.md §1.1: auditoria/scheduler/executor.py es
re-ejecución periódica por cron, no un BoundedLoop de una sola auditoría.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ESTADO_PATH = REPO_ROOT / "harness" / "estado.json"
LEDGER_PATH = REPO_ROOT / "LEDGER.md"
GATES_DIR = REPO_ROOT / "gates"
SCOPE_DIR = REPO_ROOT / "scope"

TOPE_REINTENTOS_POR_ETAPA = 3
MAX_ITERACIONES_GLOBAL = 30  # 10 etapas x 3 reintentos (docs/design.md)

# Etapas del workflow (Anexo Técnico U3 §2). "gate_bloqueante" solo se marca
# en G0, G3, G5 -- los tres con firma humana obligatoria (Anexo §2, "Dónde
# está el humano"). G1/G2/G4 son gates reales pero no exigen parada dura.
ETAPAS = [
    {"id": 0, "nombre": "Encargo y autorización", "rol": "Humano", "gate": "G0", "gate_bloqueante": True},
    {"id": 1, "nombre": "Definición del criterio de auditoría", "rol": "Humano+COMPLIANCE", "gate": "G0", "gate_bloqueante": True},
    {"id": 2, "nombre": "Planificación", "rol": "SPEC/Humano", "gate": None, "gate_bloqueante": False},
    {"id": 3, "nombre": "Recolección de evidencia", "rol": "RECON", "gate": "G1", "gate_bloqueante": False},
    {"id": 4, "nombre": "Normalización e inventario", "rol": "Determinista", "gate": "G2", "gate_bloqueante": False},
    {"id": 5, "nombre": "Análisis y verificación", "rol": "ANALISTA/VERIFICADOR", "gate": "G3", "gate_bloqueante": True},
    {"id": 6, "nombre": "Evaluación de riesgo", "rol": "ANALISTA+Humano", "gate": "G3", "gate_bloqueante": True},
    {"id": 7, "nombre": "Correlación normativa", "rol": "COMPLIANCE", "gate": "G4", "gate_bloqueante": False},
    {"id": 8, "nombre": "Reporte", "rol": "REDACTOR", "gate": "G5", "gate_bloqueante": True},
    {"id": 9, "nombre": "Comunicación, remediación y seguimiento", "rol": "Humano", "gate": None, "gate_bloqueante": False},
]


def ahora_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def anexar_ledger(tipo: str, actor: str, resumen: str, ref: str) -> None:
    ts = ahora_iso()
    ident = f"LDG-HARNESS-{int(datetime.now(timezone.utc).timestamp() * 1000)}"
    linea = f"{ts} | {ident} | {tipo} | {actor} | {resumen} | {ref}\n"
    with LEDGER_PATH.open("a", encoding="utf-8") as f:
        f.write(linea)


def cargar_estado() -> dict:
    if ESTADO_PATH.exists():
        return json.loads(ESTADO_PATH.read_text(encoding="utf-8"))
    return {
        "etapa_actual": 0,
        "intentos_etapa_actual": 0,
        "iteraciones_totales": 0,
        "detenido": False,
        "motivo_detencion": None,
    }


def guardar_estado(estado: dict) -> None:
    ESTADO_PATH.write_text(json.dumps(estado, indent=2, ensure_ascii=False), encoding="utf-8")


def etapa_por_id(etapa_id: int) -> dict:
    return next(e for e in ETAPAS if e["id"] == etapa_id)


def gate_firmado(gate_id: str) -> bool:
    """True solo si gates/<gate_id>.md existe y su campo Firma humana no está en [PENDIENTE]."""
    gate_path = GATES_DIR / f"{gate_id}.md"
    if not gate_path.exists():
        return False
    contenido = gate_path.read_text(encoding="utf-8")
    for linea in contenido.splitlines():
        if linea.strip().startswith("**Firma humana:**"):
            return "[PENDIENTE]" not in linea
    return False


def validar_prerrequisitos_g0() -> tuple[bool, str]:
    """Validación real de etapa 0/1 (no un stub): scope/ completo y con
    ventana de trabajo real, no el placeholder "A DEFINIR POR EL GRUPO".
    """
    import yaml

    alcance_path = SCOPE_DIR / "alcance.yaml"
    allowlist_path = SCOPE_DIR / "allowlist.txt"
    etica_path = SCOPE_DIR / "declaracion_etica.md"

    faltantes = [p.name for p in (alcance_path, allowlist_path, etica_path) if not p.exists()]
    if faltantes:
        return False, f"Archivos de scope/ faltantes: {', '.join(faltantes)}"

    alcance = yaml.safe_load(alcance_path.read_text(encoding="utf-8"))
    ventana = alcance.get("ventana_de_trabajo", {})
    inicio = str(ventana.get("fecha_inicio", ""))
    fin = str(ventana.get("fecha_fin", ""))
    if "A DEFINIR" in inicio.upper() or "A DEFINIR" in fin.upper() or not inicio or not fin:
        return False, (
            "scope/alcance.yaml.ventana_de_trabajo sigue en 'A DEFINIR POR EL GRUPO' — "
            "no se puede completar la etapa 0/1 con una ventana de trabajo sin fecha real "
            "(no se inventa una fecha para pasar la verificación)"
        )

    return True, "scope/ completo: alcance.yaml, allowlist.txt, declaracion_etica.md, ventana con fechas reales"


def ejecutar_etapa(etapa: dict) -> tuple[bool, str]:
    """Ejecuta el trabajo de una etapa. Etapa 0/1 tienen validación real.
    Las demás son intencionalmente NotImplementedError hasta sus tareas
    correspondientes (T-012 en adelante) -- no se simulan como exitosas.
    """
    if etapa["id"] in (0, 1):
        return validar_prerrequisitos_g0()
    return False, f"Etapa {etapa['id']} ({etapa['nombre']}) aún no implementada (ver docs/tasks.md)"


def detener(estado: dict, motivo: str, tipo: str = "RECHAZO") -> None:
    """tipo='RECHAZO' para fallos reales (tope de reintentos, etc.);
    tipo='DECISION' para una parada esperada del propio diseño (p. ej.
    etapa completada, esperando firma humana de gate) -- no es un rechazo,
    es el pipeline funcionando como se diseñó."""
    estado["detenido"] = True
    estado["motivo_detencion"] = motivo
    guardar_estado(estado)
    anexar_ledger(tipo, "ORQUESTADOR", motivo, f"etapa:{estado['etapa_actual']}")
    print(f"\nDETENIDO: {motivo}", file=sys.stderr)
    sys.exit(1)


def cmd_run(_args: argparse.Namespace) -> None:
    estado = cargar_estado()

    if estado["detenido"]:
        print(f"El harness sigue detenido: {estado['motivo_detencion']}", file=sys.stderr)
        print("Resuelve el bloqueo o firma el gate pendiente con --sign-gate antes de --continue.", file=sys.stderr)
        sys.exit(1)

    while estado["etapa_actual"] < len(ETAPAS):
        if estado["iteraciones_totales"] >= MAX_ITERACIONES_GLOBAL:
            detener(estado, f"Tope global de iteraciones alcanzado ({MAX_ITERACIONES_GLOBAL})")

        etapa = etapa_por_id(estado["etapa_actual"])

        # Gate bloqueante: si ya se completó el trabajo de la etapa pero el
        # gate correspondiente no está firmado, nos detenemos aquí, no
        # seguimos "por si acaso".
        if etapa["gate_bloqueante"] and gate_firmado(etapa["gate"]) is False and estado.get("etapa_lista"):
            detener(
                estado,
                f"Etapa {etapa['id']} lista pero {etapa['gate']} no tiene firma humana real "
                f"(gates/{etapa['gate']}.md). Usa --sign-gate {etapa['gate']} --by NOMBRE --date FECHA.",
                tipo="DECISION",
            )

        estado["iteraciones_totales"] += 1
        ok, detalle = ejecutar_etapa(etapa)

        if ok:
            anexar_ledger(
                "DECISION",
                "ORQUESTADOR",
                f"Etapa {etapa['id']} ({etapa['nombre']}) completada: {detalle}",
                f"etapa:{etapa['id']}",
            )
            if etapa["gate_bloqueante"]:
                estado["etapa_lista"] = True
                guardar_estado(estado)
                detener(
                    estado,
                    f"Etapa {etapa['id']} lista, esperando firma humana de {etapa['gate']} "
                    f"antes de avanzar (parada real, no informativa)",
                    tipo="DECISION",
                )
            estado["etapa_actual"] += 1
            estado["intentos_etapa_actual"] = 0
            estado["etapa_lista"] = False
            guardar_estado(estado)
            print(f"OK etapa {etapa['id']} ({etapa['nombre']})")
            continue

        estado["intentos_etapa_actual"] += 1
        guardar_estado(estado)
        anexar_ledger(
            "RECHAZO",
            "ORQUESTADOR",
            f"Etapa {etapa['id']} ({etapa['nombre']}) intento {estado['intentos_etapa_actual']}/"
            f"{TOPE_REINTENTOS_POR_ETAPA} falló: {detalle}",
            f"etapa:{etapa['id']}",
        )
        print(f"FALLO etapa {etapa['id']} intento {estado['intentos_etapa_actual']}: {detalle}", file=sys.stderr)

        if estado["intentos_etapa_actual"] >= TOPE_REINTENTOS_POR_ETAPA:
            detener(
                estado,
                f"Tope de reintentos ({TOPE_REINTENTOS_POR_ETAPA}) alcanzado en etapa "
                f"{etapa['id']} ({etapa['nombre']}): {detalle}",
            )

    print("Workflow completo: las 10 etapas cerradas.")


def cmd_sign_gate(args: argparse.Namespace) -> None:
    gate_path = GATES_DIR / f"{args.gate}.md"
    if not gate_path.exists():
        print(f"No existe {gate_path} — el gate debe crearse (con criterio y evidencia) antes de firmarlo.", file=sys.stderr)
        sys.exit(1)

    contenido = gate_path.read_text(encoding="utf-8")
    if "**Firma humana:** [PENDIENTE]" not in contenido:
        print("El gate no tiene una firma [PENDIENTE] que reemplazar (¿ya está firmado, o el formato no es el esperado?).", file=sys.stderr)
        sys.exit(1)

    nueva = contenido.replace(
        "**Firma humana:** [PENDIENTE]",
        f"**Firma humana:** {args.by}, {args.date}",
    )
    gate_path.write_text(nueva, encoding="utf-8")

    estado = cargar_estado()
    estado["detenido"] = False
    estado["motivo_detencion"] = None
    guardar_estado(estado)

    anexar_ledger("GATE", "HUMANO", f"{args.gate} firmado por {args.by} ({args.date})", f"gate:{args.gate}")
    print(f"{args.gate} firmado. Ejecuta 'orquestador.py run' (o --continue) para avanzar.")


def cmd_status(_args: argparse.Namespace) -> None:
    estado = cargar_estado()
    print(json.dumps(estado, indent=2, ensure_ascii=False))


def main() -> None:
    # Nota de diseño (corrige un bug real encontrado al probar T-009): no se
    # usan subparsers de argparse para "--sign-gate"/"--continue"/"--status"
    # porque argparse trata cualquier token que empiece con "--" como una
    # opción, no como el nombre de un subcomando posicional — con
    # subparsers, "orquestador.py --sign-gate G0 ..." nunca llegaba a
    # resolverse como se esperaba. Se usan flags de nivel superior en su
    # lugar, que es exactamente lo que la interfaz pretendía ser.
    parser = argparse.ArgumentParser(description="Harness del pipeline de auditoría U3")
    parser.add_argument("run", nargs="?", help="Ejecuta/continúa el BoundedLoop (comando por defecto)")
    parser.add_argument("--continue", dest="do_continue", action="store_true", help="Alias de 'run'")
    parser.add_argument("--sign-gate", dest="gate", metavar="GATE_ID", help="Firma un gate pendiente, p. ej. G0")
    parser.add_argument("--by", help="Nombre de quien firma (con --sign-gate)")
    parser.add_argument("--date", help="Fecha real de la firma, YYYY-MM-DD (con --sign-gate)")
    parser.add_argument("--status", action="store_true", help="Muestra el estado actual")

    args = parser.parse_args()

    if args.gate:
        if not args.by or not args.date:
            parser.error("--sign-gate requiere --by y --date")
        cmd_sign_gate(args)
    elif args.status:
        cmd_status(args)
    else:
        cmd_run(args)


if __name__ == "__main__":
    main()
