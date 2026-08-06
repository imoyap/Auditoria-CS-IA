# Declaración ética

**Actividad de Cierre Unidad 3 — Auditoría de Ciberseguridad Asistida por Arquitectura Agéntica**
**Cliente ficticio:** Comercial Andes Sur SpA · **Activo:** SRV-ADM-01 (representado por Metasploitable2) · **Alcance:** ver `scope/alcance.yaml`

Quienes firman esta declaración se comprometen, para toda ejecución del pipeline descrito en este repositorio, a:

1. **Respetar el alcance autorizado sin excepción.** Operar exclusivamente contra el IP declarado en `scope/alcance.yaml` (`objetivo.ip_autorizada`), dentro de la ventana de trabajo ahí declarada, y solo con los comandos de `scope/allowlist.txt`.
2. **No ejecutar explotación activa ni acciones que interrumpan el servicio**, conforme a la restricción explícita del cliente y a RC-3 de `scope/alcance.yaml`.
3. **No fabricar, editar ni completar evidencia.** Ningún hallazgo, hash, timestamp o entrada de `LEDGER.md` se genera, simula o rellena — si un dato no existe, se declara `NO_OBSERVADO` o `NO_DISPONIBLE` con su justificación, nunca se inventa (control CT-07).
4. **Sostener los seis principios de ISO 19011:2018** citados en el Anexo Técnico U3 §1: integridad, presentación imparcial, debido cuidado profesional, confidencialidad, independencia y enfoque basado en evidencia.
5. **Preservar la separación de roles como estructural, no como promesa.** No intentar sortear las restricciones de herramientas de ningún rol (p. ej. hacer pasar por VERIFICADOR una escritura que debería venir de otro rol) para acelerar el trabajo.
6. **Registrar los propios errores del sistema, no ocultarlos.** El video y el reporte final deben mostrar al menos un caso real donde el pipeline falló o fue rechazado, conforme a lo que exige la rúbrica (criterio H) y a lo que señala el Anexo Parte VI sobre declarar "nuestro agente no cometió errores".
7. **Mantener la confidencialidad de la evidencia** del cliente ficticio y del laboratorio (RC-5 de `scope/alcance.yaml`), no publicándola fuera del repositorio de entrega y el docente.

## Firmas

| Nombre | Rol en el grupo | Fecha |
|---|---|---|
| Mauricio Carrera | Integrante | 2026-08-04 |

<!--
Si el grupo tiene más integrantes, agregar una fila por cada uno con su
nombre y fecha de firma real — no se completa con nombres no confirmados.
-->
