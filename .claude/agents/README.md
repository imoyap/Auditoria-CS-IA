# .claude/agents/

Subagentes de Claude Code — implementación ejecutable de los 5 roles (capa 5). Cada archivo (`recon.md`, `analista.md`, `verificador.md`, `compliance.md`, `redactor.md`) declara `tools`/`disallowedTools` en YAML frontmatter, aplicados por el runtime de Claude Code, no por instrucción de system prompt.

Superficie de herramientas por rol: ver `docs/design.md` §a.2. Ningún rol salvo RECON recibe `Bash`; toda escritura de los demás roles pasa por una skill del proyecto (`.claude/skills/`) que impone sus propias invariantes.

Ver `docs/tasks.md` T-007.
