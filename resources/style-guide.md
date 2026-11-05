# Guía de traducción de WordPress a español de España (es_ES) para agentes

Instrucciones para traducir archivos `.po` de WordPress (núcleo, plugins y temas) y revisar traducciones pendientes (*waiting*) en GlotPress, siguiendo los criterios del equipo de WordPress España.

Basada en la [Guía de traductores del equipo de WordPress España](https://es.wordpress.org/team/handbook/traducciones/guia/) y ampliada con criterios del equipo para uso por agentes.

---

## 1. Fuentes y prioridad

Cuando dos fuentes entren en conflicto, prevalece la de mayor rango:

1. **Instrucciones explícitas del revisor humano** en la sesión de trabajo.
2. **Glosario oficial** (`glossary.csv`, exportado de [translate.wordpress.org/locale/es/default/glossary](https://translate.wordpress.org/locale/es/default/glossary/)).
3. **Esta guía.**
4. **Memoria de traducción** (`resources/translation-memory.csv`): referencia de consistencia para frases completas.

Uso del glosario:

- Columnas: `en, es, pos, description`. La columna `description` contiene usos prohibidos («No usar…») y matices de contexto que son obligatorios.
- Si una entrada ofrece varias opciones separadas por « / », elige según el contexto que indique `description`.
- Comprueba la categoría gramatical (`pos`): el mismo término puede tener traducciones distintas como sustantivo y como verbo (*link* → «enlace» / «enlazar»).
- Si una entrada parece errónea (ver sección 9), aplica el criterio correcto y señálalo en el informe.

---

## 2. Normas generales

- **No se traducen** los nombres de temas y plugins: «Contact Form 7», «Astra», «Jetpack», «WooCommerce».
- **Productos de otras empresas:** se respeta la decisión de cada empresa. Usa el nombre oficial que la propia empresa emplea en español de España; unas traducen sus productos y otras no, y a veces solo algunos.
  - ✅ «Hojas de cálculo de Google» (nombre oficial en español) · «Search Console» (Google no lo traduce).
  - Comprueba el nombre en la web o la interfaz oficial en español de la empresa. Si no puedes verificarlo, deja el nombre original y anótalo como duda en el informe.
- Traducción **contextual, no literal**: «Page Management Documentation» → «Documentación de la gestión de páginas», no «Documentación gestión páginas».
- Si un término inglés es polisémico y en español no, usa la palabra española adecuada para cada contexto.
- Prioriza palabras españolas que expresen el concepto antes que anglicismos, salvo que el glosario indique que el término no se traduce.

---

## 3. Estilo

### 3.1 Tratamiento

- **Tuteo siempre.** Nunca «usted».
- Dirígete directamente al usuario cuando la frase lo permita.

### 3.2 Voz de WordPress

- WordPress habla en **primera persona del singular**, como una persona.
  - ✅ «Lo siento, no he podido encontrar la página.»
  - ❌ «Lo sentimos, no se ha podido encontrar la página.»
- Si el original usa **«we» explícitamente** (p. ej., una empresa hablando de sí misma), se mantiene el plural: «No hemos podido conectar con nuestros servidores».

### 3.3 Naturalidad

Las traducciones deben ser legibles y naturales. Evita la pasiva refleja y las construcciones impersonales calcadas del inglés.

- *A license is required to perform this action*
  - ✅ «Necesitas una licencia para realizar esta acción.»
  - ❌ «Se requiere una licencia para poder realizar esta acción.»

### 3.4 Acciones: infinitivo o imperativo

Depende de quién propone la acción:

| Tipo | Forma | Ejemplos |
|---|---|---|
| Acción que **ejecuta el usuario** (botones, menús, comandos) | Infinitivo | «Publicar», «Guardar cambios», «Salir» |
| Acción que **se propone al usuario** (llamadas a la acción, invitaciones, recomendaciones) | Imperativo con tuteo | «Descarga WordPress», «Actualiza a Premium», «Conecta tu cuenta a Google» |

Si no hay contexto suficiente (`msgctxt`, comentarios, referencias de archivo), usa infinitivo y anota la cadena como duda.

### 3.5 Mensajes de progreso

Gerundio: «Saving…» → «Guardando…».

### 3.6 Lenguaje inclusivo (preferencia, no norma)

- Si hay una alternativa neutra **natural**, evita la marca de género:
  - «Welcome to Astra» → «Te damos la bienvenida a Astra» (mejor que «Bienvenido a Astra»).
  - «Are you sure…?» → «¿Seguro que…?» (mejor que «¿Estás seguro…?»).
- Si la alternativa queda forzada, usa la forma habitual (masculino genérico).
- **Nunca** desdoblamientos («usuario/a», «los/las», @, x), salvo que sea imprescindible especificarlo.

### 3.7 Mayúsculas

- Solo en la primera palabra, aunque el inglés use mayúscula en cada palabra (*Title Case*).
  - ✅ «Subir archivo» · ❌ «Subir Archivo»
- Se mantienen las mayúsculas de nombres propios y productos.

---

## 4. Tipografía

- **Comillas:** siempre españolas «», y anidadas «… “…” …». Se convierten vengan como vengan en el original (`"…"`, `“…”`, `‘…’`).
- **Signos de apertura:** siempre ¿ y ¡.
- **Resto de caracteres tipográficos:** se respetan como vengan en el original. Si el original trae `...`, se mantiene `...`; si trae `…`, se mantiene `…`.
- Coma tras «Por favor» cuando va seguido de la petición: «Por favor, inténtalo de nuevo».

---

## 5. Requisitos técnicos del formato .po

- No modifiques `msgid`, `msgid_plural`, `msgctxt`, comentarios (`#.`, `#:`, `#,`) ni la cabecera, salvo los campos de traducción.
- **Placeholders:** conserva todos, sin alterarlos: `%s`, `%d`, `%1$s`, `%2$d`, `{name}`, `%%`. En los numerados puedes cambiar el orden en la frase, pero no el número.
- **HTML:** conserva etiquetas y atributos. Traduce solo el texto visible y los atributos legibles (`title`, `alt`) si procede. No traduzcas URL salvo que exista una versión localizada oficial.
- **Entidades y escapes:** conserva `&amp;`, `&nbsp;`, `\n`, `\"`, etc.
- **Espacios y saltos de línea** al inicio o al final: igual que en el original.
- **Plurales:** es_ES usa `nplurals=2; plural=(n != 1);`. Rellena siempre `msgstr[0]` (singular) y `msgstr[1]` (plural).
- **Formatos de fecha:** usa los equivalentes del glosario (p. ej. `F jS, Y` → `j \d\e F \d\e Y`).
- Valida el archivo final (p. ej. `msgfmt --check`) y verifica que el número de placeholders coincide en cada cadena.

---

## 6. Modo traducción

1. Traduce las cadenas vacías y las marcadas como *fuzzy*. No modifiques las ya traducidas salvo petición expresa.
2. Antes de cada cadena, consulta el glosario y la memoria de traducción (coincidencias exactas y parecidas).
3. **Traduce todas las cadenas**, sin dejar huecos ni pausar el trabajo por dudas.
4. Al terminar, presenta las dudas agrupadas: cadena original, contexto, traducción aplicada, alternativa y pregunta concreta.
5. Aplica las respuestas del revisor antes de entregar el archivo final. No es necesario marcar las dudas como *fuzzy*.
6. Si una respuesta establece un criterio general, añádelo a las reglas o a la memoria de traducción.

**Informe de entrega:**

- Dudas resueltas y criterio aplicado.
- Términos no incluidos en el glosario y traducción elegida.
- Conflictos detectados entre el glosario y el contexto.

---

## 7. Modo revisión (cadenas *waiting*)

Emite un veredicto para cada cadena:

| Situación | Acción |
|---|---|
| Correcta, o solo difiere en matices mínimos de estilo respecto a otra opción válida | **Aprobar** |
| Errores menores: tilde, coma tras «Por favor», comillas no españolas, mayúscula sobrante | **Corregir y aprobar** |
| Incumple el glosario, el tuteo, la voz de WordPress, rompe placeholders/HTML, cambia el sentido, es claramente poco natural o inconsistente con la memoria de traducción | **Rechazar** con comentario |
| No hay contexto suficiente para decidir | **Dudosa**: se pregunta al revisor al terminar |

**Consistencia:** la misma cadena o fórmula debe traducirse igual en todo el proyecto. Contrasta con la memoria de traducción y con las traducciones ya aprobadas del proyecto, si están disponibles.

**El masculino genérico no es motivo de rechazo.** Como mucho, se sugiere la alternativa neutra si es natural.

**Comentarios de rechazo:**

- Breves, amables y en tuteo, dirigidos al traductor.
- Citan el motivo concreto (término del glosario, regla o error).
- Incluyen la traducción propuesta.

> Ejemplo: Según el glosario, «dashboard» se traduce como «escritorio». Propuesta: «Ir al escritorio».

**Salida:** tabla con `original`, `traducción sugerida`, `veredicto`, `traducción final` (si se corrige) y `comentario`.

---

## 8. Memoria de traducción

Archivo `resources/translation-memory.csv` con frases completas ya fijadas.

| Columna | Contenido |
|---|---|
| `en` | Cadena original |
| `es` | Traducción aprobada |
| `contexto` | `msgctxt` o descripción breve, si aplica |
| `origen` | Proyecto de procedencia (núcleo de WordPress, WooCommerce, Astra…) |
| `notas` | Opcional: motivo o decisión |

- **Glosario** = términos sueltos. **Memoria de traducción** = frases completas.
- Coincidencia exacta → se reutiliza. Coincidencia parecida → sirve de modelo.
- Solo se añaden cadenas confirmadas o corregidas por un revisor humano.

---

## 9. Pendientes

Posibles erratas en el glosario, en revisión:

- *QuickPress* → «ublicación rápida» (falta la P).
- *deprecate* → «descarta» (el infinitivo sería «descartar»).
- *expire* / *expires* → «caduca», con categoría gramatical incorrecta.
- *expanse* → «expandir» (probablemente *expand*).
- *troubleshooting* → «diagnosticar» como verbo (sería el sustantivo «diagnóstico»).
- Entradas duplicadas: *endpoint*, *page*.

Ante la duda: pregunta al revisor humano. Las decisiones del equipo se debaten en el canal [#polyglots-es](https://wordpress.slack.com/archives/C0B936628M6) del Slack de Make WordPress.
