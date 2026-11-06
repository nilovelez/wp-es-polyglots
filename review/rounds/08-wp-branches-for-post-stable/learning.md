Strings 66 · human changes 6 · model proposals 5 · kept 5 · edited 0 · reverted 0 · missed 0 · doubts 1

## Doubts (1)

- #2 Choose an original or branch value for every supported conflict before requesting review.
  - original: Antes de solicitar una revisión, elige el valor del original o de la rama para cada conflicto que admita resolución.
  - model: Antes de solicitar una revisión, elige el valor del original o de la rama para cada conflicto que se pueda resolver.
  - reason: Pregunta: «supported conflict» significa un conflicto que el plugin sabe resolver. El glosario da «compatible», y aquí no encaja: «conflicto compatible» no se entiende. ¿Dejamos «que admita resolución» o usamos la propuesta?

## Model proposal kept (5)

- #47 This branch cannot be reviewed until its baseline is valid.
  - original: Esta rama no se puede revisar hasta que su referencia inicial sea válida.
  - model: Esta rama no se puede revisar hasta que su estado de referencia sea válido.
  - reason: En el readme del plugin, «baseline» se traduce como «estado de referencia». Aquí aparece «referencia inicial»; conviene unificarlo.
- #48 Post Branch Workflow
  - original: Flujo de trabajo de las ramas de entradas
  - model: Flujo de trabajo de la rama de la entrada
  - reason: Por coherencia con «Rama de la entrada», el nombre del panel en el readme del plugin. «Post Branch» no es «ramas de entradas».
- #52 Open Review changes in the editor and inspect Base, Original and Branch before deciding. Approval applies only to the exact requested snapshot.
  - original: Abre «Revisar cambios» en el editor y compara «Referencia», «Original» y «Rama» antes de decidir. La aprobación solo se aplica a la versión exacta enviada a revisión.
  - model: Abre «Revisar cambios» en el editor y compara «Referencia», «Original» y «Rama» antes de decidir. La aprobación solo se aplica a la instantánea exacta enviada a revisión.
  - reason: Según el glosario, «snapshot» es «instantánea», no «versión».
- #56 Legacy branch
  - original: Rama de una versión anterior
  - model: Rama heredada
  - reason: Según el glosario, «legacy» es «heredado», no «de una versión anterior».
- #66 Create safe working branches for published WordPress content and merge them back without changing the public post while editing.
  - original: Crea ramas de trabajo independientes para el contenido publicado de WordPress y fusiónalas con el original sin modificar la versión pública mientras editas.
  - model: Crea ramas de trabajo independientes para el contenido publicado de WordPress y fusiónalas con el original sin modificar la entrada pública mientras editas.
  - reason: Según el glosario, «post» es «entrada». Aquí se habla de la entrada pública, no de una «versión pública».
