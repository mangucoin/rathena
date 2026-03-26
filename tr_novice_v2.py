#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Translate novice.txt: all mes and select strings from English to LATAM Spanish.
This is a massive batch translation script.
Rules:
- Only translate text inside mes "..." and select("...") strings
- Use informal tu form (LATAM Spanish)
- No double quotes inside mes strings, use single quotes instead
- No colons inside select() option text
- Keep proper nouns as-is
- Preserve all script logic, variables, functions, coordinates, color codes, NPC names in brackets
"""

filepath = r"D:\Xponzy Network\Ragnarok-Server\rathena\npc\pre-re\jobs\novice\novice.txt"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

repls = [
    # === Shion NPC ===
    ('mes "What are you";', 'mes "Que haces";'),
    ('mes "still doing here?";', 'mes "todavia aqui?";'),
    ("mes \"Oh, you used a ^3355FFButterfly Wing^000000, didn't you?\";", 'mes "Oh, usaste un ^3355FFButterfly Wing^000000, verdad?";'),
    ("mes \"You're supposed to use the Butterfly Wing when you want to go back to a town ^666666after^000000 completing your training here, alright?\";", 'mes "Se supone que debes usar el Butterfly Wing cuando quieras volver a una ciudad ^666666despues^000000 de completar tu entrenamiento aqui, de acuerdo?";'),
    ('mes "Now, let me send";', 'mes "Ahora, dejame";'),
    ('mes "you back to the";', 'mes "enviarte de vuelta a los";'),
    ('mes "Training Grounds.";', 'mes "Campos de Entrenamiento.";'),
    ('mes "The Training Grounds";', 'mes "Los Campos de Entrenamiento";'),
    ('mes "are located just past";', 'mes "estan justo pasando";'),
    ('mes "the bridge located";', 'mes "el puente ubicado";'),
    ('mes "to the right.";', 'mes "a la derecha.";'),
    ("mes \"Although you'll\";", 'mes "Aunque tendras que";'),
    ('mes "be sitting through";', 'mes "sentarte en";'),
    ('mes "some classes, you";', 'mes "algunas clases, no";'),
    ("mes \"won't regret it.\";", 'mes "te arrepentiras.";'),
    ('mes "Now, go for it!";', 'mes "Ahora, adelante!";'),
    ('mes "Hey...";', 'mes "Oye...";'),
    ('mes "You little rascal!";', 'mes "Pequeno bribonzuelo!";'),
    ('mes "Wait...";', 'mes "Espera...";'),
    ('mes "Calm down Shion.";', 'mes "Calmate Shion.";'),
    ("mes \"You're a professional\";", 'mes "Eres una entrenadora";'),
    ("mes \"trainer! Don't get all\";", 'mes "profesional! No te";'),
    ('mes "upset at a Novice!";', 'mes "enojes con un Novato!";'),
    ("mes \"Go and cross the bridge to the right, right now! ^666666*Ahem*^000000 You'll see and castle, and inside you can meet all sorts of tutors.\";", 'mes "Ve y cruza el puente a la derecha, ahora mismo! ^666666*Ejem*^000000 Veras un castillo, y adentro podras conocer todo tipo de tutores.";'),
    ("mes \"If you can't see the entrance, just change your in-game camera angle by holding down the ^3355FFright Mouse button^000000 and dragging your mouse. Easy, right?\";", 'mes "Si no puedes ver la entrada, cambia el angulo de tu camara manteniendo presionado el ^3355FFboton derecho del Mouse^000000 y arrastrando el mouse. Facil, verdad?";'),
    ('mes "To reset your camera angle,";', 'mes "Para reiniciar el angulo de tu camara,";'),
    ('mes "just double-click the right Mouse button. Okay then, take care!";', 'mes "solo haz doble clic en el boton derecho del Mouse. Bien, cuidate!";'),
    ('mes "Oh, and before you leave,";', 'mes "Oh, y antes de irte,";'),
    ("mes \"learn how to treat a lady nice, okay? Then they might give you gifts like this!\";", 'mes "aprende a tratar bien a una dama, de acuerdo? Asi podrian darte regalos como este!";'),
    ('mes "Huh...?";', 'mes "Eh...?";'),
    ('mes "Why are you";', 'mes "Por que sigues";'),
    ('mes "still here?";', 'mes "aqui?";'),
    ('mes "^666666*Sigh...*^000000";', 'mes "^666666*Suspiro...*^000000";'),
    ("mes \"Hey, when you enter the Training Grounds, you'll learn all sorts of things that will help you play the game. You'll even have the chance to get zeny and other rewards.\";", 'mes "Oye, cuando entres a los Campos de Entrenamiento, aprenderas todo tipo de cosas que te ayudaran a jugar. Incluso tendras la oportunidad de conseguir zeny y otras recompensas.";'),
    ('mes "You can even gain";', 'mes "Incluso puedes ganar";'),
    ('mes "experience like this!";', 'mes "experiencia asi!";'),
    ("mes \"Everything you'll learn here in the Training Grounds will benefit your gameplay. So just think positive, okay?\";", 'mes "Todo lo que aprendas aqui en los Campos de Entrenamiento beneficiara tu juego. Asi que piensa positivo, de acuerdo?";'),
    ('mes "Hello there~";', 'mes "Hola~";'),
    ('mes "Welcome to the";', 'mes "Bienvenido a los";'),
    ('mes "Training Grounds!";', 'mes "Campos de Entrenamiento!";'),
    ("mes \"Let's see.\";", 'mes "Veamos.";'),
    ('mes "Your name is...";', 'mes "Tu nombre es...";'),
    ('mes "My name is Shion.";', 'mes "Mi nombre es Shion.";'),
    ("mes \"Yes, this is the first time we've met, of course. Hahahaha~!\";", 'mes "Si, esta es la primera vez que nos vemos, por supuesto. Jajajaja~!";'),
    ("mes \"Now that we've met, is there anything I can help you with?\";", 'mes "Ahora que nos conocemos, hay algo en lo que pueda ayudarte?";'),
    ("mes \"I'm here for your questions~\";", 'mes "Estoy aqui para tus preguntas~";'),
    ('select("Where should I go?:About Basic Interfaces.:Who the crap are you?")', 'select("A donde deberia ir?:Sobre las Interfaces Basicas.:Quien diablos eres?")'),
    ('mes "Do you see the bridge to your";', 'mes "Ves el puente a tu";'),
    ("mes \"right side? Just cross the bridge and you'll arrive at a castle. All you have to do is walk inside!\";", 'mes "derecha? Solo cruza el puente y llegaras a un castillo. Todo lo que tienes que hacer es entrar!";'),
    ('mes "The entrance of the castle";', 'mes "La entrada del castillo";'),
    ('mes "is a ^4D4DFFspinning white light^000000. These portals are what allow you to move from one zone to another.";', 'mes "es una ^4D4DFFluz blanca giratoria^000000. Estos portales te permiten moverte de una zona a otra.";'),
    ('mes "Do you know how to move?";', 'mes "Sabes como moverte?";'),
    ("mes \"Left click on a spot, and you'll walk over to that spot. Piece of cake, huh?\";", 'mes "Haz clic izquierdo en un lugar y caminaras hacia alli. Pan comido, no?";'),
    ('mes "So go for it!";', 'mes "Asi que adelante!";'),
    ('mes "Basically, you must enter the castle in order to start your adventures.";', 'mes "Basicamente, debes entrar al castillo para comenzar tus aventuras.";'),
    ('mes "There are soldiers";', 'mes "Hay soldados";'),
    ("mes \"at the entrance, so don't\";", 'mes "en la entrada, asi que no";'),
    ('mes "worry about getting lost.";', 'mes "te preocupes por perderte.";'),
    ('mes "Take care now~!";', 'mes "Cuidate~!";'),
    ('mes "Basic Interfaces...";', 'mes "Interfaces Basicas...";'),
    ('mes "Do you know what Click, Double-click and Drag mean?";', 'mes "Sabes que significan Clic, Doble clic y Arrastrar?";'),
    ('mes "When you press the";', 'mes "Cuando presionas el";'),
    ('mes "left Mouse button once,";', 'mes "boton izquierdo del Mouse una vez,";'),
    ("mes \"that is a click. When you press the mouse button twice in a row, that's a double-click.\";", 'mes "eso es un clic. Cuando presionas el boton del mouse dos veces seguidas, eso es un doble clic.";'),
    ('mes "Dragging is when you move your Mouse while holding down the";', 'mes "Arrastrar es cuando mueves tu Mouse mientras mantienes presionado el";'),
    ('mes "Mouse button after clicking on something.";', 'mes "boton del Mouse despues de hacer clic en algo.";'),
    ('mes "Before we start talking about";', 'mes "Antes de empezar a hablar sobre";'),
    ("mes \"the Basic Interfaces, you should remember these terms, just because we'll be using them frequently.\";", 'mes "las Interfaces Basicas, deberias recordar estos terminos, ya que los usaremos frecuentemente.";'),
    ('mes "Inside the castle, there is a Basic Interfaces Tutor who can teach you the basics more clearly, okay? Enter the castle to start your training.";', 'mes "Dentro del castillo hay un Tutor de Interfaces Basicas que te ensenara los fundamentos mas claramente. Entra al castillo para comenzar tu entrenamiento.";'),
    ('mes "The entrance";', 'mes "La entrada";'),
    ('mes "of the castle is";', 'mes "del castillo es";'),
    ('mes "a ^4D4DFFspinning white light^000000.";', 'mes "una ^4D4DFFluz blanca giratoria^000000.";'),
    ("mes \"Me? I'm Shion!\";", 'mes "Yo? Soy Shion!";'),
    ("mes \"But that's a rude way of asking! I'm volunteering my time and effort here, so you've got to show me a little bit of respect at least!\";", 'mes "Pero esa es una forma muy grosera de preguntar! Estoy como voluntaria aqui, asi que al menos muestrame un poco de respeto!";'),
    # Receptionist extras
    ('mes "Hello, you look to be new here.";', 'mes "Hola, pareces ser nuevo aqui.";'),
    ('mes "What is your name?";', 'mes "Como te llamas?";'),
    ("mes \"Sorry, but I don't think I heard\";", 'mes "Lo siento, creo que no te";'),
    ('mes "you correctly";', 'mes "escuche bien";'),
    ('mes "Please, take your time.";', 'mes "Por favor, tomate tu tiempo.";'),
]

count = 0
for old, new in repls:
    if old != new and old in content:
        content = content.replace(old, new)
        count += 1

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Applied {count} unique replacements")
