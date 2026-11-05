# Flujo de moderación de cadenas *waiting* (es_ES)

Flujo de trabajo para quien modera traducciones pendientes (PTE del proyecto para el locale, o GTE del locale) en translate.wordpress.org. No es una guía para colaboradores: las reglas de traducción y los criterios de veredicto están en `resources/style-guide.md` y en el glosario (`resources/glossary.csv`).

---

## 1. Flujo

1. **Descargar** las cadenas *waiting* del proyecto como `.po` (en GlotPress: filtro *Waiting* y exportar, o `polyglots fetch`).
2. **Revisar** el `.po` (pasada de reglas + revisión completa) con la guía y el glosario. Resultado: un `-repaired.po` con las correcciones aplicadas.
3. **Resolver a mano lo que queda**: las cadenas que la revisión no resuelve salen marcadas como *fuzzy*. Se corrigen en Poedit.
4. **Subir** el `-repaired.po` al proyecto (ver sección 2).
5. **Aprobar el resto**: las *waiting* que no se han tocado se aprueban en bloque, tras comprobar el contador.

---

## 2. Subida del `.po` y permisos

| Quien sube | Qué pasa con las cadenas que cambian |
|---|---|
| PTE del proyecto para ese locale, o GTE del locale | Sustituyen a las *waiting*. El formulario de subida permite elegir si quedan **aprobadas** (actuales) o en **waiting**. |
| Sin permiso de edición | Cada cadena cambiada añade **otra *waiting***. Las idénticas se ignoran. |

Consecuencias para moderadores:

- Si se sube como **aprobadas**, quedan en *waiting* solo las cadenas no tocadas; esas se aprueban en bloque.
- Si se sube como **waiting**, hay que aprobar todo después.
- Antes del último paso, mirar el contador de *waiting* para confirmar que no queda nada inesperado.

---

## 3. Veredictos

Los criterios (aprobar, corregir y aprobar, rechazar con comentario, dudosa) son los de la sección 7 de la guía. En este flujo:

- **Aprobar** y **Corregir y aprobar** → entran en el `-repaired.po` ya resueltas.
- **Rechazar** → se corrige en el `.po` y se deja el comentario al traductor.
- **Dudosa** → se pregunta al moderador al terminar; hasta entonces queda como *fuzzy*.

---

## 4. Con la herramienta `polyglots` (ada.tools)

- `polyglots fetch <url del proyecto> --locale es_ES [--no-ai] [--out-dir <carpeta>]`: descarga las *waiting*. Sin `--no-ai` hace también la primera pasada.
- `polyglots review <archivo>.po --locale es_ES`: revisión completa. Genera `<archivo>-repaired.po`.
- La herramienta **no sube ni aprueba nada**. Esos pasos son siempre del moderador.
- La salida se guarda junto al archivo de entrada; `--out-dir` la redirige.
- Reglas del locale: `polyglots/rules/es_ES.yaml` (mistakes, patterns, guidance, capitalization, register, sentenceEnd), cargado desde el generador de reglas de la herramienta.
- Modelos locales (Ollama) solo para borradores de traducción; la revisión local es experimental.

### Qué detecta cada pasada (calibración)

- La **pasada de reglas** (sin IA) detecta los incumplimientos de glosario y de tuteo, pero no los problemas de sentido, preposición o naturalidad.
- El **comprobador de glosario integrado** da falsos positivos con etiquetas HTML, URL y nombres de producto. Tomarlo como pista, no como veredicto.
- Antes de aprobar en bloque, conviene revisar una muestra de las cadenas que la herramienta da por buenas.

---

## 5. Decisiones recurrentes de moderación

Criterios aprendidos en revisiones reales. Si una decisión establece un criterio general, se añade aquí o a la memoria de traducción.

- *Dashboard* de un servicio externo (no el Escritorio de WordPress): pendiente de decidir si se mantiene «escritorio» por glosario o se usa otra fórmula para todo el proyecto.
- Constantes y rutas de menú de WordPress (p. ej. *authentication salt*, «Plugins > Añadir nuevo plugin > Subir plugin»): contrastar con la traducción del núcleo es_ES antes de rechazar.
- El masculino genérico no es motivo de rechazo.
- Cambios mínimos de estilo: se aprueba. Tilde, coma tras «Por favor,» y similares: se corrige y se publica.

El registro de calibración de la herramienta está en `polyglots/calibration-log.md`.
