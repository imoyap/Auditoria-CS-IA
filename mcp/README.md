# mcp/

Capa 3 — conocimiento. Servidores MCP de solo lectura, con corpus offline (el laboratorio no tiene acceso a Internet).

- `conocimiento_tecnico/` — CWE relevante + `consultar_epss_kev()`, que siempre declara `NO_DISPONIBLE` con justificación (no hay EPSS/KEV offline en este entorno; ver Anexo §10, nota de laboratorio).
- `conocimiento_normativo/` — ISO/IEC 27001:2022 Anexo A, NIST CSF 2.0, CIS v8, normativa chilena (Leyes 21.663, 21.719, 21.459).

Distinto en propósito del MCP existente en `auditoria/mcp/` (que expone herramientas de ejecución sobre la base de datos del framework genérico, no un corpus de conocimiento citable — ver `docs/GAP_ANALYSIS.md` §1.1).

Ver `docs/tasks.md` T-017, T-018.
