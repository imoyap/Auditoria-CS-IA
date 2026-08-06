#!/usr/bin/env bash
# harness/controles/reject_and_log.sh — hook PreToolUse (T-008, REQ-B-03)
# Corregido en T-013 (ver LEDGER.md LDG-044/LDG-045): el diseño original
# solo dejaba pasar por Bash los comandos de red de scope/allowlist.txt
# para RECON, y ningún Bash en absoluto para los demás roles -- lo que en
# la práctica les impedía ejecutar el script de su propia skill
# (calcular_riesgo.py, registrar_veto.py, correlacionar.py,
# generar_reporte.py/priorizar.py). Encontrado ejecutando RECON de verdad
# contra el objetivo real, no en una revisión de diseño.
#
# Uso: invocado por Claude Code como hooks.PreToolUse.hooks[].command en el
# frontmatter de cada .claude/agents/<rol>.md, con el nombre del ROL como
# argumento posicional $1. Recibe el evento PreToolUse como JSON por stdin.
#
# Comportamiento:
#   - Todo rol puede invocar por Bash ÚNICAMENTE el/los script(s) de su
#     propia skill (tabla SCRIPTS_PROPIOS más abajo), sin encadenamiento de
#     comandos, pipes ni redirección -- una invocación simple del
#     intérprete de Python sobre ese script exacto, con cualquier argumento.
#   - RECON, además, puede usar los comandos de red de scope/allowlist.txt
#     (con ${IP_AUTORIZADA} resuelto desde scope/alcance.yaml), y Write
#     solo bajo evidencias/raw/ o evidencias/manifest.sha256.
#   - Cualquier otro uso de Bash/Write/Edit se rechaza.
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

# Script(s) propio(s) de la skill de cada rol -- la única superficie de
# Bash que cada rol tiene, sin importar qué otra cosa declare `tools:`.
SCRIPTS_PROPIOS = {
    "RECON": [r"\.claude/skills/enumerar/scripts/registrar_evidencia\.py"],
    "ANALISTA": [r"\.claude/skills/clasificar/scripts/calcular_riesgo\.py"],
    "VERIFICADOR": [r"\.claude/skills/registrar_veto/scripts/registrar_veto\.py"],
    "COMPLIANCE": [r"\.claude/skills/correlacionar/scripts/correlacionar\.py"],
    "REDACTOR": [
        r"\.claude/skills/redactar/scripts/generar_reporte\.py",
        r"\.claude/skills/priorizar/scripts/priorizar\.py",
    ],
}

METACARACTERES_PROHIBIDOS = [";", "&&", "||", "`", "$(", ">", "<", "|", "\n"]

# Un heredoc con delimitador ENTRE COMILLAS (<<'EOF' o <<"EOF") es literal:
# el shell no expande variables ni sustituye comandos dentro de su cuerpo,
# así que no puede usarse para inyectar comandos adicionales. Esto permite
# pasarle a un script propio datos reales (p. ej. la salida de nmap) que
# contengan ';', '|' u otros metacaracteres de forma legítima -- sin abrir
# la puerta a encadenar comandos de verdad. Un heredoc SIN comillas en el
# delimitador (<<EOF) sí permite expansión dentro del cuerpo, así que NO
# se exime -- se sigue escaneando completo.
# Encontrado ejecutando RECON de verdad contra el objetivo (T-013,
# LEDGER.md LDG-047): el filtro original escaneaba el heredoc completo y
# rechazaba el ';' legítimo dentro de un banner de nmap real.
HEREDOC_COMILLADO = re.compile(r"<<\s*(['\"])(\w+)\1")

def _separar_heredoc_literal(cmd: str) -> tuple[str, bool]:
    """Retorna (porción a validar por metacaracteres, hubo_heredoc_comillado)."""
    m = HEREDOC_COMILLADO.search(cmd)
    if not m:
        return cmd, False
    # Todo lo anterior al operador << es sintaxis de shell real y se valida
    # igual que siempre; el cuerpo del heredoc (comillado) se exime.
    return cmd[: m.start()], True

def es_invocacion_de_script_propio(cmd: str) -> tuple[bool, str]:
    cmd_norm = cmd.replace("\\", "/")
    porcion_a_validar, hubo_heredoc = _separar_heredoc_literal(cmd_norm)

    for m in METACARACTERES_PROHIBIDOS:
        if m == "<" and hubo_heredoc:
            continue  # el "<<" del propio heredoc comillado es lo esperado
        if m in porcion_a_validar:
            return False, f"comando contiene metacaracter no permitido ({m!r}) fuera de un heredoc comillado -- solo se acepta una invocación simple (+ heredoc comillado opcional)"

    if not re.match(r'^\s*"?(python3?|py)"?\s', porcion_a_validar):
        return False, "no comienza con un intérprete de Python conocido (python/python3/py)"
    for patron_script in SCRIPTS_PROPIOS.get(rol, []):
        if re.search(patron_script, porcion_a_validar):
            return True, ""
    return False, f"no invoca ninguno de los scripts propios de {rol}: {SCRIPTS_PROPIOS.get(rol, [])}"

if tool == "Bash":
    cmd = tool_input.get("command", "")
    ok, motivo_script = es_invocacion_de_script_propio(cmd)
    if ok:
        allow()
        sys.exit(0)

    if rol == "RECON":
        with open(alcance_path, encoding="utf-8") as f:
            alcance = yaml.safe_load(f)
        ip = alcance["objetivo"]["ip_autorizada"]
        with open(allowlist_path, encoding="utf-8") as f:
            patterns = [l.rstrip("\n") for l in f if l.strip() and not l.strip().startswith("#")]
        for pat in patterns:
            resolved = pat.replace("${IP_AUTORIZADA}", re.escape(ip))
            if re.match(resolved, cmd):
                allow()
                sys.exit(0)
        deny(f"Comando Bash fuera de scope/allowlist.txt y no es su script de skill ({motivo_script}): {cmd!r}")
    else:
        deny(f"Comando Bash rechazado para {rol} ({motivo_script}): {cmd!r}")

elif tool == "Write":
    if rol != "RECON":
        deny(f"Intento de uso de herramienta fuera de tabla de permisos: {tool}")
    else:
        path = tool_input.get("file_path", "")
        norm = path.replace("\\", "/")
        if "/evidencias/raw/" in norm or norm.endswith("evidencias/manifest.sha256"):
            allow()
        else:
            deny(f"Write de RECON fuera de evidencias/raw/ o manifest.sha256: {path!r}")

else:
    deny(f"Intento de uso de herramienta fuera de tabla de permisos: {tool}")
PYEOF
)"

if [[ "$DECISION" == ALLOW ]]; then
  exit 0
fi

MOTIVO="${DECISION#DENY::}"
log_rechazo "$MOTIVO"
echo "BLOQUEADO ($ROL): $MOTIVO" >&2
exit 2
