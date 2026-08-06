# Reporte Final de Auditoría — Comercial Andes Sur SpA

**Activo evaluado:** SRV-ADM-01 (Metasploitable2, 192.168.56.117)

## Resumen Ejecutivo

Total de hallazgos: 4 (Crítica: 1, Alta: 1, Media: 0, Baja: 0 + 2 sin severidad técnica asignable (sin CVE/CVSS catalogado, o verificación aún pendiente — ver columna Estado por hallazgo))

*Estas cifras se calculan por agregación directa sobre los hallazgos verificados, no se redactan a mano (control CT-05).*

## Hallazgos

| ID | Hallazgo | Severidad | Estado | evidence_id |
|---|---|---|---|---|
| H-01 | Bindshell root sin autenticacion expuesto en 1524/tcp (Metasploitable root shell) | NO_OBSERVADO | VALIDADO | 01_nmap_full |
| H-02 | vsftpd 2.3.4 con backdoor conocido embebido en el binario, puerto 21/tcp | Crítica | OBSERVADO | 01_nmap_full |
| H-03 | UnrealIRCd con troyano/backdoor conocido, puertos 6667 y 6697 tcp | NO_OBSERVADO | INCONCLUSO | 01_nmap_full |
| H-04 | distccd sin autenticacion permite ejecucion remota de comandos, puerto 3632/tcp | Alta | OBSERVADO | 01_nmap_full |

## Advertencia

Este documento constituye un análisis técnico de controles de seguridad y su correspondencia con obligaciones normativas. No sustituye asesoría legal. La calificación jurídica definitiva de la organización, sus roles y sus obligaciones debe ser validada por abogado. La normativa chilena de ciberseguridad y protección de datos se encuentra en despliegue por etapas; los criterios sujetos a reglamento pendiente se señalan como tales.
