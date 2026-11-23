# Guía de traducción de WordPress a español de España (es_ES)

Normas para traducir WordPress (núcleo, plugins y temas) al español de España.

Basada en la [Guía de traductores del equipo de WordPress España](https://es.wordpress.org/team/handbook/traducciones/guia/) y ampliada con criterios del equipo.

---

## 1. Fuentes y prioridad

Cuando dos fuentes entren en conflicto, prevalece la de mayor rango:

1. **Glosario oficial** ([translate.wordpress.org/locale/es/default/glossary](https://translate.wordpress.org/locale/es/default/glossary/)).
2. **Esta guía.**

Uso del glosario:

- Las notas del glosario («No usar…») y sus matices de contexto son obligatorios.
- Si una entrada ofrece varias opciones separadas por « / », elige según el contexto que indique su nota.
- Comprueba la categoría gramatical: el mismo término puede tener traducciones distintas como sustantivo y como verbo (*link* → «enlace» / «enlazar»).
- Si una entrada parece errónea, aplícala igualmente y coméntalo en #polyglots-es.

Las decisiones del equipo se debaten en el canal [#polyglots-es](https://wordpress.slack.com/archives/C0B936628M6) del Slack de Make WordPress.

---

## 2. Normas generales

- **No se traducen** los nombres de temas y plugins: «Contact Form 7», «Astra», «Jetpack», «WooCommerce».
  - El nombre se copia tal cual, aunque lleve palabras en inglés: «Bugalou for WooCommerce».
  - La parte descriptiva del título sí se traduce: «Bugalou – Live Chat, AI Chatbot & Customer Support Inbox» → «Bugalou – Chat en vivo, chatbot con IA y bandeja de atención al cliente».
- Los nombres de las pantallas, funciones, planes y opciones de un plugin no son nombres propios: se traducen, y con el término del glosario si lo tiene. *Builder* → «Maquetador», *Entries* → «Registros».
- **Productos de otras empresas:** se respeta la decisión de cada empresa. Usa el nombre oficial que la propia empresa emplea en español de España; unas traducen sus productos y otras no, y a veces solo algunos.
  - ✅ «Hojas de cálculo de Google» (nombre oficial en español) · «Search Console» (Google no lo traduce).
  - Si no sabes cómo lo llama la empresa en español, tradúcelo. Se deja el nombre original, u otro distinto, solo cuando se sabe que la empresa lo hace así: «Search Console». *Twilio Auth Token* → «token de identificación de Twilio».
  - Lo mismo con la interfaz de otros servicios: se usa el nombre que tiene en su versión en español («rol: Lector» en Google Analytics). «Escritorio» y «perfil» son los nombres de WordPress; el *dashboard* de un servicio externo, preferentemente «panel».
- Traducción **contextual, no literal**: «Page Management Documentation» → «Documentación de la gestión de páginas», no «Documentación gestión páginas».
- Si un término inglés es polisémico y en español no, usa la palabra española adecuada para cada contexto.
- Prioriza palabras españolas que expresen el concepto antes que anglicismos, salvo que el glosario indique que el término no se traduce.

---

## 3. Estilo

### 3.1 Tratamiento

- **Tuteo siempre.** Nunca «usted».
- Dirígete directamente al usuario cuando la frase lo permita.
- **Hablar a una empresa o a un servicio: «vosotros».** Si el texto se dirige a la empresa, la tienda o el servicio que está detrás de un plugin o un tema (preguntas frecuentes, formularios de contacto, soporte), lo natural es la segunda persona del plural: «¿Ofrecéis envoltorio para regalo?», «¿Qué métodos de pago aceptáis?», «¿Podéis ayudarme con la configuración?». Si la traducción usa «tú» («¿Ofreces…?»), no es motivo de rechazo, pero un «vosotros» correcto no se cambia.
- **La empresa habla al cliente: «tú» o una forma genérica, nunca «vosotros».** El cliente no forma parte de un grupo con la empresa: «Te ayudamos a configurar tu producto», «Las preguntas que más nos hacen», «Las preguntas que más recibimos». «Las preguntas que más nos hacéis» se corrige.

### 3.2 Voz de WordPress

- WordPress habla en **primera persona del singular**, como una persona.
  - ✅ «Lo siento, no he podido encontrar la página.»
  - ❌ «Lo sentimos, no se ha podido encontrar la página.»
- Si el original usa **«we» explícitamente** (p. ej., una empresa hablando de sí misma), se mantiene el plural: «No hemos podido conectar con nuestros servidores».

### 3.3 Lenguaje sencillo y directo

Escribe frases sencillas y directas. Evita las frases complejas, los rodeos y la pasiva que no hace falta, sobre todo si calca el inglés. La pasiva refleja vale cuando suena natural: «Se han guardado los cambios».

- *A license is required to perform this action*
  - ✅ «Necesitas una licencia para realizar esta acción.»
  - ❌ «Se requiere una licencia para poder realizar esta acción.»

### 3.4 Acciones: infinitivo o imperativo

Depende de quién propone la acción:

| Tipo | Forma | Ejemplos |
|---|---|---|
| Acción que **ejecuta el usuario** (botones, menús, comandos) | Infinitivo | «Publicar», «Guardar cambios», «Salir» |
| Acción que **se propone al usuario** (llamadas a la acción, invitaciones, recomendaciones) | Imperativo con tuteo | «Descarga WordPress», «Mejora a Premium», «Conecta tu cuenta a Google» |

Si no hay contexto suficiente (`msgctxt`, comentarios, referencias de archivo), usa infinitivo y anota la cadena como duda.

### 3.5 Mensajes de progreso

Gerundio: «Saving…» → «Guardando…».

### 3.6 Lenguaje inclusivo (preferencia, no norma)

- Si hay una alternativa neutra **natural**, evita la marca de género:
  - «Welcome to Astra» → «Te damos la bienvenida a Astra» (mejor que «Bienvenido a Astra»).
  - «Are you sure…?» → «¿Seguro que…?» (mejor que «¿Estás seguro…?»).
- Si la alternativa queda forzada, usa la forma habitual (masculino genérico). El masculino genérico no es un error.
- **Nunca** desdoblamientos («usuario/a», «los/las», @, x), salvo que sea imprescindible especificarlo.

### 3.7 Mayúsculas

- Solo en la primera palabra, aunque el inglés use mayúscula en cada palabra (*Title Case*).
  - ✅ «Subir archivo» · ❌ «Subir Archivo»
- Se usan mayúsculas cuando el texto se refiere a un elemento del sistema por su nombre, solo en la primera palabra: «ve a la pantalla Ajustes», «el Escritorio de WordPress». Si se habla de él de forma genérica, en minúscula: «ve a la pantalla de ajustes del plugin», «el kit de migración».
- Se mantienen las mayúsculas de nombres propios y productos.

### 3.8 Registros de cambios

El registro de cambios (*changelog*) es la lista de novedades y correcciones de cada versión de un plugin o un tema.

- Cada entrada, en participio: «Añadido…», «Corregido…», «Mejorado…». Todas las entradas del registro, con la misma forma.
- Los tipos de cambio, como dice el glosario: *Fix* = «Corrección», *Tweak* = «Retoque», *Feature* = «Característica».
- Los números de versión y las fechas se dejan como en el original.

---

## 4. Tipografía

- **Comillas:** siempre españolas «», y anidadas «… “…” …». Se convierten vengan como vengan en el original (`"…"`, `“…”`, `‘…’`).
  - Excepción: si toda la cadena es un texto literal para un buscador o un agente de IA (una instrucción, una consulta de ejemplo), se dejan las comillas del original, también las rectas. Un término citado dentro de una frase lleva «» como siempre: *Search for "WSMS"* → Busca «WSMS».
- **Signos de apertura:** siempre ¿ y ¡.
- **Resto de caracteres tipográficos:** se respetan como vengan en el original. Si el original trae `...`, se mantiene `...`; si trae `…`, se mantiene `…`.
- **Puntuación del final:** los puntos suspensivos, los dos puntos y los signos de cierre del final de la cadena se dejan como en el original. El guion largo «—» se puede cambiar por «:», «;» o «,».
- **Números con «#»:** «Pedido #%d» se deja con «#», como en el original; no se cambia por «n.º %d».
- Coma tras «Por favor» cuando va seguido de la petición: «Por favor, inténtalo de nuevo».
- **Abreviaturas:** «p. ej.», no «ej.».

---

## 5. Requisitos técnicos del formato .po

- No modifiques `msgid`, `msgid_plural`, `msgctxt`, comentarios (`#.`, `#:`, `#,`) ni la cabecera, salvo los campos de traducción.
- **Placeholders:** conserva todos, sin alterarlos: `%s`, `%d`, `%1$s`, `%2$d`, `{name}`, `%%`. En los numerados puedes cambiar el orden en la frase, pero no el número.
- **Código:** no se traducen los shortcodes, los hooks, las funciones, las clases, las variables ni los nombres de archivo: `[embed]`, `wp_head`, `get_option()`, `$post_id`, `wp-config.php`.
- **HTML:** conserva etiquetas y atributos. Traduce solo el texto visible y los atributos legibles (`title`, `alt`) si procede. No traduzcas URL salvo que exista una versión localizada oficial.
- **Nombres de etiquetas y atributos HTML** (*viewport*, *canonical*, *hreflang*, *og:url*): no se traducen cuando nombran la etiqueta: «la etiqueta viewport». La traducción del glosario («área visible») es para la interfaz.
- **Entidades y escapes:** conserva `&amp;`, `&nbsp;`, `\n`, `\"`, etc.
- **Espacios y saltos de línea** al inicio o al final: igual que en el original.
- **Longitud:** la traducción debe medir más o menos lo mismo que el original; en español suele ser algo más larga. Si mide 5 veces el original o más, o una quinta parte o menos, GlotPress la marca y probablemente rompe la interfaz: traduce de forma más concisa («Undo» = «Deshacer», no «Deshacer el último cambio»).
- **Plurales:** es_ES usa `nplurals=2; plural=(n != 1);`. Rellena siempre `msgstr[0]` (singular) y `msgstr[1]` (plural).
- **Formatos de fecha:** usa los equivalentes del glosario (p. ej. `F jS, Y` → `j \d\e F \d\e Y`).
