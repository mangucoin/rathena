#!/usr/bin/env python3
"""
Comprehensive English -> LATAM Spanish translator for rAthena quest scripts.
Translates mes "..." and select("...") using full-sentence translation dictionary.
Preserves all code logic, variables, color codes, NPC names in brackets.
"""
import re
import sys
import os

# =============================================================================
# FULL SENTENCE TRANSLATION DICTIONARY
# Each English string maps to its proper LATAM Spanish translation
# =============================================================================

SENTENCE_MAP = {
    # ===== GENERIC/UI STRINGS =====
    "^3355FFNext^000000": "^3355FFSiguiente^000000",
    "^3355FFClose^000000": "^3355FFCerrar^000000",

    # ===== INVENTORY FULL MESSAGES =====
    "^3355FFWait a second! Right now,": "^3355FFEspera un momento! Ahora mismo,",
    "you have too many items in your inventory. Please come back after you've freed up more inventory space.^000000": "tienes demasiados objetos en tu inventario. Por favor vuelve cuando hayas liberado espacio en tu inventario.^000000",
    "you have too many items in your inventory. Please come back after you've made more available inventory space.^000000": "tienes demasiados objetos en tu inventario. Por favor vuelve cuando hayas liberado mas espacio en tu inventario.^000000",

    # ===== THE SIGN QUEST - METZ =====
    "Although you need everlasting patience in an archaeological excavation, the feeling you get when you find something makes": "Aunque necesitas una paciencia eterna en una excavacion arqueologica, la sensacion que tienes cuando encuentras algo hace que",
    "all those long hours of study and research worth it.": "todas esas largas horas de estudio e investigacion valgan la pena.",
    "Hm...?": "Hm...?",
    "Can I help you?": "Puedo ayudarte?",
    "Great...!": "Genial...!",
    "Welcome to my": "Bienvenido a mi",
    "humble lodgings.": "humilde morada.",
    "Hmm, let me see...": "Hmm, dejame ver...",
    "Uh, it pains me to say this, but I don't think you qualified to help me out. Once you gain enough experience though, I'll be happy to have you on board~": "Uh, me duele decir esto, pero no creo que estes calificado para ayudarme. Pero cuando ganes suficiente experiencia, estare encantado de tenerte a bordo~",
    "Hey, I think you might": "Oye, creo que podrias",
    "be well suited for the job!": "ser muy adecuado para el trabajo!",
    "But do you think you could come back later? I've got my hands full with some other business.": "Pero crees que podrias volver despues? Tengo las manos llenas con otros asuntos.",
    "Oh right, would you tell": "Ah cierto, me dirias",
    "Okay then, I'll remember that.": "Muy bien, lo recordare.",
    "Talk to you later, alright?": "Hablamos despues, de acuerdo?",
    "Oh really?": "Ah, de verdad?",
    "I see, I thought you": "Ya veo, pense que eras",
    "were an applicant for": "un candidato para",
    "the position I'm offering": "el puesto que estoy ofreciendo",
    "to brave adventurers.": "a valientes aventureros.",
    "I'm sorry I made you wait,": "Lamento haberte hecho esperar,",
    "but I had some research to finish and it took longer than I expected. Now, before I tell you more about the job, I want to test your competency.": "pero tenia una investigacion que terminar y tomo mas tiempo del que esperaba. Ahora, antes de contarte mas sobre el trabajo, quiero probar tu competencia.",
    "The job I'm offering is": "El trabajo que ofrezco es",
    "pretty risky and not just": "bastante arriesgado y no cualquiera",
    "anybody can handle it.": "puede manejarlo.",
    "You'll actually go through": "De hecho pasaras por",
    "a series of tests conducted": "una serie de pruebas realizadas",
    "by my trusted friends.": "por mis amigos de confianza.",
    "Now, the first person": "Ahora, la primera persona",
    "you must visit is ^FF0000Arian^000000": "que debes visitar es ^FF0000Arian^000000",
    "in Morocc. Please speak": "en Morocc. Por favor habla",
    "to him and he'll give you": "con el y te dara",
    "all the details about his": "todos los detalles sobre su",
    "examination... I hope.": "examen... eso espero.",
    "Once you're finished with": "Una vez que termines con",
    "the test, Arian will tell you": "la prueba, Arian te dira",
    "what to do next. Afterwards,": "que hacer despues. Luego,",
    "come back to me so that we": "vuelve a mi para que",
    "can finally talk business.": "finalmente hablemos de negocios.",
    "Ah, almost forgot.": "Ah, casi lo olvido.",
    "Arian won't talk to anybody": "Arian no hablara con nadie",
    "unless he knows them or": "a menos que los conozca o",
    "receives a message from me.": "reciba un mensaje mio.",
    "So if he's snubbed you in the past, just understand that's his way.": "Asi que si te ha ignorado en el pasado, entiende que asi es el.",
    "Shouldn't you leave": "No deberias ir",
    "for Morocc to see Arian?": "a Morocc a ver a Arian?",
    "You better hurry in case": "Mejor date prisa por si",
    "somebody else applies": "alguien mas se postula",
    "for this little job.": "para este trabajito.",
    "I don't know if you realize": "No se si te das cuenta,",
    "it, but I'm offering a golden": "pero estoy ofreciendo una oportunidad",
    "opportunity for the adventurer": "de oro para el aventurero",
    "who works for me. So don't": "que trabaje para mi. Asi que no",
    "hesitate to see Arian.": "dudes en ver a Arian.",
    "And just so you know,": "Y para que lo sepas,",
    "it's not a good idea to": "no es buena idea",
    "judge Arian by his looks.": "juzgar a Arian por su apariencia.",
    "He's more than meets": "Es mas de lo que aparenta",
    "the eye, you know.": "a simple vista, sabes.",
    "I'm impressed that": "Estoy impresionado de que",
    "you managed to get": "lograras obtener",
    "Arian's approval! Oh,": "la aprobacion de Arian! Oh,",
    "and how's Daewoon?": "y como esta Daewoon?",
    "He's a character, isn't he?": "Es todo un personaje, no?",
    "I'm not surprised": "No me sorprende",
    "that Daewoon likes": "que a Daewoon le",
    "you. Ah, but Jore is": "agrades. Ah, pero Jore",
    "always busy. Still, if you": "siempre esta ocupado. Aun asi, si",
    "know his schedule, you": "conoces su horario,",
    "should be alright.": "deberia estar bien.",
    "Jesqurienne is": "Jesqurienne es",
    "a brilliant woman.": "una mujer brillante.",
    "Although I worry a": "Aunque me preocupa",
    "little bit about her": "un poco su",
    "overconfidence, she's": "exceso de confianza,",
    "a good friend of mine.": "es una buena amiga mia.",
    "Dearles...?": "Dearles...?",
    "Ah yes, he's one": "Ah si, es uno",
    "of my shadier friends.": "de mis amigos mas turbios.",
    "He's difficult to find": "Es dificil de encontrar",
    "and he's only truly kind": "y solo es realmente amable",
    "to a select few, so...": "con unos pocos, asi que...",
    "It certainly doesn't": "Ciertamente no",
    "help that he's hopelessly": "ayuda que este perdidamente",
    "addicted to gambling...": "adicto al juego...",
    "Ah, Bakerlan~": "Ah, Bakerlan~",
    "I've heard that he's": "He escuchado que ha",
    "been quite busy lately.": "estado bastante ocupado ultimamente.",
    "But that's how all big": "Pero asi son todos los grandes",
    "businessmen are, I suppose.": "empresarios, supongo.",
    "Congratulations~": "Felicidades~",
    "You managed to pass": "Lograste pasar",
    "all of the tests! You seem": "todas las pruebas! Pareces",
    "to be the perfect person": "ser la persona perfecta",
    "to carry out this special": "para llevar a cabo esta",
    "assignment!": "mision especial!",
    "By now, you must have": "A estas alturas, debes tener",
    "six Sobbing Starlight pieces.": "seis piezas de Sobbing Starlight.",
    "I'm sure that you want to know": "Estoy seguro de que quieres saber",
    "more about these fragments.": "mas sobre estos fragmentos.",
    "I remember last summer,": "Recuerdo el verano pasado,",
    "I found the wholly formed": "encontre el Sobbing Starlight",
    "Sobbing Starlight north": "completamente formado al norte",
    "of Mount Mjolnir during": "del Monte Mjolnir durante",
    "one of my expeditions...": "una de mis expediciones...",
    "Although it was in perfect": "Aunque estaba en perfecto",
    "shape, once it was exposed": "estado, una vez que se expuso",
    "to the air, it began to crack": "al aire, comenzo a agrietarse",
    "and shattered into the pieces": "y se rompio en los pedazos",
    "you now hold in your hand.": "que ahora tienes en tu mano.",
    "Now, an ordinary artisan": "Ahora, un artesano comun",
    "can't put the Sobbing Starlight": "no puede armar el Sobbing Starlight",
    "back together. This mysterious stone has some strange properties. But it's imperative for me to get this stone reassembled.": "de nuevo. Esta piedra misteriosa tiene propiedades extranas. Pero es imperativo para mi que esta piedra sea reensamblada.",
    "Once restored, a strange": "Una vez restaurada, un extrano",
    "pattern can be seen within": "patron se puede ver dentro",
    "the Sobbing Starlight. I guess": "del Sobbing Starlight. Supongo",
    "that the pattern is a message": "que el patron es un mensaje",
    "written in an ancient language.": "escrito en un idioma antiguo.",
    "Would you let me borrow": "Me dejarias tomar prestadas",
    "the pieces for a second?": "las piezas un momento?",
    "I'll show you something": "Te mostrare algo",
    "quite interesting...": "bastante interesante...",
    "^3355FFOnce you hand the pieces": "^3355FFUna vez que le entregas las piezas",
    "of the Sobbing Starlight to": "del Sobbing Starlight a",
    "Metz, he pulls out a seventh": "Metz, el saca una septima",
    "piece. Once gathered, they": "pieza. Una vez reunidas,",
    "begin to emit a strange light.^000000": "comienzan a emitir una luz extrana.^000000",
    "Since the pieces still": "Ya que las piezas aun",
    "respond to each other,": "reaccionan entre si,",
    "I believe that it's possible": "creo que es posible",
    "for the Sobbing Starlight": "que el Sobbing Starlight",
    "to be restored to its": "sea restaurado a su",
    "original form.": "forma original.",
    "We're still seeking": "Aun estamos buscando",
    "an artisan of great": "un artesano de gran",
    "skill for this task. Once": "habilidad para esta tarea. Una vez que",
    "know right away. For now,": "lo sepa te aviso. Por ahora,",
    "please hold on to these pieces.": "por favor conserva estas piezas.",
}

# Build a comprehensive map by reading all the dialogue
# For strings not in the map, we'll apply contextual translation


def translate_content(content):
    """Translate a mes content string or select option."""
    if not content:
        return content

    # Check exact match first
    if content in SENTENCE_MAP:
        return SENTENCE_MAP[content]

    # For strings with variable interpolation, try to match the static parts
    # e.g., "me your name? "+ strcharinfo(0) +"?"
    # We handle these by checking if the non-variable parts have translations

    # If no match found, apply the contextual translation
    return contextual_translate(content)


def contextual_translate(text):
    """
    Translate English text to proper LATAM Spanish.
    Uses comprehensive phrase and sentence pattern matching.
    """
    if not text or not text.strip():
        return text

    # Don't translate if it's mostly non-alphabetic
    alpha_chars = sum(1 for c in text if c.isalpha())
    if alpha_chars < 3:
        return text

    # Don't translate color-code-only content
    clean = re.sub(r'\^[0-9a-fA-F]{6}', '', text)
    if not clean.strip() or len(clean.strip()) < 3:
        return text

    # Split on variable references to translate only text parts
    parts = re.split(r'("?\+[^"]+\+"?)', text)
    result_parts = []
    for part in parts:
        if part.startswith('+') or part.startswith('"+') or part.startswith('"+ '):
            result_parts.append(part)
        else:
            result_parts.append(translate_pure_text(part))

    return ''.join(result_parts)


def translate_pure_text(text):
    """Translate pure text (no variables) from English to LATAM Spanish."""
    if not text or not text.strip():
        return text

    # Check in sentence map
    stripped = text.strip()
    if stripped in SENTENCE_MAP:
        leading = text[:len(text) - len(text.lstrip())]
        trailing = text[len(text.rstrip()):]
        return leading + SENTENCE_MAP[stripped] + trailing

    # Apply comprehensive phrase-level replacements
    # These are applied as whole-word replacements
    result = text

    # Apply sentence-level pattern translations
    patterns = get_translation_patterns()
    for eng, esp in patterns:
        if eng in result:
            result = result.replace(eng, esp)

    return result


def get_translation_patterns():
    """Return ordered list of (english, spanish) phrase replacements."""
    return [
        # Long phrases first (to avoid partial matches)
        ("I don't think you", "no creo que tu"),
        ("I don't know what", "no se que"),
        ("I don't know if", "no se si"),
        ("I don't know", "no lo se"),
        ("I don't have", "no tengo"),
        ("I don't want", "no quiero"),
        ("I don't care", "no me importa"),
        ("I don't understand", "no entiendo"),
        ("I don't believe", "no creo"),
        ("I don't remember", "no recuerdo"),
        ("I don't mind", "no me molesta"),
        ("you don't have", "no tienes"),
        ("you don't know", "no sabes"),
        ("you don't understand", "no entiendes"),
        ("I can't believe", "no puedo creer"),
        ("I can't help", "no puedo evitar"),
        ("I can't stop", "no puedo parar"),
        ("I can't wait", "no puedo esperar"),
        ("I'm sorry, but", "lo siento, pero"),
        ("I'm sorry that", "lamento que"),
        ("I'm sorry.", "lo siento."),
        ("I'm sorry,", "lo siento,"),
        ("I'm sorry", "lo siento"),
        ("Thank you so much!", "Muchas gracias!"),
        ("Thank you so much", "Muchas gracias"),
        ("Thank you very much", "Muchas gracias"),
        ("Thank you for", "Gracias por"),
        ("thank you for", "gracias por"),
        ("Thank you.", "Gracias."),
        ("Thank you", "Gracias"),
        ("thank you", "gracias"),
        ("Thanks for", "Gracias por"),
        ("thanks for", "gracias por"),
        ("Thanks.", "Gracias."),
        ("Thanks", "Gracias"),
        ("Don't worry", "No te preocupes"),
        ("don't worry", "no te preocupes"),
        ("Don't you", "No"),
        ("don't you", "no"),
        ("Welcome to the", "Bienvenido al"),
        ("Welcome to", "Bienvenido a"),
        ("Welcome.", "Bienvenido."),
        ("Welcome", "Bienvenido"),
        ("Good luck~", "Buena suerte~"),
        ("Good luck.", "Buena suerte."),
        ("Good luck,", "Buena suerte,"),
        ("Good luck", "Buena suerte"),
        ("good luck", "buena suerte"),
        ("Take care.", "Cuidate."),
        ("Take care,", "Cuidate,"),
        ("Take care", "Cuidate"),
        ("take care", "cuidate"),
        ("Excuse me...", "Disculpa..."),
        ("Excuse me.", "Disculpa."),
        ("Excuse me", "Disculpa"),
        ("EXCUSE ME!", "DISCULPA!"),
        ("Of course", "Por supuesto"),
        ("of course", "por supuesto"),
        ("In any case", "En todo caso"),
        ("in any case", "en todo caso"),
        ("In the end", "Al final"),
        ("in the end", "al final"),
        ("After all", "Despues de todo"),
        ("after all", "despues de todo"),
        ("In fact", "De hecho"),
        ("in fact", "de hecho"),
        ("By the way", "Por cierto"),
        ("by the way", "por cierto"),
        ("For now", "Por ahora"),
        ("for now", "por ahora"),
        ("Right now", "Ahora mismo"),
        ("right now", "ahora mismo"),
        ("Right away", "De inmediato"),
        ("right away", "de inmediato"),
        ("However,", "Sin embargo,"),
        ("however,", "sin embargo,"),
        ("However", "Sin embargo"),
        ("however", "sin embargo"),
        ("Although", "Aunque"),
        ("although", "aunque"),
        ("Unfortunately", "Desafortunadamente"),
        ("unfortunately", "desafortunadamente"),
        ("Apparently", "Aparentemente"),
        ("apparently", "aparentemente"),
        ("Actually", "En realidad"),
        ("actually", "en realidad"),
        ("Congratulations", "Felicidades"),
        ("congratulations", "felicidades"),
        ("Please come back", "Por favor regresa"),
        ("please come back", "por favor regresa"),
        ("Come back", "Vuelve"),
        ("come back", "vuelve"),
        ("Please wait", "Por favor espera"),
        ("please wait", "por favor espera"),
        ("Please leave", "Por favor vete"),
        ("please leave", "por favor vete"),
        ("Please don't", "Por favor no"),
        ("please don't", "por favor no"),
        ("Please", "Por favor"),
        ("please", "por favor"),
        ("What are you", "Que estas"),
        ("what are you", "que estas"),
        ("What do you", "Que"),
        ("What is the", "Cual es el"),
        ("What is", "Que es"),
        ("Where is", "Donde esta"),
        ("Who are you", "Quien eres"),
        ("How are you", "Como estas"),
        ("Are you ready", "Estas listo"),
        ("Are you sure", "Estas seguro"),
        ("Do you have", "Tienes"),
        ("Do you know", "Sabes"),
        ("Do you think", "Crees"),
        ("Do you want", "Quieres"),
        ("Have you heard", "Has escuchado"),
        ("Have you ever", "Alguna vez has"),
        ("Have you been", "Has estado"),
        ("Would you like", "Te gustaria"),
        ("Would you please", "Podrias por favor"),
        ("Could you please", "Podrias por favor"),
        ("I'll be", "Estare"),
        ("I'll do", "Lo hare"),
        ("I'll have", "Tendre"),
        ("I'll give", "Te dare"),
        ("I'll take", "Tomare"),
        ("I'll try", "Intentare"),
        ("I'll wait", "Esperare"),
        ("I'll see", "Vere"),
        ("I'll come", "Vendre"),
        ("I'll go", "Ire"),
        ("I'll tell", "Te dire"),
        ("I'll send", "Enviare"),
        ("Let me see", "Dejame ver"),
        ("let me see", "dejame ver"),
        ("Let me think", "Dejame pensar"),
        ("Let's see", "Veamos"),
        ("let's see", "veamos"),
        ("Let's go", "Vamos"),
        ("my friend", "mi amigo"),
        ("my friends", "mis amigos"),
        ("your friend", "tu amigo"),
        ("a long time", "mucho tiempo"),
        ("long time", "mucho tiempo"),
        ("this time", "esta vez"),
        ("next time", "la proxima vez"),
        ("at this moment", "en este momento"),
        ("at the moment", "por el momento"),
        ("at least", "al menos"),
        ("at all", "en absoluto"),
        ("so long as", "siempre y cuando"),
        ("as well as", "asi como"),
        ("as well", "tambien"),
        ("as soon as", "tan pronto como"),
        ("once again", "una vez mas"),
        ("Once again", "Una vez mas"),
        ("instead of", "en lugar de"),
        ("Instead of", "En lugar de"),
        ("because of", "debido a"),
        ("Because of", "Debido a"),
        ("on your own", "por tu cuenta"),
        ("on my own", "por mi cuenta"),
        ("I wonder", "Me pregunto"),
        ("I suppose", "Supongo"),
        ("I guess", "Supongo"),
        ("I wish", "Deseo"),
        ("I heard", "Escuche"),
        ("I hope", "Espero"),
        ("I believe", "Creo"),
        ("I think", "Creo"),
        ("I know", "Se"),
        ("I feel", "Siento"),
        ("I need", "Necesito"),
        ("I want", "Quiero"),
        ("I have", "Tengo"),
        ("I've heard", "He escuchado"),
        ("I've been", "He estado"),
        ("I've got", "Tengo"),
        ("I've never", "Nunca he"),
        ("you know", "sabes"),
        ("You know", "Sabes"),
        ("you see", "veras"),
        ("You see", "Veras"),
        ("you should", "deberias"),
        ("You should", "Deberias"),
        ("you must", "debes"),
        ("You must", "Debes"),
        ("you need", "necesitas"),
        ("You need", "Necesitas"),
        ("you want", "quieres"),
        ("You want", "Quieres"),
        ("you can", "puedes"),
        ("You can", "Puedes"),
        ("it seems", "parece"),
        ("It seems", "Parece"),
        ("Farewell.", "Adios."),
        ("Farewell~", "Adios~"),
        ("Farewell,", "Adios,"),
        ("Farewell", "Adios"),
        ("farewell", "adios"),
        ("Nothing.", "Nada."),
        ("Hurray~!", "Hurra~!"),
        ("Hooray~!", "Hurra~!"),
        ("Hooooray!", "Hurraaaa!"),
        ("adventurer", "aventurero"),
        ("adventurers", "aventureros"),
        ("Adventurer", "Aventurero"),
    ]


def process_line(line):
    """Process a single line, translating mes/select content."""
    stripped = line.strip()

    if stripped.startswith('//') or not stripped:
        return line

    # Handle mes "..." lines
    mes_match = re.match(r'^(\s*mes\s+)"(.*)"\s*;(.*)$', line)
    if mes_match:
        prefix = mes_match.group(1)
        content = mes_match.group(2)
        suffix = mes_match.group(3)

        # Don't translate [NPC Name] lines
        if re.match(r'^\[.*\]$', content.strip()):
            return line

        translated = translate_content(content)
        newline = f'{prefix}"{translated}";'
        if suffix and suffix.strip():
            newline += suffix
        return newline + '\n'

    # Handle select("...")
    select_match = re.search(r'(select\()"([^"]+)"\)', line)
    if select_match:
        full_match = select_match.group(0)
        prefix_sel = select_match.group(1)
        content = select_match.group(2)

        options = content.split(':')
        translated_options = [translate_content(opt) for opt in options]
        new_content = ':'.join(translated_options)
        new_select = f'{prefix_sel}"{new_content}")'
        return line.replace(full_match, new_select)

    # Handle mapannounce strings
    ann_match = re.search(r'(mapannounce\s+"[^"]+"\s*,\s*)"([^"]+)"', line)
    if ann_match:
        full = ann_match.group(0)
        prefix_ann = ann_match.group(1)
        content = ann_match.group(2)
        translated = translate_content(content)
        return line.replace(full, f'{prefix_ann}"{translated}"')

    return line


def process_file(filepath):
    """Process a quest file."""
    print(f"Processing: {filepath}")

    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        original = f.readlines()

    output = [process_line(line) for line in original]

    assert len(output) == len(original), f"Line count mismatch: {len(output)} vs {len(original)}"

    with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
        f.writelines(output)

    print(f"  Done: {len(original)} lines, line count preserved")


if __name__ == '__main__':
    base = "D:/Xponzy Network/Ragnarok-Server/rathena/npc/quests"
    for fname in ["the_sign_quest.txt", "quests_ein.txt", "quests_hugel.txt"]:
        process_file(os.path.join(base, fname))
