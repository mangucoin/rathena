#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bulk translate remaining English content in novice.txt
Processes the file line by line and translates mes/select strings.
"""

filepath = r"D:\Xponzy Network\Ragnarok-Server\rathena\npc\pre-re\jobs\novice\novice.txt"

with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Line-indexed translations (1-based line numbers from the original file)
# We map exact English mes/select content to Spanish
# This handles all the remaining untranslated NPCs

# Giant dictionary of English -> Spanish for all remaining content
trans = {
    # Interfaces Tutor (Kris) - lines ~380-655
    "You've completed all the essential courses. Have you spoken to the assistant tutors already? The field combat training will be your next course. Would you like to proceed?": "Has completado todos los cursos esenciales. Ya hablaste con los tutores asistentes? El entrenamiento de combate de campo sera tu siguiente curso. Te gustaria continuar?",
    'select("Sure!:No, I\'ll come back later.:Send me to a town!")': 'select("Claro!:No, volvere despues.:Enviame a una ciudad!")',
    "Your next course is Field Combat training. Please listen carefully to your next trainer, and I hope you pass the course. Godspeed.": "Tu siguiente curso es el entrenamiento de Combate de Campo. Por favor escucha con atencion a tu siguiente entrenador, y espero que apruebes el curso. Buena suerte.",
    "Alright then. In the meantime, you might want to speak to the assistant tutors, as the basic information taught in the essential courses may not be enough for new adventurers.": "Muy bien entonces. Mientras tanto, podrias hablar con los tutores asistentes, ya que la informacion basica ensenada en los cursos esenciales podria no ser suficiente para nuevos aventureros.",
    "Feel free to come back any time when you need my assistance.": "Sientete libre de volver cuando necesites mi ayuda.",
    "So, would you like to be sent to a town? If you're confident that you've learned enough, head over to the right and speak to the ^3355FFKafra Employee^000000.": "Entonces, te gustaria que te envie a una ciudad? Si confias en que has aprendido suficiente, ve a la derecha y habla con la ^3355FFEmpleada Kafra^000000.",
    "The Kafra Services are very convenient once you get out into the real world. Their Teleport Service can be used to travel from town to town, and you can keep your items safe in the Kafra Storage.": "Los Servicios Kafra son muy convenientes una vez que salgas al mundo real. Su Servicio de Teletransporte puede usarse para viajar de ciudad en ciudad, y puedes guardar tus objetos en el Almacen Kafra.",
    "We may never meet again, but I hope you grow stronger and become a great adventurer. Godspeed.": "Quizas nunca nos volvamos a ver, pero espero que te hagas mas fuerte y te conviertas en un gran aventurero. Buena suerte.",
    "Hello, may I see your": "Hola, puedo ver tu",
    "proof of registration?": "comprobante de registro?",
    "Ah, \" + strcharinfo(0) + \", you've applied for an old training course that we no longer provide for our trainees. Let me issue a new proof of registration for you.": "Ah, \" + strcharinfo(0) + \", te inscribiste en un curso antiguo que ya no ofrecemos. Dejame darte un nuevo comprobante de registro.",
    "Okay, now": "Bien, ahora",
    "you're ready to go.": "estas listo.",
    "In my class, I teach the": "En mi clase, enseno el",
    "use of the most basic": "uso de las interfaces",
    "interfaces.": "mas basicas.",
    "would you like to learn": "te gustaria aprender",
    "more about interface": "mas sobre los fundamentos",
    "fundamentals?": "de las interfaces?",
    'select("Yes.:Nah, I\'m a pro~:Cancel.")': 'select("Si.:Nah, soy un pro~:Cancelar.")',
    "First, it's possible to move every interface window on your screen by dragging the window. Just click on the window, hold down the mouse button and move your mouse.": "Primero, es posible mover cada ventana de interfaz en tu pantalla arrastrando la ventana. Solo haz clic en la ventana, manten presionado el boton del mouse y mueve el mouse.",
    "Now, let me explain each interface window according to their default positions on your screen.": "Ahora, dejame explicarte cada ventana de interfaz segun sus posiciones predeterminadas en tu pantalla.",
    "At the upper left side of your screen, you will see a window with your character name and level. This is the ^3355FFBasic Information Window^000000.": "En la parte superior izquierda de tu pantalla, veras una ventana con el nombre y nivel de tu personaje. Esta es la ^3355FFVentana de Informacion Basica^000000.",
    "Let me give you": "Dejame darte",
    "some experience points.": "algunos puntos de experiencia.",
    "Keep an eye on your Basic Info Window and observe the change in your Base Level experience gauge.": "Observa tu Ventana de Info Basica y mira el cambio en la barra de experiencia de Nivel Base.",
    "Did you see...?": "Lo viste...?",
    "As you gain experience,": "A medida que ganas experiencia,",
    "the experience gauge fills up.": "la barra de experiencia se llena.",
    "Once it is 100 % full, you gain an experience level, and the gauge is reset to 0.": "Una vez que este al 100%, ganas un nivel de experiencia, y la barra se reinicia a 0.",
    "But...": "Pero...",
    "I guess you're already familiar with the Base Level experience gauge.": "supongo que ya estas familiarizado con la barra de experiencia de Nivel Base.",
    "At the bottom of the Basic Info Window, you will see two different experience gauge bars. The top bar is for your current Base Level, and the bottom one displays experience for your current Job Level.": "En la parte inferior de la Ventana de Info Basica, veras dos barras de experiencia diferentes. La barra superior es para tu Nivel Base actual, y la inferior muestra la experiencia de tu Nivel de Trabajo actual.",
    "When the Job Level": "Cuando la barra de Experiencia",
    "Experience bar is filled, you will earn a Job Level, and a ^3355FFSkill Point^000000. Skill Points are spent to learn skills for your character.": "de Nivel de Trabajo se llene, ganaras un Nivel de Trabajo, y un ^3355FFPunto de Habilidad^000000. Los Puntos de Habilidad se usan para aprender habilidades para tu personaje.",
    "On the right side": "En el lado derecho",
    "of the Basic Info window,": "de la ventana de Info Basica,",
    "you will see various": "veras varios",
    "Menu buttons.": "botones de Menu.",
    "Clicking these Menu buttons will open other Interface Windows, such as the Inventory Window": "Al hacer clic en estos botones del Menu se abriran otras Ventanas de Interfaz, como la Ventana de Inventario",
    "or Party Window.": "o la Ventana de Grupo.",
    "Now...": "Ahora...",
    "The ^3355FFChat Window^000000 is": "La ^3355FFVentana de Chat^000000 esta",
    "located at the bottom": "ubicada en la parte inferior",
    "of your screen.": "de tu pantalla.",
    "At the bottom right of the Chat Window, you should see 2 blue buttons. The left button allows you to change your chatting options.": "En la parte inferior derecha de la Ventana de Chat, veras 2 botones azules. El boton izquierdo te permite cambiar tus opciones de chat.",
    "The '^3355FFSend to All^000000' option": "La opcion '^3355FFEnviar a Todos^000000'",
    "allows you to chat with": "te permite chatear con",
    "everyone on your screen.": "todos en tu pantalla.",
    "The '^3355FFSend to Party^000000' and '^3355FFSend to Guild^000000' options allows you to send messages to only members of your party or guild, regardless of how far they are.": "Las opciones '^3355FFEnviar al Grupo^000000' y '^3355FFEnviar al Gremio^000000' te permiten enviar mensajes solo a miembros de tu grupo o gremio, sin importar que tan lejos esten.",
    "You can drag the Scroll Bar": "Puedes arrastrar la Barra de Desplazamiento",
    "on the right side of the Chat Window to review a conversation. Since the Chat Window is always active, you won't have any problem communicating with other players.": "en el lado derecho de la Ventana de Chat para revisar una conversacion. Como la Ventana de Chat siempre esta activa, no tendras problemas para comunicarte con otros jugadores.",
    "Now, one of the most important interfaces is the ^3355FFMini-Map^000000, located at the upper-right of your screen.": "Ahora, una de las interfaces mas importantes es el ^3355FFMini-Mapa^000000, ubicado en la parte superior derecha de tu pantalla.",
    "The red dots on the Mini-Map indicate locations of ^3355FFWarp Portals^000000 which connect to different zones.": "Los puntos rojos en el Mini-Mapa indican las ubicaciones de ^3355FFPortales Warp^000000 que conectan a diferentes zonas.",
    "If you've joined a party or a guild, the Mini-Map will also show you the location of your party or guild members if they are on the same map.": "Si te has unido a un grupo o gremio, el Mini-Mapa tambien te mostrara la ubicacion de los miembros de tu grupo o gremio si estan en el mismo mapa.",
    "Please click the Menu buttons": "Por favor haz clic en los botones del Menu",
    "on the right side of your Basic Info window and familiarize yourself with the other interfaces.": "en el lado derecho de tu ventana de Info Basica y familiarizate con las otras interfaces.",
    "Well, that was my brief overview on in-game interfaces. It might seem like a lot of information now, but it will soon become second nature.": "Bueno, esa fue mi breve descripcion de las interfaces del juego. Puede parecer mucha informacion ahora, pero pronto sera algo natural.",
    "Let me give you a little bit of Job experience points. Open your Skill Window and distribute your Skill Points into ^3355FFBasic Skills^000000.": "Dejame darte algunos puntos de experiencia de Trabajo. Abre tu Ventana de Habilidades y distribuye tus Puntos de Habilidad en ^3355FFHabilidades Basicas^000000.",
    "Your Job Level is much higher than I had expected. You must already know the basic information by now.": "Tu Nivel de Trabajo es mucho mas alto de lo que esperaba. Ya debes conocer la informacion basica a estas alturas.",
    "Now, why don't you speak to Edwin? He will teach you more regarding the basic use of Skills. Ah, and let me give you a small present: a Tattered Novice Ninja Suit!": "Ahora, por que no hablas con Edwin? El te ensenara mas sobre el uso basico de Habilidades. Ah, y dejame darte un pequeno regalo: un Tattered Novice Ninja Suit!",
    "Let me guide you": "Dejame guiarte",
    "to the Field Combat": "al Curso de Entrenamiento",
    "Training Course.": "de Combate de Campo.",
    "You can come back any time if you feel that you need a review.": "Puedes volver cuando sientas que necesitas repasar.",
    "How may I help you?": "En que puedo ayudarte?",
    "Can I see your proof of registration?": "Puedo ver tu comprobante de registro?",
    "It seems that you haven't attended the Skill Information class yet. Please talk to a tutor to the very left of this room to attend his class.": "Parece que aun no has asistido a la clase de Informacion de Habilidades. Por favor habla con un tutor al extremo izquierdo de esta sala para asistir a su clase.",
    'select("Thank you!:I\'m tired of classes~:Cancel")': 'select("Gracias!:Estoy cansado de clases~:Cancelar")',
    "When you attend the Skill Information class, you'll gain a better understanding of the use of skills.": "Cuando asistas a la clase de Informacion de Habilidades, obtendras una mejor comprension del uso de habilidades.",
    "Since the use of skills is integral to survival in Midgard, I strongly suggest that you attend the class. Come, I shall guide you there.": "Ya que el uso de habilidades es fundamental para sobrevivir en Midgard, te sugiero que asistas a la clase. Ven, te guiare alli.",
    "I see. In that case, you must be ready for the Field Combat Training Course. Shall I send you there right away?": "Ya veo. En ese caso, debes estar listo para el Curso de Combate de Campo. Te envio alli de inmediato?",
    'select("No! W-wait!:Please do~!")': 'select("No! E-espera!:Por favor~!")',
    "...?!": "...?!",
    "O...kay then.": "E-esta bien.",
    "Please come back": "Por favor vuelve",
    "when you're ready.": "cuando estes listo.",
    "Godspeed,": "Buena suerte,",
    "young Novice.": "joven Novato.",
    "It looks like you still haven't attended the Item Information class yet. Please speak to the tutor to the very right of this room to attend her class.": "Parece que aun no has asistido a la clase de Informacion de Objetos. Por favor habla con la tutora al extremo derecho de esta sala para asistir a su clase.",
    'select("Thank you.:I\'m tired of classes~:Cancel")': 'select("Gracias.:Estoy cansado de clases~:Cancelar")',
    "The Item Information class is very useful for you to learn how to use your Hot keys and Hot key bars. Come, let me guide you there.": "La clase de Informacion de Objetos es muy util para aprender a usar tus Teclas Rapidas y barras de Teclas Rapidas. Ven, dejame guiarte alli.",

    # Cecil (Skill Tutor)
    "Did you need more help?": "Necesitas mas ayuda?",
    "I see that you've completed all the essential courses. Did you speak to the assistant tutors too?": "Veo que has completado todos los cursos esenciales. Tambien hablaste con los tutores asistentes?",
    'select("Send me to the next course!:Assistant tutors?:Take me to a town!")': 'select("Enviame al siguiente curso!:Tutores asistentes?:Llevame a una ciudad!")',
    "Ah! Right, right.": "Ah! Cierto, cierto.",
    "You've got to take on the Field Combat Training Course sometime, I suppose.": "Supongo que tendras que hacer el Curso de Combate de Campo en algun momento.",
    "Man, I'm so jealous of the instructors in the Field Combat Training Course. Teaching basic information is just soooo not as cool as beating stuff up.": "Vaya, les tengo tanta envidia a los instructores del Curso de Combate de Campo. Ensenar informacion basica no es tan genial como pelear.",
    "Ah, right.": "Ah, cierto.",
    "Field Combat.": "Combate de Campo.",
    "I'm sending you now.": "Te envio ahora.",
    "Good luck, kid!": "Buena suerte, chico!",
    "You know about the": "Conoces a los",
    "assistant tutors, don't you?": "tutores asistentes, verdad?",
    "Listen. The three of tutors in this room only teach the most basic information. The courses we teach are meant to be passed quickly.": "Escucha. Los tres tutores en esta sala solo ensenan la informacion mas basica. Los cursos que ensenamos estan hechos para completarse rapido.",
    "But some people might benefit a little bit more if they learned some more detailed information.": "Pero algunas personas podrian beneficiarse mas si aprendieran informacion mas detallada.",
    "If you're completely new to Ragnarok, it couldn't hurt to attend the classes held by the assistant tutors at least once.": "Si eres completamente nuevo en Ragnarok, no estaria mal asistir a las clases de los tutores asistentes al menos una vez.",
    "A guy named Leo Handerson seems to know a lot about skills, so I think his knowledge would be useful to you.": "Un tipo llamado Leo Handerson parece saber mucho sobre habilidades, asi que creo que su conocimiento te seria util.",
    "A town...?": "Una ciudad...?",
    "What do I look like, your own personal Peco Peco?": "Que parezco, tu Peco Peco personal?",
    "That's right, you might be too young to know about that. Listen, if you want to move to a town, speak to the Kafra Lady to the right, okay?": "Es verdad, quizas eres muy joven para saber de eso. Escucha, si quieres ir a una ciudad, habla con la Senora Kafra a la derecha, de acuerdo?",
}

# Apply translations line by line
applied = 0
for i, line in enumerate(lines):
    for eng, spa in trans.items():
        if eng in line:
            lines[i] = line.replace(eng, spa)
            applied += 1
            break

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print(f"Applied {applied} line translations")
