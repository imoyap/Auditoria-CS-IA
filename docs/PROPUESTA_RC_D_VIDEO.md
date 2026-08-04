# PROPUESTA DEL GRUPO — RC-1 a RC-6, D1–D8, estructura de 6 bloques del video

**Estado: APROBADO sin modificaciones — `LEDGER.md`, entrada `LDG-004` (2026-08-03T23:49:23-04:00).** Ninguno de los tres bloques de este documento proviene del Anexo Técnico U3, la Rúbrica U3, `docs/Instruccion.html` ni la guía Rapid7 de Metasploitable — se verificó exhaustivamente que ninguno de los cuatro documentos fuente los define (ver `docs/GAP_ANALYSIS.md` y `docs/requirements.md`, REQ-A-04/REQ-B-06/REQ-H-02). Esto es una **definición propia del grupo**, amparada por la frase del Anexo Parte I: *"Cada grupo puede modificarlo, pero debe justificar cada modificación."* Cada ítem cita la referencia externa que lo justifica. A partir de esta aprobación, estos contenidos son la fuente citable para REQ-A-04, REQ-B-06 y REQ-H-02 de `docs/requirements.md`.

**Alcance comprometido de D1–D8:** el grupo se compromete a implementar **D1, D2 y D6** (las tres recomendadas en la sección 2); D3, D4, D5, D7 y D8 quedan como extensiones adicionales opcionales si el tiempo alcanza, no como compromiso de entrega.

---

## 1. RC-1 a RC-6 — Reglas de compromiso propuestas

Basadas en la estructura estándar de Rules of Engagement de **NIST SP 800-115 §3** y **PTES (Rules of Engagement)** — ambas ya citadas por el Anexo como "referencias de técnica" (§1) — y en las restricciones explícitas del cliente ficticio descritas en `docs/Instruccion.html` (líneas 2855–2858: *"Ventana de trabajo acotada. No se autoriza explotación activa ni interrupción del servicio"*).

| ID | Regla | Justificación / fuente |
|---|---|---|
| **RC-1** | **Alcance exclusivo.** Toda operación se dirige únicamente al IP declarado en `scope/alcance.yaml` (`192.168.56.117`). Cualquier destino distinto aborta la ejecución y se registra como `RECHAZO`. | NIST SP 800-115 §3.2 (definición de alcance); condición de cierre de G0 del Anexo §5 ("una prueba negativa contra un destino no autorizado aborta correctamente"). |
| **RC-2** | **Ventana de trabajo acotada.** La ejecución solo ocurre dentro de la ventana horaria declarada en `scope/alcance.yaml`; fuera de ella, el harness rechaza iniciar el BoundedLoop. | Restricción explícita del cliente en `docs/Instruccion.html` ("ventana de trabajo acotada"); PTES (Pre-engagement, definición de ventana). |
| **RC-3** | **Prohibición de explotación activa e interrupción de servicio.** Ningún rol invoca módulos de explotación (Metasploit u otros) ni realiza acciones que puedan degradar el servicio del objetivo. RECON opera solo con herramientas de reconocimiento pasivo/semi-activo de la allowlist (`nmap`, `nc`, `curl`, `nikto` en modo no destructivo). | Restricción explícita del cliente en `docs/Instruccion.html`; condición de reprobación automática de la rúbrica ("uso de exploits activos sin autorización expresa del docente"). |
| **RC-4** | **Condición de aborto.** Cualquier comando fuera de la allowlist, cualquier señal de inestabilidad del objetivo, o el agotamiento del tope de iteraciones del BoundedLoop detiene la ejecución de inmediato; el estado se congela y se documenta, no se reintenta silenciosamente. | OSSTMM 3 (regla de "no dañar"); Anexo §5, criterio de cierre de G1. |
| **RC-5** | **Manejo de evidencia y confidencialidad.** Toda evidencia cruda (`evidencias/raw/`) y todo hallazgo se tratan como confidenciales del cliente ficticio; no se publican fuera del repositorio de entrega del grupo y el docente. | ISO 19011:2018, principio de confidencialidad (ya citado en Anexo §1 como uno de los "seis principios que la automatización tiende a erosionar"). |
| **RC-6** | **Escalamiento.** Ante un hallazgo de riesgo Crítico o Inaceptable (banda ≥15, Anexo §11), o ante cualquier incidente durante la ejecución (p. ej. el objetivo deja de responder), el grupo lo registra en el ledger y lo comunica al docente antes de continuar — no se decide solo. | Anexo §2, "Dónde está el humano" (el humano es obligatorio en los momentos de mayor consecuencia); apetito de riesgo declarado del cliente (Anexo §11). |

**Nota de diseño:** RC-1, RC-3 y RC-4 son verificables automáticamente (allowlist + verificación de destino + BoundedLoop, ya cubiertos por REQ-A-02 y REQ-B-05 de `requirements.md`); RC-2, RC-5 y RC-6 son verificables por revisión (declaración + evidencia de cumplimiento, no un validador de software). Esta distinción importa para la banda 8 de la rúbrica ("implementadas y demostradas, no solo declaradas") — hay que decidir cómo demostrar RC-2/5/6 sin inventar un mecanismo técnico donde el Anexo no lo pide.

---

## 2. D1–D8 — Dimensiones de extensión propuestas

El Anexo solo nombra **D2 — rol de contradicción explícita** (§4). Las siete restantes se proponen por analogía con capacidades que el propio Anexo menciona como posibles pero no obligatorias (re-verificación automatizada, retest diferencial, etc.). La rúbrica banda 13–14 de criterio B exige **3 o más**, implementadas y demostradas en video — el grupo no necesita las 8, solo elegir cuáles construir.

| ID | Dimensión | De dónde sale la idea |
|---|---|---|
| **D1** | **Re-verificación automatizada con artefacto capturado**, como alternativa/complemento a la firma humana para VALIDADO en casos donde existe un segundo artefacto reproducible. | Anexo §2: *"El sistema puede proponer VALIDADO; solo un humano **o una re-verificación automatizada con artefacto capturado** puede confirmarlo."* |
| **D2** | **Rol de contradicción explícita** — el rol cuyo único trabajo es argumentar en contra del cierre de cada hallazgo. | Anexo §4, definido explícitamente. |
| **D3** | **Corpus normativo chileno propio** (no solo ISO/NIST genérico) cargado en el MCP de conocimiento, con las tres leyes citadas (21.663, 21.719, 21.459) indexadas y citables por artículo. | Anexo §14, tabla de marcos a integrar. |
| **D4** | **Retest diferencial / detección de drift** — comparar una segunda ejecución contra la primera y reportar solo lo que cambió. | Anexo §2, etapa 9 ("...y retest diferencial"). |
| **D5** | **Panel de trazabilidad del ledger y los gates** — vista consolidada (aunque sea un script que imprime una tabla) que cruza hallazgos, gates y entradas del ledger para auditar el propio pipeline. | Extensión razonable sobre la exigencia de trazabilidad de criterio D; no citada literalmente en el Anexo — marcada como idea del grupo. |
| **D6** | **Motor determinista de cálculo de riesgo** — script que aplica las tablas de impacto/probabilidad (Anexo §9–10) sin intervención del LLM, con tests que fijan el resultado esperado para cada combinación de factores. | Ya exigido como base por REQ-B-04 (skill `clasificar`); como *extensión* se propone llevarlo a cobertura de test explícita, no solo cálculo. |
| **D7** | **Controles CT-01 a CT-07 como suite de validación continua** (se ejecutan automáticamente antes de cada cierre de gate, no manualmente bajo demanda). | Extensión razonable sobre el harness — no citada literalmente, marcada como idea del grupo. |
| **D8** | **Integridad del informe final** — el PDF/markdown final se firma con su propio hash, publicado junto al reporte, para que cualquier modificación posterior sea detectable. | Extensión razonable sobre criterio G/D — no citada literalmente, marcada como idea del grupo. |

**Recomendación:** D1, D2 y D6 son las tres más baratas de justificar porque ya están ancladas en texto explícito del Anexo o se derivan directamente de un REQ ya existente (REQ-D-03, REQ-B-02, REQ-B-04) — implementarlas bien como parte de la base ya casi las deja demostradas. D3, D4, D5, D7, D8 son adicionales genuinas si el tiempo alcanza.

---

## 3. Estructura de 6 bloques del video — propuesta

El Anexo ancla un solo punto de referencia: **"bloque 4" = el ejemplo del ledger** (Anexo §6, línea 140: *"Ese es exactamente el bloque 4 del video"* — el ejemplo `LDG-018/019/020` de propuesta→rechazo→decisión). La estructura completa se propone hacia atrás y hacia adelante desde ese ancla, para que encaje con lo que la rúbrica banda 10 de criterio H exige explícitamente (identificación de integrantes, ejecución real en pantalla, bloque de punto de control humano con error concreto, autocrítica).

| Bloque | Contenido | Ancla en la rúbrica/Anexo |
|---|---|---|
| **1** | Presentación: cada integrante se identifica; se resume el encargo (cliente Comercial Andes Sur SpA, activo Metasploitable2/`192.168.56.117`, restricciones). | Rúbrica H, banda 10: "Todos los integrantes intervienen e se identifican." |
| **2** | Arquitectura del pipeline: las 8 capas, los 5 roles y su tabla de permisos (mostrar `roles/verificador.md` sin herramientas de escritura como evidencia). | Criterio B — separación estructural de actores. |
| **3** | Ejecución real en pantalla: recolección → normalización → análisis, terminal visible, sin cortes que oculten fallos. | Rúbrica H, banda 10: "Ejecución real en pantalla, terminal legible, cortes anunciados." |
| **4** | **Punto de control humano** — igual al ejemplo del Anexo: un rol intenta algo indebido (p. ej. VERIFICADOR intentando escribir, o un hallazgo sin evidencia suficiente), el sistema lo rechaza, y la entrada `RECHAZO` aparece en `LEDGER.md` en vivo. | Anexo §6 (ancla explícita); rúbrica H, banda 10: "muestra un error concreto del sistema agéntico, la razón del rechazo y su registro en el ledger." Mismo artefacto que REQ-B-03/REQ-H-01. |
| **5** | Reporte final: generación autónoma en vivo, matriz de correlación, resumen ejecutivo, y el momento en que el sistema se detiene a pedir firma humana en G5. | Criterio G, banda 10: "El mecanismo de generación se demuestra en video, incluido el punto donde se detiene y pide firma humana." |
| **6** | Cierre y autocrítica: qué falló durante la construcción del sistema, qué limitaciones tiene hoy, qué no se llegó a cubrir — sin narrar que "no cometió errores". | Anexo Parte VI ("Nuestro agente no cometió errores" → rúbrica H banda 0–2); rúbrica H banda 10 exige justamente lo contrario. |

---

## Próximo paso

Cerrado. `docs/requirements.md` fue actualizado para desbloquear REQ-A-04, REQ-B-06 y REQ-H-02 citando este documento como fuente. Sigue la Fase 2 (`docs/design.md`).
