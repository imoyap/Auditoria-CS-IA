# roles/

Documentación humana-legible de los 5 roles del concilio (capa 5). Cada archivo declara alcance, herramientas permitidas y prohibiciones explícitas, siguiendo la tabla del Anexo Técnico U3 §4 y `docs/design.md` §a.2.

La implementación ejecutable equivalente vive en `.claude/agents/<rol>.md`, con `tools`/`disallowedTools` reales — este directorio es la referencia legible que un humano audita, no el mecanismo de aplicación.

Archivos esperados: `recon.md`, `analista.md`, `verificador.md`, `compliance.md`, `redactor.md`. Ver `docs/tasks.md` T-006.
