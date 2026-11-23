# Referencia rápida de criterios es_ES

Resumen de los criterios aprendidos en las rondas de revisión. El detalle está en `style-guide.md`, `moderation-guide.md` y `../polyglots/calibration-log.md`.

El glosario, la guía de estilo y estos criterios son decisiones del equipo es_ES tomadas por consenso, no preferencias personales, y se aplican para que las traducciones sean coherentes. También se revisan: si una norma es incoherente, está desfasada o no encaja con lo que se traduce ahora, se señala para que el equipo la revise.

Prioridad si hay conflicto: instrucciones del revisor → glosario → guía.

## Criterios de traducción

- Tuteo; WordPress habla en primera persona del singular; infinitivo para acciones del usuario, imperativo para propuestas.
- **website = «sitio web»; site = «sitio»** (glosario). No quitar «sitio web» cuando el original dice *website*.
- **email = «correo electrónico».** En textos largos (descripciones, párrafos, preguntas frecuentes) «correo» a secas se corrige a «correo electrónico», también en «dirección de correo electrónico» y «correos electrónicos enviados». En cadenas cortas de interfaz (botones, etiquetas, menús, títulos breves) «correo» es válido para mantener una longitud parecida al original: se aprueba.
- Comillas «» siempre (también en lugar de `"…"` y `'…'`); «p. ej.», no «ej.».
- Mayúscula solo en la primera palabra; los nombres comunes (idiomas, planes, pestañas) en minúscula dentro de listas. Los nombres de funciones, planes, opciones y servicios de un plugin **no son nombres propios**: «nube de traducción», «plan gratuito», «exclusiones de traducción», «bandera + nombre», «Directorio de plugins». Las mayúsculas de *Title Case* en mitad de frase se corrigen. Solo conservan mayúscula las marcas y los productos («WGRank Translate», «Search Console»). Una función del plugin descrita en el texto va en minúscula aunque el traductor la escribiera con mayúscula («el kit de migración», «la nube de traducción»).
- Sinónimos frente al glosario: si el glosario da un término, se usa ese aunque el sinónimo se entienda. *supported* = «compatible» (no «admitido»), *default* = «por defecto» (no «predeterminado»), *Dashboard* = «escritorio» (no «panel»), *Feature* en registros de cambios = «Característica» (no «Función»), *monitor* = «supervisar» (no «monitorizar»).
- Registros de cambios: al traducir, una sola forma verbal en todas las entradas (participio: «Añadido», «Corregido»); *Fix* = Corrección, *Tweak* = Retoque, *Feature* = Característica. Al revisar, una entrada con otra forma verbal no es motivo de cambio si el sentido es correcto.
- *admin* / *administrator*: «administrador» es la persona o el perfil; «administración» es el área de administración. *Administrator request* = «solicitudes del administrador», no «solicitudes de administración».
- *meta title* = «meta título», *meta description* = «meta descripción» (dos palabras), aunque el glosario oficial diga que no se traducen. Está en `glossary-overrides.csv`, que manda sobre `glossary.csv`.
- Nombres de idiomas con variante: *Chinese, Simplified* = «chino simplificado», *Chinese, Traditional* = «chino tradicional» (no «chino (China)» ni «chino (Taiwán)»). Se traduce la variante que dice el original.
- **Anglicismos:** se evitan cuando hay término en español, también en textos técnicos de seguridad. *authentication* = «identificación» (no «autenticación»), *authenticate* = «identificar», *two-factor authentication* / *2FA* = «identificación en dos pasos» (no «autenticación de dos factores»; la sigla 2FA se deja).
- *whitelist* como sustantivo = «lista blanca»; *to whitelist* (verbo) = «añadir a los admitidos»; *whitelisted* = «admitido» («IP admitidas»). *blacklist* = «lista negra».
- *badge*: «insignia» (glosario) encaja sobre todo en productos (el cartelito de «en oferta»). Para el globo con un contador junto a un elemento del menú, «distintivo» y otras opciones razonables también son válidas: se aprueba.
- Los términos del glosario que el traductor deja en inglés (*checkout*, *slider*, *hook*, *frontend*, *sitemap*, *firewall*) son error.
- El masculino genérico no es motivo de rechazo. Cambios mínimos de estilo: se aprueba. Tilde o coma tras «Por favor,»: se corrige y se publica.
- Fallos habituales de la herramienta: marca *fuzzy* cadenas correctas, pone «Escritorio» con mayúscula en mitad de frase, normaliza entradas sueltas del registro de cambios, aplica *core* → «núcleo» donde no toca.
