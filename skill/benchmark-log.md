# Registro de pruebas de la skill

Una entrada por prueba: modelo, ronda, resultado frente al `corrected.po` aprobado por Nilo, causas de los fallos y cambios hechos en la skill. Se compara con `python3 skill/scripts/po_tool.py compare <referencia> <candidato>`.

Aviso: `resources/quick-reference.md` incluye criterios aprendidos en las rondas 01 y 02, así que estas pruebas no son del todo ciegas.

## 2026-11-05 · Sonnet · ronda 01 (MailBridgeAPI, readme, 72 cadenas) · skill v1

- Referencia: 26 cambios. Sonnet: 11 cambios + 1 duda. Coinciden 9 (3 de ellas con diferencias menores).
- **Fallos (17):**
  - ~13 por dejar «correo» en lugar de «correo electrónico» en textos largos. El glosario solo prohíbe «email» y «correo e».
  - 2 «solicitudes de administración» por *administrator request*.
  - 1 «nombres de servidor» por *host names*.
  - 1 preposición: «Compatibilidad del correo».
  - 1 de estilo («se admiten» → «son compatibles»), que no es regla.
- **Cambios de más (2):** «Quitado» por «Eliminado» (#70) y participio en una entrada del registro de cambios (#59). Según Nilo, su propuesta es más correcta, pero la original es suficientemente buena: no se cambia, y menos en un registro de cambios.
- **Duda (#62):** *badge*, «distintivo» frente a «insignia». Nilo: las dos valen. «Insignia» es más de producto y aquí es el globo del contador del menú, así que se aprueba.
- **Cambios en la skill:**
  - Nuevo apartado «Cuándo cambiar una cadena» en la referencia rápida (solo errores; «correo» solo se corrige en textos largos).
  - Criterios de *admin* y *host name*.
  - En SKILL.md, revisión del sentido frase a frase.

## 2026-11-05 · Sonnet · ronda 02 (WGRank, readme, 161 cadenas) · skill v2

- Referencia: 50 cambios. Sonnet: 42 cambios. Coinciden 39: 27 idénticos y 12 con diferencias menores de redacción.
- **Fallos (11):**
  - Sinónimos frente al glosario: «admitidos» (*supported* = «compatible», 2), «predeterminado» (*default* = «por defecto», 2), «Función» (*Feature* = «Característica», 1), «panel» (*Dashboard* = «escritorio», dentro de una diferencia).
  - Mayúsculas de *Title Case* en nombres de funciones y opciones: «Nube de Traducción», «Bandera + Nombre», «Exclusiones de traducción», «Directorio de Plugins» (4 fallos + 2 diferencias).
  - *sitemap* en inglés en #158 (sí lo vio en #96).
  - «Configuración de ajustes» redundante (#93).
- **Diferencias:** en #127 y #144 dejó los nombres de pestaña en inglés con la traducción entre paréntesis («Cache», «Settings» (Ajustes)); la referencia los traduce.
- **Cambios de más (3), coherentes con las reglas:** comillas en #48, «p. ej.» en #79 y mayúsculas en #156. En #137 corrigió la concordancia («estructuras… personalizadas»), que la referencia dejó en masculino.
- **Cambios en la skill:**
  - Nuevo `po_tool.py lint` con pistas automáticas: término del glosario ausente o en inglés, mayúsculas en mitad de frase, «ej.» y comillas rectas. Sobre el `original.po` marca 45 de los 50 cambios de la ronda 02 y 20 de los 26 de la ronda 01. SKILL.md obliga a revisar cada pista.
  - En la referencia rápida: mayúsculas en nombres de funciones, elementos de la interfaz citados y sinónimos frente al glosario.

## 2026-11-05 · Sonnet · ronda 03 (Webandroll OrderFlow, dev, 356 cadenas) · skill v3 · primera ronda real

- Flujo completo con Poedit: `review.po` → Nilo revisa las 356 cadenas → `finalize`.
- Resultado: 46 cambios. Sonnet propuso 45 cambios y 1 duda.
  - Mantenidos: 44.
  - Editado por Nilo: 1 (#355, «No se pudo» → «No se ha podido», aprovechando que ya se cambiaba).
  - Deshechos: 0. Se le escaparon: 0.
  - La duda (#234, icono «Check» → «Marca de verificación») se aceptó.
- Propuestas principales:
  - *delete* → «borrar» (unas 25).
  - «Lo sentimos» → «Lo siento».
  - Del glosario: *notification* → «aviso», *role* → «perfil», *stock* → «inventario», *placeholder* → «marcador de posición», *header* → «cabecera», *default* → «por defecto».
  - Texto añadido por el traductor en la descripción del plugin.
- Feedback de Nilo: hay pequeñas desviaciones que no son motivo de rechazo. «requiere» es mejorable («necesita») y «No se pudo» también («No se ha podido»), pero no se cambian solo por eso.
- **Cambios en la skill:** formas preferidas solo cuando ya se cambia la cadena.

## 2026-11-06 · Sonnet · ronda 04 (BetterDocs, stable, 164 cadenas) · skill v3

- Traducciones hechas por otro usuario con su propia skill de traducción: aplica bien el glosario (`lint` solo marcó 12 cadenas).
- Resultado: 8 cambios, los 8 propuestos por Sonnet y aceptados. Ni deshechos ni escapados.
- Cambios:
  - Puntos suspensivos `...` respetados como en el original (3).
  - Términos que no se traducen: *FAQ Schema* → «Schema de FAQ».
  - *masonry* → «mosaico», *modal* → «emergente», «Lo sentimos» → «Lo siento».
  - «FAQs» → «FAQ».
- **Cambios en la skill:** `lint` avisa también cuando se traduce un término que el glosario marca como «no se traduce».

## 2026-11-06 · ronda 05 (torlann, stable, 3053 cadenas) · descartada

- Lote para rechazar entero: traducción automática sin coherencia, con alucinaciones, sin glosario ni guía y con muchas cadenas copiadas en inglés. Lo decidió Nilo mirando los originales.
- Sonnet la revisó con diez subagentes en paralelo y se gastó casi toda la cuota diaria. Lección: en rondas grandes, primero las cifras baratas (`lint`, cadenas iguales al inglés) y la decisión de Nilo. Nunca subagentes en paralelo con el mismo modelo.
- Se borraron sus archivos para que no se reutilice por accidente.

## 2026-11-06 · Haiku · ronda 06 (Effortless Website Health Check, dev, 300 cadenas) · skill v3 · primera ronda real con Haiku

- Resultado: 78 cambios. Haiku propuso 78 cambios y 2 dudas: Nilo mantuvo los 78. Ni editados, ni deshechos, ni escapados.
- Problema principal del traductor: tratamiento de usted en todo el plugin («Añada», «considere», «su empresa») sin escribir nunca «usted». La cuenta de «usted» y `lint` no lo detectan. Es una señal que falta para detectar lotes malos.
- Dudas: *viewport* como nombre de etiqueta HTML. Nilo lo dejó en inglés, y queda anotado en la referencia rápida.
- Incidencia: `review-po` rompía el `.po` cuando la traducción original tenía saltos de línea (Poedit: *keyword unknown*). Corregido.

## 2026-11-06 · Haiku · ronda 07 (WP Branches for Post, readme, 106 cadenas) · skill v3

- Resultado: 20 cambios. Haiku propuso 18 cambios y 2 dudas. Mantenidos: 17. Editado: 1. Ni deshechos ni escapados.
- Rechazos casi todos por el glosario: *delete* = «borrar», *legacy* = «heredado», *warning* = «advertencia», *capability* = «capacidad», *shortcut* = «atajo», *supported* = «compatible», *clear* = «vaciar», *rollback* = «retroceso». Nilo los mantuvo todos, también los que parecían de matiz («aviso» → «advertencia», «permisos» → «capacidades»): el glosario manda.
- Además vio una frase que faltaba (#23) y un sentido incompleto (#87).
- Editado (#68): Nilo acortó la frase y quitó la lista de estados («siempre que esté publicado, sea privado…»).
- Dudas (#28, #70): *media item*. Nilo eligió «archivo de medios», según el glosario, y no «archivo multimedia». Queda en la referencia rápida.
- `lint`: 53 pistas, muchas de ellas ruido por *review* («revisión» editorial, no «reseña»). Haiku las descartó bien con la nota del encargo.
- Subida: el `corrected.po` de la ronda 06 fallaba con `ERR_FAILED` al subirlo desde la unidad `X:` (SMB), y funcionaba al copiarlo al disco local. Se arregló devolviendo `FileInfoCacheLifetime` a 10 en Windows (las cachés de directorios y de archivos no encontrados siguen a 0).

## 2026-11-06 · Haiku · ronda 08 (WP Branches for Post, stable, 66 cadenas) · skill v3

- Resultado: 6 cambios. Haiku propuso 5 cambios y 1 duda, y Nilo mantuvo todo. Ni editados, ni deshechos, ni escapados.
- Rechazos por coherencia con el readme aprobado en la ronda 07 (se le pasó como referencia): «estado de referencia», «Rama de la entrada», *snapshot* = «instantánea», *legacy* = «heredado», «entrada pública».
- Duda (#2): en *supported conflict*, «compatible» no encaja. Nilo aceptó «conflicto que se pueda resolver»: el glosario no se aplica cuando el término no tiene ese sentido.
- Incidencia: los comentarios para el traductor citaban «la ronda 07». Se reescribieron antes de pasarlos a Nilo, y SKILL.md ahora prohíbe citar rondas o archivos internos.

## 2026-11-06 · Haiku · ronda 09 (ifthenpay Payments for WPForms, stable, 118 cadenas) · skill v3

- Resultado: 29 cambios. Haiku propuso 28 cambios y 2 dudas: Nilo los mantuvo todos. Ni editados, ni deshechos, ni escapados. Según Nilo, era una traducción complicada y la hizo muy bien.
- Cambios principales: *Gateway Key* → «clave de pasarela» y *Backoffice Key* → «clave de Backoffice», que estaban en inglés (unas 15 cadenas, todas coherentes); *Payment Gateway* → «Pasarela de pago», también en el nombre del campo; del glosario, *default*, *entry* = «registro», *unable* y *required*.
- Guion largo (#28, #48): Haiku devolvió el «—» del inglés donde el traductor puso «;» o «:». Opus recomendó deshacerlo, por ser un anglicismo, y Nilo lo mantuvo: entra en la regla de mantener la puntuación del original, que ya está en la referencia rápida.
- Dudas: «Pay by Link» se queda en inglés, como nombre del producto de ifthenpay; *form builder* se queda «constructor de formularios», no «maquetador».

## 2026-11-06 · Haiku · ronda 10 (ifthenpay Payments for WPForms, readme, 66 cadenas) · skill v3

- Resultado: 28 cambios. Haiku propuso 28 cambios y ninguna duda, y Nilo los mantuvo todos. Ni editados, ni deshechos, ni escapados.
- Coherencia con la ronda 09, que se le pasó como referencia: «clave de pasarela», «clave de Backoffice», «Pasarela de pago», «registro».
- Del glosario: *addon* = «extensión», *merchant* = «vendedor», *notify* = «avisar», *authentication* = «identificación», *bug* = «fallo», *frontend* = «parte pública», *sandbox* = «entorno de pruebas», *modal* = «emergente», *release* = «versión». Aplicó también la regla nueva del guion largo (#7 y #11) y «correo electrónico» en textos largos.
- #49: Nilo aceptó «escritorio del vendedor» para el *dashboard* de un servicio externo (el Backoffice de ifthenpay). Es un dato para la pregunta abierta sobre el *Dashboard* externo.

## 2026-11-06 · Haiku · ronda 11 (AI Blog Writer, stable, 495 cadenas) · skill v3 · prueba de tamaño

- Una sola pasada secuencial con las 495 cadenas, sin subagentes.
- Resultado: 55 cambios. Haiku propuso 46 cambios y 2 dudas. Mantenidos: 37. Editados: 9. Deshechos: 0. Escapados: 8.
- **Tamaño:** no se ve cansancio. Las propuestas por cuartos son 8, 16, 14 y 10, y las pistas de `lint`, 37, 32, 32 y 29. Los fallos no se concentran al final y casi todos salen de criterios nuevos de Nilo, no de errores de atención. 495 cadenas de interfaz caben bien en una pasada.
- **Escapados (8):**
  - 6 por «n.º %d» en lugar de «#%d». Es un criterio nuevo de Nilo: se deja «#», como en el original. Ahora `lint` lo avisa.
  - 2 de idiomas: «chino (China)» y «chino (Taiwán)» por *Chinese, Simplified/Traditional*. Era un error de sentido que no vio.
- **Editados (9):**
  - 4 por *meta title* y *meta description*. Haiku siguió el glosario oficial (no se traducen), pero Nilo quiere «meta título» y «meta descripción». Se creó `resources/glossary-overrides.csv`, que manda sobre el glosario en `po_tool.py glossary` y `lint`.
  - El resto, retoques de Nilo: «Su perfil», «clave de API», «perfil del escritor», «Perfil #%d borrado», «— recuperado».
- `lint` con la entrada nueva del glosario detectó una errata en la revisión de Nilo («meta descrición»), que se corrigió antes de generar `corrected.po`.
- Dudas: *Supported* como estado → «Compatible» (aquí el glosario sí aplica). *OK* → «Correcto» se mantuvo.

## 2026-11-06 · Haiku · ronda 12 (Digital Targets GEO Score, stable, 905 cadenas) · skill v3 · prueba de tamaño

- Una sola pasada secuencial, sin subagentes. Haiku partió el trabajo por su cuenta en 6 tramos seguidos (`partNN.jsonl`).
- Resultado: 31 cambios. Haiku propuso 31 cambios y 1 duda. Mantenidos: 29. Editados: 2. Ni deshechos ni escapados. Nilo: «muy buena pinta», no encontró nada importante.
- **Tamaño:** propuestas por cuartos 3, 2, 11 y 16, frente a 45, 30, 47 y 89 pistas de `lint`. La primera mitad tenía pocas propuestas, pero Nilo no encontró nada escapado: el traductor era bueno. 905 cadenas de interfaz caben bien en una pasada.
- Editados:
  - #80: Nilo cambió «bloque FAQ» por «bloque de preguntas frecuentes» en un texto largo que explica qué es una página FAQ. No era importante y queda como candidato, no como regla.
  - #176: toda la cadena va entre comillas en el original (un texto de ejemplo). Haiku las quitó y Nilo las devolvió. Ahora está en la referencia rápida: se mantienen las comillas que forman parte del texto.
- Duda (#873): *scan* → «comprobar» se mantiene. «Analizar» y «explorar» también valen.

## 2026-11-06 · Haiku · ronda 13 (ReportedIP Hive, stable, 2287 cadenas) · skill v3 · prueba de tamaño

- Tres tramos seguidos (1-765, 766-1530, 1531-2287) en la misma sesión, sin subagentes, con `terms.md` para la coherencia. Las decisiones se añadían al terminar cada tramo.
- Primera pasada: 236 propuestas (89, 77 y 70 por tramo) y 1 duda. No se ve cansancio.
- **Incoherencia entre tramos:** `terms.md` decía *authentication* = «identificación», pero solo se aplicó en 2 cadenas, y quedaron 38 con «autenticación» y 31 con «dos factores». La detecté (Opus) antes de pasar el archivo a Nilo, que decidió:
  - Glosario: «identificación en dos pasos». Se evitan los anglicismos.
  - *whitelist* como sustantivo = «lista blanca»; como verbo = «añadir a los admitidos».
  - Haiku lo aplicó en una segunda pasada. Quedan 0 «autentic», pero al menos un verbo sin cambiar (#90).
- Resultado: 291 cambios propuestos, aceptados en bloque por Nilo («me vale»), sin revisarlos cadena a cadena. La medición de esta ronda no es comparable con las demás.
- Lección: en rondas por tramos, comprobar antes de `review-po` que los términos de `terms.md` se aplicaron en todo el archivo. Anotado en `review/README.md`.

## 2026-11-08 · GDA Kraft Booking (dev, 2447 cadenas) · descartada, sin número de ronda

- El traductor usa usted de forma sistemática: 108 cadenas con «su» para *your* (ninguna con «tu») y 53 imperativos de usted. La guía dice «Tuteo siempre». Detectado con las cifras baratas, sin pasar por ningún modelo.
- Nilo rechaza el lote entero en lugar de pasarlo a tuteo.

## 2026-11-08 · Haiku · ronda 22 (MHM Rentiva, stable, 3302 cadenas) · directa, sin revisión humana

- Cinco tramos seguidos de unas 660 cadenas, unos 14 minutos. Traducción humana y buena. Primera ronda con las notas del glosario en las pistas de `lint`.
- Haiku: 388 decisiones (337 rechazos, 48 correcciones, 3 dudas). Casi todo del glosario y aplicando sus notas: *delete* = «borrar» (~49), *rating* fuera del directorio = «puntuación» (~45), «#%d» en lugar de «n.º» (~45), *default* (~38), *remove* = «quitar» salvo borrados físicos (~32), *login* / *logged in* = «acceder» / «conectado» (~28), *receipt* = «recibo» (~26), «aviso» (~23).
- Auditoría de Opus: 13 descartadas y 1 editada. «asistencia» → «soporte» (13): el glosario solo da «dar soporte» para el verbo y «asistencia» es correcto. #2205: Haiku reformulaba «¿Estás completamente seguro?»; solo se aplica «borrar». Quedan 372 cambios.
- Dudas que se dejan como estaban: *endpoint* en la API REST (#1240) y *Commit* en botones (#1241, #1274).

## 2026-11-08 · Haiku · ronda 21 (Gratora, stable, 3523 cadenas) · directa, sin revisión humana

- Cinco tramos seguidos de unas 705 cadenas, unos 15 minutos. Traducción humana y buena.
- Durante la revisión, Nilo cambió el criterio de *recurring*: se prefiere «periódico», pero «recurrente» se acepta (128 cadenas sin tocar). Se le avisó a Haiku a mitad de ronda y lo aplicó.
- Haiku: 100 decisiones (89 rechazos, 4 correcciones, 7 dudas). Casi todo del glosario: *next* = «siguiente» (22), *set* = «establecer» (10), «aviso» (7), *entry* de datos = «registro» (7), «enlazar» (6), *admin* persona = «administrador» (5), *hero*, *onboarding*, «casilla de verificación».
- Auditoría de Opus: 8 descartadas, todas reformulaciones de algo correcto o sin entrada de glosario («programación», «juego de credenciales», «online», «ni tú ni el donante podéis», #3296 «Bold» en tokens de estilo = «Negrita»). Quedan 85 cambios; las 7 dudas se quedan como estaban.
- Dudas: *sandbox* en PayPal (6 cadenas; el traductor lo deja como en la interfaz de PayPal) y #3170 «Friend».
- Conflictos con el glosario que señala Haiku: *fee* = «cuota» frente a «comisiones» de pasarela, *designation* = «nombramiento», *fixed* = «corregido» para valores fijos, *wizard*, *get started*, *preset* = «preajuste» frente a «predefinidos».

## 2026-11-08 · Haiku · ronda 20 (TWT AEO Ultimate, stable, 3707 cadenas) · directa, sin revisión humana

- La más grande hasta ahora de una vez. Cinco tramos seguidos de unas 750 cadenas en la misma sesión, con `terms.md`, unos 26 minutos. Traducción humana y buena.
- Haiku: 553 cambios. Guion largo restaurado en 449 cadenas, por la regla que había entonces (el traductor lo cambiaba por «:», «;» o paréntesis), 30 de mayúsculas, 55 de glosario y precisión (*set*, *check*, *next*, *fix*, *delete*, *render*, *caption*, *membership*, *frontend*…).
- Auditoría de Opus, corregida con Nilo: 553 decisiones, 431 descartadas y 50 editadas o añadidas; quedan 134 cambios.
  - Guion largo: Nilo no lo habría cambiado. La raya se puede sustituir por «:» o «;», no rompe nada y no es motivo de rechazo. Lo que se mantiene es lo que puede romper, como los puntos suspensivos finales. La regla de la referencia rápida venía de generalizar un caso de la ronda 10 y se ha corregido. Se descartan los cambios que solo ponían la raya, y en los que tenían otra corrección se mantiene la puntuación del traductor.
  - *Toggle X* = «Alternar X» (12 etiquetas): «Activar o desactivar X» alarga mucho la cadena.
  - «preguntas frecuentes» → «FAQ» por el glosario: se mantiene lo del traductor (#310, #560). En la ronda 12 Nilo también puso «preguntas frecuentes».
  - #712 «Open Knowledge File» es el nombre de un formato: no se traduce.
  - #202: faltaba «↳ Follow-up rows:» del original, y a Haiku también se le pasó.
- Nilo: *scope* = «ámbito» es correcto. *endpoint* = «variable» del glosario solo vale para WooCommerce: hay que revisarlo en el glosario. «OK» = «Correcto» es arriesgado, porque «OK» puede ser un estado o el botón «Aceptar».
- Falso positivo de `check` en #2035 («80% structural»), el mismo de la ronda 18.

## 2026-11-08 · Haiku · ronda 19 (Ensomedia Security, dev, 2467 cadenas) · directa, sin revisión humana

- Tres tramos seguidos (1-820, 821-1640, 1641-2467) en la misma sesión, con `terms.md`. Traducción humana y correcta, pero ignoraba el glosario.
- Primera pasada: 422 cambios. Casi todos del glosario: *scan* = «exploración» (~144), *login* = «acceder» (~64), «identificación» (~45), «correo electrónico» en textos largos (~42), *role* = «perfil» (~43), *Dashboard* = «Escritorio» (~31), «malintencionado», «alojamiento», «por defecto», «borrar».
- Haiku cambió los verbos de *login* a «acceder», pero dejó «inicio de sesión» como duda (~120 cadenas). El glosario lo resuelve («acceder / acceso», «Iniciar sesión» incorrecto). En una segunda pasada lo aplicó, junto con *sign out* = «salir», y deshizo «Escritorio» para el panel del servicio externo shieldwave.io (21 cadenas): el glosario se refiere al escritorio de WordPress.
- Auditoría de Opus: 523 decisiones, 1 descartada y 13 editadas.
  - *host* como empresa («pide a tu desarrollador o a tu alojamiento») → «proveedor de alojamiento» (13).
  - Descartada la #843: «¿Hacer que salgan todos los usuarios, incluido tú?» se lee peor que «¿Cerrar la sesión de todos los usuarios, incluida la tuya?».
  - `audit_decisions.py` acepta ahora `--edits` para reformular propuestas, además de descartarlas.
- Dudas sin resolver, que se dejan como estaban: *release* = «paquete oficial», *vendor build*, *bulk* = «en masa», *threat feed* = «fuente de amenazas», interfaz de Cloudflare en inglés.

## 2026-11-06 · Haiku · rondas 14–16 · directas, sin revisión humana

Haiku revisa y Opus audita en lugar de Nilo (`review/README.md`, «Direct rounds»). No cuentan en las mediciones.

| Ronda | Cadenas | Propuestas de Haiku | Aplicadas | Descartadas por Opus |
|---|---|---|---|---|
| 14 quote3d-for-woocommerce stable | 834 | 36 | 33 (32 + 1 añadida) | 4 |
| 15 paypercut-payments-for-woocommerce stable | 726 | 77 | 73 | 4 |
| 16 route-finder dev | 1635 (dos tramos) | 360 | 358 | 2 |

- Descartes de Opus:
  - URL localizada que existe (#2 de la ronda 14).
  - *Clear* → «Vaciar» en botones (14).
  - «eliminar» → «quitar» en borrados físicos de ajustes y claves (15).
  - «se borran» → «se vacían» (15).
  - Dos dudas sin resolver (16), que se dejan como estaban.
- Criterio nuevo de Nilo: *Clear filters* = «Quitar filtros» o «Limpiar filtros». Se aplicó al #135 de la ronda 14.
- Ronda 16:
  - 82 correcciones de mayúsculas de *Title Case* y 37 de comillas: el traductor no seguía la guía en eso.
  - *zoom* → «ampliación» (35), según el glosario. Pendiente de confirmar con Nilo, por la cantidad de cadenas.
  - El traductor usaba el tratamiento de usted en 4 cadenas («Configure», «Considere»), que se corrigieron.

## 2026-11-08 · Haiku · ronda 17 (Flooring Calculator for WooCommerce, stable, 114 cadenas) · skill v3

- Haiku como subagente (`model: haiku`); Nilo lo sigue en la pestaña de subprocesos.
- Resultado: 17 cambios. Haiku propuso 16 cambios y 2 dudas. Mantenidos: 15. Deshecho: 1. Ni editados ni escapados.
- Deshecho (#52): en el menú, «Flooring calculator» no es el nombre del plugin sino lo que hace la pantalla, así que se traduce: «Calculadora de suelos». El nombre completo del plugin (#1, #5) sí se queda en inglés.
- Dudas (#17, #18): *shop default* → «valor por defecto de la tienda», sin omitir *default*.
- Nilo confirmó las preguntas de Haiku: la pasiva refleja («se vende por metros») vale, y «Hay %s en existencias» para *%s in stock*.

## 2026-11-08 · Haiku · ronda 18 (Flooring Calculator for WooCommerce, readme, 139 cadenas) · skill v3

- Haiku como subagente, con los términos que Nilo eligió en la ronda 17 como contexto.
- Resultado: 34 cambios. Haiku propuso 34 cambios, sin dudas. Mantenidos: 34. Ni editados, ni deshechos, ni escapados.
- Aprobados sin cambio, como Haiku: «Funciones» para *feature*, «finalización de compra», «edición en lote» y «está en» para *is set to*.
- Fallo de `po_tool.py check`: toma «5 % for» o «10% for» por marcadores de printf (#16, #60, #76). Pendiente de arreglar.

## 2026-11-08 · Arcadys Municipal Core (stable, 2672 cadenas) · descartada, sin número de ronda

- El original está en español de América, no en inglés: 2650 cadenas son copia exacta del original y las otras 22 solo añaden el plural. Detectado con las cifras baratas, sin pasar por ningún modelo.
- Nilo: se rechaza el lote entero y se avisa a quien lo envió de que, para poder traducir un plugin, el original tiene que estar en inglés de EE. UU.
- Se borraron sus archivos, como en la ronda 05.

## 2026-11-06 · Haiku frente a Sonnet · rondas 03 y 04 · skill v3

Haiku revisó a ciegas los `original.po` de las rondas 03 y 04. Se compara con la revisión final de Nilo (`reviewed.po`). Ojo: Nilo revisó partiendo de las propuestas de Sonnet, así que la referencia favorece a Sonnet.

| Ronda | Cambios de Nilo | Sonnet: mantenidos / editados / deshechos / escapados / dudas | Haiku: mantenidos / editados / deshechos / escapados / dudas |
|---|---|---|---|
| 04 BetterDocs (164) | 8 | 8 / 0 / 0 / 0 / 0 | 3 / 1 / 1 / 3 / 6 |
| 03 OrderFlow (356) | 46 | 44 / 1 / 0 / 0 / 1 | 35 / 5 / 0 / 6 / 1 |

- Haiku acierta en lo gordo: glosario, «Lo siento», el texto añadido en la descripción. Se le escapan matices del glosario: *set* = «establecer», *check* = «comprobar», y coherencia con *delete* en todas las cadenas.
- Hace más preguntas: 6 dudas en BetterDocs, algunas razonables («TOC», «text» como valor de ejemplo) y otras que Sonnet resolvió solo.
- Un cambio de más: «Icono de impresión» por «Icono de imprimir».
- En dos casos aplicó mejor que la referencia la nota del glosario de «eliminar» para plugins, pero Nilo optó por «borrar» en todo. `po_tool.py` encuentra `resources/` desde cualquier carpeta.
