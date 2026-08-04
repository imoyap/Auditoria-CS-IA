# gates/

Capa 8 — control humano, artefacto. Un archivo `GX.md` por gate (`G0.md` a `G5.md`), formato exacto del Anexo Técnico U3 §5 (copiado literal, no aproximado):

```markdown
## Gate [ID] — [nombre]
**Criterio:** [condición verificable, redactada ANTES de empezar]
**Evidencia presentada:** [artefacto, ubicación, cómo verificarlo]
**Concilio:** [roles convocados]
**Objeciones:** [texto de cada objeción y cómo se resolvió, o "abierta"]
**Veredicto:** APPROVE | APPROVE_WITH_FINDINGS | REJECT
**Hallazgos abiertos:** [con ID]
**Firma humana:** [nombre, fecha] (obligatoria en G0, G3 y G5)
```

Ningún gate se cierra (`Firma humana` distinto de `[PENDIENTE]`) sin una firma humana real — el harness se detiene y exige un comando explícito `--sign-gate`, no continúa por sí solo. Ver `docs/design.md`, sección del harness.
