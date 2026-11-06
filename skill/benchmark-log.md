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
