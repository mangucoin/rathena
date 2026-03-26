#!/usr/bin/env python3
import re, sys

PHRASE_TRANSLATIONS = [
    ("Cat Paw Merchant Association", "Asociacion de Comerciantes Pata de Gato"),
    ("Cat Gamers Director", "Director de Cat Gamers"),
    ("Cat Gamers Certificate", "Certificado de Cat Gamers"),
    ("Yggdrasil Berry", "Yggdrasil Berry"),
    ("Malangdo Can", "Lata de Malangdo"),
    ("Malangdo Cans", "Latas de Malangdo"),
    ("Adventure Card", "Tarjeta de Aventura"),
    ("Aventura Card", "Tarjeta de Aventura"),
    ("Bravery Team", "Equipo Valiente"),
    ("Flag Point", "Punto de Bandera"),
    ("Flag Points", "Puntos de Bandera"),
    ("Flag Game", "Juego de Banderas"),
    ("Fix Kit", "Kit de Reparacion"),
    ("Beginning Compass", "Brujula Inicial"),
    ("Cleaning Brush", "Cepillo de Limpieza"),
    ("Unidentified Fish", "Pez No Identificado"),
    ("Rock Paper Scissors", "Piedra Papel Tijera"),
    ("Plain Sauce", "Salsa Simple"),
    ("Ice Cream", "Helado"),
    ("Ice Creams", "Helados"),
    ("Ice Piece", "Trozo de Hielo"),
    ("Ice Pieces", "Trozos de Hielo"),
    ("Fish Tail", "Cola de Pez"),
    ("Fish Tails", "Colas de Pez"),
    ("Rat Tail", "Cola de Rata"),
    ("Rat Tails", "Colas de Rata"),
    ("Glass Bead", "Canica de Cristal"),
    ("ship biscuit", "galleta marinera"),
    ("Ship biscuit", "Galleta marinera"),
    ("Village Chief", "Jefe de la Aldea"),
    ("village chief", "jefe de la aldea"),
    ("President of Meeting", "Presidente de la Reunion"),
    ("Thank you so much", "Muchas gracias"),
    ("Thank you very much", "Muchas gracias"),
    ("Thank you", "Gracias"),
    ("thank you", "gracias"),
    ("Thanks so much", "Muchas gracias"),
    ("Thanks a lot", "Muchas gracias"),
    ("Thanks for", "Gracias por"),
    ("thanks for", "gracias por"),
    ("Thanks", "Gracias"),
    ("thanks", "gracias"),
    ("Please come back", "Por favor vuelve"),
    ("please come back", "por favor vuelve"),
    ("Please come again", "Por favor vuelve"),
    ("please come again", "por favor vuelve"),
    ("Please help", "Por favor ayuda"),
    ("please help", "por favor ayuda"),
    ("Please wait", "Por favor espera"),
    ("please wait", "por favor espera"),
    ("Please don't", "Por favor no"),
    ("please don't", "por favor no"),
    ("Please do not", "Por favor no"),
    ("Please", "Por favor"),
    ("please", "por favor"),
    ("I'm sorry", "Lo siento"),
    ("I am sorry", "Lo siento"),
    ("Sorry", "Lo siento"),
    ("sorry", "lo siento"),
    ("Excuse me", "Disculpa"),
    ("excuse me", "disculpa"),
    ("Of course", "Por supuesto"),
    ("of course", "por supuesto"),
    ("Good bye", "Adios"),
    ("Goodbye", "Adios"),
    ("Good luck", "Buena suerte"),
    ("Good job", "Buen trabajo"),
    ("Good idea", "Buena idea"),
    ("Well done", "Bien hecho"),
    ("Welcome", "Bienvenido"),
    ("welcome", "bienvenido"),
    ("Hello", "Hola"),
    ("hello", "hola"),
    ("How are you doing", "Como te va"),
    ("How are you", "Como estas"),
    ("See you later", "Hasta luego"),
    ("See you tomorrow", "Hasta manana"),
    ("See you next", "Nos vemos en la proxima"),
    ("See you", "Nos vemos"),
    ("see you", "nos vemos"),
    ("Take care", "Cuidate"),
    ("take care", "cuidate"),
    ("Come again", "Vuelve otra vez"),
    ("come again", "vuelve otra vez"),
    ("Come back", "Vuelve"),
    ("come back", "vuelve"),
    ("Come here", "Ven aqui"),
    ("Go away", "Vete de aqui"),
    ("go away", "vete de aqui"),
    ("Get out", "Sal de aqui"),
    ("get out", "sal de aqui"),
    ("Be quiet", "Guarda silencio"),
    ("Be careful", "Ten cuidado"),
    ("be careful", "ten cuidado"),
    ("Watch out", "Ten cuidado"),
    ("watch out", "ten cuidado"),
    ("Don't worry", "No te preocupes"),
    ("don't worry", "no te preocupes"),
    ("Do not worry", "No te preocupes"),
    ("Don't forget", "No olvides"),
    ("don't forget", "no olvides"),
    ("Do not forget", "No olvides"),
    ("Don't touch", "No toques"),
    ("don't touch", "no toques"),
    ("Do not touch", "No toques"),
    ("Don't lie", "No mientas"),
    ("don't lie", "no mientas"),
    ("Do not lie", "No mientas"),
    ("I don't know", "No lo se"),
    ("I do not know", "No lo se"),
    ("I don't care", "No me importa"),
    ("I don't understand", "No entiendo"),
    ("I don't think so", "No lo creo"),
    ("I don't remember", "No recuerdo"),
    ("I can't", "No puedo"),
    ("I cannot", "No puedo"),
    ("I won't", "No lo hare"),
    ("I will not", "No lo hare"),
    ("I couldn't", "No pude"),
    ("I could not", "No pude"),
    ("I have no", "No tengo"),
    ("I have to", "Tengo que"),
    ("I need to", "Necesito"),
    ("I need", "Necesito"),
    ("I want to", "Quiero"),
    ("I want", "Quiero"),
    ("I think", "Creo"),
    ("I believe", "Creo"),
    ("I hope", "Espero"),
    ("I wish", "Deseo"),
    ("I feel", "Siento"),
    ("I know", "Se"),
    ("I see", "Ya veo"),
    ("I understand", "Entiendo"),
    ("I agree", "Estoy de acuerdo"),
    ("I remember", "Recuerdo"),
    ("I heard", "Escuche"),
    ("I found", "Encontre"),
    ("I will give you", "Te dare"),
    ("I will help", "Ayudare"),
    ("I will wait", "Esperare"),
    ("I will come", "Vendre"),
    ("I will go", "Ire"),
    ("I will try", "Intentare"),
    ("I will do", "Lo hare"),
    ("I will", "Lo hare"),
    ("Let me", "Dejame"),
    ("let me", "dejame"),
    ("Let's go", "Vamonos"),
    ("let's go", "vamonos"),
    ("Let's see", "Veamos"),
    ("let's see", "veamos"),
    ("Let's", "Vamos a"),
    ("let's", "vamos a"),
    ("Here you go", "Aqui tienes"),
    ("Here you are", "Aqui estas"),
    ("Here is", "Aqui esta"),
    ("Here are", "Aqui estan"),
    ("Right now", "Ahora mismo"),
    ("right now", "ahora mismo"),
    ("Right away", "Enseguida"),
    ("By the way", "Por cierto"),
    ("by the way", "por cierto"),
    ("In fact", "De hecho"),
    ("in fact", "de hecho"),
    ("Actually", "En realidad"),
    ("actually", "en realidad"),
    ("However", "Sin embargo"),
    ("however", "sin embargo"),
    ("Therefore", "Por lo tanto"),
    ("therefore", "por lo tanto"),
    ("Moreover", "Ademas"),
    ("moreover", "ademas"),
    ("Besides", "Ademas"),
    ("besides", "ademas"),
    ("Although", "Aunque"),
    ("although", "aunque"),
    ("Even though", "Aunque"),
    ("even though", "aunque"),
    ("Anyway", "De todos modos"),
    ("anyway", "de todos modos"),
    ("Anyways", "De todos modos"),
    ("anyways", "de todos modos"),
    ("After all", "Despues de todo"),
    ("after all", "despues de todo"),
    ("At first", "Al principio"),
    ("at first", "al principio"),
    ("As usual", "Como siempre"),
    ("as usual", "como siempre"),
    ("As always", "Como siempre"),
    ("as always", "como siempre"),
    ("At least", "Al menos"),
    ("at least", "al menos"),
    ("How come", "Como es que"),
    ("how come", "como es que"),
    ("What happened", "Que paso"),
    ("Really?", "En serio?"),
    ("really?", "en serio?"),
    ("Really", "De verdad"),
    ("really", "de verdad"),
    ("Finally", "Finalmente"),
    ("finally", "finalmente"),
    ("Suddenly", "De repente"),
    ("suddenly", "de repente"),
    ("Exactly", "Exactamente"),
    ("exactly", "exactamente"),
    ("Probably", "Probablemente"),
    ("probably", "probablemente"),
    ("Perhaps", "Tal vez"),
    ("perhaps", "tal vez"),
    ("Maybe", "Tal vez"),
    ("maybe", "tal vez"),
    ("Never", "Nunca"),
    ("never", "nunca"),
    ("Always", "Siempre"),
    ("always", "siempre"),
    ("Sometimes", "A veces"),
    ("sometimes", "a veces"),
    ("Especially", "Especialmente"),
    ("especially", "especialmente"),
    ("You should", "Deberias"),
    ("you should", "deberias"),
    ("You must", "Debes"),
    ("you must", "debes"),
    ("You need to", "Necesitas"),
    ("you need to", "necesitas"),
    ("You need", "Necesitas"),
    ("you need", "necesitas"),
    ("You can", "Puedes"),
    ("you can", "puedes"),
    ("Can you", "Puedes"),
    ("can you", "puedes"),
    ("Could you", "Podrias"),
    ("could you", "podrias"),
    ("Would you", "Podrias"),
    ("would you", "podrias"),
    ("Do you want", "Quieres"),
    ("do you want", "quieres"),
    ("Do you know", "Sabes"),
    ("do you know", "sabes"),
    ("Do you have", "Tienes"),
    ("do you have", "tienes"),
    ("There is", "Hay"),
    ("there is", "hay"),
    ("There are", "Hay"),
    ("there are", "hay"),
    ("This is", "Esto es"),
    ("this is", "esto es"),
    ("That is", "Eso es"),
    ("that is", "eso es"),
    ("What is", "Que es"),
    ("what is", "que es"),
    ("It is", "Es"),
    ("it is", "es"),
    ("It was", "Fue"),
    ("it was", "fue"),
    ("Congratulations", "Felicidades"),
    ("congratulations", "felicidades"),
    ("Congrats", "Felicidades"),
    ("congrats", "felicidades"),
    ("today", "hoy"),
    ("Today", "Hoy"),
    ("tomorrow", "manana"),
    ("Tomorrow", "Manana"),
    ("yesterday", "ayer"),
    ("Yesterday", "Ayer"),
    ("adventure", "aventura"),
    ("Adventure", "Aventura"),
    ("adventurer", "aventurero"),
    ("Adventurer", "Aventurero"),
    ("island", "isla"),
    ("Island", "Isla"),
    ("village", "aldea"),
    ("Village", "Aldea"),
    ("meeting", "reunion"),
    ("Meeting", "Reunion"),
    ("humans", "humanos"),
    ("Humans", "Humanos"),
    ("human", "humano"),
    ("Human", "Humano"),
    ("friend", "amigo"),
    ("friends", "amigos"),
    ("enemy", "enemigo"),
    ("enemies", "enemigos"),
    ("treasure", "tesoro"),
    ("present", "regalo"),
    ("reward", "recompensa"),
    ("secret", "secreto"),
    ("problem", "problema"),
    ("danger", "peligro"),
]

def translate_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    lines = content.split('\n')
    out = [process_line(l) for l in lines]
    assert len(out) == len(lines)
    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        f.write('\n'.join(out))
    print(f"Done: {filepath} ({len(lines)} lines)")

def process_line(line):
    stripped = line.strip()
    if not stripped or stripped.startswith('//'):
        return line
    m = re.match(r'^(\s*mes\s+)"(.*)";(.*)$', line)
    if m:
        prefix, content, suffix = m.group(1), m.group(2), m.group(3)
        translated = translate_mes(content)
        translated = translated.replace('"', "'")
        return f'{prefix}"{translated}";{suffix}'
    if 'select(' in line:
        def repl(match):
            c = match.group(1)
            parts = c.split(':')
            tp = [apply_translations(p).replace(':', '') for p in parts]
            return 'select("' + ':'.join(tp) + '")'
        return re.sub(r'select\("([^"]*)"\)', repl, line)
    if stripped.startswith('announce ') or stripped.startswith('mapannounce '):
        m2 = re.match(r'^(\s*(?:map)?announce\s+)"(.*?)"(.*)$', line)
        if m2:
            prefix, content, suffix = m2.group(1), m2.group(2), m2.group(3)
            return f'{prefix}"{apply_translations(content)}"{suffix}'
    return line

def translate_mes(content):
    protected = {}
    counter = [0]
    def protect(m):
        key = f"\x00P{counter[0]}\x00"
        counter[0] += 1
        protected[key] = m.group(0)
        return key
    result = re.sub(r"'\+[^+]+\+'", protect, content)
    result = re.sub(r"'\+[^']+$", protect, result)
    result = re.sub(r"^[^']+\+'", protect, result)
    result = apply_translations(result)
    for key, val in protected.items():
        result = result.replace(key, val)
    return result

def apply_translations(text):
    if not text or not text.strip():
        return text
    colors = {}
    cc = [0]
    def prot_color(m):
        k = f"\x01C{cc[0]}\x01"
        cc[0] += 1
        colors[k] = m.group(0)
        return k
    result = re.sub(r'\^[0-9a-fA-F]{6}', prot_color, text)
    for eng, spa in PHRASE_TRANSLATIONS:
        result = result.replace(eng, spa)
    for k, v in colors.items():
        result = result.replace(k, v)
    return result

if __name__ == '__main__':
    for path in sys.argv[1:]:
        translate_file(path)
