# Anexo Técnico — Unidad 3

## Arquitectura de referencia, workflow de auditoría, clasificación de riesgo y correlación normativa

*Documento de apoyo para el estudiante. Es la base sobre la cual cada grupo construye su propia versión.*

---

## Parte I — El workflow del proceso de auditoría

### 1. Primero: auditoría no es pentest

Es la distinción que ordena todo lo demás y la que más se pierde cuando se automatiza.

| | Prueba de penetración | Auditoría de ciberseguridad |
|---|---|---|
| **Pregunta** | ¿Puedo entrar? | ¿La realidad observada se ajusta al criterio declarado? |
| **Producto** | Demostración de compromiso | Juicio fundado sobre conformidad y riesgo |
| **Requisito previo** | Autorización y alcance | Autorización, alcance y criterio de auditoría |
| **Éxito** | Encontrar una ruta de explotación | Poder sostener cada afirmación con evidencia |
| **Sesgo peligroso** | Confundir "no entré" con "es seguro" | Confundir "el escáner lo dijo" con "está verificado" |

**Consecuencia práctica:** antes de ejecutar el primer comando hay que declarar contra qué se audita. Sin criterio, no hay hallazgo — hay observación técnica sin significado. Para esta actividad, el criterio de auditoría se compone de al menos: ISO/IEC 27001:2022 Anexo A, NIST CSF 2.0 y la normativa chilena aplicable al cliente.

**Referencias de proceso:** ISO 19011:2018 (directrices para auditoría de sistemas de gestión), ISO/IEC 27007 (auditoría de SGSI), ISACA ITAF.
**Referencias de técnica:** NIST SP 800-115, OSSTMM 3, PTES, OWASP WSTG.

Los seis principios de ISO 19011 que la automatización tiende a erosionar y que su pipeline debe preservar: **integridad, presentación imparcial, debido cuidado profesional, confidencialidad, independencia y enfoque basado en evidencia**.

### 2. Workflow canónico de referencia

Diez etapas. Cada grupo puede modificarlo, pero debe justificar cada modificación.

| # | Etapa | Producto de la etapa | Actor principal | ¿Gate? |
|---|---|---|---|---|
| 0 | Encargo y autorización | Carta de alcance firmada, ventana, contactos, restricciones | Humano | G0 |
| 1 | Definición del criterio de auditoría | Lista de controles y obligaciones contra los cuales se auditará | Humano + COMPLIANCE | G0 |
| 2 | Planificación | Plan de pruebas: qué se verificará, con qué herramienta, qué evidencia se espera | SPEC / Humano | — |
| 3 | Recolección de evidencia | Artefactos crudos con hash y timestamp | RECON | G1 |
| 4 | Normalización e inventario | JSON canónico de activos, servicios, versiones, banners | Determinista (sin LLM) | G2 |
| 5 | Análisis y verificación | Hallazgos candidatos con estado VALIDADO / OBSERVADO / INCONCLUSO | ANALISTA → VERIFICADOR | G3 |
| 6 | Evaluación de riesgo | Severidad técnica + impacto + probabilidad + riesgo contextual | ANALISTA + Humano | G3 |
| 7 | Correlación normativa | Matriz hallazgo ↔ control ↔ obligación ↔ evidencia requerida | COMPLIANCE | G4 |
| 8 | Reporte | Informe final generado, coherente y trazable | REDACTOR | G5 |
| 9 | Comunicación, remediación y seguimiento | Plan con responsables y plazos, y retest diferencial | Humano | — |

#### Dónde está el humano

Un pipeline agéntico sin puntos de detención no es autonomía: es ausencia de control. Los tres momentos donde el humano es obligatorio:

1. **Antes de empezar (G0).** Autoriza el alcance. Ningún agente inicia sin scope firmado.
2. **Al asignar el estado VALIDADO (G3).** El sistema puede proponer VALIDADO; solo un humano o una re-verificación automatizada con artefacto capturado puede confirmarlo.
3. **Al firmar el informe (G5).** La responsabilidad profesional no es transferible a un modelo.

---

## Parte II — Arquitectura agéntica de referencia

### 3. Las ocho capas

```
┌───────────────────────────────────────────────────────────────┐
│ 8. CONTROL HUMANO — gates de firma, veto, aceptación          │
├───────────────────────────────────────────────────────────────┤
│ 6. HARNESS — orquestación, gates, ledger, estado, BoundedLoop │
├──────────────┬──────────────┬─────────────────────────────────┤
│ 5. ROLES      │ 4. SKILLS    │ 3. CONOCIMIENTO (MCP)          │
│ RECON         │ enumerar     │ CVE / CWE / CVSS                │
│ ANALISTA      │ clasificar   │ ISO 27001:2022 Anexo A          │
│ VERIFICADOR   │ correlacionar│ NIST CSF 2.0 / CIS v8           │
│ COMPLIANCE    │ redactar     │ Corpus normativo chileno        │
│ REDACTOR      │ priorizar    │ (solo lectura, citable)         │
├──────────────┴──────────────┴─────────────────────────────────┤
│ 2. NORMALIZACIÓN — parsers deterministas → JSON canónico       │
├───────────────────────────────────────────────────────────────┤
│ 1. RECOLECCIÓN — nmap, nc, curl, nikto → crudo + SHA-256       │
├───────────────────────────────────────────────────────────────┤
│ OBJETIVO — 192.168.56.101 (solo lectura)                       │
└───────────────────────────────────────────────────────────────┘
```

**La regla de oro de la capa 2:** el modelo de lenguaje nunca lee la terminal directamente. Lee el JSON normalizado. La mayor parte de las alucinaciones de los informes generados por IA se originan en pedirle a un modelo que interprete texto crudo largo y ambiguo. Un parser determinista no alucina un banner que no está.

### 4. Los cinco roles del concilio

| Rol | Pregunta que hace | Herramientas que tiene | Herramientas que NO tiene | Poder |
|---|---|---|---|---|
| **RECON** | ¿Qué hay realmente ahí? | Ejecutor de allowlist, escritura en `evidencias/raw/` | Redacción de hallazgos | Voz |
| **ANALISTA** | ¿Qué significa esto y cuánto vale? | Lectura del JSON canónico, MCP de CVE/CWE/CVSS | Ejecución de comandos, asignación de VALIDADO | Voz |
| **VERIFICADOR** | ¿La evidencia demuestra lo que dice demostrar? | Lectura de todo | Escritura sobre hallazgos | Veto de cierre |
| **COMPLIANCE** | ¿A qué control y a qué obligación corresponde, y por qué a este cliente? | MCP normativo | Modificación de severidades | Voz |
| **REDACTOR** | ¿Está dicho de forma que el destinatario lo entienda y pueda actuar? | Plantillas, datos verificados | Creación de contenido no trazable | Voz |

**Separación de actores (obligatoria):** quien redacta un hallazgo no puede validarlo dentro del mismo ciclo. Y la separación debe ser estructural, no de buena fe: al VERIFICADOR simplemente no se le entregan herramientas de escritura. Un veto se levanta con evidencia, no con insistencia.

**Rol opcional de alto valor (dimensión de extensión D2):** el rol de **contradicción explícita**, cuyo único trabajo es construir el mejor argumento en contra del cierre de cada hallazgo. Es el rol que más incomoda y el que más errores atrapa. Si nunca objeta nada, no se está ejerciendo.

### 5. Los gates

Formato de cierre de gate — se escribe en `gates/GX.md` y se referencia en el ledger:

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

| Gate | Criterio de cierre verificable |
|---|---|
| **G0 — Alcance** | Existe scope firmado con IP autorizada. La allowlist está versionada. Una prueba negativa contra un destino no autorizado aborta correctamente. |
| **G1 — Recolección** | Todo artefacto crudo tiene hash y timestamp. El manifiesto verifica. No hay comandos ejecutados fuera de allowlist en el log. |
| **G2 — Inventario** | Cada servicio del JSON canónico apunta a una línea del artefacto crudo. Cero servicios sin origen. |
| **G3 — Clasificación** | Cada hallazgo tiene evidencia, estado, CWE, vector CVSS completo, impacto y probabilidad con factores declarados. Firma humana sobre cada VALIDADO. |
| **G4 — Correlación** | Cada hallazgo tiene al menos un control ISO, una categoría NIST, un control CIS y la línea "aplica porque". Cada control tiene evidencia requerida declarada. |
| **G5 — Reporte** | Los siete controles anti-alucinación pasan. Cero afirmaciones sin `evidence_id`. Firma humana del informe. |

`APPROVE_WITH_FINDINGS` es el veredicto más honesto y el más frecuente: el gate cierra y los hallazgos quedan visibles y fechados, en vez de desaparecer.

### 6. El ledger

Archivo append-only, versionado. Nunca se edita ni se borra: una decisión revocada genera una entrada `SUPERSEDE` que referencia la original.

```
[ISO-8601] | [ID] | [DECISION|GATE|HALLAZGO|SUPERSEDE|RECHAZO] | [actor] | [resumen en una línea] | [ref]
```

Ejemplo real de lo que se espera ver:

```
2026-08-14T10:22:41-04:00 | LDG-018 | HALLAZGO | ANALISTA | Propone H-07 "CMS WordPress desactualizado" desde banner HTTP | ev:04_nmap_sv.txt
2026-08-14T10:24:03-04:00 | LDG-019 | RECHAZO | VERIFICADOR | Veto a H-07: ningún artefacto contiene la cadena wordpress. Inferencia no sostenida | ev:manifest.sha256
2026-08-14T10:31:15-04:00 | LDG-020 | DECISION | HUMANO | Se acepta el veto. H-07 se descarta, no se reetiqueta como INCONCLUSO por ausencia total de indicio | gate:G3
```

*Ese es exactamente el bloque 4 del video.*

### 7. Los siete controles anti-alucinación

Cada uno corresponde a un error real observado en los informes de CertEngine analizados en la Unidad 1.

| ID | Control | Error de CertEngine que previene | Implementación mínima |
|---|---|---|---|
| **CT-01** | Trazabilidad obligatoria. Toda afirmación del reporte lleva `evidence_id`. | Hallazgos sin respaldo | Validador que rechaza el reporte si alguna afirmación carece de identificador |
| **CT-02** | Prohibición de inferencia de servicio. No se declara un producto que no aparezca literalmente en un artefacto crudo. | Hallazgo de CMS y de registro SPF fabricados | Búsqueda literal de la cadena en `evidencias/raw/` antes de admitir el hallazgo |
| **CT-03** | Coherencia de severidad. Un mismo hallazgo tiene la misma severidad en todas las secciones. | Severidades contradictorias entre resumen y detalle | Comparación automática entre matriz, tabla y ficha del hallazgo |
| **CT-04** | Remediación aplicable. La remediación no puede apuntar a la versión vulnerable ni a un componente inexistente. | Remediación que recomendaba la misma versión afectada | Verificación de que la versión objetivo de la remediación ≠ versión instalada |
| **CT-05** | Consistencia numérica. Los conteos y cifras del resumen ejecutivo se recalculan desde los datos, no se escriben. | Cifras divergentes entre secciones | El resumen se genera por agregación, no por redacción |
| **CT-06** | Estado condicionado por la red. Un hallazgo que no pudo alcanzarse por condiciones de red no puede marcarse verificado. | Hallazgos bloqueados por NAT marcados "Verified" | Regla: si el intento de verificación falló, el estado máximo es INCONCLUSO |
| **CT-07** | Cero dato sintético. Si un dato no existe, la ausencia se mide, se fecha y se muestra como hallazgo. Nunca se rellena. | Informe simétrico y completo sobre datos incompletos | Marcadores `NO_OBSERVADO` que el generador propaga al informe |

---

## Parte III — Clasificación de riesgo

### 8. Severidad técnica ≠ riesgo organizacional

CVSS mide la vulnerabilidad. La matriz de riesgo mide lo que le pasa a este cliente.

vsftpd 2.3.4 tiene un CVSS base de 10,0 en cualquier parte del mundo. Pero el riesgo de vsftpd 2.3.4 en SRV-ADM-01 de Comercial Andes Sur depende de si ese servidor está en la red plana donde trabajan 140 personas, de si toca datos de clientes, y de si existe un módulo de explotación estable y público. Esos tres datos son los que convierten una severidad en un riesgo.

Reportar solo el CVSS es entregar el trabajo a medias. Reportar una matriz de riesgo sin CVSS es entregar una opinión.

### 9. Cálculo del impacto (escala 1–5)

Sume los factores. Cada uno vale 0, 1 o 2.

| Factor | 0 | 1 | 2 |
|---|---|---|---|
| Pérdida de confidencialidad | Ninguna | Parcial | Total |
| Pérdida de integridad | Ninguna | Parcial | Total |
| Pérdida de disponibilidad | Ninguna | Parcial | Total |
| Datos personales involucrados | No | Datos personales comunes | Datos sensibles (salud, biométricos, NNA) |
| Criticidad operacional del activo | Baja | Media | Alta |

| Suma | 0–1 | 2–3 | 4–5 | 6–7 | 8–10 |
|---|---|---|---|---|---|
| **Impacto** | 1 Muy bajo | 2 Bajo | 3 Medio | 4 Alto | 5 Muy alto |

### 10. Cálculo de la probabilidad (escala 1–5)

| Factor | 0 | 1 | 2 |
|---|---|---|---|
| Exploit público funcional | No existe | PoC parcial o inestable | Módulo estable y documentado |
| Puntaje de explotación predicha (EPSS o equivalente) | Percentil bajo | Percentil medio | Percentil alto |
| Presencia en catálogo de explotación conocida (tipo CISA KEV) | No | — | Sí |
| Autenticación requerida | Privilegiada | Usuario común | Ninguna |
| Exposición del activo | Segmentado, sin ruta desde el usuario | Red interna plana | Alcanzable desde redes no confiables |

| Suma | 0–1 | 2–3 | 4–5 | 6–7 | 8–10 |
|---|---|---|---|---|---|
| **Probabilidad** | 1 Muy baja | 2 Baja | 3 Media | 4 Alta | 5 Muy alta |

> **Nota de laboratorio.** El entorno está aislado y sin acceso a Internet. Si su MCP de conocimiento no dispone de EPSS o KEV offline, declaren el factor como `NO_DISPONIBLE` y justifiquen el valor asignado por los factores restantes. No lo inventen — eso es exactamente lo que prohíbe CT-07, y se detecta.

### 11. La matriz 5×5

Riesgo inherente = Impacto × Probabilidad (1 a 25)

| I \ P | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| **5** | 5 | 10 | 15 | 20 | 25 |
| **4** | 4 | 8 | 12 | 16 | 20 |
| **3** | 3 | 6 | 9 | 12 | 15 |
| **2** | 2 | 4 | 6 | 8 | 10 |
| **1** | 1 | 2 | 3 | 4 | 5 |

| Banda | Valor | Tratamiento exigido | Plazo de referencia |
|---|---|---|---|
| Bajo | 1 – 4 | Aceptar y monitorear | Ciclo anual |
| Medio | 5 – 9 | Plan de remediación | 90 días |
| Alto | 10 – 14 | Plan de remediación con responsable nominado | 30 días |
| Crítico | 15 – 19 | Contención + remediación | 7 días |
| Inaceptable | 20 – 25 | Contención inmediata; evaluar aislamiento del activo | 24 – 48 horas |

**Apetito de riesgo declarado por Comercial Andes Sur:** no acepta riesgo residual ≥ 15 en activos que traten datos personales. Ese umbral es el que determina qué se escala al comité de gerencia.

**Riesgo residual** = el riesgo recalculado suponiendo aplicado el control propuesto. Se reporta junto al inherente; sin él, la priorización no tiene sustento.

### 12. La regla de divergencia (criterio de auditor)

Cuando la banda CVSS y la banda de riesgo contextual difieren en **más de un nivel**, el grupo debe justificar la divergencia por escrito, en el propio hallazgo.

Es el momento en que se ejerce el juicio profesional, y es el que ningún agente debe resolver solo.

**Ejemplo de justificación aceptable:**

> H-03 tiene CVSS 9,8 (Crítico) por ejecución remota sin autenticación. El riesgo contextual se evalúa en 12 (Alto) y no en 20, porque el servicio afectado no procesa ni almacena datos de clientes y la explotación exige presencia en la red interna, que requiere credencial de dominio previa. La divergencia se sostiene en la segmentación observada en el hallazgo H-11 y no en una estimación. Si la segmentación se pierde, este riesgo sube a 20 automáticamente.

**Ejemplo de justificación inaceptable:** "se considera menos riesgoso por el contexto del cliente."

---

## Parte IV — Correlación normativa y de cumplimiento

### 13. Formato de la matriz de correlación

Es el entregable E4. Una fila por hallazgo, y estas columnas como mínimo:

```
ID | Hallazgo | evidence_id | Estado | CWE | CVE | Vector CVSS | I | P | Riesgo |
Control ISO/IEC 27001:2022 | Función/Categoría NIST CSF 2.0 | Control CIS v8 |
Obligación normativa CL | Aplica porque | Evidencia requerida | Brecha | Remediación |
Esfuerzo | Responsable | Plazo | Riesgo residual
```

Dos columnas son las que hacen útil el documento y las que más se omiten:

- **"Aplica porque"** — una línea que explica por qué esa obligación alcanza a este cliente. Sin ella, la matriz se lee como copia de la ley y nadie la usa.
- **"Evidencia requerida"** — qué se le exhibe a un fiscalizador o a un auditor de certificación: política aprobada con fecha, registro de configuración, bitácora, contrato con encargado, resultado de prueba. Un control sin evidencia demostrable es, en la práctica, un control que no existe.

### 14. Marcos a integrar

| Función | Marco | Uso en esta actividad |
|---|---|---|
| Criterio de auditoría | ISO/IEC 27001:2022 Anexo A (93 controles en 4 temas) | Vara principal de conformidad |
| Criterio de auditoría | NIST CSF 2.0 (GV, ID, PR, DE, RS, RC) | Vista de capacidad organizacional |
| Criterio de auditoría | CIS Controls v8 (IG1/IG2/IG3) | Vara operativa: qué hacer el lunes |
| Clasificación de debilidad | CWE | Tipo de debilidad |
| Identificación | CVE / NVD | Vulnerabilidad conocida específica |
| Severidad | CVSS 3.1 (vector completo obligatorio) | Severidad técnica |
| Probabilidad | EPSS, catálogo de explotación conocida | Insumo de probabilidad, no de severidad |
| Técnica adversaria | MITRE ATT&CK | Qué haría un atacante con el hallazgo |
| Riesgo | ISO 31000 / ISO/IEC 27005 / NIST SP 800-30 | Método de evaluación de riesgo |
| Proceso de auditoría | ISO 19011:2018 / ISO/IEC 27007 | Cómo se conduce la auditoría |
| Normativa CL — ciberseguridad | Ley 21.663 (Marco de Ciberseguridad, ANCI) | Deberes de gestión de riesgos y reporte de incidentes |
| Normativa CL — datos personales | Ley 21.719 | Medidas de seguridad, brechas, roles de tratamiento |
| Normativa CL — legalidad del ejercicio | Ley 21.459 (delitos informáticos) | Marco que hace del alcance autorizado un asunto legal, no de etiqueta |

### 15. Ejemplos trabajados

Se entregan tres filas resueltas como referencia de nivel esperado. El resto de la matriz es trabajo del grupo.

#### Ejemplo 1 — Telnet expuesto

| Campo | Valor |
|---|---|
| Hallazgo | Servicio Telnet activo en 23/tcp; credenciales y sesión en texto claro |
| Estado | VALIDADO (conexión establecida y captura de banner; verificación adicional con `nc`) |
| CWE | CWE-319 — Transmisión de información sensible en texto claro |
| Severidad técnica | Alta |
| Impacto | C=2, I=1, D=0, datos personales=1, criticidad=2 → suma 6 → **4** |
| Probabilidad | exploit=0, EPSS=NO_DISPONIBLE, KEV=0, auth=2, exposición=1 → suma 3 → **2** |
| Riesgo inherente | 4 × 2 = **8 (Medio)** |
| Control ISO/IEC 27001:2022 | A.8.20 Seguridad de redes · A.8.24 Uso de criptografía · A.8.21 Seguridad de servicios de red |
| NIST CSF 2.0 | PR.DS-02 (datos en tránsito protegidos) · PR.PS-01 (gestión de configuración) |
| CIS v8 | 4.1 Proceso de configuración segura · 4.8 Desinstalar servicios innecesarios · 3.10 Cifrar datos sensibles en tránsito |
| Obligación normativa CL | Ley 21.719: deber de adoptar medidas técnicas apropiadas al riesgo del tratamiento |
| Aplica porque | El servidor está en la misma red plana desde la que se administran los sistemas que tratan datos de clientes; una credencial capturada en esa red habilita acceso a esos sistemas |
| Evidencia requerida | Estándar de configuración segura aprobado, con Telnet prohibido; registro de configuración del host; resultado de la verificación posterior |
| Brecha | No existe estándar de configuración segura ni proceso de baja de servicios obsoletos |
| Remediación | Deshabilitar y desinstalar el servicio `telnetd`; habilitar acceso exclusivamente por SSH con autenticación por clave; bloquear 23/tcp en el firewall de host |
| Esfuerzo / Plazo | Bajo / 30 días |
| Riesgo residual | 4 × 1 = **4 (Bajo)** |

#### Ejemplo 2 — vsftpd 2.3.4

| Campo | Valor |
|---|---|
| Hallazgo | Versión de vsftpd con puerta trasera documentada (CVE-2011-2523) |
| Estado | OBSERVADO — la versión se identificó por banner; no se ejecutó explotación, por prohibición del alcance |
| CWE | CWE-912 — Funcionalidad oculta |
| Severidad técnica | Crítica (CVSS 10,0) |
| Impacto | C=2, I=2, D=2, datos personales=1, criticidad=2 → suma 9 → **5** |
| Probabilidad | exploit=2, EPSS=NO_DISPONIBLE, KEV=0, auth=2, exposición=1 → suma 5 → **3** |
| Riesgo inherente | 5 × 3 = **15 (Crítico)** |
| Control ISO/IEC 27001:2022 | A.8.8 Gestión de vulnerabilidades técnicas · A.8.19 Instalación de software en sistemas operativos |
| NIST CSF 2.0 | ID.RA-01 (vulnerabilidades identificadas) · PR.PS-02 (mantenimiento de software) |
| CIS v8 | 7.3 Gestión automatizada de parches de SO · 2.2 Software soportado |
| Obligación normativa CL | Ley 21.663: deber de aplicar medidas de gestión de riesgos y de reportar incidentes de efecto significativo, en los términos del régimen aplicable a la organización |
| Aplica porque | La ejecución remota sin autenticación sobre un activo de la red de administración habilita un incidente con potencial afectación de datos personales, lo que activa a la vez el deber de seguridad de la Ley 21.719 |
| Evidencia requerida | Inventario de software con versiones; procedimiento de gestión de vulnerabilidades con SLA por severidad; registro del último ciclo de parcheo |
| Brecha | No hay proceso de gestión de vulnerabilidades ni inventario de versiones |
| Remediación | Actualizar a versión soportada del paquete o migrar a SFTP; verificar que la versión objetivo no sea la afectada (control CT-04) |
| Esfuerzo / Plazo | Medio / 7 días |
| Riesgo residual | 5 × 1 = **5 (Medio)** |

> Obsérvese el estado **OBSERVADO** y no VALIDADO. El alcance prohibió explotar. La versión es un indicio fuerte, no una confirmación. Marcar esto como VALIDADO sería exactamente el error de CertEngine, y aquí cuesta puntaje.

#### Ejemplo 3 — Ausencia como hallazgo

| Campo | Valor |
|---|---|
| Hallazgo | No se observó evidencia de registro de eventos de autenticación en los servicios expuestos |
| Estado | INCONCLUSO — la verificación exigía acceso al host, fuera del alcance autorizado |
| CWE | CWE-778 — Registro insuficiente |
| Impacto / Probabilidad | No se calcula: sin verificación, no se asigna riesgo cuantitativo |
| Control ISO/IEC 27001:2022 | A.8.15 Registro de eventos · A.8.16 Actividades de monitoreo |
| NIST CSF 2.0 | DE.CM-01 · DE.AE-03 |
| CIS v8 | 8.2 Recolección de logs de auditoría · 8.5 Logs detallados |
| Aplica porque | Sin registro no es posible acreditar el momento ni el alcance de una brecha, requisito práctico para cumplir cualquier deber de notificación |
| Evidencia requerida | Política de registro; configuración de envío a repositorio central; muestra de logs con retención declarada |
| Recomendación | Ampliar el alcance de una auditoría posterior a revisión con credenciales sobre el host |

> Ese tercer ejemplo es el más importante de los tres. Un informe que solo contiene lo que se pudo verificar y omite lo que no se pudo, engaña por omisión. Registrar la ausencia, fecharla y explicar por qué no se pudo verificar es el comportamiento profesional — y es lo que exige el control CT-07.

### 16. Advertencia obligatoria en el entregable

Todo informe del grupo debe cerrar con:

> Este documento constituye un análisis técnico de controles de seguridad y su correspondencia con obligaciones normativas. No sustituye asesoría legal. La calificación jurídica definitiva de la organización, sus roles y sus obligaciones debe ser validada por abogado. La normativa chilena de ciberseguridad y protección de datos se encuentra en despliegue por etapas; los criterios sujetos a reglamento pendiente se señalan como tales.

**Errores a evitar en esta parte:**

- Afirmar que algo "está prohibido" cuando la norma exige condiciones. La mayoría de las obligaciones son condicionadas, no prohibitivas.
- Copiar el texto del artículo como si fuera análisis. El cliente puede leer la ley; les paga por saber qué hacer el lunes.
- Asumir la calificación de operador de importancia vital. Es una determinación de autoridad, no una autoevaluación.
- Prometer que un control "garantiza cumplimiento". Los controles reducen exposición y producen evidencia; nadie garantiza el criterio de un fiscalizador.

---

## Parte V — Estructura mínima del repositorio (E2)

```
U2_GRUPO-XX/
├── README.md                    # arquitectura, decisiones, extensiones elegidas
├── scope/
│   ├── alcance.yaml              # IP autorizada, ventana, restricciones
│   ├── allowlist.txt             # comandos permitidos
│   └── declaracion_etica.md      # firmada por los integrantes
├── roles/                        # definición de cada rol: alcance, herramientas, prohibiciones
├── skills/                       # procedimientos reutilizables
├── mcp/                          # configuración de los servidores de conocimiento
├── harness/
│   ├── orquestador.*             # ciclo, BoundedLoop, WIP=1
│   └── controles/                # CT-01 a CT-07 implementados
├── evidencias/
│   ├── raw/                      # artefactos crudos, sin editar
│   └── manifest.sha256
├── normalizado/                  # JSON canónico
├── gates/                        # G0..G5 cerrados
├── LEDGER.md                     # append-only
└── reporte/
    ├── reporte_final.md
    ├── reporte_final.pdf
    └── matriz_correlacion.csv
```

---

## Parte VI — Errores frecuentes que ya sabemos que van a aparecer

| Error | Por qué ocurre | Cómo se ve en la corrección |
|---|---|---|
| Un solo agente hace todo y se le llama "arquitectura agéntica" | Es lo más rápido de montar | Criterio B baja a la banda 6–9 |
| El modelo lee el output crudo de nmap directamente | Se salta la capa 2 porque "igual funciona" | Aparecen servicios que no están en la evidencia; CT-02 lo atrapa |
| Todos los hallazgos quedan VALIDADO | Se confunde "el escáner lo dijo" con "lo verifiqué" | Criterios D y E bajan simultáneamente |
| La matriz de riesgo replica el CVSS | No se contextualizó nada | Criterio E banda 4–7: riesgo tratado como sinónimo de severidad |
| Todos los hallazgos mapean al mismo control ISO | Se mapeó por comodidad, no por análisis | Criterio F banda 6–9 |
| El ledger se escribe al final, de una sola vez | Se trató la gobernanza como papeleo | Timestamps consecutivos delatan la reconstrucción → reprobación automática |
| El video muestra diapositivas en el bloque de ejecución | La corrida falló y no se rehízo | Criterio H banda 4–6 |
| "Nuestro agente no cometió errores" | No se revisó críticamente el propio sistema | Criterio H banda 0–2 |

---

*Anexo Técnico U3 versión 1.0 (© CHSecurity Academic Framework to Diplomado en Ciberseguridad by C4A)*
