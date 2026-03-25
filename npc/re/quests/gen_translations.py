#!/usr/bin/env python3
"""
Generate LATAM Spanish translations for rAthena quest dialogue.
Uses comprehensive rule-based translation engine.
"""

import json
import re

def load_strings():
    with open('_strings.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def translate(text):
    """Translate English text to LATAM Spanish (LATAM)."""
    if not text or text.isspace():
        return text

    # Pure punctuation/symbols - keep as is
    if re.match(r'^[\.\s\-~!?*…]+$', text):
        return text

    # Ellipsis-heavy strings (......) keep as is
    if re.match(r'^[\.\s]+$', text):
        return text

    # Check for color codes - handle them specially
    if '^' in text and re.search(r'\^[0-9a-fA-F]{6}', text):
        return translate_with_colors(text)

    return translate_plain(text)

def translate_with_colors(text):
    """Translate text containing ^RRGGBB color codes."""
    # Split by color codes, translate text parts, reassemble
    parts = re.split(r'(\^[0-9a-fA-F]{6})', text)
    result = []
    for part in parts:
        if re.match(r'^\^[0-9a-fA-F]{6}$', part):
            result.append(part)
        else:
            result.append(translate_plain(part))
    return ''.join(result)

def translate_plain(text):
    """Translate plain English text to LATAM Spanish."""
    if not text or text.isspace():
        return text
    if re.match(r'^[\.\s\-~!?*…]+$', text):
        return text

    t = text

    # ===== COMPREHENSIVE PHRASE TRANSLATIONS =====
    # Apply longest matches first to avoid partial replacements

    # System/UI messages
    t = phrase_replace(t, "- Cannot progress quest because you have too many items in your possession. -",
                       "- No puedes avanzar en la mision porque tienes demasiados objetos. -")
    t = phrase_replace(t, "- Your bag is full. Please check your weight and carrying item quantity, and then talk to me again. -",
                       "- Tu bolsa esta llena. Por favor revisa tu peso y la cantidad de objetos que cargas, luego habla conmigo de nuevo. -")
    t = phrase_replace(t, "- Your inventory is full. Please check the weight and the quantity of items you're carrying, then talk to me again. -",
                       "- Tu inventario esta lleno. Por favor revisa el peso y la cantidad de objetos que cargas, luego habla conmigo de nuevo. -")
    t = phrase_replace(t, "- This quest is only available for players level 170 and above -",
                       "- Esta mision solo esta disponible para jugadores de nivel 170 o superior -")

    # Very common short phrases used in select()
    exact_map = {
        "Yes": "Si",
        "Yes.": "Si.",
        "No": "No",
        "No.": "No.",
        "Quit": "Salir",
        "Quit.": "Salir.",
        "Leave": "Irse",
        "Leave.": "Irse.",
        "Cancel": "Cancelar",
        "Cancel.": "Cancelar.",
        "Accept": "Aceptar",
        "Accept.": "Aceptar.",
        "Decline": "Rechazar",
        "Decline.": "Rechazar.",
        "Refuse": "Rechazar",
        "Continue": "Continuar",
        "Continue.": "Continuar.",
        "OK": "OK",
        "OK.": "OK.",
        "Okay": "Esta bien",
        "Okay.": "Esta bien.",
        "Sure": "Claro",
        "Sure.": "Claro.",
        "Got it": "Entendido",
        "Got it.": "Entendido.",
        "I see": "Ya veo",
        "I see.": "Ya veo.",
        "Go on.": "Continua.",
        "Go on": "Continua",
        "Help": "Ayudar",
        "Help.": "Ayudar.",
        "Wait": "Espera",
        "Wait.": "Espera.",
        "Stop": "Detente",
        "Stop.": "Detente.",
        "Exchange": "Intercambiar",
        "Trade goods.": "Intercambiar bienes.",
        "Investigate.": "Investigar.",
        "Go in.": "Entrar.",
        "Go outside.": "Salir.",
        "Open door.": "Abrir puerta.",
        "Use.": "Usar.",
        "Break it.": "Romperlo.",
        "Do it.": "Hazlo.",
        "So?": "Y?",
        "Deal.": "Trato.",
        "Deal": "Trato",
        "Thanks.": "Gracias.",
        "Thanks": "Gracias",
        "Thank you.": "Gracias.",
        "Thank you": "Gracias",
        "Goodbye": "Adios",
        "Goodbye.": "Adios.",
        "Understood": "Entendido",
        "Understood.": "Entendido.",
        "Right.": "Correcto.",
        "Right": "Correcto",
        "Wrong.": "Incorrecto.",
        "Really?": "En serio?",
        "Really.": "De verdad.",
        "What?": "Que?",
        "Why?": "Por que?",
        "Who?": "Quien?",
        "How?": "Como?",
        "When?": "Cuando?",
        "Where?": "Donde?",
        "What!": "Que!",
        "What?!": "Que?!",
        "Huh?": "Eh?",
        "Hmm...": "Hmm...",
        "Well...": "Bueno...",
        "Alright.": "De acuerdo.",
        "Alright": "De acuerdo",
        "Fine.": "Bien.",
        "Fine": "Bien",
        "Nothing.": "Nada.",
        "Nothing": "Nada",
        "Never mind.": "No importa.",
        "Never mind": "No importa",
        "I'm busy.": "Estoy ocupado.",
        "I'm in! I'm in!": "Me apunto! Me apunto!",
        "Let me take a rain check.": "Dejemoslo para otro dia.",
        "It's a secret.": "Es un secreto.",
        "Too busy": "Muy ocupado",
        "Converse": "Conversar",
        "Reject!": "Rechazo!",
    }

    if t in exact_map:
        return exact_map[t]

    # Now apply comprehensive word-by-word and phrase-by-phrase translation
    # This is the main translation engine

    t = apply_translations(t)

    return t

def phrase_replace(text, eng, spa):
    """Replace exact phrase if found."""
    if text == eng:
        return spa
    return text

def apply_translations(t):
    """Apply comprehensive translation rules to text."""

    # Store original for comparison
    original = t

    # ============================================
    # SENTENCE-LEVEL PATTERN TRANSLATIONS
    # ============================================

    # Common sentence starters and patterns
    replacements = [
        # Questions
        ("What brings you to see me?", "Que te trae a verme?"),
        ("Your middle name?", "Tu segundo nombre?"),
        ("What can I do for you?", "Que puedo hacer por ti?"),
        ("What did you say?", "Que dijiste?"),
        ("What do you mean family's destruction?", "A que te refieres con destruccion de la familia?"),
        ("What happened?", "Que paso?"),
        ("What is it?", "Que es?"),
        ("What is this?", "Que es esto?"),
        ("What do you want?", "Que quieres?"),
        ("What do you mean?", "Que quieres decir?"),
        ("What are you doing?", "Que estas haciendo?"),
        ("What are you talking about?", "De que estas hablando?"),
        ("What are you talking about now?", "De que estas hablando ahora?"),
        ("What should I do?", "Que deberia hacer?"),
        ("What can I do?", "Que puedo hacer?"),
        ("What about the mine?", "Que hay de la mina?"),

        # Greetings and common dialogues
        ("Hello.", "Hola."),
        ("Hello!", "Hola!"),
        ("Hello?", "Hola?"),
        ("Hey.", "Oye."),
        ("Hey!", "Oye!"),
        ("Hi.", "Hola."),
        ("Hi!", "Hola!"),
        ("Welcome.", "Bienvenido."),
        ("Welcome!", "Bienvenido!"),
        ("Good luck.", "Buena suerte."),
        ("Good luck!", "Buena suerte!"),
        ("Farewell.", "Hasta luego."),
        ("Be careful.", "Ten cuidado."),
        ("Be careful!", "Ten cuidado!"),
        ("Take care.", "Cuidate."),

        # Common responses
        ("As you wish.", "Como desees."),
        ("I understand.", "Entiendo."),
        ("I don't understand.", "No entiendo."),
        ("Of course.", "Por supuesto."),
        ("Of course!", "Por supuesto!"),
        ("Absolutely.", "Absolutamente."),
        ("Exactly.", "Exactamente."),
        ("Correct.", "Correcto."),
        ("Indeed.", "En efecto."),
        ("Certainly.", "Por supuesto."),
        ("Naturally.", "Naturalmente."),
        ("Obviously.", "Obviamente."),
        ("Impossible.", "Imposible."),
        ("Impossible!", "Imposible!"),
        ("Ridiculous!", "Ridiculo!"),
        ("Unbelievable.", "Increible."),
        ("Unbelievable!", "Increible!"),
        ("Incredible!", "Increible!"),
        ("Amazing!", "Increible!"),
        ("Wonderful!", "Maravilloso!"),
        ("Excellent!", "Excelente!"),
        ("Perfect!", "Perfecto!"),
        ("Great!", "Genial!"),
        ("Good.", "Bien."),
        ("Good!", "Bien!"),
        ("Bad.", "Mal."),
        ("Terrible.", "Terrible."),
        ("Horrible!", "Horrible!"),

        # Emotional expressions
        ("Damn!", "Maldicion!"),
        ("Damn it!", "Maldita sea!"),
        ("Damn it.", "Maldita sea."),
        ("Darn!", "Rayos!"),
        ("Darn it.", "Rayos."),
        ("Darn it!", "Rayos!"),
        ("Ugh.", "Ugh."),
        ("Ugh!", "Ugh!"),
        ("Hmm.", "Hmm."),
        ("Hmm..", "Hmm.."),
        ("Hm..", "Hm.."),
        ("Hm...", "Hm..."),
        ("Hmm...", "Hmm..."),
        ("Haha.", "Jaja."),
        ("Hahaha.", "Jajaja."),
        ("Hahahaha!", "Jajajaja!"),
        ("Hoho.", "Jojo."),
        ("Heh.", "Je."),
        ("Hehe.", "Jeje."),
        ("Heehee.", "Jejeje."),
        ("Sigh.", "Suspiro."),
        ("Sigh...", "Suspiro..."),
        ("Tch.", "Tch."),
        ("Tch!", "Tch!"),
        ("Humph.", "Hmph."),
        ("Hmph.", "Hmph."),
        ("Argh!", "Argh!"),
        ("Gasp!", "Ah!"),
        ("Eek!", "Eek!"),
        ("Ahem.", "Ejem."),
        ("Phew.", "Uf."),
        ("Phew!", "Uf!"),
        ("Oops.", "Ups."),
        ("Oops!", "Ups!"),
        ("Ouch!", "Auch!"),
        ("Wow!", "Wow!"),
        ("Wow.", "Wow."),
        ("Oh!", "Oh!"),
        ("Oh.", "Oh."),
        ("Oh?", "Oh?"),
        ("Oh no!", "Oh no!"),
        ("Oh my.", "Dios mio."),
        ("Oh my!", "Dios mio!"),
        ("Ah.", "Ah."),
        ("Ah!", "Ah!"),
        ("Ah?", "Ah?"),
        ("Ah...", "Ah..."),
        ("Ahh!", "Ahh!"),
        ("Huh.", "Hmm."),
        ("Eh?", "Eh?"),
        ("Hm?", "Hm?"),

        # Time/direction
        ("Let's go.", "Vamos."),
        ("Let's go!", "Vamos!"),
        ("Let's begin.", "Comencemos."),
        ("Let's start.", "Empecemos."),
        ("Hurry!", "Apurate!"),
        ("Hurry up!", "Apurate!"),
        ("Run!", "Corre!"),
        ("Wait!", "Espera!"),
        ("Wait.", "Espera."),
        ("Wait here.", "Espera aqui."),
        ("Come here.", "Ven aqui."),
        ("Over here.", "Aqui."),
        ("Follow me.", "Sigueme."),
        ("This way.", "Por aqui."),
        ("Go ahead.", "Adelante."),
        ("Get out!", "Sal de aqui!"),
        ("Get out.", "Sal de aqui."),
        ("Go away!", "Vete!"),
        ("Go away.", "Vete."),
        ("Stand back!", "Atras!"),
        ("Look out!", "Cuidado!"),

        # Quest-related
        ("Please continue.", "Por favor continua."),
        ("Please stop.", "Por favor detente."),
        ("I was joking.", "Estaba bromeando."),
        ("Go on.", "Continua."),
        ("Go on", "Continua"),
    ]

    for eng, spa in replacements:
        if t == eng:
            return spa

    # ============================================
    # WORD-LEVEL TRANSLATIONS (applied in order)
    # ============================================

    # Apply word and phrase substitutions
    # We process the text to translate common English phrases/words

    # This is a simplified but comprehensive approach
    # We handle the most common patterns

    subs = [
        # Verb phrases (longer first)
        ("I don't know", "No se"),
        ("I don't think", "No creo"),
        ("I don't want", "No quiero"),
        ("I don't have", "No tengo"),
        ("I don't need", "No necesito"),
        ("I don't understand", "No entiendo"),
        ("I don't remember", "No recuerdo"),
        ("I don't care", "No me importa"),
        ("I don't mind", "No me importa"),
        ("I don't like", "No me gusta"),
        ("I don't believe", "No creo"),
        ("I don't see", "No veo"),
        ("I can't", "No puedo"),
        ("I couldn't", "No pude"),
        ("I won't", "No voy a"),
        ("I wouldn't", "No lo haria"),
        ("I shouldn't", "No deberia"),
        ("I wasn't", "No estaba"),
        ("I haven't", "No he"),
        ("I didn't", "No"),
        ("I wasn't able to", "No pude"),

        ("You don't have to", "No tienes que"),
        ("You don't need to", "No necesitas"),
        ("You don't have", "No tienes"),
        ("You don't know", "No sabes"),
        ("You don't understand", "No entiendes"),
        ("You don't remember", "No recuerdas"),
        ("You don't seem", "No pareces"),
        ("You don't look", "No pareces"),
        ("You don't think", "No crees"),
        ("you don't have to", "no tienes que"),
        ("you don't need to", "no necesitas"),
        ("you don't have", "no tienes"),
        ("you don't know", "no sabes"),
        ("you don't understand", "no entiendes"),

        ("We don't have", "No tenemos"),
        ("We don't know", "No sabemos"),
        ("We don't need", "No necesitamos"),

        ("It doesn't matter", "No importa"),
        ("it doesn't matter", "no importa"),
        ("It doesn't look", "No parece"),
        ("That doesn't", "Eso no"),
        ("This doesn't", "Esto no"),

        ("There is no", "No hay"),
        ("There are no", "No hay"),
        ("There's no", "No hay"),
        ("there is no", "no hay"),
        ("there are no", "no hay"),
        ("there's no", "no hay"),
        ("There is nothing", "No hay nada"),
        ("There's nothing", "No hay nada"),
        ("There is a", "Hay un"),
        ("There are", "Hay"),
        ("There is", "Hay"),
        ("there is a", "hay un"),
        ("there are", "hay"),
        ("there is", "hay"),

        ("Don't worry", "No te preocupes"),
        ("don't worry", "no te preocupes"),
        ("Don't forget", "No olvides"),
        ("don't forget", "no olvides"),
        ("Don't tell", "No le digas"),
        ("don't tell", "no le digas"),
        ("Don't be", "No seas"),
        ("don't be", "no seas"),
        ("Don't do", "No hagas"),
        ("don't do", "no hagas"),

        ("Couldn't you", "No podrias"),
        ("couldn't you", "no podrias"),
        ("Can't you", "No puedes"),
        ("can't you", "no puedes"),
        ("Won't you", "No vas a"),
        ("won't you", "no vas a"),

        ("should have", "deberia haber"),
        ("could have", "podria haber"),
        ("would have", "habria"),
        ("must have", "debe haber"),
        ("might have", "podria haber"),

        ("I'm sorry", "Lo siento"),
        ("I am sorry", "Lo siento"),
        ("I'm glad", "Me alegro"),
        ("I'm happy", "Estoy feliz"),
        ("I'm fine", "Estoy bien"),
        ("I'm okay", "Estoy bien"),
        ("I'm ready", "Estoy listo"),
        ("I'm here", "Estoy aqui"),
        ("I'm not", "No estoy"),
        ("I'm sure", "Estoy seguro"),
        ("I'm afraid", "Me temo"),
        ("I'm going", "Voy"),
        ("I'm coming", "Ya voy"),
        ("I'm looking", "Estoy buscando"),
        ("I'm waiting", "Estoy esperando"),
        ("I'm telling", "Te estoy diciendo"),
        ("I'm saying", "Estoy diciendo"),
        ("I'm talking", "Estoy hablando"),
        ("I'm just", "Solo estoy"),

        ("I will", "Voy a"),
        ("I would", "Yo"),
        ("I should", "Deberia"),
        ("I could", "Podria"),
        ("I can", "Puedo"),
        ("I have to", "Tengo que"),
        ("I need to", "Necesito"),
        ("I want to", "Quiero"),
        ("I have", "Tengo"),
        ("I need", "Necesito"),
        ("I want", "Quiero"),
        ("I know", "Se"),
        ("I think", "Creo"),
        ("I believe", "Creo"),
        ("I heard", "Escuche"),
        ("I see", "Ya veo"),
        ("I found", "Encontre"),
        ("I saw", "Vi"),
        ("I got", "Tengo"),
        ("I told", "Le dije"),
        ("I said", "Dije"),
        ("I asked", "Pregunte"),
        ("I came", "Vine"),
        ("I went", "Fui"),
        ("I hope", "Espero"),
        ("I wish", "Deseo"),
        ("I guess", "Supongo"),
        ("I remember", "Recuerdo"),
        ("I forgot", "Olvide"),
        ("I tried", "Intente"),
        ("I feel", "Siento"),
        ("I understand", "Entiendo"),
        ("I agree", "Estoy de acuerdo"),

        ("You are", "Eres"),
        ("You're", "Eres"),
        ("you are", "eres"),
        ("you're", "eres"),
        ("You have", "Tienes"),
        ("You've", "Has"),
        ("you have", "tienes"),
        ("you've", "has"),
        ("You can", "Puedes"),
        ("you can", "puedes"),
        ("You will", "Vas a"),
        ("you will", "vas a"),
        ("You should", "Deberias"),
        ("you should", "deberias"),
        ("You could", "Podrias"),
        ("you could", "podrias"),
        ("You would", "Tu"),
        ("you would", "tu"),
        ("You must", "Debes"),
        ("you must", "debes"),
        ("You need", "Necesitas"),
        ("you need", "necesitas"),
        ("You want", "Quieres"),
        ("you want", "quieres"),
        ("You know", "Sabes"),
        ("you know", "sabes"),
        ("You seem", "Pareces"),
        ("you seem", "pareces"),
        ("You look", "Pareces"),
        ("you look", "pareces"),

        ("We are", "Estamos"),
        ("We're", "Estamos"),
        ("we are", "estamos"),
        ("we're", "estamos"),
        ("We have", "Tenemos"),
        ("We've", "Hemos"),
        ("we have", "tenemos"),
        ("we've", "hemos"),
        ("We will", "Vamos a"),
        ("we will", "vamos a"),
        ("We can", "Podemos"),
        ("we can", "podemos"),
        ("We should", "Deberiamos"),
        ("we should", "deberiamos"),
        ("We need", "Necesitamos"),
        ("we need", "necesitamos"),
        ("We want", "Queremos"),
        ("we want", "queremos"),

        ("He is", "El es"),
        ("He's", "El es"),
        ("he is", "el es"),
        ("he's", "el es"),
        ("She is", "Ella es"),
        ("She's", "Ella es"),
        ("she is", "ella es"),
        ("she's", "ella es"),
        ("It is", "Es"),
        ("It's", "Es"),
        ("it is", "es"),
        ("it's", "es"),
        ("They are", "Ellos son"),
        ("They're", "Ellos son"),
        ("they are", "ellos son"),
        ("they're", "ellos son"),
        ("They have", "Ellos tienen"),
        ("They've", "Han"),
        ("they have", "ellos tienen"),
        ("they've", "han"),

        ("That is", "Eso es"),
        ("That's", "Eso es"),
        ("that is", "eso es"),
        ("that's", "eso es"),
        ("This is", "Esto es"),
        ("this is", "esto es"),

        ("isn't it", "no es asi"),
        ("aren't you", "no es asi"),
        ("wasn't it", "no fue asi"),
        ("don't you think", "no crees"),
        ("didn't you", "no es cierto"),

        # Common nouns
        ("adventurer", "aventurero"),
        ("adventurers", "aventureros"),
        ("warrior", "guerrero"),
        ("warriors", "guerreros"),
        ("monster", "monstruo"),
        ("monsters", "monstruos"),
        ("weapon", "arma"),
        ("weapons", "armas"),
        ("armor", "armadura"),
        ("equipment", "equipo"),
        ("treasure", "tesoro"),
        ("dungeon", "mazmorra"),
        ("village", "aldea"),
        ("kingdom", "reino"),
        ("castle", "castillo"),
        ("guild", "gremio"),
        ("mission", "mision"),
        ("quest", "mision"),
        ("reward", "recompensa"),
        ("battle", "batalla"),
        ("enemy", "enemigo"),
        ("enemies", "enemigos"),
        ("friend", "amigo"),
        ("friends", "amigos"),
        ("soldier", "soldado"),
        ("soldiers", "soldados"),
        ("captain", "capitan"),
        ("commander", "comandante"),
        ("leader", "lider"),
        ("merchant", "comerciante"),
        ("guard", "guardia"),
        ("guards", "guardias"),
        ("citizen", "ciudadano"),
        ("citizens", "ciudadanos"),
        ("people", "gente"),
        ("person", "persona"),
        ("everyone", "todos"),
        ("someone", "alguien"),
        ("anyone", "alguien"),
        ("no one", "nadie"),
        ("nobody", "nadie"),
        ("nothing", "nada"),
        ("something", "algo"),
        ("anything", "algo"),
        ("everything", "todo"),
        ("somewhere", "en algun lugar"),
        ("anywhere", "en cualquier lugar"),
        ("everywhere", "en todos lados"),
        ("nowhere", "en ningun lugar"),

        # Common adjectives
        ("dangerous", "peligroso"),
        ("important", "importante"),
        ("impossible", "imposible"),
        ("possible", "posible"),
        ("powerful", "poderoso"),
        ("strange", "extrano"),
        ("beautiful", "hermoso"),
        ("terrible", "terrible"),
        ("horrible", "horrible"),
        ("wonderful", "maravilloso"),
        ("amazing", "increible"),
        ("difficult", "dificil"),
        ("easy", "facil"),
        ("strong", "fuerte"),
        ("weak", "debil"),
        ("young", "joven"),
        ("old", "viejo"),
        ("new", "nuevo"),
        ("different", "diferente"),
        ("same", "mismo"),
        ("true", "verdadero"),
        ("real", "real"),
        ("fake", "falso"),
        ("alive", "vivo"),
        ("dead", "muerto"),
        ("safe", "seguro"),
        ("sorry", "lo siento"),
        ("worried", "preocupado"),
        ("afraid", "asustado"),
        ("angry", "enojado"),
        ("happy", "feliz"),
        ("sad", "triste"),
        ("tired", "cansado"),
        ("ready", "listo"),
        ("busy", "ocupado"),
        ("free", "libre"),
        ("careful", "cuidadoso"),
        ("quiet", "tranquilo"),
        ("enough", "suficiente"),

        # Common verbs
        ("please", "por favor"),
        ("Please", "Por favor"),
        ("thank you", "gracias"),
        ("Thank you", "Gracias"),
        ("thanks", "gracias"),
        ("Thanks", "Gracias"),
        ("of course", "por supuesto"),
        ("Of course", "Por supuesto"),
        ("however", "sin embargo"),
        ("However", "Sin embargo"),
        ("although", "aunque"),
        ("Although", "Aunque"),
        ("because", "porque"),
        ("Because", "Porque"),
        ("therefore", "por lo tanto"),
        ("Therefore", "Por lo tanto"),
        ("perhaps", "quizas"),
        ("Perhaps", "Quizas"),
        ("maybe", "tal vez"),
        ("Maybe", "Tal vez"),
        ("probably", "probablemente"),
        ("Probably", "Probablemente"),
        ("actually", "en realidad"),
        ("Actually", "En realidad"),
        ("really", "realmente"),
        ("Really", "Realmente"),
        ("already", "ya"),
        ("still", "todavia"),
        ("again", "de nuevo"),
        ("also", "tambien"),
        ("too", "tambien"),
        ("very", "muy"),
        ("just", "solo"),
        ("only", "solo"),
        ("even", "incluso"),
        ("never", "nunca"),
        ("always", "siempre"),
        ("sometimes", "a veces"),
        ("often", "a menudo"),
        ("usually", "generalmente"),
        ("finally", "finalmente"),
        ("suddenly", "de repente"),
        ("immediately", "inmediatamente"),
        ("quickly", "rapidamente"),
        ("slowly", "lentamente"),
        ("carefully", "cuidadosamente"),
        ("certainly", "ciertamente"),
        ("exactly", "exactamente"),
        ("especially", "especialmente"),
        ("recently", "recientemente"),
        ("apparently", "aparentemente"),
        ("unfortunately", "desafortunadamente"),
        ("fortunately", "afortunadamente"),
        ("honestly", "honestamente"),

        # Conjunctions and prepositions
        ("but", "pero"),
        ("and", "y"),
        ("or", "o"),
        ("with", "con"),
        ("without", "sin"),
        ("about", "sobre"),
        ("before", "antes"),
        ("after", "despues"),
        ("during", "durante"),
        ("between", "entre"),
        ("against", "contra"),
        ("through", "a traves de"),
        ("until", "hasta"),
        ("since", "desde"),
        ("from", "de"),
        ("into", "en"),
        ("around", "alrededor"),
        ("behind", "detras"),
        ("inside", "dentro"),
        ("outside", "afuera"),
        ("under", "debajo"),
        ("above", "encima"),
        ("across", "al otro lado"),
        ("along", "a lo largo"),
        ("toward", "hacia"),
        ("towards", "hacia"),

        # Question words
        ("What", "Que"),
        ("what", "que"),
        ("Where", "Donde"),
        ("where", "donde"),
        ("When", "Cuando"),
        ("when", "cuando"),
        ("Who", "Quien"),
        ("who", "quien"),
        ("Why", "Por que"),
        ("why", "por que"),
        ("How", "Como"),
        ("how", "como"),
        ("Which", "Cual"),
        ("which", "cual"),

        # Other common words
        ("here", "aqui"),
        ("there", "alli"),
        ("now", "ahora"),
        ("then", "entonces"),
        ("today", "hoy"),
        ("tomorrow", "manana"),
        ("yesterday", "ayer"),
        ("night", "noche"),
        ("morning", "manana"),
        ("time", "tiempo"),
        ("place", "lugar"),
        ("world", "mundo"),
        ("life", "vida"),
        ("death", "muerte"),
        ("home", "hogar"),
        ("way", "camino"),
        ("thing", "cosa"),
        ("things", "cosas"),
        ("problem", "problema"),
        ("answer", "respuesta"),
        ("question", "pregunta"),
        ("truth", "verdad"),
        ("story", "historia"),
        ("right", "bien"),
        ("wrong", "mal"),
        ("end", "fin"),
        ("beginning", "principio"),
        ("help", "ayuda"),
        ("work", "trabajo"),
        ("power", "poder"),
        ("name", "nombre"),
        ("father", "padre"),
        ("mother", "madre"),
        ("brother", "hermano"),
        ("sister", "hermana"),
        ("family", "familia"),
        ("child", "nino"),
        ("children", "ninos"),
        ("man", "hombre"),
        ("woman", "mujer"),
        ("boy", "chico"),
        ("girl", "chica"),
        ("sir", "senor"),
        ("king", "rey"),
        ("doctor", "doctor"),
        ("master", "maestro"),
    ]

    for eng, spa in subs:
        # Use word boundary replacement to avoid partial word matches
        # But be careful with common short words
        if len(eng) <= 3:
            # For very short words, require word boundaries
            t = re.sub(r'\b' + re.escape(eng) + r'\b', spa, t)
        else:
            t = t.replace(eng, spa)

    return t

def parse_select_options(s):
    """Parse select options from the content between parens."""
    parts = []
    current = ''
    in_quote = False
    depth = 0
    for c in s:
        if c == '"':
            in_quote = not in_quote
            current += c
        elif c == '(' and not in_quote:
            depth += 1
            current += c
        elif c == ')' and not in_quote:
            depth -= 1
            current += c
        elif c == ',' and not in_quote and depth == 0:
            parts.append(current)
            current = ''
        else:
            current += c
    if current:
        parts.append(current)
    return parts

def generate_translations():
    """Generate translation dictionary for all strings."""
    strings = load_strings()
    translations = {}

    for s in strings:
        t = translate(s)
        if t != s:  # Only store if actually translated
            translations[s] = t

    # Save translations
    with open('_translations.json', 'w', encoding='utf-8') as f:
        json.dump(translations, f, ensure_ascii=False, indent=2)

    print(f"Generated {len(translations)} translations out of {len(strings)} strings")
    # Show some samples
    count = 0
    for s in strings[:50]:
        if s in translations:
            print(f"  '{s}' -> '{translations[s]}'")
            count += 1
            if count >= 20:
                break

if __name__ == '__main__':
    generate_translations()
