# Explicación simple para grabar el video (T-043)

Este documento traduce `docs/GUION_VIDEO.md` a lenguaje llano, con frases que puedes decir casi tal cual frente a la cámara, sin necesitar dominar los detalles técnicos. Adapta el tono a tu manera de hablar — lo importante es que la idea quede clara.

---

## La idea general (memorizar esto, es la base de todo)

> "Construimos un sistema donde 5 roles de inteligencia artificial hacen una auditoría de seguridad, pero **ninguno tiene permiso para hacer más de lo que le corresponde**. El que revisa evidencia no puede escribir el reporte. El que verifica un hallazgo no puede darlo por válido él solo — eso lo tiene que confirmar una persona real, con su nombre y fecha. Y todo lo que pasa queda registrado en una bitácora con la hora exacta, para que se pueda comprobar que nada se inventó."

Esa es la frase que sostiene todo el video. Todo lo demás es mostrar evidencia de que eso es cierto.

---

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

## Si el docente pregunta algo que no sabes responder

Está bien decir, literalmente:

> "Esa parte específica la trabajamos apoyándonos en herramientas de asistencia técnica, pero puedo mostrarle exactamente dónde está documentada la decisión y por qué se tomó así" — y buscar la entrada correspondiente en `LEDGER.md` o `docs/tasks.md`. Ambos archivos tienen una entrada para cada decisión importante, citando el motivo.

No es necesario memorizar cada línea de código — el punto del sistema es justamente que las decisiones quedan documentadas, no que ustedes las memoricen todas.
