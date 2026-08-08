# Comandos para grabar en PowerShell — T-043

Versión de `docs/COMANDOS_VIDEO.md` adaptada a **Windows PowerShell** (no Git Bash). Cada comando de este archivo fue probado real, uno por uno, en una terminal PowerShell antes de escribirse aquí (2026-08-07).

## Paso 0 — antes de empezar a grabar

En la PowerShell que usaste ya se ven bien las tildes por defecto (`Crítico`, `§`) — no hace falta el `chcp` que sí es obligatorio en Git Bash. Solo verifica una vez:
```powershell
python3 -c "print('Prueba: Crítico, § válido, año')"
```
Si se ve bien, listo. Si no, ejecuta también `chcp.com 65001` antes de grabar.

**Importante — no uses el comando `bash` a secas en esta máquina.** En PowerShell, `bash` resuelve a WSL (Windows Subsystem for Linux), no a Git Bash — son entornos distintos y el bloque 4 fallará. Usa siempre la ruta completa de Git Bash, como se muestra abajo.

---

## Bloque 1 — Presentación

Mostrar el archivo completo (ábrelo en el editor, no hace falta comando):
```
scope/alcance.yaml
```

---

## Bloque 2 — Arquitectura

Mostrar sin comando: `.claude/agents/verificador.md`.

**D6 en vivo:**
```powershell
python3 .claude/skills/clasificar/scripts/test_calcular_riesgo.py
```
Salida esperada: 12/12 líneas `[OK]`, termina en `TODOS LOS CASOS PASARON`.

---

## Bloque 3 — Ejecución real en pantalla

**Evidencia cruda real (primeras 15 líneas):**
```powershell
Get-Content evidencias\raw\01_nmap_full.txt -TotalCount 15
```

**Verificación de integridad (equivalente a `sha256sum -c`):**
```powershell
Get-Content evidencias\manifest.sha256 | ForEach-Object {
    $partes = $_ -split '\*'
    $hashEsperado = $partes[0].Trim()
    $archivo = $partes[1].Trim()
    $hashReal = (Get-FileHash $archivo -Algorithm SHA256).Hash.ToLower()
    if ($hashReal -eq $hashEsperado) { Write-Output "$archivo : OK" } else { Write-Output "$archivo : FALLO" }
}
```
Salida esperada: `OK` para los 2 archivos de evidencia.

**Inventario normalizado:**
```powershell
python3 -c "
import json
d = json.load(open('normalizado/inventario.json', encoding='utf-8'))
print('Total de servicios:', len(d['servicios']))
print(json.dumps(d['servicios'][0], ensure_ascii=False, indent=2))
"
```

**Los 4 hallazgos finales:**
```powershell
python3 -c "
import json
for l in open('normalizado/candidatos.json', encoding='utf-8'):
    d = json.loads(l)
    print(d['check_id'], '->', d['estado'], '|', d['hallazgo'][:60])
"
```
Salida esperada (verificada real en PowerShell, 2026-08-07):
```
H-01 -> VALIDADO | Bindshell root sin autenticacion expuesto en 1524/tcp (Metas
H-02 -> OBSERVADO | vsftpd 2.3.4 con backdoor conocido embebido en el binario, p
H-03 -> INCONCLUSO | UnrealIRCd con troyano/backdoor conocido, puertos 6667 y 669
H-04 -> OBSERVADO | distccd sin autenticacion permite ejecucion remota de comand
```

---

## Bloque 4 — Punto de control humano (EN VIVO)

```powershell
'{"tool_name":"Write","tool_input":{"file_path":"reporte/reporte_final.md"}}' | & "C:\Program Files\Git\bin\bash.exe" harness/controles/reject_and_log.sh VERIFICADOR
Write-Output "codigo de salida: $LASTEXITCODE"
Get-Content LEDGER.md -Tail 1
```
Salida esperada: `BLOQUEADO (VERIFICADOR): ...`, código `2`, y una línea `RECHAZO | VERIFICADOR | ...` nueva y real al final de `LEDGER.md`, con el timestamp exacto del momento de la grabación.

**Nota técnica (para quien pregunte por qué se usa esa ruta completa):** se encontraron y corrigieron 2 bugs reales preparando este bloque en PowerShell — documentados en `LEDGER.md` `LDG-074` — relacionados con que `bash` sin ruta completa activa WSL en vez de Git Bash en esta máquina, y con que PowerShell antepone un carácter invisible (BOM) al canalizar texto a un programa externo. Ambos ya están corregidos en el script; usar la ruta completa de Git Bash es la forma correcta de invocarlo desde PowerShell.

---

## Bloque 5 — Reporte final y firma humana (EN VIVO, con gate desechable)

**Mostrar el reporte real:**
```powershell
Get-Content reporte\reporte_final.md
```

**Crear el gate de prueba:**
```powershell
@'
## Gate GDEMO — Demostración en vivo para el video

**Firma humana:** [PENDIENTE]
'@ | Set-Content -Path gates\GDEMO.md -Encoding utf8
```

**Intento SIN firma (debe fallar):**
```powershell
python3 harness/orquestador.py --sign-gate GDEMO
Write-Output "codigo de salida: $LASTEXITCODE"
```

**Firma real, en vivo, con el nombre real de quien firma:**
```powershell
$fecha = Get-Date -Format 'yyyy-MM-dd'
python3 harness/orquestador.py --sign-gate GDEMO --by "NOMBRE APELLIDO" --date $fecha
Get-Content gates\GDEMO.md
```
Reemplazar `"NOMBRE APELLIDO"` por el nombre real de quien firma en cámara.

**Limpieza (no es un gate real):**
```powershell
Remove-Item gates\GDEMO.md -Force
```

---

## Bloque 6 — Cierre y autocrítica

Sin comandos — apoyarse en `docs/GUION_VIDEO.md` bloque 6.

---

## Verificación posterior a la grabación

```powershell
git status --short
```
Debe mostrar como máximo cambios en `LEDGER.md` (las entradas reales de los bloques 4 y 5) y ningún `gates\GDEMO.md` sin eliminar.
