import re, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))

SRC = os.path.join(HERE, 'es_ES.base.yaml')
OUT = os.path.join(HERE, 'es_ES.yaml')

def q(s):
    return "'" + s.replace("'", "''") + "'"

# (wrong, right, note)
M = [
 # Register / voice
 ("lo sentimos", "lo siento", 'WordPress speaks in first person singular; plural only if the source says "we" (glossary: sorry).'),
 ("perdona", "lo siento", 'Glossary: sorry - do not use "Perdona"; use "Lo siento".'),
 # Access
 ("iniciar sesión", "acceder", 'Glossary: login - use "Acceder", never "Iniciar sesión".'),
 ("inicia sesión", "accede", 'Glossary: login - use "Acceder", never "Iniciar sesión".'),
 ("inicio de sesión", "acceso", 'Glossary: login - use "Acceder"/"acceso", never "inicio de sesión".'),
 ("cerrar sesión", "salir", 'Glossary: log out / sign out - use "Salir".'),
 # Terms with a banned alternative
 ("autentica", "identificar / identificación", 'Glossary: authenticate/authentication - use "identificar/identificación", never "autenticar/autenticación".'),
 ("autentifica", "identificar / identificación", 'Glossary: authenticate/authentication - use "identificar/identificación", never "autentificar/autentificación".'),
 ("malas palabras", "palabras malsonantes", 'Glossary: bad words.'),
 ("computador", "ordenador", 'Glossary: computer - "ordenador" in Spain, never "computador/computadora".'),
 ("contenidos", "contenido", 'Glossary: content - do not use the plural "contenidos" (fixed phrases like "tabla de contenidos" are fine).'),
 ("tablero", "escritorio", 'Glossary: Dashboard - use "Escritorio", never "tablero".'),
 ("panel de control", "escritorio", 'Glossary: Dashboard - use "Escritorio", never "panel de control".'),
 ("deseleccion", "anular selección", 'Glossary: deselect - use "anular selección", never "deseleccionar".'),
 ("e-mail", "correo electrónico", 'Glossary: email - use "correo electrónico", never "e-mail".'),
 ("encript", "cifrar / cifrado", 'Glossary: encrypt - use "cifrar/cifrado", never "encriptar/encriptación".'),
 ("escond", "ocultar", 'Glossary: hide - use "ocultar", never "esconder".'),
 ("expira", "caduca / caducado / caducidad", 'Glossary: expire - use "caduca/caducado/caducidad", never "expira/expirado/expiración".'),
 ("inválid", "no válido", 'Glossary: invalid - use "no válido", never "inválido".'),
 ("vincular", "enlazar", 'Glossary: link (verb) - use "enlazar", never "vincular".'),
 ("vínculo", "enlace", 'Glossary: link (noun) - use "enlace", never "vínculo".'),
 ("linkear", "enlazar", 'Glossary: link (verb) - use "enlazar", never "linkear".'),
 ("administrar", "gestionar", 'Glossary: manage - use "gestionar", never "administrar".'),
 ("mapear", "asignar", 'Glossary: map (verb) - use "asignar", never "mapear".'),
 ("mapeo", "asignación", 'Glossary: mapping - use "asignación", never "mapeo".'),
 ("minific", "minimizar / minimización", 'Glossary: minify - use "minimizar/minimización", never "minificar".'),
 ("monitore", "supervisar / seguir / vigilar", 'Glossary: monitor - never "monitorear".'),
 ("monitoriz", "seguimiento / vigilancia / supervisión", 'Glossary: monitoring - never "monitorización".'),
 ("notific", "aviso / avisar", 'Glossary: notification/notify - use "aviso/avisar", never "notificación/notificar".'),
 ("apodo", "alias", 'Glossary: nickname - use "alias", never "apodo".'),
 ("nickname", "alias", 'Glossary: nickname - use "alias".'),
 ("librería", "biblioteca", 'Glossary: library - use "biblioteca"; "librería" only means a bookshop.'),
 ("poderos", "potente", 'Glossary: powerful - use "potente", never "poderoso".'),
 ("recurrente", "periódico", 'Glossary: recurring - use "periódico", never "recurrente".'),
 ("reportar", "informar", 'Glossary: report (verb) - use "informar", never "reportar".'),
 ("reporte", "informe", 'Glossary: report (noun) - use "informe", never "reporte".'),
 ("requerid", "obligatorio / necesario", 'Glossary: required - always "obligatorio"; "requerido" only in rare, well-justified cases.'),
 ("salvar", "guardar", 'Glossary: save - use "guardar", never "salvar".'),
 ("basura", "papelera", 'Glossary: trash - use "papelera", never "basura".'),
 ("aterrizaje", "destino", 'Glossary: landing - use "página de destino", never "aterrizaje".'),
 ("tienda de conveniencia", "tienda de proximidad", 'Glossary: convenience store - the first is common in AI output, unused in Spain.'),
 ("complemento", "plugin (add-on: extensión)", 'Glossary: plugin is not translated; add-on is "extensión", not "complemento".'),
 ("código corto", "shortcode", 'Glossary: shortcode is not translated.'),
 ("código abreviado", "shortcode", 'Glossary: shortcode is not translated.'),
]

P = [
 # dict: kind find|text, value, level, ignoreCase, when(dict), replace, note
 dict(find=r'(sitio|página) web', level='hint', ic=True, when={'notSource':'web'},
      note='Glossary: “site” is “sitio”, not “sitio web” or “página web”, unless the source says website or web page.'),
 dict(find=r'\b[Uu]sted(es)?\b', level='error', ic=False,
      note='WordPress addresses the reader as "tú", never "usted".'),
 dict(find=r'\b[Cc]lick\b', level='error', ic=False,
      note='Spanish spelling is "clic" (no k). Glossary: click.'),
 dict(text='se requiere', level='hint',
      note='Impersonal calque. Prefer a direct form ("Necesitas...").'),
 dict(find=r'[Pp]or favor [^,.;:]', level='hint', ic=False,
      note='A comma follows "Por favor" when a request comes after it.'),
 dict(find=r' {2,}', level='fix', ic=False, replace=' ',
      note='One space between words.'),
 dict(find=r'\b[Ee]stás segur[oa]\b', level='hint', ic=False,
      note='Glossary: are you sure - use "¿Seguro que...?" (works for every gender), not "¿Estás seguro/a...?".'),
 dict(find=r'\b[Bb]ienvenidos?\b|^[Bb]ienvenida\b', level='hint', ic=False, when={'source':'welcome'},
      note='Glossary: Welcome - prefer "Te damos la bienvenida" (gender-neutral). A preference, not a hard rule: accept the gendered form if the neutral one sounds forced.'),
 dict(find=r'\b[Rr]ol(es)?\b', level='hint', ic=False,
      note='Glossary: role - use "perfil/perfiles", never "rol".'),
 dict(find=r'\b[Tt]ours?\b', level='hint', ic=False,
      note='Glossary: tour - use "recorrido", not "tour".'),
 dict(find=r'\b[Mm]ontos?\b', level='hint', ic=False,
      note='Glossary: monto - nobody in Spain says "monto"; use "importe".'),
 dict(find=r'\b[Ll]inks?\b', level='hint', ic=False,
      note='Glossary: link - use "enlace", never "link".'),
 dict(find=r'\b[Pp]ixel(es)?\b', level='hint', ic=False,
      note='Glossary: pixel - spelled with an accent: "píxel/píxeles".'),
 dict(find=r'\b[Hh]osting\b', level='hint', ic=False,
      note='Glossary: hosting - use "alojamiento".'),
 dict(find=r'\b[Cc]arros?\b|\b[Cc]estas?\b', level='hint', ic=False, when={'source':'cart'},
      note='Glossary: cart - use "carrito", never "carro" or "cesta".'),
 dict(find=r'\b[Ee]x[aá]menes\b|\b[Ee]xamen\b', level='hint', ic=False, when={'source':'quiz'},
      note='Glossary: quiz - use "cuestionario", not "examen".'),
 dict(find=r'\b[Rr]eceptor(es)?\b', level='hint', ic=False, when={'source':'receiver'},
      note='Glossary: receiver - use "destinatario", not "receptor".'),
 dict(find=r'\b[Cc]arg(a|ar|as|an|ado|ada|ados|adas|ando|o|ue|uen)\b', level='hint', ic=False, when={'source':'upload'},
      note='Glossary: upload - use "subir/subida", never "cargar/carga".'),
 dict(find=r'\b[Ee]mails?\b', level='hint', ic=False,
      note='Glossary: email - use "correo electrónico" ("dirección de correo electrónico"). Ignore product names and code.'),
 dict(find=r'\b[Aa]greg(ar|a|as|an|ue|uen|amos)\b', level='hint', ic=False,
      note='Glossary: add - use "añadir", never "agregar/agrega". "Agregado" in the sense of aggregated is fine.'),
 dict(find=r'\bBCC\b', level='hint', ic=False,
      note='Glossary: BCC - use the Spanish abbreviation "CCO" (Con Copia Oculta). Ignore header names in code.'),
 dict(find=r'dirección de correo(?! electrónico)', level='hint', ic=True,
      note='Glossary: email address - use "dirección de correo electrónico".'),
 # Round 2 (WGRank) and round 1 follow-ups
 dict(find=r'\b[Ii]dentif(icarse|icarte|icándose|ícate)\b', level='hint', ic=False, when={'source':'log in'},
      note='Glossary: login - "Identificarse" is incorrect; use "Acceder". (Authenticate = "identificar" is fine.)'),
 dict(find=r'\b[Ii]dentif(icarse|icarte|icándose|ícate)\b', level='hint', ic=False, when={'source':'login'},
      note='Glossary: login - "Identificarse" is incorrect; use "Acceder". (Authenticate = "identificar" is fine.)'),
 dict(find=r'\b[Ii]dentif(icarse|icarte|icándose|ícate)\b', level='hint', ic=False, when={'source':'sign in'},
      note='Glossary: sign in - "Identificarse" is incorrect; use "Acceder". (Authenticate = "identificar" is fine.)'),
 dict(find=r'(?<![-\w])(checkout|sliders?|hooks?|frontend|front-end|sitemaps?|firewalls?)(?![-\w])', level='hint', ic=True,
      note='Glossary terms left in English: checkout = "finalizar compra" / "pago"; slider = "carrusel" / "control deslizante"; hook = "gancho"; frontend = "parte pública" / "vista pública"; sitemap = "mapa del sitio"; firewall = "cortafuegos". Ignore code and file names.'),
 dict(find=r'\bcompromiso\b', level='hint', ic=False, when={'source':'engagement'},
      note='Glossary: engagement - use "participación", not "compromiso".'),
 dict(find=r'actualiz\w+ a(l)? (un |tu |el )?plan', level='hint', ic=True, when={'source':'upgrade'},
      note='Glossary: upgrade - "actualizar" for a new version, "mejorar" when moving to a higher plan.'),
 dict(find=r'fragmentos enriquecidos|resultados enriquecidos', level='hint', ic=True,
      note='Glossary: snippet - not translated for search result boxes: use "snippets enriquecidos".'),
 dict(find=r'(?<!p\. )\bej\.', level='hint', ic=False,
      note='Spanish abbreviation is "p. ej." (por ejemplo), not "ej.".'),
 dict(find=r'(?<![=\w])"[^"<>=]+"(?![\w>])', level='hint', ic=False,
      note='Use Spanish quotation marks «...» (nested “...”), not straight quotes. Ignore HTML attributes and code.'),
 dict(find=r"(?<![\w=])'[^'<>]+'(?!\w)", level='hint', ic=False,
      note="Use Spanish quotation marks «...» (nested “...”), not single straight quotes. Ignore code."),
 dict(find=r', [A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(, [A-ZÁÉÍÓÚÑ][a-záéíóúñ]+){2,}', level='hint', ic=False,
      note='A list of capitalized common nouns (languages, plans, options): Spanish writes them in lowercase after the first word. Ignore brand and product names.'),
]

def sv(x):
    if re.search(r': | #|^[-?:,\[\]{}#&*!|>\'"%@`]|:$', x):
        return q(x)
    return x

def emit_m(w, r, n):
    return f"  - wrong: {sv(w)}\n    right: {sv(r)}\n    note: {q(n)}\n"

def emit_p(p):
    out = ''
    if 'find' in p:
        out += f"  - find: {q(p['find'])}\n"
    else:
        out += f"  - text: {p['text']}\n"
    out += f"    level: {p['level']}\n"
    if p.get('replace') is not None:
        out += f"    replace: {q(p['replace'])}\n"
    if 'find' in p and p.get('ic'):
        out += "    ignoreCase: true\n"
    if p.get('when'):
        k, v = next(iter(p['when'].items()))
        out += f"    when: {{{k}: {v}}}\n"
    out += f"    note: {q(p['note'])}\n"
    return out

t = open(SRC, encoding='utf-8').read()

m_start = t.index('mistakes:')
p_comment = t.index('# Literal text or regular expressions')
p_start = t.index('patterns:')
s_comment = t.index('# How a sentence ends')

m_block = 'mistakes:\n' + ''.join(emit_m(*x) for x in M) + '\n'
p_block = 'patterns:\n' + ''.join(emit_p(p) for p in P) + '\n'

new = t[:m_start] + m_block + t[p_comment:p_start] + p_block + t[s_comment:]
G_ADD = ' website = sitio web (site = sitio only); checkout = pago / finalizar compra; slider = carrusel; hook = gancho; frontend = parte pública; sitemap = mapa del sitio; firewall = cortafuegos; engagement = participación; upgrade to a higher plan = mejorar. In changelogs use one verb form for every entry (participle: Añadido, Corregido). Names of languages, plans and tabs are lowercase after the first word.'
G_OLD = '"clic" has no k.\''
assert new.count(G_OLD) == 1
new = new.replace(G_OLD, '"clic" has no k.' + G_ADD + "'")
g = re.search(r"^guidance: (.*)$", new, re.M).group(1)
print('guidance length', len(g))
assert len(g) <= 1500
open(OUT, 'w', encoding='utf-8').write(new)
print('mistakes', len(M), 'patterns', len(P))
