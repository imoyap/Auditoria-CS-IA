#!/usr/bin/env bash
# harness/controles/reject_and_log.sh — hook PreToolUse (T-008, REQ-B-03)
#
# Uso: invocado por Claude Code como hooks.PreToolUse.hooks[].command en el
# frontmatter de cada .claude/agents/<rol>.md, con el nombre del ROL como
# argumento posicional $1. Recibe el evento PreToolUse como JSON por stdin
# (campos tool_name / tool_input, formato de Claude Code).
#
# Comportamiento:
#   - RECON: permite Bash solo si el comando matchea un patrón de
#     scope/allowlist.txt (con ${IP_AUTORIZADA} resuelto desde
#     scope/alcance.yaml); permite Write solo bajo evidencias/raw/ o
#     evidencias/manifest.sha256. Cualquier otro uso se rechaza.
#   - Para los demás roles (ANALISTA, VERIFICADOR, COMPLIANCE, REDACTOR): el
#     matcher del hook ya sólo dispara sobre Bash/Write/Edit, herramientas que
#     ninguno de esos roles tiene en su `tools:` — llegar aquí es en sí mismo
#     la violación. Se rechaza siempre.
#
# Salida: código 0 = permite; código 2 = bloquea (contrato de Claude Code
# para hooks PreToolUse). Toda decisión de rechazo se anexa a LEDGER.md.

set -euo pipefail

ROL="${1:?Uso: reject_and_log.sh <ROL>}"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
LEDGER="${REPO_ROOT}/LEDGER.md"
ALCANCE="${REPO_ROOT}/scope/alcance.yaml"
ALLOWLIST="${REPO_ROOT}/scope/allowlist.txt"

INPUT_JSON="$(cat)"

log_rechazo() {
  local motivo="$1"
  local ts
  ts="$(date -Iseconds)"
  local id="LDG-HOOK-$(date +%s%N)"
  printf '%s | %s | RECHAZO | %s | %s | ref:hook\n' \
    "$ts" "$id" "$ROL" "$motivo" >> "$LEDGER"
}

# Delega la decisión a Python: JSON de entrada + YAML de alcance + allowlist
# de texto son más fáciles de validar ahí de forma robusta que en bash puro.
# El JSON de entrada se pasa por variable de entorno (no por stdin) porque
# stdin ya se usa para entregarle el propio script a `python3 -`.
DECISION="$(HOOK_INPUT_JSON="$INPUT_JSON" python3 - "$ROL" "$ALCANCE" "$ALLOWLIST" <<'PYEOF'
import json, os, re, sys, yaml

rol, alcance_path, allowlist_path = sys.argv[1], sys.argv[2], sys.argv[3]
payload = json.loads(os.environ["HOOK_INPUT_JSON"])
tool = payload.get("tool_name", "")
tool_input = payload.get("tool_input", {}) or {}

def deny(motivo):
    print("DENY::" + motivo)

def allow():
    print("ALLOW")

if rol != "RECON":
    # Ningún otro rol tiene Bash/Write/Edit en su `tools:` — llegar aquí ya
    # es la violación (defensa en profundidad; en operación normal el
    # runtime ni siquiera ofrece la herramienta al modelo).
    deny(f"Intento de uso de herramienta fuera de tabla de permisos: {tool}")
    sys.exit(0)

# --- Reglas específicas de RECON ---
with open(alcance_path, encoding="utf-8") as f:
    alcance = yaml.safe_load(f)
ip = alcance["objetivo"]["ip_autorizada"]

if tool == "Bash":
    cmd = tool_input.get("command", "")
    with open(allowlist_path, encoding="utf-8") as f:
        patterns = [l.rstrip("\n") for l in f if l.strip() and not l.strip().startswith("#")]
    for pat in patterns:
        resolved = pat.replace("${IP_AUTORIZADA}", re.escape(ip))
        if re.match(resolved, cmd):
            allow()
            sys.exit(0)
    deny(f"Comando Bash fuera de scope/allowlist.txt: {cmd!r}")
elif tool == "Write":
    path = tool_input.get("file_path", "")
    norm = path.replace("\\", "/")
    if "/evidencias/raw/" in norm or norm.endswith("/evidencias/manifest.sha256") or norm.endswith("evidencias/manifest.sha256"):
        allow()
    else:
        deny(f"Write de RECON fuera de evidencias/raw/ o manifest.sha256: {path!r}")
else:
    deny(f"Herramienta no contemplada en la superficie de RECON: {tool}")
PYEOF
)"

if [[ "$DECISION" == ALLOW ]]; then
  exit 0
fi

MOTIVO="${DECISION#DENY::}"
log_rechazo "$MOTIVO"
echo "BLOQUEADO ($ROL): $MOTIVO" >&2
exit 2
