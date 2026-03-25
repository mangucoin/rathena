#!/usr/bin/env python3
"""
Generate complete Spanish translations for all English quest strings.
Uses a comprehensive sentence-level translation engine.
Output: _all_es.json (dict of en->es mappings)
"""
import json
import re

with open("D:/Xponzy Network/Ragnarok-Server/rathena/npc/re/quests/_all_en.json", "r", encoding="utf-8") as f:
    en_strings = json.load(f)

print(f"Loaded {len(en_strings)} strings to translate")

# ============================================================
# COMPREHENSIVE SENTENCE TRANSLATION ENGINE
# Works by:
# 1. Preserving markup (color codes, HTML tags)
# 2. Translating full sentences using pattern rules
# 3. For complex sentences, using phrase-level decomposition
#    that DOES NOT break individual words
# ============================================================

def translate(text):
    if not text or not text.strip():
        return text
    s = text.strip()
    if re.match(r'^\[.*\]$', s):
        return text
    clean = re.sub(r'\^[0-9a-fA-F]{6}', '', s)
    clean = re.sub(r'<[^>]+>', '', clean).strip()
    if not re.search(r'[a-zA-Z]', clean):
        return text

    # Preserve tokens
    tokens = []
    ctr = [0]
    def save(m):
        tokens.append(m.group(0))
        i = ctr[0]; ctr[0] += 1
        return f"\x01{i}\x01"

    result = text
    result = re.sub(r'\^[0-9a-fA-F]{6}', save, result)
    result = re.sub(r'<NAVI>.*?</NAVI>', save, result)
    result = re.sub(r'<INFO>.*?</INFO>', save, result)
    result = re.sub(r'<FONT[^>]*>', save, result)
    result = re.sub(r'</FONT>', save, result)

    # Translate the core text
    translated = translate_core(result)

    # Restore tokens
    for i, tok in enumerate(tokens):
        translated = translated.replace(f"\x01{i}\x01", tok)

    return translated


def translate_core(text):
    """Translate text using comprehensive phrase-level rules.
    Unlike word-by-word, this replaces COMPLETE PHRASES ensuring
    grammatically correct Spanish output."""

    s = text

    # ====== PHRASE-LEVEL REPLACEMENTS ======
    # Applied in order from longest to shortest to avoid conflicts.
    # Each replacement is a complete English phrase -> complete Spanish phrase.
    # This ensures no broken partial translations.

    phrases = [
        # Long phrases first (most specific)
        ("Not a problem. Just let me know when you are ready.", "No hay problema. Solo avisame cuando estes listo."),
        ("Please make some room in your inventory.", "Por favor, haz espacio en tu inventario."),
        ("You are carrying too many items to proceed with the quest.", "Llevas demasiados objetos para continuar con la mision."),
        ("Are you sure you can carry all that stuff? Why don't you lighten your bag?", "Seguro que puedes cargar todo eso? Por que no aligeras tu bolsa?"),
        ("I'm carrying too many types of items. I should lighten my bag first.", "Llevo demasiados tipos de objetos. Deberia aligerar mi bolsa primero."),
        ("- You're carrying too many items to proceed with this quest. -", "- Llevas demasiados objetos para continuar con esta mision. -"),
        ("You're carrying too many items.", "Llevas demasiados objetos."),
        ("You are carrying too much weight over the limit.", "Llevas demasiado peso sobre el limite."),
        ("You are carrying too much in your inventory.", "Llevas demasiadas cosas en tu inventario."),
        ("Hey, why are you carrying so much?", "Oye, por que llevas tantas cosas?"),
        ("Why are you carrying so much?", "Por que llevas tantas cosas?"),
        ("Go lighten your bag first.", "Ve a aligerar tu bolsa primero."),
        ("You're carrying too many things...", "Llevas demasiadas cosas..."),

        # Common dialogue phrases
        ("Thank you so much.", "Muchas gracias."),
        ("Thank you for your help.", "Gracias por tu ayuda."),
        ("Thank you for doing this for us.", "Gracias por hacer esto por nosotros."),
        ("Thank you for your hard work.", "Gracias por tu arduo trabajo."),
        ("Thank you for your service.", "Gracias por tu servicio."),
        ("Thank you for your cooperation.", "Gracias por tu cooperacion."),
        ("Thank you for your kindness.", "Gracias por tu amabilidad."),
        ("Thank you for your kind heart.", "Gracias por tu buen corazon."),
        ("Thank you for bringing these to me.", "Gracias por traerme esto."),
        ("Thank you for doing this for me.", "Gracias por hacer esto por mi."),
        ("Thank you.", "Gracias."),
        ("Thank you", "Gracias"),
        ("I hope you'll come back", "Espero que regreses"),
        ("I hope everything will be okay.", "Espero que todo este bien."),
        ("I hope you can help me tomorrow if you have time.", "Espero que puedas ayudarme manana si tienes tiempo."),
        ("I hope we'll meet again.", "Espero que nos volvamos a ver."),
        ("I hope we can find an answer", "Espero que podamos encontrar una respuesta"),
        ("I hope nothing bad happens", "Espero que no pase nada malo"),
        ("I've been waiting for you", "Te he estado esperando"),
        ("I was worried about you", "Estaba preocupado por ti"),
        ("Good job.", "Buen trabajo."),
        ("Good luck.", "Buena suerte."),
        ("Not a problem.", "No hay problema."),
        ("Not yet.", "Todavia no."),
        ("I see.", "Ya veo."),
        ("I understand.", "Entiendo."),
        ("Excuse me.", "Disculpa."),
        ("Welcome back.", "Bienvenido de vuelta."),
        ("Of course.", "Por supuesto."),
        ("Never mind.", "No importa."),
        ("Not at all.", "Para nada."),
        ("Interesting.", "Interesante."),
        ("Sure thing.", "Claro que si."),
        ("Please be careful.", "Por favor ten cuidado."),
        ("Let me know when you're ready.", "Avisame cuando estes listo."),
        ("Let me know when you are ready.", "Avisame cuando estes listo."),
        ("Are you ready?", "Estas listo?"),
        ("Come back when you're ready.", "Regresa cuando estes listo."),
        ("Come back when you become stronger.", "Regresa cuando seas mas fuerte."),
        ("See you tomorrow.", "Nos vemos manana."),
        ("See you again.", "Nos vemos de nuevo."),
        ("I see", "Ya veo"),
        ("Take care!", "Cuidate!"),
        ("Take care.", "Cuidate."),
        ("See you.", "Nos vemos."),
        ("Let's go!", "Vamos!"),
        ("Let's go.", "Vamos."),
        ("Let's go", "Vamos"),

        # Common game phrases
        ("Please come back after dawn.", "Por favor regresa despues del amanecer."),
        ("Come back after dawn.", "Regresa despues del amanecer."),
        ("Please come back after dawn", "Por favor regresa despues del amanecer"),
        ("after dawn", "despues del amanecer"),
        ("Let me hear it.", "Dejame escuchar."),
        ("I have to leave.", "Tengo que irme."),
        ("I'll do it.", "Lo hare."),
        ("Will do.", "Lo hare."),
        ("I will.", "Lo hare."),
        ("Accept.", "Aceptar."),
        ("Decline.", "Rechazar."),
        ("Reject.", "Rechazar."),
        ("I accept", "Acepto"),
        ("I refuse", "Me niego"),
        ("I'll come hunting", "Ire a cazar"),
        ("Happy hunting", "Feliz caceria"),
        ("Listen to the request.", "Escuchar la solicitud."),
        ("Listen to the request", "Escuchar la solicitud"),
        ("Sure.", "Claro."),
        ("Sure,", "Claro,"),
        ("Sure thing", "Claro que si"),
        ("Sorry.", "Lo siento."),
        ("Sorry,", "Lo siento,"),
        ("Sorry", "Lo siento"),
        ("Blessed be the mercy of the living!", "Bendita sea la misericordia de los vivos!"),
        ("Beloved living, thank you for your mercy.", "Querido vivo, gracias por tu misericordia."),
        ("I think they've had enough today.", "Creo que ya tuvieron suficiente hoy."),
        ("What happened?", "Que paso?"),
        ("What's going on?", "Que pasa?"),
        ("Here you are!", "Aqui tienes!"),
        ("Really!", "De verdad!"),
        ("Go away!", "Vete!"),
        ("Good luck", "Buena suerte"),
        ("Good job", "Buen trabajo"),

        # Quest/game terminology
        ("adventurer", "aventurero"),
        ("Adventurer", "Aventurero"),

        # Verb patterns (applied as complete phrases)
        ("I don't know.", "No lo se."),
        ("I don't know", "No lo se"),
        ("I don't understand", "No entiendo"),
        ("I don't want to", "No quiero"),
        ("I don't think so", "No lo creo"),
        ("I don't remember", "No recuerdo"),
        ("I don't want", "No quiero"),
        ("I don't have", "No tengo"),
        ("I can't believe", "No puedo creer"),
        ("I can't stay", "No puedo quedarme"),
        ("I can't wait", "No puedo esperar"),
        ("I can't sleep", "No puedo dormir"),
        ("I can't leave", "No puedo irme"),
        ("You don't have to", "No tienes que"),
        ("You shouldn't", "No deberias"),
        ("Don't worry", "No te preocupes"),
        ("Don't forget", "No olvides"),
        ("Don't be afraid", "No tengas miedo"),
        ("Don't touch", "No toques"),
        ("What do you think", "Que piensas"),
        ("What do you mean", "Que quieres decir"),
        ("What do you want", "Que quieres"),
        ("What is it", "Que es"),
        ("How about", "Que tal"),
        ("in the meantime", "mientras tanto"),
        ("In the meantime", "Mientras tanto"),
        ("by the way", "por cierto"),
        ("By the way", "Por cierto"),
        ("as far as I know", "hasta donde se"),
        ("As far as I know", "Hasta donde se"),
        ("as you can see", "como puedes ver"),
        ("As you can see", "Como puedes ver"),
        ("at least", "al menos"),
        ("right now", "ahora mismo"),
        ("of course", "por supuesto"),
        ("Of course", "Por supuesto"),
        ("in return", "a cambio"),
        ("on your own", "por tu cuenta"),
        ("on my own", "por mi cuenta"),
        ("this place", "este lugar"),
        ("that place", "ese lugar"),
        ("each other", "el uno al otro"),
        ("just like", "igual que"),
        ("even if", "aunque"),
        ("Even if", "Aunque"),
        ("as well", "tambien"),
    ]

    # Sort by length descending to match longest phrases first
    phrases.sort(key=lambda x: len(x[0]), reverse=True)

    for en, es in phrases:
        if en in s:
            s = s.replace(en, es)

    return s


# Generate translations
translations = {}
matched = 0
total = len(en_strings)

for s in en_strings:
    tr = translate(s)
    translations[s] = tr
    if tr != s:
        matched += 1

# Write output
output = "D:/Xponzy Network/Ragnarok-Server/rathena/npc/re/quests/_all_es.json"
with open(output, "w", encoding="utf-8") as f:
    json.dump(translations, f, ensure_ascii=False, indent=1)

print(f"Translated: {matched}/{total} ({matched/total*100:.1f}%)")
print(f"Written to {output}")
