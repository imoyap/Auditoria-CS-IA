# Comandos listos para grabar — T-043

Complemento de `docs/GUION_VIDEO.md`. Cada comando de abajo fue probado real antes de escribirse aquí (2026-08-07) — cópialos y pégalos tal cual en la terminal durante la grabación. Ejecutar desde la raíz del repositorio, **en Git Bash**.

**¿Van a grabar desde una terminal PowerShell en vez de Git Bash?** Usen `docs/COMANDOS_VIDEO_POWERSHELL.md` en su lugar — la sintaxis de varios comandos (heredocs, `bash`, fechas) es distinta y ya está adaptada y probada ahí.

## Paso 0 — ANTES de empezar a grabar (obligatorio en Windows/Git Bash)

La consola de Windows por defecto usa la página de códigos 850 (DOS), no UTF-8 — con eso, cualquier texto con tildes/eñes se ve roto en pantalla (`Cr�tico` en vez de `Crítico`), aunque el dato real esté correcto. Antes de grabar, en la misma terminal que van a usar:

```bash
chcp.com 65001
export PYTHONIOENCODING=utf-8
```

Verificar que quedó bien:
```bash
python3 -c "print('Prueba: Crítico, § válido, año')"
```
Debe verse exactamente así, sin ningún `�`. Si se abre una terminal nueva para grabar, repetir este paso — no es permanente entre sesiones de terminal.

---

## Bloque 1 — Presentación

Mostrar el archivo completo (no hace falta comando, abrir en el editor):
```
scope/alcance.yaml
```
Señalar en voz las secciones `objetivo` (IP autorizada, mecanismo de autorización) y `reglas_de_compromiso` (RC-1 a RC-6).

---

## Bloque 2 — Arquitectura

Mostrar sin comando: `.claude/agents/verificador.md` (señalar `tools:`/`disallowedTools:` y el `hooks.PreToolUse`).

**D6 en vivo:**
```bash
python3 .claude/skills/clasificar/scripts/test_calcular_riesgo.py
```
Salida esperada: 12/12 líneas `[OK]`, termina en `TODOS LOS CASOS PASARON`.

---

## Bloque 3 — Ejecución real en pantalla

**Evidencia cruda real:**
```bash
head -15 evidencias/raw/01_nmap_full.txt
sha256sum -c evidencias/manifest.sha256
```

**Inventario normalizado (capa 2, sin LLM):**
```bash
python3 -c "
import json
d = json.load(open('normalizado/inventario.json', encoding='utf-8'))
print('Total de servicios:', len(d['servicios']))
print(json.dumps(d['servicios'][0], ensure_ascii=False, indent=2))
"
```

**Los 4 hallazgos finales:**
```bash
python3 -c "
import json
for l in open('normalizado/candidatos.json', encoding='utf-8'):
    d = json.loads(l)
    print(d['check_id'], '->', d['estado'], '|', d['hallazgo'][:60])
"
```
Salida esperada (verificada real, 2026-08-07):
```
H-01 -> VALIDADO | Bindshell root sin autenticacion expuesto en 1524/tcp (Metas
H-02 -> OBSERVADO | vsftpd 2.3.4 con backdoor conocido embebido en el binario, p
H-03 -> INCONCLUSO | UnrealIRCd con troyano/backdoor conocido, puertos 6667 y 669
H-04 -> OBSERVADO | distccd sin autenticacion permite ejecucion remota de comand
```

---

## Bloque 4 — Punto de control humano (EN VIVO, genera una entrada real y nueva en el ledger)

```bash
echo '{"tool_name":"Write","tool_input":{"file_path":"reporte/reporte_final.md"}}' | bash harness/controles/reject_and_log.sh VERIFICADOR
echo "código de salida: $?"
tail -1 LEDGER.md
```
Salida esperada: `BLOQUEADO (VERIFICADOR): ...`, código `2`, y una línea `RECHAZO | VERIFICADOR | ...` nueva y real al final de `LEDGER.md` — con timestamp del momento exacto de la grabación. Explicar en voz: esto es el runtime rechazando la herramienta, no un mensaje simulado.

---

## Bloque 5 — Reporte final y firma humana (EN VIVO, con gate desechable)

**Mostrar el reporte real:**
```bash
cat reporte/reporte_final.md
```

**Demostrar el mecanismo de parada/firma** (crea y elimina un gate de prueba — no toca G0/G3/G5 reales):
```bash
cat > gates/GDEMO.md <<'EOF'
## Gate GDEMO — Demostración en vivo para el video

**Firma humana:** [PENDIENTE]
EOF

# Intento SIN firma -- debe fallar
python3 harness/orquestador.py --sign-gate GDEMO
echo "código de salida: $?"

# Firma real, en vivo, con el nombre real de quien firma
python3 harness/orquestador.py --sign-gate GDEMO --by "NOMBRE APELLIDO" --date "$(date +%Y-%m-%d)"
cat gates/GDEMO.md

# Limpieza -- no es un gate real
rm gates/GDEMO.md
```
Reemplazar `"NOMBRE APELLIDO"` por el nombre real de quien firma en cámara. Explicar en voz: el primer intento falla porque faltan `--by`/`--date`; el segundo reemplaza `[PENDIENTE]` por la firma real — este es el mismo mecanismo exacto que cerró G0, G3 y G5 de verdad.

**Después de grabar**, si `git status` muestra `gates/GDEMO.md` o cambios en `LEDGER.md` por esta prueba, no hace falta revertir el ledger (es append-only, la entrada de prueba queda documentada como tal, igual que `LDG-070`) — solo confirmar que `gates/GDEMO.md` fue eliminado (`git status` no debe mostrarlo).

---

## Bloque 6 — Cierre y autocrítica

Sin comandos — apoyarse en las limitaciones reales listadas en `docs/GUION_VIDEO.md` bloque 6. Si se quiere mostrar algo en pantalla, `LEDGER.md` buscando `LDG-062` (bug real de acentos) o `LDG-068` (objeción real de CONTRADICTOR) sirve como evidencia visual de autocrítica genuina.

---

## Verificación posterior a la grabación

```bash
git status --short
```
Debe mostrar como máximo cambios en `LEDGER.md` (las entradas reales generadas durante la grabación de los bloques 4 y 5) y ningún `gates/GDEMO.md` sin eliminar. Comitear esas entradas nuevas del ledger como parte de la entrega final, citando que provienen de la grabación del video.
