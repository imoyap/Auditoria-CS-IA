# Explicación simple para grabar el video (T-043)

Este documento traduce `docs/GUION_VIDEO.md` a lenguaje llano, con frases que puedes decir casi tal cual frente a la cámara, sin necesitar dominar los detalles técnicos. Adapta el tono a tu manera de hablar — lo importante es que la idea quede clara.

---

## La idea general (memorizar esto, es la base de todo)

> "Construimos un sistema donde 5 roles de inteligencia artificial hacen una auditoría de seguridad, pero **ninguno tiene permiso para hacer más de lo que le corresponde**. El que revisa evidencia no puede escribir el reporte. El que verifica un hallazgo no puede darlo por válido él solo — eso lo tiene que confirmar una persona real, con su nombre y fecha. Y todo lo que pasa queda registrado en una bitácora con la hora exacta, para que se pueda comprobar que nada se inventó."

Esa es la frase que sostiene todo el video. Todo lo demás es mostrar evidencia de que eso es cierto.

---

## Bloque 0 (opcional) — Cómo se armó el entorno de trabajo

Esto no es uno de los 6 bloques obligatorios de la rúbrica, pero si quieren mostrar profesionalismo en la gestión de versiones, o si el docente pregunta "¿cómo organizaron el repositorio?", esta es la secuencia real, verificada contra el historial de git (no es una reconstrucción de memoria):

> "El docente creó un repositorio base en su cuenta pública de GitHub y también subió el mismo proyecto comprimido a un Drive compartido. Nosotros hicimos un fork de la rama del docente a nuestra propia cuenta de GitHub — eso nos dio una copia independiente para trabajar sin afectar el repositorio original. Por separado, descargamos el archivo comprimido del Drive, lo descomprimimos en una carpeta de nuestro computador, y abrimos esa carpeta en Visual Studio Code."
>
> "Dentro de esa carpeta local inicializamos nuestro propio control de versiones y ahí construimos todo el pipeline de auditoría de 5 roles — cada archivo, cada decisión, con fecha y hora real registrada en nuestra bitácora. Al terminar, conectamos ese trabajo local con el fork que ya teníamos en GitHub, y lo subimos a una rama nueva, para no sobrescribir la rama principal que había heredado el historial del repositorio del docente."

Si preguntan por qué no se subió directamente a la rama principal (`main`): porque esa rama ya tenía el historial heredado del fork, y sobrescribirla habría borrado ese contenido — se optó por la vía segura de usar una rama nueva.

### Cómo se fue construyendo el proyecto con Claude Code

> "Trabajamos con Claude Code, un asistente de inteligencia artificial, integrado directamente en Visual Studio Code como una consola. La forma de trabajar fue: nosotros le entregábamos los documentos que el docente nos dio — el Anexo Técnico, la Rúbrica de evaluación, las instrucciones del curso — colocándolos dentro de la carpeta `docs/` del proyecto. A medida que avanzábamos, cuando la IA necesitaba un dato que no tenía (por ejemplo, la dirección IP real de la máquina, o una confirmación de alcance), nos lo pedía explícitamente antes de continuar, y nosotros se lo entregábamos. Así, paso a paso, revisando y aprobando cada decisión importante, se fue generando toda la estructura del proyecto que ven aquí."

Esto es importante decirlo porque demuestra que **hubo supervisión humana real en cada paso**, no que la IA hizo todo sola sin control — que es exactamente lo que la rúbrica busca (criterio "dónde está el humano").

## Bloque 1 — Presentación

Cada integrante dice su nombre. Luego, uno explica el encargo:

> "Hicimos una auditoría de seguridad simulada sobre una máquina de laboratorio llamada Metasploitable2, en la dirección 192.168.56.117. El cliente ficticio es 'Comercial Andes Sur SpA'. Nos pusieron reglas claras: solo podíamos trabajar en una ventana de tiempo autorizada, y **nunca podíamos explotar activamente ninguna vulnerabilidad** — solo detectarla y documentarla."

Mostrar en pantalla: `scope/alcance.yaml`.

## Bloque 2 — Arquitectura

> "El sistema tiene 5 roles, cada uno con un trabajo específico y permisos limitados. Por ejemplo, este es el rol VERIFICADOR."

Mostrar `.claude/agents/verificador.md` y decir:

> "Noten que en la configuración, este rol **no tiene permiso de escritura** — no puede crear ni modificar archivos directamente. Solo puede usar un único script que anexa una línea a nuestra bitácora. Esto es una restricción técnica, no una promesa — si intenta hacer otra cosa, el sistema lo bloquea automáticamente, se los mostramos en el bloque 4."

Ejecutar en vivo (ver `docs/COMANDOS_VIDEO.md`):
```bash
python3 .claude/skills/clasificar/scripts/test_calcular_riesgo.py
```
> "Esto es el motor que calcula el riesgo de cada hallazgo — es determinista, es decir, siempre da el mismo resultado con los mismos datos, no depende del criterio del modelo de IA. Aquí se ve que pasa las 12 pruebas comparando contra los ejemplos numéricos del documento del curso."

## Bloque 3 — Ejecución real en pantalla

> "Ahora mostramos la evidencia real que se capturó de la máquina."

Ejecutar los comandos del bloque 3 de `docs/COMANDOS_VIDEO.md` y decir:

> "Este es el resultado real de escanear la máquina — encontramos 30 servicios abiertos. De esos, el sistema propuso 4 hallazgos candidatos, y después de verificarlos, quedaron así:
> - Uno **validado**: un shell de administrador sin contraseña, expuesto directamente.
> - Dos **observados**: se detectó la versión de un software con una vulnerabilidad conocida, pero no se confirmó activándola — porque eso estaba prohibido.
> - Uno **inconcluso**: no había suficiente evidencia para confirmar ni descartar."

## Bloque 4 — Punto de control humano (el más importante de la rúbrica)

Ejecutar el comando del bloque 4 (rechazo en vivo) y decir:

> "Aquí vamos a intentar, a propósito, que el rol VERIFICADOR haga algo que no le corresponde: escribir un archivo directamente."

*(ejecutar el comando)*

> "Como ven, el sistema lo bloqueó de inmediato — código de error 2, y automáticamente quedó registrado en la bitácora con la hora exacta de este momento. Esto no es una regla que le pedimos amablemente a la inteligencia artificial que respete — es una restricción técnica del programa, no puede saltársela aunque quisiera."

## Bloque 5 — Reporte final y firma humana

Mostrar `reporte/reporte_final.md` (o el HTML) y decir:

> "Este es el informe final, generado automáticamente a partir de los datos ya verificados — no es texto libre escrito por la IA, es una plantilla rellenada con los datos reales."

Ejecutar la demostración de firma (bloque 5 de `docs/COMANDOS_VIDEO.md`) y decir:

> "Y este es el momento clave: antes de que un hallazgo se pueda dar por 'confirmado' de forma definitiva, el sistema se detiene y exige que una persona lo firme con su nombre real y la fecha. Miren: sin ese dato, falla. Con el dato, se firma. El sistema en ningún momento se firma a sí mismo."

## Bloque 6 — Cierre y autocrítica

> "Para terminar, queremos ser honestos sobre las limitaciones de lo que hicimos:
> - Uno de los 4 hallazgos quedó sin poder confirmarse — no porque el sistema fallara, sino porque la evidencia real no alcanzaba, y decidimos no inventar una conclusión.
> - Durante la construcción encontramos varios errores reales: un diseño inicial de permisos que no funcionaba y tuvimos que rediseñar, y un error donde la palabra 'Crítica' con tilde no se contaba bien en el resumen del reporte.
> - Y la ventana de tiempo autorizada la tuvimos que extender dos veces porque el trabajo tomó más de lo planeado."

---

## Las carpetas y archivos más importantes (para explicar si preguntan, o para el bloque 2)

Frase de entrada sugerida:

> "El proyecto está organizado en carpetas, cada una con un propósito específico. Se las resumo:"

| Carpeta / archivo | Qué contiene, en palabras simples |
|---|---|
| **`docs/`** | Toda la documentación del proyecto: los documentos que nos dio el docente (`anexo_tecnico_u3.md`, `rubrica_evaluacion_u3.md`), y los que fuimos generando nosotros a medida que avanzábamos — el análisis inicial (`GAP_ANALYSIS.md`), los requisitos (`requirements.md`), el diseño (`design.md`), el plan de tareas (`tasks.md`), y los guiones para este mismo video. |
| **`scope/`** | El **alcance autorizado** de la auditoría: `alcance.yaml` dice exactamente qué máquina se puede auditar, en qué horario, y con qué reglas (nunca explotar, nunca salirse del rango). También está `declaracion_etica.md`, firmada por los integrantes, y `allowlist.txt`, la lista exacta de comandos permitidos. |
| **`roles/`** | Una descripción en texto de cada uno de los 5 roles del sistema (qué hace, qué NO puede hacer, y con qué "voz" actúa) — es la documentación humana de lo que después se implementó técnicamente en `.claude/agents/`. |
| **`.claude/agents/`** | La implementación técnica real de cada rol — el archivo que le dice al sistema exactamente qué herramientas tiene permitidas cada uno (por ejemplo, `verificador.md` no tiene permiso de escritura). |
| **`.claude/skills/`** | Las herramientas concretas (scripts) que cada rol puede ejecutar — una carpeta por tarea (`enumerar`, `clasificar`, `correlacionar`, `redactar`, etc.). |
| **`evidencias/`** | La evidencia **real** recolectada de la máquina auditada: el resultado completo del escaneo (`raw/01_nmap_full.txt`), una captura de pantalla que confirma la IP de la máquina, y un archivo con el "huella digital" (hash) de cada evidencia, para probar que no fue alterada después. |
| **`normalizado/`** | Los datos ya procesados: el inventario de todos los servicios encontrados (`inventario.json`), los hallazgos candidatos y su estado final (`candidatos.json`), y la tabla que los cruza con normativa legal (`matriz_borrador.csv`). |
| **`gates/`** | Los "puntos de control" (G0 a G5) — cada uno es un archivo que dice qué se revisó, quién lo aprobó, y (en los tres más importantes) quién lo firmó con su nombre real. |
| **`harness/`** | El motor que controla todo el flujo — el "director de orquesta" que avanza etapa por etapa y se detiene a pedir firma humana cuando corresponde. |
| **`mcp/`** | Dos "bases de consulta" que los roles usan para no inventar información: una con vulnerabilidades conocidas (CWE/CVSS), otra con normativa (ISO, NIST, leyes chilenas). |
| **`reporte/`** | **El entregable final** — el informe completo, en Markdown y en HTML, listo para presentar. |
| **`LEDGER.md`** | La bitácora — el archivo más importante para demostrar honestidad: cada decisión, cada rechazo, cada firma, con fecha y hora real de cuando ocurrió. |
| **`README.md`** | La puerta de entrada del proyecto — resume todo el flujo de 10 etapas y dónde interviene cada rol, para alguien que recién abre el repositorio. |

> "No hace falta que memoricemos cada archivo — lo importante es que quede claro que cada carpeta tiene un propósito específico, y que nada se mezcla: la evidencia real está separada de los datos procesados, y esos están separados del reporte final."

---

## Si el docente pregunta algo que no sabes responder

Está bien decir, literalmente:

> "Esa parte específica la trabajamos apoyándonos en herramientas de asistencia técnica, pero puedo mostrarle exactamente dónde está documentada la decisión y por qué se tomó así" — y buscar la entrada correspondiente en `LEDGER.md` o `docs/tasks.md`. Ambos archivos tienen una entrada para cada decisión importante, citando el motivo.

No es necesario memorizar cada línea de código — el punto del sistema es justamente que las decisiones quedan documentadas, no que ustedes las memoricen todas.
