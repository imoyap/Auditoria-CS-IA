#!/usr/bin/env python3
"""mcp/conocimiento_tecnico/server.py — servidor MCP de solo lectura (capa 3).

IMPORTANTE: debe ejecutarse con el intérprete de Python que tiene instalado
el SDK `mcp` (en este equipo: C:\\Python314\\python.exe, no el `python3` del
PATH, que es una instalación distinta sin el SDK). Si se ejecuta con el
intérprete equivocado, `import mcp` resuelve por error a esta misma carpeta
del repositorio (namespace package vacío) en vez del SDK real — bug real
encontrado y documentado en LEDGER.md durante T-017.

Corpus offline (mcp/conocimiento_tecnico/corpus_cwe.json). `consultar_epss_kev`
siempre declara NO_DISPONIBLE: este laboratorio está aislado sin acceso a
Internet (Anexo Técnico U3 §10, nota de laboratorio) — la ausencia se declara
por diseño del servidor, no por omisión del modelo que lo consulta (CT-07).
"""

from __future__ import annotations

import json
from pathlib import Path

from mcp.server.fastmcp import FastMCP

CORPUS_PATH = Path(__file__).resolve().parent / "corpus_cwe.json"

mcp = FastMCP("conocimiento-tecnico")


def _cargar_corpus() -> dict:
    return json.loads(CORPUS_PATH.read_text(encoding="utf-8"))


@mcp.tool()
def buscar_cwe(consulta: str) -> dict:
    """Busca un CWE por ID exacto (p. ej. "CWE-319") o por coincidencia de texto
    en el nombre. Retorna NO_OBSERVADO si no hay coincidencia -- nunca aproxima
    ni inventa un identificador."""
    corpus = _cargar_corpus()
    consulta_norm = consulta.strip().upper()
    for entrada in corpus["entradas"]:
        if entrada["id"].upper() == consulta_norm:
            return {"resultado": entrada, "fuente": corpus["fuente"]}
    for entrada in corpus["entradas"]:
        if consulta.strip().lower() in entrada["nombre"].lower() or consulta.strip().lower() in entrada["nombre_es"].lower():
            return {"resultado": entrada, "fuente": corpus["fuente"]}
    return {"resultado": "NO_OBSERVADO", "razon": f"Sin coincidencia para {consulta!r} en el corpus offline"}


@mcp.tool()
def consultar_epss_kev(cve: str) -> dict:
    """Consulta EPSS (puntaje de explotación predicha) y presencia en catálogo
    KEV para un CVE. Siempre retorna NO_DISPONIBLE en este entorno: es un
    laboratorio aislado sin acceso a Internet (Anexo Técnico U3 §10)."""
    return {
        "cve": cve,
        "epss": "NO_DISPONIBLE",
        "kev": "NO_DISPONIBLE",
        "razon": "Entorno de laboratorio aislado, sin acceso a Internet a fuentes EPSS/KEV en vivo",
    }


if __name__ == "__main__":
    mcp.run()
