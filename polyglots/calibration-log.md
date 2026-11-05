# Registro de calibración de la herramienta `polyglots` (es_ES)

Una entrada por ronda: qué detectó la herramienta, qué se le escapó y en qué se equivocó. Sirve para afinar `polyglots/rules/es_ES.yaml` y, más adelante, para comparar modelos locales.

## Ronda 1: MailBridgeAPI Email Delivery (readme, 72 cadenas)

- **Acertó:** los 9 incumplimientos de glosario (*authenticate*, *iniciar sesión*, BCC, *notification*, *locale*).
- **Alargó** «correo» a «correo electrónico» en 10 cadenas (glosario).
- **Se le escapó:** preposiciones y sentido («Compatibilidad del correo»), «Añadido» donde el original decía *Show*, «solicitudes de administración» y «nombres de servidor SMTP» (*hostname* no se traduce).
- **Se equivocó:**
  - Pasó cuatro entradas del registro de cambios de participio a «Añadir» / «Se añade» y rompió la coherencia del bloque.
  - Escribió «Escritorio» con mayúscula en mitad de frase.
  - Marcó *fuzzy* una cadena correcta, alegando una comilla que no existe.

## Ronda 2: WGRank Translate (readme, 161 cadenas)

- **Acertó:** *firewall*, *deselect*, *default*, *feature*, *notification*, *post types*, *monitor*, *sitemap*, *settings*.
- **Se le escapó:**
  - Términos del glosario que el traductor dejó en inglés: *checkout*, *sliders*, *hooks*, *frontend*, *sitemaps*.
  - *Engagement* («compromiso»), *upgrade* de plan, *rich snippets*.
  - Comillas rectas y simples, «ej.» en lugar de «p. ej.», y mayúsculas en las listas de idiomas.
  - «Metadados» (portugués) y «¿Es compatible con SEO?» (sentido).
- **Se equivocó:**
  - «Tecnología núcleo» para *Core Technology*: *core* del glosario es el núcleo de WordPress.
  - «Escritorio» con mayúscula en mitad de frase, otra vez.
  - Cambió «parcheado» por «Se corrigió» sin necesidad.
  - Marcó *fuzzy* tres cadenas correctas.

## Lecciones

- *Website* = «sitio web» (glosario); solo *site* es siempre «sitio». No hay que quitar «sitio web» cuando el original dice *website*.
- La comprobación de glosario integrada detecta bien lo mal traducido, pero no lo que se deja en inglés. Para eso hacen falta *patterns*.
- Los registros de cambios deben mantener una sola forma verbal en todas las entradas. La herramienta tiende a «normalizar» entradas sueltas.
- Una advertencia de la herramienta que dice «propuesta sin cambios» suele ser un falso positivo: se quita la marca *fuzzy*.

## Candidatos a regla (pendientes de repetirse)

- «Escritorio» con mayúscula en mitad de frase: falta confirmar la norma del núcleo.
- Regla sobre el verbo en los registros de cambios: no se puede expresar como una regla sobre una sola cadena.
