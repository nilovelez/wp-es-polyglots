# Propuestas para la guía de traductores y el glosario

Criterios de coherencia que han salido en las rondas de revisión y que no están (o no están igual) en la [Guía de traductores del equipo de WordPress España](https://es.wordpress.org/team/handbook/traducciones/guia/) ni en el glosario oficial de translate.wordpress.org. El revisor los propone al equipo para actualizar las guías generales, que son las que usa todo el mundo.

Mientras no se publiquen, se aplican desde `quick-reference.md` y `glossary-overrides.csv`. Cuando una propuesta se publique, se marca como publicada y su copia local se quita o se ajusta para que coincida con el texto oficial.

Documento para los moderadores: [Propuestas de cambio al glosario es_ES](https://claude.ai/artifact/8JUkHKheM5j3NHLAtywhcs).

Estados: **pendiente** (sin proponer) · **propuesta** (enviada al equipo) · **aprobada** · **publicada** · **descartada**.

## Glosario

| Término | Glosario actual | Propuesta | Origen | Estado |
|---|---|---|---|---|
| *meta title*, *meta description* | «meta title», «meta description» (no traducir) | «meta título», «meta descripción» | Ronda 11 (AI Blog Writer, #144, #145, #282, #285) | pendiente |
| *two-factor authentication* | *two-factor* = «dos pasos»; *authentication* = «identificación» (sin entrada para la expresión) | Añadir la expresión: «identificación en dos pasos»; la sigla 2FA se deja | Ronda 13 (ReportedIP Hive, unas 70 cadenas con «autenticación de dos factores») | pendiente |
| *whitelist* | Sin entrada | Sustantivo: «lista blanca». Verbo (*to whitelist*): «añadir a los admitidos»; *whitelisted*: «admitido» | Ronda 13 (ReportedIP Hive, 36 cadenas) | pendiente |
| *clear* | «vaciar» (verbo) | Añadir nota: para dejar de aplicar un filtro, «quitar» o «limpiar» (*Clear filters* = «Quitar filtros»); «vaciar» es para contenidos (papelera, caché) | Rondas 14 y 16 | pendiente |
| *media item* / *media file* | *media* = «medios» | Añadir: «archivo de medios» (no «archivo multimedia») | Ronda 07 (WP Branches for Post, #28, #70) | pendiente |
| *supported* | «compatible» | Añadir nota: cuando no habla de compatibilidad (p. ej., *supported conflict*, un conflicto que el plugin sabe resolver), se traduce por el sentido | Ronda 08 (#2) | pendiente |
| *endpoint* | «variable» | Revisar: «variable» solo vale para los *endpoints* de WooCommerce (el revisor); en «REST endpoints» o una API, «rutas» o se deja «endpoint» | Rondas 07 (#82), 13 y 20 | pendiente |
| *Dashboard*, *role* | «Escritorio», «perfil» | Añadir nota: son los nombres de WordPress. Los roles de un servicio externo usan el nombre de su interfaz en español («rol: Lector» en GA4); su *dashboard*, preferentemente «panel», aunque «escritorio» también vale | Rondas 10, 14, 15, 19 y 20 | pendiente |
| *recurring* | «periódico». Nota: «NO usar recurrente» | Cambiar la nota: se prefiere «periódico», pero «recurrente» también se acepta (no es motivo de rechazo) | Ronda 21 (Gratora, unas 125 cadenas) | pendiente |
| *scope* | «extensión» (cabecera de tabla) | Añadir acepción: «ámbito» para el alcance de un permiso o ajuste | Ronda 20 | pendiente |
| *zoom* (sustantivo) | Solo el verbo: «ampliar / acercar» | Añadir sustantivo: «ampliación» | Ronda 16 | pendiente |
| *page*, *endpoint* | Entradas duplicadas en el CSV | Dejar una de cada | Revisión del CSV | pendiente |
| A debatir (sin decisión) | *FAQ* en textos explicativos, *OK* como estado, *login* sustantivo, *sign out* en frases, *feed* que no es RSS, *vendor* de software, *merchant* en nombres de producto, *release* como paquete, *upsell*, *fee* de pasarela = «comisiones», *designation* = «destino», *fixed* = «fijo», *preset* = «predefinido» | Ver el documento de propuestas | Rondas 12 a 21 | pendiente |

## Guía de traductores

| Tema | Propuesta | Origen | Estado |
|---|---|---|---|
| Puntuación del original | Se mantiene la puntuación que puede romper algo: los puntos suspensivos finales tal como vienen y los signos de cierre al final. El guion largo «—» se puede sustituir por «:», «;» o «,», y no es motivo para cambiar una traducción. Las comillas pasan a «». | Rondas 04, 09, 10 y 20 | pendiente |
| Comillas en texto literal | Si toda la cadena es un texto literal para un buscador o un agente de IA (una instrucción, una consulta de ejemplo), se dejan las comillas del original, también las rectas. | Ronda 12 (#176) | pendiente |
| Numeración «#%d» | «Pedido #%d» se deja con «#», como en el original; no se cambia por «n.º %d». | Ronda 11 (6 cadenas) | pendiente |
| *email* en textos largos | En textos largos, «correo electrónico»; en cadenas cortas de interfaz, «correo» es válido. | Ronda 01 | pendiente |
| Interfaces de otros servicios | Cuando un texto cita la interfaz de otro servicio (Google, Cloudflare…), se usa el nombre que tiene en su versión en español; los términos del glosario como «Escritorio» o «perfil» son los de WordPress. | Rondas 19 y 20 | pendiente |
| Nombres de etiquetas HTML | Los nombres de etiquetas y atributos (*viewport*, *canonical*, *hreflang*, *og:url*) no se traducen cuando nombran la etiqueta. | Ronda 06 | pendiente |
| Variantes de idioma | *Chinese, Simplified* = «chino simplificado», *Chinese, Traditional* = «chino tradicional» (no «chino (China)» ni «chino (Taiwán)»). | Ronda 11 (#379, #380) | pendiente |
| Nombres de funciones de un plugin | Los nombres de funciones, planes y opciones de un plugin no son nombres propios: solo la primera palabra con mayúscula. | Ronda 02 | pendiente |
| Cuándo cambiar una cadena (revisión) | Solo se cambia lo que es un error; las formas preferidas («necesita», «No se ha podido…») se aplican solo si ya se cambia la cadena por otro motivo. | Rondas 01 y 03 | pendiente |
