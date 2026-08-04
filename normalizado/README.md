# normalizado/

Capa 2 — normalización. JSON/CSV canónico producido por parsers deterministas a partir de `evidencias/raw/`. El modelo de lenguaje nunca lee la salida cruda de una herramienta directamente (regla de oro de la capa 2, Anexo §3) — siempre lee estos archivos.

- `inventario.json` — activos/servicios/versiones, cada uno con puntero a la línea del artefacto crudo de origen (criterio de cierre G2).
- `candidatos.json` — hallazgos propuestos por ANALISTA, antes de verificación (nunca en estado VALIDADO).
- `matriz_borrador.csv` — salida de la skill `correlacionar`, previa a consolidarse en `reporte/matriz_correlacion.csv`.

Ver `docs/tasks.md` T-015, T-021, T-027.
