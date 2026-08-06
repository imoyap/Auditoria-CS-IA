#!/usr/bin/env python3
"""mcp/conocimiento_normativo/server.py — servidor MCP de solo lectura (capa 3).

Debe ejecutarse con C:\\Python314\\python.exe (el que tiene el SDK `mcp`
instalado) -- ver la nota de LEDGER.md LDG-025 sobre por qué `python3` del
PATH no sirve para esto en este equipo.

Corpus offline (mcp/conocimiento_normativo/corpus_normativo.json), tomado
únicamente de docs/anexo_tecnico_u3.md §14-15 -- no se amplía con
conocimiento general no verificado para este ejercicio. Cada tool retorna
NO_OBSERVADO si no hay coincidencia exacta, nunca aproxima ni inventa un
identificador de control (CT-02 aplicado a esta capa).
"""

from __future__ import annotations

import json
from pathlib import Path

from mcp.server.fastmcp import FastMCP

CORPUS_PATH = Path(__file__).resolve().parent / "corpus_normativo.json"

mcp = FastMCP("conocimiento-normativo")


def _cargar_corpus() -> dict:
    return json.loads(CORPUS_PATH.read_text(encoding="utf-8"))


def _buscar(lista: list[dict], consulta: str) -> dict:
    consulta_norm = consulta.strip().upper()
    for entrada in lista:
        if entrada["id"].upper() == consulta_norm:
            return entrada
    for entrada in lista:
        if consulta.strip().lower() in entrada["nombre"].lower():
            return entrada
    return None


@mcp.tool()
def buscar_control_iso(consulta: str) -> dict:
    """Busca un control de ISO/IEC 27001:2022 Anexo A por ID (p. ej. "A.8.20")
    o por texto en el nombre. NO_OBSERVADO si no hay coincidencia."""
    corpus = _cargar_corpus()
    resultado = _buscar(corpus["iso27001_2022_anexoA"], consulta)
    if resultado:
        return {"resultado": resultado, "fuente": corpus["fuente"]}
    return {"resultado": "NO_OBSERVADO", "razon": f"Sin coincidencia para {consulta!r} en el corpus ISO 27001 Anexo A offline"}


@mcp.tool()
def buscar_categoria_nist(consulta: str) -> dict:
    """Busca una categoría de NIST CSF 2.0 por ID (p. ej. "PR.DS-02") o por
    texto en el nombre. NO_OBSERVADO si no hay coincidencia."""
    corpus = _cargar_corpus()
    resultado = _buscar(corpus["nist_csf_2"], consulta)
    if resultado:
        return {"resultado": resultado, "fuente": corpus["fuente"]}
    return {"resultado": "NO_OBSERVADO", "razon": f"Sin coincidencia para {consulta!r} en el corpus NIST CSF 2.0 offline"}


@mcp.tool()
def buscar_control_cis(consulta: str) -> dict:
    """Busca un (sub)control de CIS Controls v8 por ID (p. ej. "4.8") o por
    texto en el nombre. NO_OBSERVADO si no hay coincidencia."""
    corpus = _cargar_corpus()
    resultado = _buscar(corpus["cis_v8"], consulta)
    if resultado:
        return {"resultado": resultado, "fuente": corpus["fuente"]}
    return {"resultado": "NO_OBSERVADO", "razon": f"Sin coincidencia para {consulta!r} en el corpus CIS v8 offline"}


@mcp.tool()
def buscar_obligacion_cl(consulta: str) -> dict:
    """Busca una obligación normativa chilena por ID (p. ej. "Ley21719") o por
    texto en el nombre/obligación. NO_OBSERVADO si no hay coincidencia."""
    corpus = _cargar_corpus()
    consulta_norm = consulta.strip().upper()
    for entrada in corpus["normativa_cl"]:
        if entrada["id"].upper() == consulta_norm or consulta.strip().lower() in entrada["nombre"].lower() or consulta.strip().lower() in entrada["obligacion"].lower():
            return {"resultado": entrada, "fuente": corpus["fuente"]}
    return {"resultado": "NO_OBSERVADO", "razon": f"Sin coincidencia para {consulta!r} en el corpus de normativa chilena offline"}


if __name__ == "__main__":
    mcp.run()
