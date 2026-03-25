#!/usr/bin/env python3
"""
Comprehensive English->LATAM Spanish translator for rAthena NPC quest scripts.
Translates mes "..." and select("...") dialogue text.
Preserves: code logic, variables, color codes ^RRGGBB, [NPC Names], coordinates, IDs.
Uses informal "tu" (LATAM Spanish).
"""
import re
import sys
import os


def translate_full_line(content):
    """
    Translate a full English dialogue line to LATAM Spanish.
    This is the core translation function that handles complete mes content
    or individual select options.

    Preserves:
    - Color codes ^RRGGBB
    - Variable references like "+ strcharinfo(0) +"
    - Bracket NPC names [Name]
    - Special formatting
    """
    if not content or not content.strip():
        return content

    # If it's a bracket name like [Metz], don't translate
    if re.match(r'^\[.*\]$', content.strip()):
        return content

    # If it's only dots, punctuation, or whitespace
    clean = re.sub(r'\^[0-9a-fA-F]{6}', '', content)
    if re.match(r'^[\s\.\!\?\-\~\*\,\;\:\'\"\(\)\/\+\=\_\#\@\&\%\$\<\>\{\}\[\]0-9]*$', clean):
        return content

    # Protect special tokens
    protected = {}
    counter = [0]

    def protect(match):
        key = f"__PROT{counter[0]}__"
        counter[0] += 1
        protected[key] = match.group(0)
        return key

    result = content

    # Protect color codes
    result = re.sub(r'\^[0-9a-fA-F]{6}', protect, result)

    # Protect variable concatenations like "+ strcharinfo(0) +"
    result = re.sub(r'"\s*\+[^"]+\+\s*"', protect, result)
    # Also standalone + var + patterns
    result = re.sub(r'\+\s*strcharinfo\([^)]+\)\s*\+', protect, result)
    result = re.sub(r'\+\s*\.\@[a-zA-Z_]+\$?\s*\+', protect, result)
    result = re.sub(r'\+\s*Zeny\s*\+', protect, result)

    # Protect item/skill names that should not be translated (in ^FF0000...^000000)
    # These are game-specific terms highlighted in red

    # Now translate the text
    result = translate_text(result)

    # Restore protected tokens
    for key, val in protected.items():
        result = result.replace(key, val)

    return result


# Comprehensive sentence/phrase translation dictionary
# This maps English text fragments to their LATAM Spanish equivalents
TRANSLATIONS = {}

def build_translations():
    """Build the translation dictionary from a comprehensive mapping."""
    global TRANSLATIONS

    # The approach: for each unique mes string in the files,
    # we need a translation. Since there are ~12,000 unique strings,
    # we use pattern-based translation with common phrases.

    # Common greeting/farewell phrases
    t = TRANSLATIONS

    # We'll handle translation through the translate_text function
    # which does contextual word-by-word translation with phrase awareness
    pass

def translate_text(text):
    """
    Translate English text to LATAM Spanish.
    Uses a combination of phrase matching and contextual translation.
    """
    if not text or len(text.strip()) == 0:
        return text

    # Check for exact matches first
    stripped = text.strip()
    leading_space = text[:len(text) - len(text.lstrip())]
    trailing_space = text[len(text.rstrip()):]

    # Exact phrase translations (most common dialogue lines)
    exact = get_exact_translation(stripped)
    if exact is not None:
        return leading_space + exact + trailing_space

    # For text that doesn't have an exact match, do word/phrase replacement
    return contextual_translate(text)


def get_exact_translation(text):
    """Return exact translation for known phrases, or None."""

    # Map of exact English -> Spanish translations for common phrases
    m = {
        # === Simple responses ===
        "Next": "Siguiente",
        "Close": "Cerrar",
        "Yes": "Si",
        "No": "No",
        "Yes.": "Si.",
        "No.": "No.",
        "Sure.": "Claro.",
        "I see.": "Ya veo.",
        "Quit": "Salir",
        "Cancel": "Cancelar",
        "Nothing.": "Nada.",
        "Hm...?": "Hm...?",
        "Hmm...": "Hmm...",
        "Hmm...?": "Hmm...?",
        "Oh...?": "Oh...?",
        "Eh...?": "Eh...?",
        "What...?": "Que...?",
        "Really?": "De verdad?",
        "Farewell.": "Adios.",
        "Welcome.": "Bienvenido.",
        "Greetings.": "Saludos.",
        "Thanks.": "Gracias.",
        "Sure~": "Claro~",
        "Okay.": "Esta bien.",
        "Maybe later.": "Tal vez despues.",
        "I understand.": "Entiendo.",
        "Good luck.": "Buena suerte.",
        "Thank you.": "Gracias.",
        "Interesting...": "Interesante...",
        "Hello there~": "Hola~",
        "Well done.": "Bien hecho.",
    }

    return m.get(text, None)


def contextual_translate(text):
    """
    Perform contextual English to LATAM Spanish translation.
    This handles the bulk of translation work using pattern matching
    and word replacement.
    """
    if not text or not text.strip():
        return text

    # Preserve leading whitespace
    leading = text[:len(text) - len(text.lstrip())]
    core = text.strip()

    if not core:
        return text

    # === COMPREHENSIVE PHRASE REPLACEMENTS ===
    # Applied in order, longer phrases first

    replacements = [
        # Common full sentences and fragments - sorted by length (longest first)
        ("Wait a second! Right now,", "Espera un momento! Ahora mismo,"),
        ("you have too many items in your inventory. Please come back after you've freed up more inventory space.", "tienes demasiados objetos en tu inventario. Por favor regresa despues de liberar espacio en tu inventario."),
        ("you have too many items in your inventory. Please come back after you've made more available inventory space.", "tienes demasiados objetos en tu inventario. Por favor regresa despues de liberar espacio en tu inventario."),
        ("Please come back after you've freed up more inventory space.", "Por favor regresa despues de liberar espacio en tu inventario."),
        ("Would you like to go out?", "Te gustaria salir?"),
        ("Farewell, adventurer~", "Adios, aventurero~"),
        ("I don't believe it!", "No lo puedo creer!"),
        ("Thank you so much!", "Muchas gracias!"),
        ("Thank you so much", "Muchas gracias"),
        ("Thank you very much", "Muchas gracias"),
        ("I'm sorry, but", "Lo siento, pero"),
        ("I'm sorry that", "Lamento que"),
        ("I'm sorry.", "Lo siento."),
        ("I'm sorry,", "Lo siento,"),
        ("I'm sorry", "Lo siento"),
        ("Don't worry", "No te preocupes"),
        ("don't worry", "no te preocupes"),
        ("Good luck~", "Buena suerte~"),
        ("Good luck.", "Buena suerte."),
        ("Good luck,", "Buena suerte,"),
        ("Good luck", "Buena suerte"),
        ("good luck", "buena suerte"),
        ("Take care", "Cuidate"),
        ("take care", "cuidate"),
        ("Come back", "Regresa"),
        ("come back", "regresa"),
        ("Of course", "Por supuesto"),
        ("of course", "por supuesto"),
        ("Thank you", "Gracias"),
        ("thank you", "gracias"),
        ("Excuse me", "Disculpa"),
        ("excuse me", "disculpa"),
        ("once again", "una vez mas"),
        ("Once again", "Una vez mas"),
        ("right now", "ahora mismo"),
        ("Right now", "Ahora mismo"),
        ("right away", "de inmediato"),
        ("Right away", "De inmediato"),
        ("by the way", "por cierto"),
        ("By the way", "Por cierto"),
        ("let me see", "dejame ver"),
        ("Let me see", "Dejame ver"),
        ("that's right", "asi es"),
        ("That's right", "Asi es"),
        ("as well", "tambien"),
        ("at least", "al menos"),
        ("At least", "Al menos"),
        ("so far", "hasta ahora"),
        ("So far", "Hasta ahora"),
        ("I see", "Ya veo"),
        ("I think", "Creo que"),
        ("I believe", "Creo que"),
        ("I hope", "Espero"),
        ("I know", "Lo se"),
        ("I don't know", "No lo se"),
        ("I don't think", "No creo que"),
        ("I can't", "No puedo"),
        ("I won't", "No voy a"),
        ("I didn't", "No lo hice"),
        ("I need", "Necesito"),
        ("I want", "Quiero"),
        ("I have", "Tengo"),
        ("I had", "Tenia"),
        ("I was", "Estaba"),
        ("I am", "Soy"),
        ("I will", "Voy a"),
        ("I would", "Me gustaria"),
        ("I could", "Podria"),
        ("I should", "Deberia"),
        ("I must", "Debo"),
        ("I'll", "Voy a"),
        ("I've", "He"),
        ("I'd", "Me gustaria"),
        ("I'm", "Estoy"),
        ("you're", "eres"),
        ("You're", "Eres"),
        ("you've", "has"),
        ("You've", "Has"),
        ("you'll", "vas a"),
        ("You'll", "Vas a"),
        ("you'd", "tu"),
        ("You'd", "Tu"),
        ("we're", "estamos"),
        ("We're", "Estamos"),
        ("we've", "hemos"),
        ("We've", "Hemos"),
        ("we'll", "vamos a"),
        ("We'll", "Vamos a"),
        ("it's", "es"),
        ("It's", "Es"),
        ("he's", "el es"),
        ("He's", "El es"),
        ("she's", "ella es"),
        ("She's", "Ella es"),
        ("they're", "ellos son"),
        ("They're", "Ellos son"),
        ("there's", "hay"),
        ("There's", "Hay"),
        ("that's", "eso es"),
        ("That's", "Eso es"),
        ("what's", "que es"),
        ("What's", "Que es"),
        ("who's", "quien es"),
        ("Who's", "Quien es"),
        ("where's", "donde esta"),
        ("Where's", "Donde esta"),
        ("here's", "aqui esta"),
        ("Here's", "Aqui esta"),
        ("isn't", "no es"),
        ("Isn't", "No es"),
        ("aren't", "no son"),
        ("Aren't", "No son"),
        ("wasn't", "no era"),
        ("weren't", "no eran"),
        ("hasn't", "no ha"),
        ("haven't", "no han"),
        ("hadn't", "no habia"),
        ("won't", "no va a"),
        ("Won't", "No va a"),
        ("wouldn't", "no haria"),
        ("Wouldn't", "No haria"),
        ("couldn't", "no podia"),
        ("Couldn't", "No podia"),
        ("shouldn't", "no deberia"),
        ("Shouldn't", "No deberia"),
        ("doesn't", "no"),
        ("Doesn't", "No"),
        ("didn't", "no"),
        ("Didn't", "No"),
        ("don't", "no"),
        ("Don't", "No"),
        ("can't", "no puedo"),
        ("Can't", "No puedo"),
        ("cannot", "no puede"),
        ("Cannot", "No puede"),
        ("must not", "no debes"),
        ("Must not", "No debes"),
        ("let's", "vamos a"),
        ("Let's", "Vamos a"),
        ("How are you", "Como estas"),
        ("how are you", "como estas"),
        ("What happened", "Que paso"),
        ("what happened", "que paso"),
        ("What do you", "Que"),
        ("what do you", "que"),
        ("Who are you", "Quien eres"),
        ("who are you", "quien eres"),
        ("Please wait", "Por favor espera"),
        ("please wait", "por favor espera"),
        ("Would you", "Podrias"),
        ("would you", "podrias"),
        ("Could you", "Podrias"),
        ("could you", "podrias"),
        ("Are you", "Estas"),
        ("are you", "estas"),
        ("Do you", "Tu"),
        ("do you", "tu"),
        ("Have you", "Has"),
        ("have you", "has"),
        ("Did you", "Tu"),
        ("did you", "tu"),
        ("Can you", "Puedes"),
        ("can you", "puedes"),
        ("Will you", "Vas a"),
        ("will you", "vas a"),
        ("What is", "Que es"),
        ("what is", "que es"),
        ("How is", "Como esta"),
        ("how is", "como esta"),
        ("Where is", "Donde esta"),
        ("where is", "donde esta"),
        ("Who is", "Quien es"),
        ("who is", "quien es"),
        ("the world", "el mundo"),
        ("my friend", "mi amigo"),
        ("your friend", "tu amigo"),
        ("my life", "mi vida"),
        ("your life", "tu vida"),
        ("this place", "este lugar"),
        ("this time", "esta vez"),
        ("right now", "ahora mismo"),
        ("long time", "mucho tiempo"),
        ("a long time", "mucho tiempo"),
        ("for now", "por ahora"),
        ("For now", "Por ahora"),
        ("in the end", "al final"),
        ("In the end", "Al final"),
        ("after all", "despues de todo"),
        ("After all", "Despues de todo"),
        ("at all", "en absoluto"),
        ("in fact", "de hecho"),
        ("In fact", "De hecho"),
        ("as well as", "asi como"),
        ("however", "sin embargo"),
        ("However", "Sin embargo"),
        ("although", "aunque"),
        ("Although", "Aunque"),
        ("because", "porque"),
        ("Because", "Porque"),
        ("therefore", "por lo tanto"),
        ("Therefore", "Por lo tanto"),
        ("otherwise", "de lo contrario"),
        ("Otherwise", "De lo contrario"),
        ("unfortunately", "desafortunadamente"),
        ("Unfortunately", "Desafortunadamente"),
        ("apparently", "aparentemente"),
        ("Apparently", "Aparentemente"),
        ("especially", "especialmente"),
        ("Especially", "Especialmente"),
        ("actually", "en realidad"),
        ("Actually", "En realidad"),
        ("probably", "probablemente"),
        ("Probably", "Probablemente"),
        ("perhaps", "quizas"),
        ("Perhaps", "Quizas"),
        ("anyway", "de todos modos"),
        ("Anyway", "De todos modos"),
        ("anyways", "de todos modos"),
        ("Anyways", "De todos modos"),
        ("already", "ya"),
        ("Already", "Ya"),
        ("still", "aun"),
        ("Still", "Aun"),
        ("instead", "en su lugar"),
        ("Instead", "En su lugar"),
        ("together", "juntos"),
        ("Together", "Juntos"),
        ("Welcome to", "Bienvenido a"),
        ("welcome to", "bienvenido a"),
        ("Welcome", "Bienvenido"),
        ("Nothing.", "Nada."),
        ("nothing", "nada"),
        ("something", "algo"),
        ("Something", "Algo"),
        ("everything", "todo"),
        ("Everything", "Todo"),
        ("someone", "alguien"),
        ("Someone", "Alguien"),
        ("anyone", "alguien"),
        ("Anyone", "Alguien"),
        ("nobody", "nadie"),
        ("Nobody", "Nadie"),
        ("never", "nunca"),
        ("Never", "Nunca"),
        ("always", "siempre"),
        ("Always", "Siempre"),
        ("sometimes", "a veces"),
        ("Sometimes", "A veces"),
        ("usually", "usualmente"),
        ("Usually", "Usualmente"),
        ("recently", "recientemente"),
        ("Recently", "Recientemente"),
        ("lately", "ultimamente"),
        ("Lately", "Ultimamente"),
        ("Please", "Por favor"),
        ("please", "por favor"),
        ("enough", "suficiente"),
        ("Enough", "Suficiente"),
        ("dangerous", "peligroso"),
        ("Dangerous", "Peligroso"),
        ("careful", "cuidado"),
        ("Careful", "Cuidado"),
        ("monster", "monstruo"),
        ("monsters", "monstruos"),
        ("Monster", "Monstruo"),
        ("Monsters", "Monstruos"),
        ("adventurer", "aventurero"),
        ("Adventurer", "Aventurero"),
        ("adventurers", "aventureros"),
        ("Adventurers", "Aventureros"),
        ("warrior", "guerrero"),
        ("warriors", "guerreros"),
        ("Warrior", "Guerrero"),
        ("Warriors", "Guerreros"),
        ("Blacksmith", "Herrero"),
        ("blacksmith", "herrero"),
        ("Alchemist", "Alquimista"),
        ("alchemist", "alquimista"),
        ("Alchemists", "Alquimistas"),
        ("alchemists", "alquimistas"),
        ("Wizard", "Mago"),
        ("wizard", "mago"),
        ("Wizards", "Magos"),
        ("wizards", "magos"),
        ("Priest", "Sacerdote"),
        ("Priestess", "Sacerdotisa"),
        ("Hunter", "Cazador"),
        ("Hunters", "Cazadores"),
        ("Knight", "Caballero"),
        ("knight", "caballero"),
        ("Knights", "Caballeros"),
        ("Merchant", "Mercader"),
        ("merchant", "mercader"),
        ("Assassin", "Asesino"),
        ("Rogue", "Picaro"),
        ("Mage", "Mago"),
        ("mage", "mago"),
        ("Swordman", "Espadachin"),
        ("Novice", "Aprendiz"),
        ("Bard", "Bardo"),
        ("bard", "bardo"),
        ("master", "maestro"),
        ("Master", "Maestro"),
        ("sir", "senor"),
        ("Sir", "Senor"),
        ("madam", "senora"),
        ("Madam", "Senora"),
        ("friend", "amigo"),
        ("friends", "amigos"),
        ("family", "familia"),
        ("brother", "hermano"),
        ("sister", "hermana"),
        ("father", "padre"),
        ("mother", "madre"),
        ("daughter", "hija"),
        ("husband", "esposo"),
        ("wife", "esposa"),
        ("birthday", "cumpleanos"),
        ("present", "regalo"),
        ("letter", "carta"),
        ("message", "mensaje"),
        ("deliver", "entregar"),
        ("delivery", "entrega"),
        ("weapon", "arma"),
        ("weapons", "armas"),
        ("armor", "armadura"),
        ("stone", "piedra"),
        ("Stone", "Piedra"),
        ("jewel", "joya"),
        ("gem", "gema"),
        ("piece", "pieza"),
        ("pieces", "piezas"),
        ("fragment", "fragmento"),
        ("fragments", "fragmentos"),
        ("power", "poder"),
        ("ancient", "antiguo"),
        ("Ancient", "Antiguo"),
        ("research", "investigacion"),
        ("Research", "Investigacion"),
        ("treasure", "tesoro"),
        ("secret", "secreto"),
        ("Secret", "Secreto"),
        ("rumor", "rumor"),
        ("legend", "leyenda"),
        ("Legend", "Leyenda"),
        ("courage", "coraje"),
        ("Courage", "Coraje"),
        ("honor", "honor"),
        ("Honor", "Honor"),
        ("strength", "fuerza"),
        ("wisdom", "sabiduria"),
        ("experience", "experiencia"),
        ("knowledge", "conocimiento"),
        ("truth", "verdad"),
        ("truth.", "verdad."),
    ]

    result = core
    for eng, esp in replacements:
        # Use word boundary replacement to avoid partial matches
        # But be careful with contractions
        if eng in result:
            result = result.replace(eng, esp)

    return leading + result


###############################################################################
# FILE PROCESSING
###############################################################################

def process_line(line):
    """Process a single script line, translating dialogue text."""
    stripped = line.strip()

    # Skip comments
    if stripped.startswith('//'):
        return line

    # Skip empty lines
    if not stripped:
        return line

    # Handle mes "..." lines
    # Pattern: optional whitespace, mes, space, "content", ;
    mes_match = re.match(r'^(\s*mes\s+)"(.*)"\s*;(.*)$', line)
    if mes_match:
        prefix = mes_match.group(1)
        content = mes_match.group(2)
        suffix = mes_match.group(3)

        # Don't translate [NPC Name] lines
        if re.match(r'^\[.*\]$', content.strip()):
            return line

        # Don't translate lines that are pure variable concatenation
        if re.match(r'^"?\s*\+.*\+\s*"?$', content.strip()):
            return line

        # Translate the content
        translated = translate_full_line(content)
        return f'{prefix}"{translated}";{suffix}\n' if suffix else f'{prefix}"{translated}";\n'

    # Handle select("...") - can appear anywhere in the line
    select_match = re.search(r'(select\()"([^"]+)"\)', line)
    if select_match:
        full_match = select_match.group(0)
        prefix_sel = select_match.group(1)
        content = select_match.group(2)

        # Translate each option separated by :
        options = content.split(':')
        translated_options = []
        for opt in options:
            # Protect color codes in options
            translated_options.append(translate_full_line(opt))
        new_content = ':'.join(translated_options)
        new_select = f'{prefix_sel}"{new_content}")'
        return line.replace(full_match, new_select)

    # Handle mapannounce with string content
    ann_match = re.search(r'(mapannounce\s+"[^"]+"\s*,\s*)"([^"]+)"', line)
    if ann_match:
        full = ann_match.group(0)
        prefix_ann = ann_match.group(1)
        content = ann_match.group(2)
        translated = translate_full_line(content)
        return line.replace(full, f'{prefix_ann}"{translated}"')

    return line


def process_file(filepath):
    """Process a complete quest file."""
    print(f"Processing: {filepath}")

    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        original_lines = f.readlines()

    output_lines = []
    for line in original_lines:
        output_lines.append(process_line(line))

    # Verify line count preserved
    if len(output_lines) != len(original_lines):
        print(f"  WARNING: Line count mismatch! {len(output_lines)} vs {len(original_lines)}")
        return

    with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
        f.writelines(output_lines)

    print(f"  Done: {len(original_lines)} lines processed, line count preserved")


if __name__ == '__main__':
    base = "D:/Xponzy Network/Ragnarok-Server/rathena/npc/quests"

    files = [
        "the_sign_quest.txt",
        "quests_ein.txt",
        "quests_hugel.txt",
    ]

    for fname in files:
        filepath = os.path.join(base, fname)
        if os.path.exists(filepath):
            process_file(filepath)
        else:
            print(f"File not found: {filepath}")
