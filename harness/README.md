# harness/

Capa 6 — orquestación, gates, ledger, estado, BoundedLoop.

- `orquestador.py` — ciclo WIP=1, tope de 30 iteraciones (10 etapas × 3 reintentos), condición de salida explícita, mecanismo `--sign-gate`/`--continue` para las paradas reales en G0/G3/G5 (no un log informativo). Ver `docs/design.md`, sección "Diseño del harness/orquestador".
- `controles/` — los 7 controles anti-alucinación CT-01 a CT-07 como scripts ejecutables.

No depende de `auditoria/` (el framework genérico existente); reutiliza patrones de `auditoria/core/engine.py` solo como antecedente de diseño, no como dependencia de código — ver `docs/GAP_ANALYSIS.md` §1.1.

Ver `docs/tasks.md` T-008, T-009.
