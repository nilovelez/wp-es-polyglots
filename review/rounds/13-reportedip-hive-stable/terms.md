# Términos de la ronda 13 (ReportedIP Hive)

Decisiones de término para mantener la coherencia entre tramos. Se revisa al inicio de cada tramo.
Base: glosario (con las notas) y guía de estilo. Lo que no está en el glosario se decide aquí.

## Seguridad
- firewall → cortafuegos (glosario).
- brute force → fuerza bruta (sustantivo: «ataque de fuerza bruta»).
- rate limit → límite de peticiones (no «límite de tasa»).
- allowlist → lista de permitidos. blocklist / denylist → lista de bloqueados.
- whitelist como sustantivo → lista blanca (se mantiene). Como verbo (to whitelist, whitelisting) → añadir a los admitidos. Adjetivo (whitelisted) → admitido («IP admitidas»). blacklist → lista negra.
- passkey → llave de acceso. security key / hardware key → llave de seguridad / llave física. No «clave» para estas llaves: la clave queda para API keys y contraseñas.
- endpoint → endpoint (se deja tal cual; el glosario da «variable», que aquí no sirve).
- malicious → malintencionado (glosario).
- onboarding → puesta en marcha (glosario). No «configuración inicial».
- notification / notifications → aviso / avisos (glosario). No «notificación». Menú «Avisos» en lugar de «Notificaciones».
- sign in / login (acción) → acceder / acceso. No «iniciar sesión», «inicio de sesión», «entrar». Pantalla de acceso → «formulario de acceso».
- scan (sitio, página, red) → explorar / exploración (glosario). scan de códigos QR → escanear.
- two-factor / 2FA: decidido por el revisor (duda #192): «identificación en dos pasos», «dos pasos» solo, y 2FA se mantiene.
- Sin «se requiere»: «Necesitas…» / «Es obligatorio…».
- Textos de ayuda y descripciones con «e-mail»/«correo»: «correo electrónico». Solo «correo» en interfaz corta (etiquetas, botones).
- Comillas en cadenas: «» (corregir las rectas, salvo texto literal para un buscador o IA).
- block (verbo) → bloquear. blocked → bloqueado.
- spam → Spam (no se traduce, glosario). honeypot → señuelo (glosario), también en «Honeypot de comentarios» → «Señuelo de comentarios». Excepción: «Honeypot Tier» es nombre de plan (se mantiene).
- bundle: en el sentido de paquete de soporte o de archivo → paquete (se mantiene). Glosario «lote» solo para productos agrupados.
- monitoring → seguimiento / vigilancia / supervisión (no «monitorización»). monitor (verbo) → vigilar / supervisar.
- login (sustantivo, en etiquetas de evento) → acceso / accesos fallidos. «Inicio de sesión fallido» no se usa.
- bulk → por lotes (glosario).
- front-end → portada / vista pública (no «parte pública»).
- two-factor / 2FA → dos pasos (glosario): «autenticación en dos pasos» si hace falta, o «dos pasos». Siglas como 2FA no se traducen.
- authentication → identificación (glosario). authenticate → identificar. authenticator app → app de identificación.
- two-factor authentication / 2FA (palabras) → identificación en dos pasos. two-factor solo → dos pasos. La sigla 2FA se mantiene. Nunca «autenticación» ni «dos factores».
- login / sign in → acceder / acceso (glosario). Para la pantalla o formulario de acceso: «formulario de acceso». No «inicio de sesión», «iniciar sesión» ni «entrar».
- sign out / logout → salir (glosario: sign out → salir).
- key (API key, Gateway, etc.) → clave (glosario). «clave de API».
- hardening → refuerzo.
- IP, HTTP, HTTPS, JSON, XML-RPC, REST, DNS, SMTP, 2FA, WAF → se quedan como están.
- IP address → dirección IP.

## Interfaz y cuentas
- Dashboard → Escritorio (glosario, no «Panel»).
- role → perfil; roles → perfiles (glosario). No «rol».
- user / username → usuario / nombre de usuario (glosario: username → nombre de usuario).
- not allowed → no tienes permisos (glosario, en plural).
- admin (noun) → administrador (perfil) / administración (área).
- settings → ajustes. setting → ajuste.
- options → opciones.
- notification / notice → aviso (glosario: notification → aviso; notice → aviso). No «notificación».
- warning → advertencia (glosario).
- default → por defecto. No «predeterminado».
- enable / enabled → activar / activado. disable / disabled → desactivar / desactivado.
- save → guardar. delete → borrar (glosario). remove → quitar; «eliminar» solo para borrado físico (usuarios, cookies, plugins).
- reset → restablecer.
- dismiss → descartar.
- check → comprobar (no «marcar», salvo para casillas).
- set (verbo) → establecer.
- scan (verbo) → explorar (glosario). Decisión a confirmar en el tramo 1: si el texto de la interfaz ya usa «comprobar» se decide tras ver el uso en el archivo.
- monitor (verbo) → supervisar. monitoring → supervisión.
- log → registro (glosario). logs → registros.
- entry (datos almacenados) → registro (glosario). Entrada de un blog → entrada.
- report (noun/verb) → informe / informar. No «reporte».
- feature → característica (glosario, en registros de cambios; «función» si el contexto lo pide).
- badge → insignia / acreditación / distinción (glosario).

## Correo y contenido
- e-mail / email → correo electrónico (glosario). En textos largos siempre «correo electrónico».
- post → entrada. page → página. site → sitio. website → sitio web (glosario, o «web»).
- content → contenido. file → archivo. upload → subir / subida. download → descargar.
- plugin / plugins → plugin / plugins (no se traducen).
- theme → tema. template → plantilla.
- widget, banner, shortcode, token, slug, schema, JavaScript, cookie, feed, Jetpack, pingback, array, URL → no se traducen (glosario).
- FAQ → no se traduce (glosario).
- Welcome → Te damos la bienvenida (glosario).
- lead → cliente potencial. customer → cliente.
- order → pedido. item → elemento (artículo solo en tiendas online).
- checkout → finalizar compra / pago.

## Acciones y formas
- Botones y acciones del usuario: infinitivo (guía 3.4). Propuestas y avisos al usuario: imperativo tuteo.
- «Por favor,» con coma (guía 4).
- «p. ej.», no «ej.».
- «#%d» se conserva (resources/quick-reference.md). No «n.º».

## Tuteo
- Nunca «usted». En los tramos se vigilan las entradas 56, 614 y 1311, que pueden tener formas de usted.

## Números de versión y nombres
- Nombres de producto y marcas no se traducen (WordPress, WooCommerce, Jetpack, Google, Cloudflare...).
- Siglas tal cual: IP, HTTP, HTTPS, DNS, JSON, XML-RPC, REST, SMTP, WAF, 2FA, GDPR → RGPD (glosario, masculino «el RGPD»).

## Pendientes a decidir al revisar
- scan: glosario «explorar». Ver uso en el archivo antes de cambiar.

## Actualización (decisión del revisor)
- Anglicismos: no «autenticación», «autenticar» ni «dos factores» en las traducciones finales. Se busca de nuevo al cerrar cada build.
- Verificado: sin «autentic» ni «dos factores» en ninguna traducción final.
