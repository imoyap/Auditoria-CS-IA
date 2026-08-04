# Rúbrica de Evaluación — Unidad 3

## Auditoría de Ciberseguridad Asistida por Arquitectura Agéntica

**Puntaje total:** 100 puntos · **Exigencia:** 60% · **Puntaje de aprobación:** 60 → nota 4,0 · **Escala:** 1,0 – 7,0

---

## Tabla resumen de ponderaciones

| Criterio | Máximo |
|---|---|
| A. Alcance, autorización y reglas de compromiso del pipeline | 8 |
| B. Arquitectura agéntica y extensión propia sobre la base | 14 |
| C. Workflow de auditoría declarado y ejecutado | 10 |
| D. Evidencia, trazabilidad y controles anti-alucinación | 14 |
| E. Clasificación de riesgo y matriz impacto × probabilidad | 12 |
| F. Correlación normativa y de cumplimiento | 14 |
| G. Reporte final generado autónomamente | 14 |
| H. Video: demostración y punto de control humano | 14 |
| **TOTAL** | **100** |

> **Nota de transcripción:** el PDF original presenta una inconsistencia entre esta tabla resumen y los encabezados de las secciones G y H más abajo. La tabla resumen asigna 14 puntos a G y 14 a H, pero los encabezados de sección y las bandas de puntaje detalladas para G y H solo llegan hasta 10. Se transcribe tal como aparece en el documento original, sin corregirlo — conviene confirmar con el docente cuál valor es el vigente antes de usarlo para autoevaluación.

---

## A. Alcance, autorización y reglas de compromiso del pipeline — 8 puntos

| Puntaje | Criterio |
|---|---|
| 8 | Declara alcance completo (activo, IP, red, ventana, restricciones) y criterio de auditoría adoptado. Las seis reglas de compromiso RC-1 a RC-6 están implementadas y demostradas, no solo declaradas. Existe allowlist versionada y verificación de destino en tiempo de ejecución. La declaración ética está firmada por todos los integrantes. |
| 6 | Alcance completo y declaración ética presente. Cuatro o cinco reglas de compromiso implementadas. Alguna verificación existe pero no se demuestra. |
| 3 | Alcance declarado pero las reglas de compromiso son enunciados en el README sin implementación verificable. |
| 0 | Alcance ausente o ambiguo. O evidencia de ejecución fuera de 192.168.56.101. O declaración ética ausente. (Ver condiciones de reprobación automática.) |

---

## B. Arquitectura agéntica y extensión propia sobre la base — 14 puntos

| Puntaje | Criterio |
|---|---|
| 13–14 | Las ocho capas están presentes y diferenciadas. Los roles tienen alcance, herramientas y prohibiciones declaradas por escrito, y la separación de actores es estructural (al VERIFICADOR no se le entregan herramientas de escritura), no de buena fe. Las skills son procedimientos reutilizables e invocables. Al menos un servidor MCP en uso real. El harness aplica BoundedLoop con tope y condición de salida. Tres o más dimensiones de extensión (D1–D8) implementadas, documentadas y demostradas en video. |
| 10–12 | Capas presentes con alguna difusa (típicamente normalización y análisis mezclados). Roles definidos pero la separación es declarativa. Tres extensiones presentes, alguna solo parcialmente demostrada. |
| 6–9 | Existe orquestación pero los roles no están realmente separados: un mismo actor recolecta, analiza y redacta. Una o dos extensiones. MCP ausente o simulado. |
| 0–5 | No hay arquitectura: hay una secuencia de prompts pegados en un chat, o un script sin componente agéntico. Sin extensión propia sobre la base. |

---

## C. Workflow de auditoría declarado y ejecutado — 10 puntos

| Puntaje | Criterio |
|---|---|
| 10 | Declara un workflow completo del proceso de auditoría (encargo → criterio → planificación → recolección → verificación → evaluación de riesgo → correlación → reporte → comunicación → seguimiento), no solo de la ejecución de herramientas. Justifica las etapas contra una referencia reconocida (ISO 19011, NIST SP 800-115, PTES, OSSTMM). Señala con precisión dónde actúa cada rol y dónde firma el humano. El workflow ejecutado coincide con el declarado. |
| 7–9 | Workflow completo y justificado, pero la ejecución diverge del diseño en algún punto sin explicarlo, o el seguimiento posterior queda fuera. |
| 4–6 | Workflow reducido a la cadena de herramientas. Confunde auditoría con pentest: no declara criterio contra el cual auditar. |
| 0–3 | No hay workflow declarado. La ejecución es una secuencia improvisada. |

---

## D. Evidencia, trazabilidad y controles anti-alucinación — 14 puntos

| Puntaje | Criterio |
|---|---|
| 13–14 | Cada afirmación del reporte final es trazable a un `evidence_id` con artefacto crudo, hash y timestamp. El manifiesto de evidencias verifica. Los siete controles CT-01 a CT-07 están implementados y al menos tres se demuestran atrapando un caso real. Los estados VALIDADO / OBSERVADO / INCONCLUSO se usan con rigor y el estado VALIDADO tiene respaldo de verificación adicional, no solo de nmap. Las ausencias se registran, no se rellenan. |
| 10–12 | Trazabilidad presente en la mayoría de hallazgos. Manifiesto existe. Cuatro a seis controles implementados. Algún hallazgo marcado VALIDADO cuya evidencia solo respalda OBSERVADO. |
| 6–9 | Hay evidencia cruda guardada pero la cadena hallazgo → evidencia se sostiene por lectura manual, no por identificador. Controles anti-alucinación mencionados sin implementar. Uso inconsistente de los tres estados. |
| 0–5 | Sin trazabilidad. Afirmaciones del reporte que no corresponden a ningún artefacto. Cualquier hallazgo no trazable es causal de revisión por deshonestidad técnica. |

---

## E. Clasificación de riesgo y matriz impacto × probabilidad — 12 puntos

| Puntaje | Criterio |
|---|---|
| 11–12 | Distingue explícitamente severidad técnica (CVSS con vector completo) de riesgo organizacional contextualizado. Impacto y probabilidad se derivan de factores declarados y trazables a fuente (subpuntajes CVSS, existencia de exploit público, EPSS o equivalente, exposición del activo, tipo de dato tratado, criticidad operacional). La matriz 5×5 tiene bandas y umbral de aceptación declarados contra el apetito de riesgo del cliente. Cuando CVSS y riesgo contextual divergen en más de una banda, la divergencia está justificada por escrito. |
| 8–10 | Matriz construida con criterio declarado y CVSS con vector. Algún parámetro asignado sin fuente. La divergencia CVSS/riesgo aparece pero se justifica de manera superficial. |
| 4–7 | Matriz presente pero los valores de impacto y probabilidad son asignaciones sin criterio verificable. CVSS reportado como número sin vector. Riesgo tratado como sinónimo de severidad. |
| 0–3 | Sin matriz, o matriz de colores sin criterio. Severidades incoherentes entre secciones del reporte. |

---

## F. Correlación normativa y de cumplimiento — 14 puntos

| Puntaje | Criterio |
|---|---|
| 13–14 | Cada hallazgo se correlaciona con: control ISO/IEC 27001:2022 (Anexo A), función y categoría NIST CSF 2.0, control CIS v8 e implicancia bajo normativa chilena aplicable al cliente. La columna "aplica porque" explica en una línea por qué esa obligación alcanza a esta organización. Para cada control se declara la evidencia requerida que se le exhibiría a un fiscalizador o auditor de certificación. La correlación es bidireccional: se puede navegar del hallazgo al control y del control a la evidencia. Incluye la advertencia de no-asesoría-legal y trata las obligaciones condicionadas como condicionadas. |
| 10–12 | Correlación con tres marcos, completa en la mayoría de hallazgos. "Aplica porque" presente pero genérico en varias filas. Evidencia requerida declarada de forma parcial. |
| 6–9 | Correlación con uno o dos marcos, o mapeo genérico repetido (todos los hallazgos apuntan al mismo control). Se cita el artículo de la ley sin traducirlo a acción. |
| 0–5 | Sin correlación normativa, o correspondencias incorrectas que no resisten revisión. Afirma prohibiciones absolutas donde la norma establece condiciones. |

---

## G. Reporte final generado autónomamente — 10 puntos

*(Ver nota de transcripción al inicio del documento respecto de la ponderación de este criterio.)*

| Puntaje | Criterio |
|---|---|
| 10 | El reporte se genera desde datos verificados, no se redacta a mano. Sigue el template canónico y lo extiende con justificación. Resumen ejecutivo escrito para el comité de gerencia, coherente numéricamente con las tablas de detalle. Priorización de remediación con responsable, esfuerzo y plazo. Remediaciones concretas y aplicables a la versión instalada. El mecanismo de generación se demuestra en video, incluido el punto donde se detiene y pide firma humana. |
| 7–9 | Reporte generado con estructura completa. Alguna sección redactada a mano sin declararlo. Remediaciones mayoritariamente concretas. Resumen ejecutivo aún demasiado técnico para su destinatario. |
| 4–6 | Reporte producido en gran medida a mano con apoyo puntual de la herramienta. Secciones del template incompletas o con placeholders. Remediaciones genéricas. |
| 0–3 | Sin generación automatizada. O reporte con incoherencias internas del tipo que se identificó en los informes de CertEngine. |

---

## H. Video: demostración y punto de control humano — 10 puntos

*(Ver nota de transcripción al inicio del documento respecto de la ponderación de este criterio.)*

| Puntaje | Criterio |
|---|---|
| 10 | Duración dentro de rango. Todos los integrantes intervienen e se identifican. Ejecución real en pantalla, terminal legible, cortes anunciados. El bloque del punto de control humano muestra un error concreto del sistema agéntico, la razón del rechazo y su registro en el ledger. Los seis bloques de la estructura exigida están presentes y en proporción. |
| 7–9 | Estructura completa y ejecución real. El punto de control humano se muestra pero el error exhibido es menor o cosmético. Algún integrante con participación mínima. Legibilidad irregular. |
| 4–6 | Demostración parcialmente narrada sobre diapositivas. Punto de control humano mencionado pero no demostrado. Fuera de rango de duración. |
| 0–2 | No demuestra ejecución. O el grupo declara que su sistema no cometió errores y no exhibe ninguna verificación crítica sobre su propio pipeline. |

---

## I. Revisión cruzada producida — 4 puntos

*Se evalúa la calidad de la revisión que el grupo produce sobre el reporte de otro grupo, no la calificación que recibe.*

| Puntaje | Criterio |
|---|---|
| 4 | Identifica hallazgos no trazables, incoherencias de severidad, correlaciones normativas forzadas y remediaciones inaplicables, citando la sección específica. Distingue error de decisión metodológica distinta. Formula al menos una observación que el grupo revisado no había considerado. |
| 3 | Revisión sustantiva con observaciones correctas pero superficiales o repetidas. |
| 1–2 | Revisión de forma: ortografía, formato, extensión. No entra en el contenido técnico. |
| 0 | No entrega revisión, o entrega una revisión de cortesía sin observaciones. |

---

## J. Defensa oral — 4 puntos

| Puntaje | Criterio |
|---|---|
| 4 | Todos los integrantes responden preguntas sobre su propio pipeline. Explican por qué un hallazgo quedó OBSERVADO y no VALIDADO, cómo se calculó un valor específico de la matriz, y qué habría pasado si el agente hubiera fallado en un punto distinto. Reconocen las limitaciones de su sistema sin defenderlo. |
| 3 | Responden correctamente con apoyo del reporte. Alguno de los integrantes conoce parcialmente el trabajo del grupo. |
| 1–2 | Solo uno o dos integrantes pueden explicar el trabajo. Respuestas que repiten el reporte sin razonamiento propio. |
| 0 | No pueden explicar decisiones de su propia entrega. |

---

## Niveles de desempeño

| Calificación | Puntaje | Nota aproximada | Descripción |
|---|---|---|---|
| Excelente | 90 – 100 | 6,3 – 7,0 | Pipeline con gobernanza real, correlación normativa defendible y juicio de auditor evidente. Entregable presentable a un cliente. |
| Muy buen desempeño | 80 – 89 | 5,5 – 6,2 | Sistema completo con omisiones menores. Comprensión sólida del rol del auditor sobre el agente. |
| Buen desempeño | 70 – 79 | 4,8 – 5,4 | Cumple lo esencial. Trazabilidad presente. Correlación y matriz mejorables. |
| Aprobado | 60 – 69 | 4,0 – 4,7 | Pipeline funcional mínimo, evidencia básica, correlación incompleta pero correcta. |
| Reprobado | 0 – 59 | 1,0 – 3,9 | No cumple criterios mínimos. |

---

## Condiciones de reprobación automática (puntaje = 0 para todo el grupo)

| Condición | Justificación |
|---|---|
| Ejecución del pipeline contra cualquier IP fuera de 192.168.56.101 | Violación del alcance autorizado — potencialmente ilegal |
| Uso de exploits activos sin autorización expresa del docente | Violación de las reglas de compromiso |
| Hallazgos en el reporte que no son trazables a un artefacto de evidencia | Dato sintético — deshonestidad técnica |
| Ledger, timestamps o hashes reconstruidos con posterioridad a la ejecución | Falsificación de trazabilidad |
| Video que simula una ejecución que no ocurrió | Deshonestidad académica grave |
| Reporte, pipeline o matriz copiados de otro grupo | Plagio |
| Reporte que no usa el template canónico como base | Incumplimiento de entregable mínimo |

---

## Conversión a escala 1,0 – 7,0

Puntaje de aprobación = 100 × 0,60 = **60 puntos**

- Si puntaje < 60: `nota = 1,0 + (puntaje / 60) × 3,0`
- Si puntaje ≥ 60: `nota = 4,0 + ((puntaje − 60) / 40) × 3,0`

Verificación de extremos: 0 puntos → 1,0 · 60 puntos → 4,0 · 100 puntos → 7,0

| Puntaje | 0 | 20 | 40 | 60 | 70 | 80 | 90 | 100 |
|---|---|---|---|---|---|---|---|---|
| Nota | 1,0 | 2,0 | 3,0 | 4,0 | 4,8 | 5,5 | 6,3 | 7,0 |

**Criterio de redondeo:** un decimal, redondeo aritmético estándar.

---

*Rúbrica U3 versión 1.0 (© Diplomado en Ciberseguridad by C4A)*
