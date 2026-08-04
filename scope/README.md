# scope/

Alcance autorizado del pipeline (capa 8 — insumo de control humano).

- `alcance.yaml` — IP autorizada, activo, ventana, restricciones, reglas de compromiso RC-1..6. Única fuente del IP autorizado (campo `objetivo.ip_autorizada`); ningún otro archivo del repo debe hardcodear su valor.
- `allowlist.txt` — comandos permitidos para RECON.
- `declaracion_etica.md` — firmada por los integrantes del grupo.

Ver `docs/tasks.md` T-002 a T-005.
