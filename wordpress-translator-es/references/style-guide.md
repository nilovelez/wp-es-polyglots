# Guía de traducción de WordPress a español de España (es_ES)

Instrucciones para traducir archivos `.po` de WordPress (núcleo, plugins y temas) y revisar traducciones pendientes (*waiting*) en GlotPress, siguiendo los criterios del equipo de WordPress España.

Basada en la [Guía de traductores del equipo de WordPress España](https://es.wordpress.org/team/handbook/traducciones/guia/) y ampliada con criterios del equipo para uso por agentes.

---

## 1. Fuentes y prioridad

Cuando dos fuentes entren en conflicto, prevalece la de mayor rango:

1. **Instrucciones explícitas del usuario**.
2. **Glosario** (`glossary.csv`).
3. **Esta guía.**

Uso del glosario:

- Columnas: `en, es, pos, description`. La columna `description` contiene usos prohibidos («No usar…») y matices de contexto que son obligatorios.
- Si una entrada ofrece varias opciones separadas por « / », elige según el contexto que indique `description`.
- Comprueba la categoría gramatical (`pos`): el mismo término puede tener traducciones distintas como sustantivo y como verbo (*link* → «enlace» / «enlazar»).
- Si una entrada parece errónea, aplícala igualmente y señálalo al terminar.

El glosario y esta guía son decisiones del equipo es_ES tomadas por consenso, no preferencias personales, y se aplican para que las traducciones sean coherentes. También se revisan: si una norma es incoherente, está desfasada o no encaja con lo que se traduce ahora, se señala para que el equipo la revise.

---

## 2. Normas generales

- **No se traducen** los nombres de temas y plugins: «Contact Form 7», «Astra», «Jetpack», «WooCommerce».
- **Productos de otras empresas:** se respeta la decisión de cada empresa. Usa el nombre oficial que la propia empresa emplea en español de España; unas traducen sus productos y otras no, y a veces solo algunos.
  - ✅ «Hojas de cálculo de Google» (nombre oficial en español) · «Search Console» (Google no lo traduce).
  - Comprueba el nombre en la web o la interfaz oficial en español de la empresa. Si no puedes verificarlo, deja el nombre original y márcalo como duda.
- Traducción **contextual, no literal**: «Page Management Documentation» → «Documentación de la gestión de páginas», no «Documentación gestión páginas».
- Si un término inglés es polisémico y en español no, usa la palabra española adecuada para cada contexto.
- Prioriza palabras españolas que expresen el concepto antes que anglicismos, salvo que el glosario indique que el término no se traduce.

### Casos concretos

- Tuteo; WordPress habla en primera persona del singular; infinitivo para acciones del usuario, imperativo para propuestas.
- **website = «sitio web»; site = «sitio»** (glosario). No quitar «sitio web» cuando el original dice *website*.
- **Se mantiene la puntuación del original que puede romper algo**: los puntos suspensivos finales tal como vienen (sin cambiar el carácter «…» por tres puntos ni al revés, para que no salte una línea distinta), y los dos puntos y signos de cierre al final de la cadena. El guion largo «—» se puede sustituir por «:», «;» o «,»: al traducir se puede mantener, pero no es motivo para cambiar una traducción. Las comillas son la excepción (siguiente punto). Si toda la cadena va entre comillas en el original (p. ej., un texto de ejemplo o una instrucción para una IA), las comillas se mantienen: forman parte del texto. Si toda la cadena es un texto literal para un buscador o un agente de IA (una instrucción, una consulta de ejemplo), se dejan las comillas del original, también las rectas. Un término citado dentro de una frase lleva «» como siempre: *Search for "WSMS"* → Busca «WSMS».
- Comillas «» siempre (también en lugar de `"…"` y `'…'`); «p. ej.», no «ej.».
- Mayúscula solo en la primera palabra; los nombres comunes (idiomas, planes, pestañas) en minúscula dentro de listas. Los nombres de funciones, planes, opciones y servicios de un plugin **no son nombres propios**: «nube de traducción», «plan gratuito», «exclusiones de traducción», «bandera + nombre», «Directorio de plugins». Las mayúsculas de *Title Case* en mitad de frase se corrigen. Solo conservan mayúscula las marcas y los productos («WGRank Translate», «Search Console»). Una función del plugin descrita en el texto va en minúscula aunque el traductor la escribiera con mayúscula («el kit de migración», «la nube de traducción»); el nombre de un menú, una pantalla o una pestaña citado como tal se escribe como aparece en la interfaz («en Ajustes > Generales», «la pestaña Herramientas»).
- Elementos de la interfaz citados (pestañas, botones, menús): se usa el nombre que ve el usuario en español, sin dejar el inglés con la traducción entre paréntesis. *Renamed "Cache" tab to "Translations"* → «Se renombró la pestaña «Caché» a «Traducciones»»; *a direct 'Settings' action link* → «un enlace de acción directo a Ajustes».
- Sinónimos frente al glosario: si el glosario da un término, se usa ese aunque el sinónimo se entienda. *supported* = «compatible» (no «admitido»), *default* = «por defecto» (no «predeterminado»), *Dashboard* = «escritorio» (no «panel»), *Feature* en registros de cambios = «Característica» (no «Función»), *monitor* = «supervisar» (no «monitorizar»).
- Registros de cambios: al traducir, una sola forma verbal en todas las entradas (participio: «Añadido», «Corregido»); *Fix* = Corrección, *Tweak* = Retoque, *Feature* = Característica. Al revisar, una entrada con otra forma verbal no es motivo de cambio si el sentido es correcto.
- *admin* / *administrator*: «administrador» es la persona o el perfil; «administración» es el área de administración. *Administrator request* = «solicitudes del administrador», no «solicitudes de administración».
- **Interfaces de otros servicios**: «Escritorio» y «perfil» son los nombres de WordPress. Si el texto cita la interfaz de otro servicio (Google Analytics, Cloudflare…), se usa el nombre que tiene ese servicio en su versión en español (p. ej., «rol: Lector»). El *dashboard* de un servicio externo se traduce preferentemente como «panel», pero «escritorio» también vale: no es motivo para cambiar una traducción.
- *host name* / *hostname* = «nombre de host», no «nombre de servidor».
- Nombres de etiquetas y atributos HTML (*viewport*, *canonical*, *hreflang*, *og:url*) no se traducen cuando nombran la etiqueta: «la etiqueta viewport», «la metaetiqueta viewport». La traducción del glosario («área visible») es para la interfaz del usuario final.
- **«#%d» se deja como en el original** («Pedido #%d», «Tarea #%d»): no se cambia por «n.º %d», que no hace falta, puede ser incorrecto y se lee peor. Si el traductor puso «n.º», se corrige a «#».
- *meta title* = «meta título», *meta description* = «meta descripción» (dos palabras).
- Nombres de idiomas con variante: *Chinese, Simplified* = «chino simplificado», *Chinese, Traditional* = «chino tradicional» (no «chino (China)» ni «chino (Taiwán)»). Se traduce la variante que dice el original.
- **Anglicismos:** se evitan cuando hay término en español, también en textos técnicos de seguridad. *authentication* = «identificación» (no «autenticación»), *authenticate* = «identificar», *two-factor authentication* / *2FA* = «identificación en dos pasos» (no «autenticación de dos factores»; la sigla 2FA se deja).
- *whitelist* como sustantivo = «lista blanca»; *to whitelist* (verbo) = «añadir a los admitidos»; *whitelisted* = «admitido» («IP admitidas»). *blacklist* = «lista negra».
- *badge*: «insignia» (glosario) encaja sobre todo en productos (el cartelito de «en oferta»). Para el globo con un contador junto a un elemento del menú, «distintivo» y otras opciones razonables también son válidas: se aprueba.
- Los términos del glosario que el traductor deja en inglés (*checkout*, *slider*, *hook*, *frontend*, *sitemap*, *firewall*) son error.
- El masculino genérico no es motivo de rechazo. Cambios mínimos de estilo: se aprueba. Tilde o coma tras «Por favor,»: se corrige y se publica.

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
| Acción que **se propone al usuario** (llamadas a la acción, invitaciones, recomendaciones) | Imperativo con tuteo | «Descarga WordPress», «Mejora a Premium», «Conecta tu cuenta a Google» |

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

## 6. Revisión

Emite un veredicto para cada cadena:

| Situación | Acción |
|---|---|
| Correcta, o solo difiere en matices mínimos de estilo respecto a otra opción válida | **Aprobar** |
| Errores menores: tilde, coma tras «Por favor», comillas no españolas, mayúscula sobrante | **Corregir y aprobar** |
| Incumple el glosario, el tuteo, la voz de WordPress, rompe placeholders/HTML, cambia el sentido o es claramente poco natural | **Rechazar** con comentario |
| No hay contexto suficiente para decidir | **Dudosa**: mejor propuesta y una pregunta concreta |

**Consistencia:** la misma cadena o fórmula debe traducirse igual en todo el proyecto. Las traducciones ya aprobadas no son referencia: aprobada no quiere decir correcta.

**El masculino genérico no es motivo de rechazo.** Como mucho, se sugiere la alternativa neutra si es natural.

**Comentarios de rechazo:**

- Breves, amables y en tuteo, dirigidos al traductor.
- Citan el motivo concreto (término del glosario, regla o error).
- Incluyen la traducción propuesta.

> Ejemplo: Según el glosario, «dashboard» se traduce como «escritorio». Propuesta: «Ir al escritorio».

### Cuándo cambiar una cadena

- **Solo se cambia lo que es un error.** Si la traducción es suficientemente buena, se aprueba aunque exista otra opción más correcta. Ejemplos de «suficientemente bueno»: «Eliminado» en lugar de «Quitado» para *Remove*; una entrada de un registro de cambios en presente («permanece visible») cuando las demás van en participio; «requiere PHP %s» en lugar de «necesita PHP %s»; «No se pudo…» o «no pudo guardarse» en lugar de «No se ha podido…». En los registros de cambios, aún más tolerancia.
- Más casos de «suficientemente bueno», que no se cambian: *remove* traducido como «eliminar» o «borrar» cuando de verdad se borra algo; *toggle* como «interruptor» (el glosario da «conmutador», que es más general, pero «interruptor» no es incorrecto para algo que se enciende y se apaga); «Sorry» omitido al principio de un mensaje de error; *issue* como «fallo»; un aviso destacado *WARNING!* como «¡ATENCIÓN!».
- **Sinónimos sistemáticos.** Muchos traductores usan siempre el mismo sinónimo en lugar del término del glosario («notificación» por *notification*, «complemento» por *add-on*, «predeterminado» por *default*, «eliminar» por *delete*, «definir» o «poner» por *set*, «saltar» por *skip*, «vincular» por *link*, «revisar» por *check*). Eso sí es error: se corrige en todas las cadenas donde aparece, también en verbos pequeños, y ajustando el género y la concordancia («la notificación enviada» → «el aviso enviado»; «el complemento» → «la extensión»).
- **Formas preferidas, solo si ya cambias la cadena por otro motivo:** «necesita» mejor que «requiere»; «No se ha podido…» (pretérito perfecto, como el núcleo) mejor que «No se pudo…». No se cambia una cadena solo por esto.
- Sí se cambia: incumplimientos del glosario, cambio de sentido (p. ej. «Añadido» cuando el original dice *Show*), preposición equivocada («Compatibilidad del correo» por *Email compatibility* → «Compatibilidad con el correo electrónico»), tipografía (comillas, «p. ej.», coma tras «Por favor,»), términos del glosario dejados en inglés.
- **email = «correo electrónico».** En textos largos (descripciones, párrafos, preguntas frecuentes) «correo» a secas se corrige a «correo electrónico», también en «dirección de correo electrónico» y «correos electrónicos enviados». En cadenas cortas de interfaz (botones, etiquetas, menús, títulos breves) «correo» es válido para mantener una longitud parecida al original: se aprueba.
