# Revisión a ciegas: MailBridgeAPI Email Delivery – Stable Readme (es, waiting)

Revisadas 72 cadenas con la guía del equipo, el glosario oficial y el YAML `es_ES.yaml`. No he visto el veredicto de la herramienta.

| Veredicto | Cadenas |
|---|---|
| Aprobar | 55 |
| Corregir y aprobar | 6 |
| Rechazar (con comentario) | 9 |
| Dudosa (decide tú) | 2 |

Estructura comprobada: etiquetas HTML, entidades, `%i`, `{id}` y URL coinciden con el original en las 72 cadenas.

---

## Rechazar (9)

Todos incumplen el glosario. Las reglas del YAML detectan los nueve.

**R1.** *No. It is used once for the secure authentication request…*
- Actual: «solicitud de **autenticación** segura»
- Propuesta: «No. Se utiliza una sola vez para la solicitud de **identificación** segura y después se descarta. El token de sesión y las claves API resultantes se cifran antes de guardarlos en la base de datos.»
- Comentario: Según el glosario, «authentication» se traduce como «identificación» (no «autenticación»). Propuesta: «solicitud de identificación segura».

**R2.** *No. Once a mailbox is selected, the plugin stores only that selected mailbox…*
- Actual: «Cuando se selecciona un buzón… desconectarse y **autenticarse** de nuevo»
- Propuesta: «No. Una vez que seleccionas un buzón, el plugin guarda únicamente ese buzón y deja de mostrar la lista de buzones de la cuenta. Un administrador debe desconectarse y volver a identificarse para elegir otro buzón.»
- Comentario: El glosario pide «identificar» en lugar de «autenticar». Además, «Una vez que seleccionas» recoge mejor el «Once» del original y suena más directo.

**R3.** *The dashboard password is used only for the HTTPS authentication request…*
- Actual: «solicitud de **autenticación** HTTPS»
- Propuesta: «La contraseña del escritorio solo se utiliza para la solicitud de **identificación** HTTPS y nunca se almacena. El token de la cuenta y las claves API seleccionadas se cifran con AES-256-GCM mediante una clave derivada de la sal de autenticación de WordPress.»
- Comentario: Glosario: «authentication» → «identificación». Sobre «sal de autenticación» (la constante AUTH_SALT), no cambio nada hasta confirmar cómo la traduce el núcleo (ver dudas).

**R4.** *…/mailboxes/ returns mailboxes belonging to the authenticated account.*
- Actual: «cuenta **autenticada**»
- Propuesta: «…devuelve los buzones que pertenecen a la cuenta identificada.»
- Comentario: Glosario: «authenticate» → «identificar».

**R5.** *…/auth/login/ authenticates the administrator. It receives the dashboard email address and password, this site's host name, plugin version, WordPress locale and notification preference.*
- Actual: «**autentica** al administrador… la dirección de correo… el idioma de WordPress y la preferencia de **notificaciones**»
- Propuesta: «`…/auth/login/` identifica al administrador. Recibe la dirección de correo electrónico y la contraseña del escritorio, el nombre de host de este sitio, la versión del plugin, la configuración regional de WordPress y la preferencia de avisos.»
- Comentario: Cuatro ajustes al glosario: «authenticate» → «identificar»; «notification» → «aviso» (no «notificación»); «locale» → «configuración regional»; y «email address» → «dirección de correo electrónico».

**R6.** *MailBridgeAPI Email Delivery connects WordPress to a mailbox that is centrally managed…*
- Actual: «Cuando un administrador **autentica** la cuenta»
- Propuesta: «…Cuando un administrador identifica la cuenta de MailBridgeAPI y bloquea un buzón para el sitio, los mensajes salientes se entregan mediante la API HTTPS de MailBridgeAPI.»
- Comentario: Glosario: «authenticate» → «identificar».

**R7.** *After selection, the plugin hides every other account mailbox…*
- Actual: «volver a **iniciar sesión**»
- Propuesta: «Tras la selección, el plugin oculta todos los demás buzones de la cuenta. Para cambiar de buzón es necesario desconectarse por completo y volver a acceder.»
- Comentario: Glosario: «sign in / login» se traduce como «acceder»; «iniciar sesión» está marcado como incorrecto.

**R8.** *Sign in using the email address and password used for the MailBridgeAPI dashboard.*
- Actual: «**Inicia sesión** con la dirección de correo…»
- Propuesta: «Accede con la dirección de correo electrónico y la contraseña utilizadas para el escritorio de MailBridgeAPI.»
- Comentario: Glosario: «sign in» → «acceder» (no «iniciar sesión»), y «email address» → «dirección de correo electrónico».

**R9.** *The plugin intercepts wp_mail()… It supports plain-text and HTML messages, Reply-To, CC, BCC and up to two attachments…*
- Actual: «…CC, **BCC** y hasta dos archivos adjuntos»
- Propuesta: cambiar solo «BCC» por «**CCO**»: «…Reply-To, CC, CCO y hasta dos archivos adjuntos.»
- Comentario: El glosario pide la abreviatura en español: BCC → CCO (Con Copia Oculta).

---

## Corregir y aprobar (6)

| # | Original | Actual | Corrección |
|---|---|---|---|
| C1 | Email compatibility (encabezado) | Compatibilidad **del** correo electrónico | Compatibilidad **con** el correo electrónico |
| C2 | Show a clear in-progress state while a connection test is running. | **Añadido** un estado de progreso claro… | **Mostrado** un estado de progreso claro mientras se ejecuta una prueba de conexión. (el original dice *Show*, no *Add*) |
| C3 | Harden administrator request validation… | solicitudes **de administración** | solicitudes **del administrador** |
| C4 | Sanitize every administrator request field… | solicitudes **de administración** | solicitudes **del administrador** |
| C5 | …does not store SMTP host names, usernames… | nombres de **servidor** SMTP | nombres de **host** SMTP (glosario: *hostname* no se traduce; otra cadena de este archivo ya usa «nombre de host») |
| C6 | Enter the email address and password used for your MailBridgeAPI dashboard. | la dirección de **correo** | la dirección de **correo electrónico** (glosario) |

---

## Dudosa (2)

**D1.** *Link the plugin header to the public MailBridgeAPI WordPress plugin page.*
- Actual: «…con la página pública del plugin MailBridgeAPI **en WordPress.org**.»
- Duda: el original no dice «WordPress.org»; podría ser la página del plugin en el sitio de MailBridgeAPI. Propuesta neutra: «…con la página pública del plugin MailBridgeAPI para WordPress.»
- Pregunta: ¿se sabe dónde está esa página?

**D2.** *Add recent-error menu badge, log clearing and filtered CSV export.*
- Actual: «un **distintivo** de menú para errores recientes»
- Duda: el glosario da para *badge* «acreditación / insignia / distinción». «Distintivo» no está. ¿Prefieres «insignia»?

---

## Aprobar (55)

Las demás cadenas son correctas y naturales: tuteo, voz de WordPress, glosario (*monitor* → supervisar, *log* → registro, *erasure* → borrado, *sender* → remitente, *header* → cabecera, *placeholder* → marcador de posición…) y consistencia interna.

Observaciones menores que no justifican rechazo:
- Varias cadenas usan la pasiva refleja («Se admiten…», «Se elimina…»). Es natural en descripciones de funciones.
- «archivos adjuntos» en lugar de «adjuntos» (glosario: *attachment* → adjunto). Es un uso corriente y más claro.
- Un elemento del registro de cambios usa presente («permanece visible») mientras los demás usan participio. Está bien.

---

## Decisiones globales pendientes

1. **«dashboard» → «escritorio» (unas doce cadenas).** Todo el archivo es coherente con el glosario, pero aquí «dashboard» es el panel web de MailBridgeAPI, no el Escritorio de WordPress. Puede confundirse («la contraseña de mi escritorio»). No lo he tocado: o se mantiene por glosario o se decide otra fórmula para todo el archivo a la vez.
2. **«authentication salt».** Es el nombre de la constante AUTH_SALT de WordPress. Habría que mirar cómo la traduce el núcleo es_ES antes de cambiar «sal de autenticación».
3. **Rutas de menú de WordPress** («Plugins > Añadir nuevo plugin > Subir plugin»): no las he comprobado contra la traducción del núcleo.

---

## Qué enseña esta revisión sobre el YAML

- Las reglas detectan los 9 rechazos. No detectan los problemas de sentido o de preposición (C1–C4), que piden criterio de revisor.
- Dos reglas daban falsos positivos y las he corregido: `email` saltaba en nombres de producto y código, y `agrega` saltaba en «resultados agregados».
- Reglas añadidas: `BCC` → CCO, y «dirección de correo» sin «electrónico».
- Siguen saltando como `hint` las cadenas con el nombre del producto «MailBridgeAPI Email Delivery», que es un nombre propio. Es ruido asumible.
