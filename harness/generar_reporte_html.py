#!/usr/bin/env python3
"""harness/generar_reporte_html.py — genera reporte/reporte_final.html

Sustitución de plantilla sobre datos ya verificados y cerrados: lee
reporte/reporte_final.md (resumen ejecutivo, advertencia legal) y
reporte/matriz_correlacion.csv (detalle completo de cada hallazgo) y los
vuelca en un HTML autocontenido, sin agregar ninguna oración que no
provenga de esos dos archivos -- mismo principio que
.claude/skills/redactar/scripts/generar_reporte.py.

Imprimible a PDF desde cualquier navegador (Ctrl/Cmd+P -> Guardar como PDF).
No requiere dependencias externas (sin pandoc/weasyprint).
"""

from __future__ import annotations

import csv
import html
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MD_PATH = REPO_ROOT / "reporte" / "reporte_final.md"
CSV_PATH = REPO_ROOT / "reporte" / "matriz_correlacion.csv"
HTML_PATH = REPO_ROOT / "reporte" / "reporte_final.html"

ESTADO_CLASE = {
    "VALIDADO": "estado-validado",
    "OBSERVADO": "estado-observado",
    "INCONCLUSO": "estado-inconcluso",
}


def _leer_markdown() -> dict:
    texto = MD_PATH.read_text(encoding="utf-8")
    cliente = re.search(r"^# Reporte Final de Auditoría — (.+)$", texto, re.MULTILINE).group(1)
    activo = re.search(r"^\*\*Activo evaluado:\*\* (.+)$", texto, re.MULTILINE).group(1)
    resumen = re.search(r"^Total de hallazgos: (.+)$", texto, re.MULTILINE).group(1)
    advertencia = texto.split("## Advertencia\n\n")[1].strip()
    return {"cliente": cliente, "activo": activo, "resumen": resumen, "advertencia": advertencia}


def _leer_matriz() -> list[dict]:
    with CSV_PATH.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def _celda(valor: str) -> str:
    valor = html.escape(valor)
    if valor in ("NO_OBSERVADO", "NO_DISPONIBLE"):
        return f'<span class="no-observado">{valor}</span>'
    return valor


def _fila_hallazgo(fila: dict) -> str:
    clase_estado = ESTADO_CLASE.get(fila["Estado"], "")
    columnas_detalle = [
        ("CWE", fila["CWE"]), ("CVE", fila["CVE"]), ("Vector CVSS", fila["Vector_CVSS"]),
        ("Impacto (I)", fila["I"]), ("Probabilidad (P)", fila["P"]), ("Riesgo inherente", fila["Riesgo"]),
        ("Control ISO/IEC 27001:2022", fila["Control_ISO"]), ("NIST CSF 2.0", fila["NIST"]),
        ("Control CIS v8", fila["Control_CIS"]), ("Obligación normativa CL", fila["Obligacion_CL"]),
        ("Evidencia requerida", fila["Evidencia_requerida"]), ("Brecha", fila["Brecha"]),
        ("Remediación / Recomendación", fila["Remediacion"]), ("Esfuerzo", fila["Esfuerzo"]),
        ("Responsable", fila["Responsable"]), ("Plazo", fila["Plazo"]),
        ("Riesgo residual", fila["Riesgo_residual"]), ("Plazo de referencia (banda)", fila["Plazo_referencia"]),
    ]
    filas_detalle = "\n".join(
        f'<tr><th>{html.escape(k)}</th><td>{_celda(v)}</td></tr>' for k, v in columnas_detalle
    )
    return f"""
    <section class="hallazgo">
      <h3><span class="id">{html.escape(fila['ID'])}</span> — {html.escape(fila['Hallazgo'])}
        <span class="badge {clase_estado}">{html.escape(fila['Estado'])}</span>
      </h3>
      <p class="aplica-porque">{html.escape(fila['Aplica_porque'])}</p>
      <table class="detalle">
        {filas_detalle}
      </table>
    </section>
    """


def generar() -> None:
    md = _leer_markdown()
    filas = _leer_matriz()
    hallazgos_html = "\n".join(_fila_hallazgo(f) for f in filas)

    doc = f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>Reporte Final de Auditoría — {html.escape(md['cliente'])}</title>
<style>
  :root {{ color-scheme: light dark; }}
  body {{ font-family: -apple-system, Segoe UI, Arial, sans-serif; max-width: 900px; margin: 2rem auto; padding: 0 1.5rem; line-height: 1.5; color: #1a1a1a; background: #fff; }}
  h1 {{ font-size: 1.6rem; border-bottom: 3px solid #1a1a1a; padding-bottom: 0.5rem; }}
  h2 {{ font-size: 1.2rem; margin-top: 2rem; border-bottom: 1px solid #ccc; padding-bottom: 0.3rem; }}
  h3 {{ font-size: 1.05rem; margin-top: 1.5rem; }}
  .meta {{ color: #555; margin-bottom: 1.5rem; }}
  .resumen {{ background: #f5f5f5; border-left: 4px solid #444; padding: 0.8rem 1rem; margin: 1rem 0; }}
  .hallazgo {{ border: 1px solid #ddd; border-radius: 6px; padding: 1rem 1.2rem; margin: 1.2rem 0; page-break-inside: avoid; }}
  .id {{ font-family: monospace; background: #eee; padding: 0.1rem 0.4rem; border-radius: 3px; }}
  .badge {{ float: right; font-size: 0.75rem; padding: 0.2rem 0.6rem; border-radius: 10px; color: #fff; }}
  .estado-validado {{ background: #b91c1c; }}
  .estado-observado {{ background: #b45309; }}
  .estado-inconcluso {{ background: #6b7280; }}
  .aplica-porque {{ font-style: italic; color: #333; }}
  table.detalle {{ width: 100%; border-collapse: collapse; margin-top: 0.6rem; font-size: 0.9rem; }}
  table.detalle th {{ text-align: left; width: 220px; vertical-align: top; padding: 0.35rem 0.5rem; background: #fafafa; border: 1px solid #e5e5e5; }}
  table.detalle td {{ padding: 0.35rem 0.5rem; border: 1px solid #e5e5e5; }}
  .no-observado {{ color: #888; font-style: italic; }}
  .advertencia {{ margin-top: 2.5rem; padding: 1rem; border: 1px solid #999; background: #fffbea; font-size: 0.9rem; }}
  @media print {{ .hallazgo {{ break-inside: avoid; }} body {{ margin: 0; }} }}
  @media (prefers-color-scheme: dark) {{
    body {{ background: #121212; color: #e5e5e5; }}
    .resumen {{ background: #1e1e1e; }}
    .hallazgo {{ border-color: #333; }}
    table.detalle th {{ background: #1a1a1a; border-color: #333; }}
    table.detalle td {{ border-color: #333; }}
    .advertencia {{ background: #2a2410; border-color: #665; }}
    .id {{ background: #222; }}
  }}
</style>
</head>
<body>
  <h1>Reporte Final de Auditoría — {html.escape(md['cliente'])}</h1>
  <p class="meta"><strong>Activo evaluado:</strong> {html.escape(md['activo'])}</p>

  <h2>Resumen Ejecutivo</h2>
  <div class="resumen">
    <p>Total de hallazgos: {html.escape(md['resumen'])}</p>
    <p style="font-size:0.85rem;color:#666;">Cifras calculadas por agregación directa sobre los hallazgos verificados (control CT-05).</p>
  </div>

  <h2>Hallazgos</h2>
  {hallazgos_html}

  <div class="advertencia">
    <strong>Advertencia</strong><br>
    {html.escape(md['advertencia'])}
  </div>
</body>
</html>
"""
    HTML_PATH.write_text(doc, encoding="utf-8")
    print(f"Generado: {HTML_PATH} ({len(filas)} hallazgos)")


if __name__ == "__main__":
    generar()
