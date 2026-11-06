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
