# Audit (direct round, no human review)

Model decisions: 77 · applied: 73 · dropped: 4

- #244 dropped: Borrar todos los ajustes y claves de la base de datos es un borrado físico: «eliminar» es válido según la nota del glosario.
  - model: Quita todos los ajustes del plugin Paypercut, incluidas las claves de API, los detalles de conexión y las preferencias de pago, e inicia la configuración de nuevo. Los pagos con Paypercut no estarán disponibles hasta que vuelvas a conectar.
- #456 dropped: «se borran» es natural para registros que se borran; «se vacían» no aporta. Mismo criterio que «Clear» → «Borrar».
  - model: Exactamente lo que se envió a Paypercut, lo más nuevo al final. Los %s más recientes se conservan en esta tienda y se vacían cuando se inicia una nueva sesión.
- #523 dropped: Borrar la clave secreta almacenada es un borrado físico: «eliminar» es válido según la nota del glosario.
  - model: Esto quitará la clave secreta de la API almacenada en WooCommerce y desactivará el método de pago de Paypercut para esta tienda.
- #542 dropped: Borrar la clave secreta almacenada es un borrado físico: «eliminar» es válido según la nota del glosario.
  - model: ¿Desconectar Paypercut de esta tienda? Esto quitará la clave secreta de la API almacenada y desactivará el método de pago.
