# Terminos de la ronda 19 (ShieldWave / Ensomedia Security)

Decisiones de termino para las tres franjas. Se relee al empezar cada franja.

## Decisiones (aplicar en todo el archivo)

| Ingles | Espanol elegido | Fuente | Notas |
|---|---|---|---|
| role (noun) | perfil | Glosario: «NO usar rol» | roles → perfiles. Ojo a «no role» → «sin perfil». |
| hosting (noun) | alojamiento | Glosario | Se usa «proveedor de alojamiento», no «proveedor de hosting». |
| authentication, authenticator app | identificación, aplicación de identificación | Referencia rápida (Anglicismos) | Evitar «autenticación». Ver duda en el informe. |
| default (adjetivo) | por defecto | Referencia rápida (no «predeterminado») | |
| backup (noun) | copia de seguridad | Glosario | «respaldo» es sinónimo: se corrige. |
| passkey | llave de acceso | Traducción ya usada en #13 | Unificar #84. |
| sign out (verb) | cerrar sesión (no se cambia; conflicto con el glosario, que dice «salir») | Glosario vs uso del traductor | Ver informe. |
| warning (noun) | advertencia | Glosario | «Aviso» solo para «advisory». |
| email (noun) | correo electrónico | Glosario / referencia rápida | Textos largos: «correo electrónico». Cadenas cortas de interfaz: «correo» se aprueba. |
| threat feed | fuente de amenazas | Decisión del traductor | Glosario: feed es RSS. Se aprueba. |
| sign in (verb) | acceder | Glosario | Traducción del traductor: «Accede», «acceso». |
| login page, sign-in (noun) | página de inicio de sesión, inicio de sesión | Sin entrada de glosario para el sustantivo | Se aprueba. Pregunta en el informe. |
| edge (Cloudflare) | edge / regla edge | Traducción del traductor | Se mantiene. |
| Cloudflare UI names (Zone, Zone WAF, My Profile, API Tokens, Custom rules) | en inglés, como las pone el traductor | Sin entrada de glosario | Se aprueban. Pregunta en el informe. |
| remove (verb) | quitar / eliminar | Glosario | «Eliminar» para borrar físicamente (token, cuentas). |
| check (verb) | comprobar | Glosario | |
| scan | explorar / exploración | Glosario | |
| set (verb) | establecer | Glosario | |
| fix (noun) | corrección | Glosario | |
| delete | borrar / eliminar | Glosario | Traducción del traductor: «Eliminación» en registros. |
| save (verb) | guardar | Glosario | |
| feature | característica (en registros) | Glosario | |
| release | versión | Glosario | |
| hook / code / snippet | gancho / código / fragmento de código | Glosario | |
| branch | rama | Glosario | |
| firewall | cortafuegos | Glosario | |
| log | registro | Glosario | |
| update / updated | actualización / actualizado | Glosario | |
| upload | subida / subir | Glosario | Ya usados. |
| token | token | Glosario (no se traduce) | |
| plugin, plugins | plugin, plugins | Glosario | |
| Live protection | Protección en tiempo real | Traducción del traductor | Consistente en la franja. |
| History (menu/tab) | Historial | Traducción del traductor | Consistente. |
| Ajustes (settings) | ajustes | Glosario | |

## Franja 1-820 (hecho: 133 decisiones)

Aplicado en todo el archivo de esta franja:

- rol → perfil (roles → perfiles); «sin rol» → «sin perfil»; «Rol predeterminado» → «Perfil por defecto».
- hosting → alojamiento («tu proveedor de alojamiento», «tu alojamiento»).
- respaldo → copia de seguridad (#13).
- autenticación → identificación (#13); «aplicación de identificación».
- predeterminado → por defecto (#87, #113, #682, #683).
- passkey → llave de acceso (#84, unificado con #13).
- Verbos: «iniciar sesión / inicia sesión / Iniciar sesión» → «acceder / accede / Acceder» (glosario: sign in, login).
- «cerrar sesión» (sign out) NO se cambia a «salir» (glosario: sign out → salir). Decisión: el término del glosario parece erróneo para una interfaz y en el archivo se usa «cerrar sesión» en varias cadenas. Conflicto de glosario para el informe. Se revirtieron #85 y #211.
- Sustantivos «inicio de sesión», «página de inicio de sesión», «inicios de sesión» NO se cambian: el glosario solo define el verbo (login → acceder / acceso). Pregunta en el informe.
- scan: «análisis» → «exploración» (sustantivo) / «explorar» (verbo). Gerundio «Analizando» → «Explorando» (#483-485).
- checkout (página) → «finalizar compra» (#425, #428, #442, #525), no «pago».
- malicious → malintencionado (glosario); «malicioso» se corrige.
- builder → maquetador (#332, #736, #758); «constructor de páginas» se corrige.
- hook → gancho (#376). Dashboard → escritorio (#200). FAQ no se traduce (#200).
- writable → tener permisos de escritura (#300, #605, #621).
- clear (historial) → vaciar (#216). Clear filter → quitar filtro (#192, se aprueba).
- warning → advertencia (#36). Aviso sigue para «advisory».
- bug → fallo (#762). hide → ocultar (#787, no «esconder»). computer → ordenador (#560).
- correo → correo electrónico en textos largos (#85, #182, #213, #307, #443, #479, #520, #529, #535, #554, #567, #572, #774). En cadenas cortas de interfaz («Correo», «dirección de correo de administración», «Comprobaciones del sitio y correo de prueba») se aprueba.
- Live protection → Protección en tiempo real (#606, #616, #774); no «en vivo».
- feed (amenazas) → fuente de amenazas: se aprueba (el glosario habla del feed RSS). Ver informe.
- edge, Cloudflare (Zone, Zone WAF, My Profile, API Tokens, Custom rules, Live threat feed) → se mantienen en inglés, como las pone el traductor. Ver informe.
- Aprobado sin cambio: «Settings > General» → «Ajustes > Generales»; «Overview» → «Resumen»; «Users» → «Usuarios»; «Appearance > Themes» → «Apariencia > Temas»; «Hardening» → «Refuerzo»; «Hosting companies» ya corregido.
- Aprobado sin cambio: «feature» en «una función» (#384): el glosario permite «función» cuando es más preciso.
- Aprobado sin cambio: «vendor build» → «compilación del autor» (#698). El glosario da «vendedor»: no encaja con un autor de plugin. Ver informe.
- Aprobado sin cambio: «uploads» (nombre de carpeta wp-content/uploads) se mantiene en inglés.
- «Activity log»: aparece como «registro de actividad» (#72, #136) y como «historial» (#756, #757, #767). No se unifica: pendiente.
- «delete» → «borrar» (glosario): el traductor usa «borrar» y «eliminar» a la vez. Pendiente de decidir en la franja 3 (ver barrido final).

## Franja 821-1640 (hecho: 252 decisiones acumuladas)

- two-factor authentication / authentication → «identificación en dos pasos» / «identificación» (el glosario de esta franja lo confirma: «No usar autenticación»). Aplicado en todas las apariciones.
- scan (verbo y sustantivo) → «explorar» / «exploración»; «scans» → «exploraciones»; «análisis» como sustantivo de scan se corrige. «analysis» (sustantivo que no es scan, #1462, #1084) se deja como «análisis».
- dashboard → «escritorio», también en el panel de shieldwave.io («en tu escritorio de shieldwave.io»). Pendiente: confirmar con Nilo si el panel externo debe seguir siendo «panel».
- checkout (página) → «finalizar compra» (#425, #428, #442, #525).
- review (directorio de plugins y temas) → «valoración» (#1547, #1548). «rate» → «valorar» (#1550).
- media → «medios» / «archivos de medios» (#1436).
- builder → «maquetador» (#1235, #1259).
- writable → «tener permisos de escritura» (#621).
- support (compatibilidad) → «compatible con» (#230).
- settings → «ajustes» (#230, «configuración previa» se corrige). «configuración» se mantiene para «configuration»/«setup».
- report → «informe» (#1207).
- hook → «gancho» (#376).
- report/reporte, n.º → «#» (#1293, #1294: «#%s» como en el original).
- Aprobado sin cambio: «release» como «paquete oficial» (#1406 y siguientes). El glosario dice «versión». Es un sentido distinto (el paquete descargable). Pregunta en el informe.
- Aprobado sin cambio: «must-use» se traduce de dos formas: «plugin must-use» (franja 1) y «plugins imprescindibles» (#1383, #1399, #1437). Inconsistente. Pendiente de decidir (ver barrido final).
- Aprobado sin cambio: «vendor build» → «compilación del autor» (#698). El glosario da «vendedor»: no encaja con un autor de plugin.
- Aprobado sin cambio: «el analizador» para «scanner» (no hay entrada de glosario para «scanner»).
- Aprobado sin cambio: «correo» en cadenas cortas de interfaz (#961, #971, #1228, #1614).
- Aprobado sin cambio: «Mi alojamiento» / «Ayuda de tu proveedor de alojamiento» ya coherentes.
- Pendiente: «delete» → «borrar» (glosario) frente a «eliminar» (el traductor usa las dos). Se decide en el barrido final.
- Pendiente: «Activity log» como «registro de actividad» (franja 1) o «historial» (#756, #757, #767). Sin unificar.

## Barrido final (franjas cruzadas)

Decisiones corregidas para que cada término quede igual en las tres franjas:

- Página de acceso (login page): «página de acceso» en todo el archivo (#85, #809, #2286 corregidas).
- Activity log: «registro de actividad» (#756, #757, #767 corregidas; antes «historial»). «Historial» queda para la pestaña History.
- Delete → «borrar» (glosario) en #44, #92, #93, #109, #110, #111, #142, #418, #421, #462, #702, #703, #705, #1243, #1244. «Eliminar» queda solo para «remove» (quitar físico, p. ej. cuentas cuando el original dice remove).
- Must-use → «imprescindible» (#361, #474 corregidas; el resto ya usaba «plugins imprescindibles»).
- Dashboard → «escritorio» también en las 7 entradas donde el original dice dashboard (#1324, #2198, #2204, #2282, #2285, #2286, #2288).
- «Post #%d» y «entry #%s» → «#» (#1293, #1294, #1977).

Estado al final: 422 decisiones (421 reject, 1 fix: #44 comillas). Chequeo de marcadores: 0 problemas. Build: corrected.po con 422 entradas.

Pendiente de decisión del revisor (no se cambia en el archivo):
- «inicio de sesión» como sustantivo (118 cadenas) frente a «acceso» (glosario, la forma nominal de login). Se deja como está.
- «cerrar sesión» (sign out) frente a «salir» (glosario). Se deja como está.
- «panel» del servicio externo shieldwave.io: se pasó a «escritorio» por el glosario. Reconsiderar.
- «aplicación de identificación» (authenticator app): resultado de aplicar la referencia rápida. Sigue sonando raro; revisar.
- Nombres de la interfaz de Cloudflare (Zone, Zone WAF, My Profile, API Tokens, Custom rules, Zone Resources) en inglés.
- «paquete oficial» para «release» (franja 3); el glosario dice «versión».

## Segunda pasada (criterio del coordinador)

- login (sustantivo): «acceso» (glosario: acceder / acceso). «inicio de sesión» se sustituye en todo el archivo (138 cadenas). «página de acceso», «dirección de acceso», «protección de acceso». Los nombres de función «inicio de sesión en dos pasos» pasan a «acceso en dos pasos».
- sign out / log out: «salir» (glosario). Cambiadas #85, #211, #834, #840, #843, #844, #921, #1441. Las frases «sesiones cerradas» (session ended) se mantienen.
- dashboard: «escritorio» solo para el panel de administración de WordPress. El servicio externo shieldwave.io se mantiene como «panel» (21 cadenas: #1326, #1479, #1505, #1508, #1514, #1515, #1516, #1518, #1520, #1528, #1529, #1531, #1532, #1533, #1539, #1643, #1668, #1670, #1859, #2133, #2209).
- Pendiente: «acceso en dos pasos» suena forzado en nombres de función; «llave de acceso» + «acceso» en la misma frase (#13, #207).
