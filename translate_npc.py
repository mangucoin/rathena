#!/usr/bin/env python3
"""
Translate rAthena NPC script files from English to LATAM Spanish.
Processes mes "...", select("..."), announce/mapannounce strings.
Preserves all code, variables, color codes, NPC names in brackets.
Uses tu form (LATAM). No double quotes inside strings. No colons in select options.
Maintains exact line count.
"""
import re
import sys

def is_likely_spanish(text):
    """Heuristic to detect if text is already in Spanish."""
    clean = text.lower().strip()
    padded = ' ' + clean + ' '
    sw = [' que ',' los ',' las ',' del ',' por ',' para ',' pero ',' con ',' una ',
          ' este ',' esta ',' mis ',' tus ',' sus ',' nos ',' les ',
          ' si ',' tu ',' yo ',' en ',' es ',' de ',' se ',' te ',' ya ',
          ' muy ',' mas ',' hay ',' ser ',' son ',' fue ',' era ',' eso ',
          ' asi ',' ahi ',' estas ',' tiene ',' puede ',' como ',
          'verdad','tambien','puedes','tienes','entrenamiento','batalla',
          'miembros','participar','unirte','decision','bendiga','molestes',
          'tablero','anuncios','mision','nivel','equipo','fabricado',
          'regalos','recompensa','experiencia','orgulloso','peligro',
          'herido','bienvenido','felicidades','necesitas','deberias',
          'trabajo','serio','quieres','curiosidad','problemas',
          'esencial','dificil','ahora','aqui','donde','cuando',
          'gracias','bueno',' bien ',' malo ',' hacia ',
          'puerta','cueva','aldea','ciudad','enemigo',
          'monstruo','cuidado','peligroso','seguro',
          'fuerte','debil','rapido',' vida ',' muerte ',
          'ayuda','dinero','arma','armadura','escudo',
          'espada','casco','botas','capa','anillo',
          'pocion','misiones','busca','habla','camina',
          'pelea','lucha','mata','regresa','vuelve',
          'sigue','entra','toma','dime','mira','escucha',
          'espera','derrota','caza','recoge','entrega',
          'completa','acepta','rechaza','confirma',
          ' eres ',' somos ',' estoy ',' estan ',
          'puedo','podemos','pueden','quiere',
          'necesita','debemos','podria','hecho',
          'dicho','visto','abierto','cerrado',
          'hablame','dime','pregunta','responde',
          'empezar','terminar','acabar','seguir',
          'subir','bajar','salir','llegar','pasar',
          'recibir','obtener','conseguir','perder',
          'ganar','morir','vivir','creer','pensar',
          'saber','conocer','querer','poder','deber',
          'estar','tener','haber','hacer','decir',
          'venir','poner','traer','llevar','dar',
          'listo','preparado','cerca','lejos',
          'dentro','fuera','arriba','abajo',
          'izquierda','derecha','norte','sur',
          'este','oeste',' rey ',' reina ',
          'principe','princesa','guerrero',
          'cazador','mago','sacerdote','ladron',
          'caballero','mercader','asesino',
          'alquimista','herrero','bardo',
          'bailarina','monje','cruzado',
          'sabio','hechicero','ranger',
          'arcobispo','mecanico','genetista',
          'trovador','vagabundo','sura',
          'guardia','soldado','capitan',
          'general','comandante','lider',
          'jefe','maestro','instructor']
    count = sum(1 for w in sw if w in padded)
    return count >= 2


def translate_text(text):
    """Translate English text to LATAM Spanish. Returns translated text."""
    if not text or not text.strip():
        return text

    # Check if already Spanish
    if is_likely_spanish(text):
        return text

    # Handle color codes: split by ^XXXXXX, translate non-code parts, rejoin
    color_pattern = r'(\^[0-9a-fA-F]{6})'
    parts = re.split(color_pattern, text)
    if len(parts) > 1:
        result = []
        for part in parts:
            if re.match(color_pattern + r'$', part):
                result.append(part)
            elif part.strip():
                result.append(translate_plain(part))
            else:
                result.append(part)
        return ''.join(result)

    return translate_plain(text)


def translate_plain(text):
    """Translate plain English text (no color codes) to Spanish."""
    if not text.strip():
        return text
    if is_likely_spanish(text):
        return text

    # Try exact match first
    stripped = text.strip()
    if stripped in TRANS:
        leading = text[:len(text)-len(text.lstrip())]
        return leading + TRANS[stripped]

    # Try case-insensitive
    for k, v in TRANS.items():
        if k.lower() == stripped.lower():
            leading = text[:len(text)-len(text.lstrip())]
            return leading + v

    # Return as-is if no translation found
    return text


# ============================================================
# MASSIVE TRANSLATION DICTIONARY
# ============================================================
TRANS = {
    # === COMMON SHORT PHRASES ===
    "What?!": "Que?!",
    "Huh?": "Eh?",
    "What?": "Que?",
    "Why?": "Por que?",
    "Really?": "En serio?",
    "Yes.": "Si.",
    "No.": "No.",
    "Okay.": "Esta bien.",
    "Sure.": "Claro.",
    "Thanks.": "Gracias.",
    "Thank you.": "Gracias.",
    "Thank you!": "Gracias!",
    "Sorry.": "Disculpa.",
    "Hello.": "Hola.",
    "Hello!": "Hola!",
    "Hi.": "Hola.",
    "Bye.": "Adios.",
    "Goodbye.": "Adios.",
    "Welcome.": "Bienvenido.",
    "Welcome!": "Bienvenido!",
    "Good luck.": "Buena suerte.",
    "Good luck!": "Buena suerte!",
    "Good luck~!": "Buena suerte~!",
    "Good job.": "Buen trabajo.",
    "Good job!": "Buen trabajo!",
    "Great.": "Genial.",
    "Great!": "Genial!",
    "Great job.": "Buen trabajo.",
    "Excellent.": "Excelente.",
    "Excellent!": "Excelente!",
    "Amazing!": "Increible!",
    "Cool.": "Genial.",
    "Cool!": "Genial!",
    "Congratulations.": "Felicidades.",
    "Congratulations!": "Felicidades!",
    "Be careful.": "Ten cuidado.",
    "Be careful!": "Ten cuidado!",
    "Nothing.": "Nada.",
    "Nevermind.": "No importa.",
    "Never mind.": "No importa.",
    "Of course.": "Por supuesto.",
    "Of course!": "Por supuesto!",
    "I see.": "Ya veo.",
    "I see...": "Ya veo...",
    "I understand.": "Entiendo.",
    "Good.": "Bien.",
    "Fine.": "Bien.",
    "Wait.": "Espera.",
    "Wait!": "Espera!",
    "Let me see...": "Dejame ver...",
    "Let's see...": "Veamos...",
    "...": "...",
    "......": "......",
    ".........": ".........",
    "Oh.": "Oh.",
    "Oh!": "Oh!",
    "Oh?": "Oh?",
    "Haha.": "Jaja.",
    "Hahaha.": "Jajaja.",
    "Hey.": "Oye.",
    "Hey!": "Oye!",
    "Come on.": "Vamos.",
    "Come on!": "Vamos!",
    "Who are you?": "Quien eres?",
    "What is it?": "Que es?",
    "What do you want?": "Que quieres?",
    "What happened?": "Que paso?",
    "How are you?": "Como estas?",
    "Are you okay?": "Estas bien?",
    "Are you sure?": "Estas seguro?",
    "Do you understand?": "Entiendes?",
    "Got it?": "Entendido?",
    "Understand?": "Entiendes?",
    "Come back later.": "Regresa despues.",
    "See you later.": "Nos vemos despues.",
    "See you.": "Nos vemos.",
    "Take care.": "Cuidate.",
    "Take care!": "Cuidate!",
    "Forget it.": "Olvidalo.",
    "Just kidding.": "Es broma.",
    "No way.": "De ninguna manera.",
    "No way!": "De ninguna manera!",
    "That's right.": "Asi es.",
    "Please.": "Por favor.",
    "Help!": "Ayuda!",
    "Help me!": "Ayudame!",
    "Stop!": "Detente!",
    "Go!": "Ve!",
    "Run!": "Corre!",
    "Hurry!": "Apurate!",
    "Hurry up!": "Apurate!",
    "Leave.": "Vete.",
    "Listen.": "Escucha.",
    "Look.": "Mira.",
    "Watch out!": "Cuidado!",
    "Careful!": "Cuidado!",
    "Danger!": "Peligro!",
    "Finally!": "Por fin!",
    "Impossible!": "Imposible!",
    "Incredible!": "Increible!",
    "Unbelievable!": "Increible!",
    "Wonderful!": "Maravilloso!",
    "Perfect!": "Perfecto!",
    "Perfect.": "Perfecto.",
    "Interesting.": "Interesante.",
    "Interesting...": "Interesante...",
    "Oops.": "Ups.",

    # === SELECT OPTIONS ===
    "Yes": "Si",
    "No": "No",
    "Accept": "Aceptar",
    "Refuse": "Rechazar",
    "Refuse!": "Rechazar!",
    "Refuse!!": "Rechazar!!",
    "Cancel": "Cancelar",
    "Continue": "Continuar",
    "Leave": "Irse",
    "Stay": "Quedarse",
    "Ignore": "Ignorar",
    "Ignore.": "Ignorar.",
    "Nothing": "Nada",
    "End Conversation.": "Terminar conversacion.",
    "End Conversation": "Terminar conversacion",
    "I'll pass.": "Paso.",
    "Not interested.": "No me interesa.",
    "Sure thing.": "Claro que si.",
    "No, way.": "No, para nada.",
    "Absolutely, I will.": "Por supuesto que si.",
    "I'm just visiting.": "Solo estoy de visita.",
    "I'm just visiting": "Solo estoy de visita",
    "A situation?": "Una situacion?",
    ".....": ".....",

    # === EDEN QUESTS ===
    "I don't have anything to say to outsiders.": "No tengo nada que decirle a los de afuera.",
    "If you want something register with my group.": "Si quieres algo, registrate en mi grupo.",
    "To register with the Eden Group ask Laime Evenor next to me.": "Para registrarte en el Grupo Eden, habla con Laime Evenor a mi lado.",
    "It's not my business but you should probably reconsider.": "No es asunto mio, pero probablemente deberias reconsiderarlo.",
    "You are so honest!": "Eres muy honesto!",
    "Gosh. You wanted to know something about equipment?": "Vaya. Querias saber algo sobre el equipo?",
    "I have a uniform set which is free for our group members.": "Tengo un conjunto de uniforme gratis para los miembros de nuestro grupo.",
    "But, I can't give it for free.": "Pero no lo puedo dar gratis.",
    "We give it to great participants who do their best in the training.": "Se lo damos a los grandes participantes que dan lo mejor de si en el entrenamiento.",
    "-Boya eyes you from top to bottom.": "-Boya te mira de arriba a abajo.",
    "Hmm... he seems to think something is wrong.-": "Hmm... parece que piensa que algo esta mal.-",
    "Due to emotion.": "Por la emocion.",
    "So, will you join the training or not?": "Entonces, te vas a unir al entrenamiento o no?",
    "I look a little bit funny, actually I am really busy I was called shining Rune Knight.": "Me veo un poco gracioso, en realidad estoy muy ocupado, me llamaban el brillante Rune Knight.",
    "Make a decision, hurry.": "Toma una decision, apurate.",
    "You are so rude!": "Eres muy grosero!",
    "-Beats quickly and this shining Rune Knight turns invisible.": "-Golpea rapido y este brillante Rune Knight se vuelve invisible.",
    "It hurts too much-": "Duele demasiado-",
    "Hey, I already talked all about the training areas.": "Oye, ya te hable de todas las areas de entrenamiento.",
    "I will explain again please concentrate.": "Te lo explicare de nuevo, por favor concentrate.",
    "An oasis souteast of Morocc.": "Un oasis al sureste de Morocc.",
    "There is a big dog in the center.": "Hay un perro grande en el centro.",
    "The detailed story is written in the log, see?": "La historia detallada esta escrita en el registro, ves?",
    "Oh you've come back.": "Oh, regresaste.",
    "Now you are adapting.": "Ahora te estas adaptando.",
    "Completed step 1.": "Paso 1 completado.",
    "We will give you a uniform and some equipment.": "Te daremos un uniforme y algo de equipo.",
    "Can you see a large blue gate next to the board?": "Puedes ver una gran puerta azul junto al tablero?",
    "Go inside then keep walking until the end of the right passage. There is an equipment storage there.": "Entra y sigue caminando hasta el final del pasillo derecho. Ahi hay un almacen de equipo.",
    "Inform the manager that I sent you. He will give you some stuff.": "Dile al encargado que yo te envie. El te dara algunas cosas.",
    "The training name was 'Conquer the Culvert!.": "El nombre del entrenamiento era 'Conquista la Alcantarilla!'.",
    "Did you explore the culvert fully?": "Exploraste la alcantarilla completamente?",
    "Come back when you've completed all the courses from the local trainer.": "Regresa cuando hayas completado todos los cursos del entrenador local.",
    "Oh you're back.": "Oh, regresaste.",
    "My team will give you a uniform and some equipment.": "Mi equipo te dara un uniforme y algo de equipo.",
    "What are you doing?": "Que estas haciendo?",
    "Get the equipment from the storage manager.": "Obtene el equipo del encargado del almacen.",
    "Our uniform is pretty awesome haha.": "Nuestro uniforme es genial, jaja.",
    "Um, did you like the supplies?": "Y, te gustaron los suministros?",
    "I like the red hat.": "Me gusta el gorro rojo.",
    "The red ribbon is really cute.": "El liston rojo es muy lindo.",
    "And you seem to.": "Y pareces estar listo.",
    "Able to take upper class, now.": "Ya puedes tomar la clase superior.",
    "What about it, do you want?": "Que dices, quieres?",
    "Actually I don't care but the uniform will be changed as upper class.": "En realidad no me importa, pero el uniforme cambiara como clase superior.",
    "The battle training is organized into steps.": "El entrenamiento de batalla esta organizado en pasos.",
    "When you able to join next step come back again after leveling more.": "Cuando puedas unirte al siguiente paso, regresa despues de subir mas de nivel.",
    "The next training step is available for those over Level 26.": "El siguiente paso de entrenamiento esta disponible para los de nivel 26 o mas.",
    "When you reach that level, come by again. get it?": "Cuando alcances ese nivel, ven de nuevo, entendido?",
    "The training area is at the north cave of Payon.": "El area de entrenamiento esta en la cueva al norte de Payon.",
    "A staff member is already dispatched there.": "Un miembro del personal ya fue enviado ahi.",
    "Find him and follow his directions.": "Encuentralo y sigue sus instrucciones.",
    "You finished the second step of training.": "Terminaste el segundo paso del entrenamiento.",
    "Now do you understand how this world is organized?": "Ahora entiendes como esta organizado este mundo?",
    "I will certify that you completed the training.": "Certificare que completaste el entrenamiento.",
    "The person in charge of equipment storage will supply you with what you need.": "La persona a cargo del almacen de equipo te dara lo que necesitas.",
    "Choose an equipment that fits your particular set of skills.": "Elige un equipo que se adapte a tus habilidades.",
    "The training area is southwest of Morocc.": "El area de entrenamiento esta al suroeste de Morocc.",
    "Enter the Saint Darmain Fortress to reach it directly.": "Entra a la Fortaleza Saint Darmain para llegar directamente.",
    "There's someone there named... Uh... he is waiting for you to follow his direction.": "Hay alguien ahi llamado... Eh... esta esperando a que sigas sus instrucciones.",
    "We serve trainees with equipment and armor after passing the second step of training.": "Les damos equipo y armadura a los aprendices despues de pasar el segundo paso del entrenamiento.",
    "Go to the storage and meet the person in charge there.": "Ve al almacen y habla con la persona a cargo.",
    "To find the storage pass the blue gate next to the mission board then at the end of the hallway to the right side.": "Para encontrar el almacen, pasa la puerta azul junto al tablero de misiones, al final del pasillo a la derecha.",
    "The person in charge of equipment storage will supply you with some equipment.": "La persona a cargo del almacen de equipo te dara algo de equipo.",
    "Hey long time no see.": "Oye, cuanto tiempo sin verte.",
    "So what's up?": "Y que pasa?",
    "Hmm... really?": "Hmm... en serio?",
    "Let me see... which step is good for you...": "Dejame ver... cual paso es bueno para ti...",
    "Sooo sorry but to join this training You need to be at least level 40.": "Lo siento mucho, pero para este entrenamiento necesitas ser al menos nivel 40.",
    "Concentrate to become higher level then come back.": "Concentrate en subir de nivel y luego regresa.",
    "Did you come to see me?": "Viniste a verme?",
    "Just that? Without anything?": "Solo eso? Sin nada?",
    "At could have least brought some chocolate...": "Al menos pudiste haber traido un chocolate...",
    "Banana roll or stripe straw... anything.": "Rollo de banana o pajita rayada... lo que sea.",
    "Oh, I don't eat snacks with cinnamon...": "Oh, no como bocadillos con canela...",
    "Umm. Orc village has a Kafra Employee there so you can use the Kafra services.": "Mmm. La aldea Orc tiene una Empleada Kafra, asi que puedes usar los servicios Kafra.",
    "One of our dispatched members is waiting in the building near the Kafra Employee.": "Uno de nuestros miembros enviados esta esperando en el edificio cerca de la Empleada Kafra.",
    "Cool! You passed the third step of training.": "Genial! Pasaste el tercer paso del entrenamiento.",
    "Umm. Orc village has a Kafra Employee there so you can use the Kafra services there.": "Mmm. La aldea Orc tiene una Empleada Kafra, asi que puedes usar los servicios Kafra ahi.",
    "First take a ship toward to Bayalan from Izlude!": "Primero toma un barco hacia Bayalan desde Izlude!",
    "There is an underground cave. Go in and get to the bottom floor where you will find a historic underwater city..": "Hay una cueva subterranea. Entra y llega al piso inferior donde encontraras una historica ciudad submarina.",
    "There is a dispatched trainee around the entrance of the Ocean City.": "Hay un aprendiz enviado cerca de la entrada de la Ciudad Oceanica.",
    "If you finish all of the steps go and get your supplies.": "Si terminas todos los pasos, ve y recoge tus suministros.",
    "We offer equipment to those who complete the training.": "Ofrecemos equipo a quienes completan el entrenamiento.",
    "We might serve you other things.": "Podemos darte otras cosas.",
    "If you have any questions, ask the person in charge of the arsenal.": "Si tienes preguntas, preguntale a la persona a cargo del arsenal.",
    "The arsenal is past the blue gate and at the end of the right side of the passage.": "El arsenal esta pasando la puerta azul, al final del lado derecho del pasillo.",
    "My boss created all the courses for the training.": "Mi jefe creo todos los cursos para el entrenamiento.",
    "After he manufactured the uniform and supplies he changed his mind and said that he can't give them for free.": "Despues de fabricar el uniforme y los suministros, cambio de opinion y dijo que no puede darlos gratis.",
    "People who show their effort for my team and the world can get some supplies.": "Las personas que muestren su esfuerzo por mi equipo y el mundo pueden obtener suministros.",
    "That's why these courses were made.": "Por eso se crearon estos cursos.",
    "Basically we are supposed to offer these supplies for beginners": "Basicamente debemos ofrecer estos suministros para principiantes",
    "but if experts want to participate this training, we accept them.": "pero si los expertos quieren participar en este entrenamiento, los aceptamos.",
    "Although the uniform and equipment might be useless.": "Aunque el uniforme y el equipo puedan ser inutiles.",
    "participating in this training means they want to become a member of our group.": "participar en este entrenamiento significa que quieren ser miembros de nuestro grupo.",
    "Yes that's all.": "Si, eso es todo.",
    "That's why when we decided a hat design it was really difficult.": "Por eso cuando decidimos el diseno del gorro fue muy dificil.",
    "Remember this when you use the equipment.": "Recuerda esto cuando uses el equipo.",
    "But if you decide to sell or trade them off, it is none of our concern.": "Pero si decides venderlos o intercambiarlos, no es asunto nuestro.",
    "I doubt that you need more training.": "Dudo que necesites mas entrenamiento.",
    "There is nothing more I can teach a battle master such as yourself.": "No hay nada mas que pueda ensenarle a un maestro de batalla como tu.",
    "Really? You already seem ready.": "En serio? Ya pareces listo.",
    "We have a total of 3 steps for the training.": "Tenemos un total de 3 pasos para el entrenamiento.",
    "Umm. You should raise your level more!": "Mmm. Deberias subir mas tu nivel!",
    "You need to be at least level 12!": "Necesitas ser al menos nivel 12!",
    "I'm sorry but those are the rules.": "Lo siento, pero esas son las reglas.",
    "The first step is course A.": "El primer paso es el curso A.",
    "Course A is called 'Conquer the Desert!'.": "El curso A se llama 'Conquista el Desierto!'.",
    "If you go there, you will find a dog around the oasis.": "Si vas ahi, encontraras un perro cerca del oasis.",
    "He is really mysterious and he can speak so don't be suprised.": "Es muy misterioso y puede hablar, asi que no te sorprendas.",
    "Why are you staring at me?": "Por que me miras fijamente?",
    "I had to come up with a password right?": "Tenia que inventar una contrasena, no?",
    "What's wrong with that password?": "Que tiene de malo esa contrasena?",
    "Anyway, that place is not far from here so, it is a reasonable place for a beginner like you.": "De todos modos, ese lugar no esta lejos de aqui, es un lugar razonable para un principiante como tu.",
    "I'll send you to the first step of course B.": "Te enviare al primer paso del curso B.",
    "Course B is called 'Conquer the Culvert!'.": "El curso B se llama 'Conquista la Alcantarilla!'.",
    "You need to register to explore the culvert in Prontera at the Knight Guild.": "Necesitas registrarte para explorar la alcantarilla en Prontera en el Gremio de Caballeros.",
    "After registering there go to the western gate of Prontera. The manager of the culvert is near the entrance.": "Despues de registrarte, ve a la puerta oeste de Prontera. El encargado esta cerca de la entrada.",
    "Once you enter the culvert you can find a dispatched cat. Don't be surprised if he talks to you.": "Una vez que entres a la alcantarilla, encontraras un gato enviado. No te sorprendas si te habla.",
    "He will give you a battle target when you tell him that.": "Te dara un objetivo de batalla cuando le digas eso.",
    "If you have any questions ask the cat.": "Si tienes preguntas, preguntale al gato.",
    "Why are you staring at me like that?": "Por que me miras asi?",
    "It's just a password that I made up.": "Es solo una contrasena que me invente.",
    "That place is nor far from here so, it is a reasonable place for a beginner like you.": "Ese lugar no esta lejos de aqui, es un lugar razonable para un principiante como tu.",
    "Travel just southwest of Morocc City.": "Viaja al suroeste de la Ciudad de Morocc.",
    "There you will find a hole in the ground to a cave called Anthell.": "Ahi encontraras un agujero en el suelo hacia una cueva llamada Anthell.",
    "There are lots of ants in there. kk?": "Hay muchas hormigas ahi. ok?",
    "It is also covered in sand so be careful in there ok.": "Tambien esta cubierta de arena, asi que ten cuidado ahi, ok.",
    "That's why it's called ant hell.": "Por eso se llama ant hell.",
    "One of our members will be waiting there.": "Uno de nuestros miembros estara esperando ahi.",
    "His name is... K? M? Hmm? Anyway I can't remember.": "Su nombre es... K? M? Hmm? En fin, no me acuerdo.",
    "He is one of us so he will know me.": "El es de los nuestros, asi que me conoce.",
    "He will give you a mission.": "Te dara una mision.",
    "If you have any questions ask him.": "Si tienes preguntas, preguntale.",
    "We haven't met for a long time that's why I can't remember his name!": "No nos hemos visto en mucho tiempo, por eso no recuerdo su nombre!",
    "That place is not far from here so, come back quickly.": "Ese lugar no esta lejos de aqui, asi que regresa rapido.",
    "Ok, blessing you~!!": "Ok, que Freya te bendiga~!!",
    "You are on the third step of course A.": "Estas en el tercer paso del curso A.",
    "This course is called 'Conquer Orc village!'.": "Este curso se llama 'Conquista la aldea Orc!'.",
    "Go through the gate of Prontera and keep walking to the west. Orc Village is in that direction.": "Pasa por la puerta de Prontera y sigue caminando al oeste. La aldea Orc esta en esa direccion.",
    "Or you can go out through the western gate of Geffen and keep heading southeast..": "O puedes salir por la puerta oeste de Geffen y seguir hacia el sureste.",
    "Umm. Orc village has a Kafra Employee dispatched there so you could use the Kafra services..": "Mmm. La aldea Orc tiene una Empleada Kafra enviada, asi que puedes usar los servicios Kafra.",
    "It's up to you.": "Es tu decision.",
    "She will explain what needs to be done there.": "Ella te explicara que se necesita hacer ahi.",
    "If you have any questions ask her.": "Si tienes preguntas, preguntale.",
    "Ok, que Freya te bendiga!": "Ok, que Freya te bendiga!",
    "You are on the third step of course B.": "Estas en el tercer paso del curso B.",
    "This course is called 'Conquer Orc dungeon!'.": "Este curso se llama 'Conquista la mazmorra Orc!'.",
    "You are on the last step.": "Estas en el ultimo paso.",
    "This course is called 'Conquer the Ocean City!'.": "Este curso se llama 'Conquista la Ciudad Oceanica!'.",
    "I don't know if it is the proper course or not, but anyway it's the last course of our training.": "No se si es el curso adecuado o no, pero de todos modos es el ultimo curso de nuestro entrenamiento.",
    "First take a ship to Byalan Island from Izlude!": "Primero toma un barco a la Isla Byalan desde Izlude!",
    "There is an underground cave. Go in and get to the bottom floor where you will find a historic underwater city..": "Hay una cueva subterranea. Entra y llega al piso inferior donde encontraras una historica ciudad submarina.",
    "Although it's underwater, you can breath so don't worry.": "Aunque esta bajo el agua, puedes respirar, asi que no te preocupes.",
    "There is a dispatched trainee around the entrance of the Ocean City.": "Hay un aprendiz enviado cerca de la entrada de la Ciudad Oceanica.",
    "Tell him that I sent you and follow his directions.": "Dile que yo te envie y sigue sus instrucciones.",

    # === TALKING DOG ===
    "kkkkuuuuahhh.": "kkkkuuuuahhh.",
    "rrrrrruuuuhh.": "rrrrrruuuuhh.",
    "bowwow..": "guauguau..",
    "You are!": "Eres!",
    "A member of the Eden Group.": "Un miembro del Grupo Eden.",
    "Have you come to give me a meal? I don't like drinks.": "Viniste a darme comida? No me gustan las bebidas.",
    "Uhh...": "Uhh...",
    "What are you saying.": "Que estas diciendo.",
    "Ahh... um...": "Ahh... eh...",
    "Gosh, did you come here to participate in the training?": "Vaya, viniste aqui a participar en el entrenamiento?",
    "If Boya sent you then you know that it's battle training.": "Si Boya te envio entonces sabes que es entrenamiento de batalla.",
    "Bow wow...": "Guau guau...",
    "If so, should I start securing this oasis more clearly?": "Si es asi, deberia empezar a asegurar este oasis mejor?",
    "Can you see a Condor flying?": "Puedes ver un Condor volando?",
    "Can you scare them away for me?": "Puedes espantarlos por mi?",
    "So people can use this oasis safer and more comfortably.": "Para que la gente pueda usar este oasis de forma mas segura y comoda.",
    "We should hunt at least 10 Condors, ok?": "Debemos cazar al menos 10 Condors, ok?",
    "I will sleep for a while.": "Dormire un rato.",
    "Krrrr woo bow...": "Krrrr woo guau...",
    "Are you ok?": "Estas bien?",
    "Haven't you seen a talking dog before?": "Nunca has visto un perro que habla?",
    "What are you talking about?": "De que estas hablando?",
    "Woooohh...": "Woooohh...",
    "I can feel my youth from you.": "Puedo sentir mi juventud en ti.",
    "Let's find the next target kk!": "Busquemos el siguiente objetivo!",
    "Ok. Let's drive the Desert Wolves out of here.": "Ok. Saquemos a los Desert Wolves de aqui.",
    "If they grow up they will become dangerous.": "Si crecen se volveran peligrosos.",
    "Why, why are you looking at me like that?": "Por que, por que me miras asi?",
    "They are wolves and I am a nice dog.": "Ellos son lobos y yo soy un buen perro.",
    "But I haven't always been a dog my entire life.": "Pero no siempre fui un perro toda mi vida.",
    "I will show you that don't have to pity me at all.": "Te mostrare que no tienes que sentir lastima por mi.",
    "They pee wherever and have no shame.": "Orinan donde sea y no tienen verguenza.",
    "Just waving their tails when they grow up and biting people without any care!": "Solo mueven la cola cuando crecen y muerden a la gente sin importarles!",
    "You must hunt at least 10!": "Debes cazar al menos 10!",
    "Exactly 10!": "Exactamente 10!",
    "You are so perfect.": "Eres perfecto.",
    "Or not. Hehe, anyway thanks for your help.": "O no. Jeje, en fin, gracias por tu ayuda.",
    "The oasis has almost been secured now.": "El oasis ya esta casi asegurado.",
    "Ok, it's the last step!": "Ok, es el ultimo paso!",
    "There's an annoying monster that hides in the sand and poisons people out of nowhere.": "Hay un monstruo molesto que se esconde en la arena y envenena a la gente de la nada.",
    "All beautiful things have some poison inside but these actually kill.": "Todas las cosas bellas tienen algo de veneno, pero estos de verdad matan.",
    "Kill Scorpions which are called the poison of the desert!": "Mata a los Scorpions que son llamados el veneno del desierto!",
    "It's the last step so let's make it simple": "Es el ultimo paso asi que hagamoslo simple",
    "Just hunt 5!": "Solo caza 5!",
    "Bow wow!": "Guau guau!",
    "Um. Excellent.": "Um. Excelente.",
    "You are awesome!": "Eres increible!",
    "Thanks to your effort the oasis is secure.": "Gracias a tu esfuerzo el oasis esta seguro.",
    "Don't look around!": "No mires alrededor!",
    "If I say it's secure!": "Si yo digo que esta seguro!",
    "Uhuhuhuh aaaang!": "Uhuhuhuh aaaang!",
    "Here here here.": "Aqui aqui aqui.",
    "If I dig more and more, I can find Scorpions but": "Si excavo mas y mas, puedo encontrar Scorpions pero",
    "this oasis will be safer for sure.": "este oasis sera mas seguro de seguro.",
    "You've helped a lot to make my rest comfortable.": "Has ayudado mucho a que mi descanso sea comodo.",
    "You've helped to conquer the desert,": "Has ayudado a conquistar el desierto,",
    "and passed the beginner training steps so I will stamp my feet.": "y pasaste los pasos de entrenamiento de principiante, asi que estampare mis patas.",
    "krrrrreuung. hup.": "krrrrreuung. hup.",
    "Go back to the Eden Group headquarters and show it to the flashy Rune Knight.": "Regresa al cuartel general del Grupo Eden y muestraselo al llamativo Rune Knight.",
    "Let me say again that you are great!": "Dejame decirte de nuevo que eres genial!",
    "Hooooohooo~": "Hooooohooo~",
    "Let's hunt only 5 Scorpions.": "Cacemos solo 5 Scorpions.",
    "So we can make peace in this oasis.": "Para que haya paz en este oasis.",
    "When I take a nap they won't chew my tail any more.": "Cuando duerma una siesta ya no me morderan la cola.",
    "Due to his mistake my feet won't be hurt at all.": "Gracias a eso ya no me lastimaran las patas.",
    "You can fight.": "Tu puedes pelear.",
    "I can rest more comfortably.": "Yo puedo descansar mas comodamente.",
    "Other people are going to be safer too.": "Otras personas tambien estaran mas seguras.",
    "Everyone will think fondly of the Eden Group.": "Todos pensaran bien del Grupo Eden.",
    "Oh, if you are tired I will help you.": "Oh, si estas cansado te ayudare.",
    "-When the dog barked, your HP and SP recovered.-": "-Cuando el perro ladro, tus HP y SP se recuperaron.-",
    "First lets follow the bald and noisy bird.": "Primero sigamos al pajaro calvo y ruidoso.",
    "Yes Condors.": "Si, Condors.",
    "Kill 10 Condors. It seems to easy, right?": "Mata 10 Condors. Parece muy facil, verdad?",
    "I don't want you to show any pity.": "No quiero que muestres lastima.",
    "I am dog with a golden heart.": "Soy un perro con corazon de oro.",
    "After hunting the 10 Desert Wolves come back again.": "Despues de cazar los 10 Desert Wolves regresa de nuevo.",
    "If you can't kill the Tarou you might get all kinds of dirty diseases.": "Si no puedes matar a los Tarou podrias contraer todo tipo de enfermedades sucias.",
    "So be proud of yourself and do your best to kill them.": "Asi que sientete orgulloso y da lo mejor de ti para matarlos.",
    "kkkkkaaaaauuuunnng.": "kkkkkaaaaauuuunnng.",
    "oopssss kup.": "oopssss kup.",
    "Why are you still here?": "Por que sigues aqui?",
    "You are done here.": "Ya terminaste aqui.",
    "Hooooo bow wow.": "Hooooo guau guau.",
    "Hey man~ What's going on?": "Oye~ Que pasa?",
    "What about the Rune Knight?": "Y el Rune Knight?",
    "Krrrrr...": "Krrrrr...",
    "Hyuk huk...": "Juk juk...",
    "The Eden Group is cool.": "El Grupo Eden es genial.",
    "They're a really good group.": "Son un grupo muy bueno.",
    "They accepted a wandering talking dog.": "Aceptaron a un perro parlante vagabundo.",
    "Take care and good luck.": "Cuidate y buena suerte.",
    "Hey look.": "Oye mira.",
    "I'm a talking dog.": "Soy un perro que habla.",
    "Not a wolf.": "No soy un lobo.",
    "I wasn't a dog originally...": "Originalmente no era un perro...",
    "Anyway are you a Eden Group member?": "De todos modos, eres miembro del Grupo Eden?",
    "Oh good to see you.": "Oh, que bueno verte.",
    "I am also a member of Eden Group.": "Yo tambien soy miembro del Grupo Eden.",
    "Why are you looking at me like that?": "Por que me miras asi?",

    # Continue with more translations...
    # Due to the massive scale, adding key patterns

    # Timid Cat
    "Meow...": "Miau...",
    "Who are you meow?": "Quien eres, miau?",
    "Why are you here meow?": "Por que estas aqui, miau?",
    "Come on meow...": "Vamos, miau...",
    "I may be standing here and talking to you like this meow but I am a still a cat meow...": "Puede que este aqui parado hablandote asi, miau, pero sigo siendo un gato, miau...",
    "Dear human you are": "Querido humano, eres",
    "a member of my group?": "miembro de mi grupo?",
    "Re... really...!": "De... de verdad...!",
    "Dear Boya's help is like a giant and...": "La ayuda del querido Boya es como un gigante y...",
    "Big and beautiful Saury...": "Saury grande y hermoso...",
    "I am shy.": "Soy timido.",
    "I want to eat mackerel.": "Quiero comer caballa.",
    "Where are the big and fresh mackerel meow?": "Donde estan las caballas grandes y frescas, miau?",
    "Do you know the big and beautiful tuna?": "Conoces el atun grande y hermoso?",
    "Dear Boya sent you here for sure.": "El querido Boya te envio aqui seguro.",
    "How do I explain this...?": "Como te explico esto...?",
    "Did something pass under my feet just now meow?": "Algo paso debajo de mis patas ahora, miau?",
    "Do you want to kill a cat.": "Quieres matar a un gato.",
    "The environment here is terrible.": "El ambiente aqui es terrible.",
    "Anyway I'm doing what I was assigned to do.": "De todos modos estoy haciendo lo que me asignaron.",
    "So hi, hello and welcome.": "Asi que hola, bienvenido.",
    "Did you come here to have a battle?": "Viniste aqui para pelear?",
    "Hunt those Thief Bugs, hurry up!": "Caza esos Thief Bugs, apurate!",
    "Hunt at least 10!": "Caza al menos 10!",
    "Meooow!": "Miaaau!",
    "I really don't like those nasty crawlers...": "De verdad no me gustan esos bichos asquerosos...",
    "Meow~!": "Miau~!",
    "Now do you understand the dirty and humid underground sewers?": "Ahora entiendes las sucias y humedas alcantarillas subterraneas?",
    "Eeeh look what's next meow.": "Eeeh mira que sigue, miau.",
    "It's a symbol of dirt next to those Thief Bugs.": "Es un simbolo de suciedad junto a esos Thief Bugs.",
    "Hunt some Tarou to make the sewers cleaner.": "Caza algunos Tarou para limpiar las alcantarillas.",
    "For our members joining this mission.": "Para nuestros miembros que se unen a esta mision.",
    "Hunt 10 Tarou.": "Caza 10 Tarou.",
    "Easy, ain't it?": "Facil, no?",
    "Why didn't I ask you at once? kkk..??": "Por que no te lo pedi de una vez? jjj..??",
    "Umm........": "Mmm........",
    "Because it's just a training mission.": "Porque es solo una mision de entrenamiento.",
    "Training missions are hard and anoying.": "Las misiones de entrenamiento son dificiles y molestas.",
    "So go hurry and hunt 10 Tarou.": "Asi que apurate y caza 10 Tarou.",
    "Clean the sewers. Now the first step is hunting Thief Bugs.": "Limpia las alcantarillas. El primer paso es cazar Thief Bugs.",
    "Isn't that simple, meow?": "No es simple, miau?",
    "Take care to check your map so you don't get lost.": "Asegurate de revisar tu mapa para no perderte.",
    "It's a service meeow.": "Es un servicio, miau.",
    "Great job~!": "Buen trabajo~!",
    "How'd you get rid of those dirty bugs and Tarou. You are brave.": "Como te deshiciste de esos bichos sucios y Tarou. Eres valiente.",
    "Now have courage because I'm sending you to a stronger opponent.": "Ahora ten valor porque te enviare a un oponente mas fuerte.",
    "But first in order to test your courage, hunt Familiars.": "Pero primero, para probar tu valor, caza Familiars.",
    "Familiars will bite you so be careful.": "Los Familiars te morderan, asi que ten cuidado.",
    "They are mean.": "Son malos.",
    "They scare me so just hunt 5 and that should be enough.": "Me asustan, asi que solo caza 5 y deberia ser suficiente.",
    "That will show me that you are brave.": "Eso me mostrara que eres valiente.",
    "I don't have anything...": "No tengo nada...",
    "What do you want meow? Familiars are waiting to fight with you, hurry up, move~!": "Que quieres, miau? Los Familiars estan esperando para pelear contigo, apurate, muevete~!",
    "Familiars are really scary.": "Los Familiars son muy aterradores.",
    "They're always flying.": "Siempre estan volando.",
    "It's the last course so cheer up.": "Es el ultimo curso, asi que animo.",
    "I will help you a little.": "Te ayudare un poco.",
    "Here, I have recovered your strengh meow..": "Aqui, he recuperado tu fuerza, miau..",
    "You are great meow~": "Eres genial, miau~",
    "You killed them so quickly!": "Los mataste tan rapido!",
    "Now you are not scared of bugs and tarou at all.": "Ahora no les tienes miedo a los bichos ni a los tarou.",
    "Thanks for participating in the Conquer the Culvert training mission.": "Gracias por participar en la mision de entrenamiento Conquista la Alcantarilla.",
    "Now go back to the headquarters and ask Instructor Boya to make sure he has the beautiful tuna...": "Ahora regresa al cuartel general y preguntale al Instructor Boya, asegurate de que tenga el hermoso atun...",
    "I will be waiting here.": "Estare esperando aqui.",
    "Do you know how to get to the Eden Group Headquarters?": "Sabes como llegar al Cuartel General del Grupo Eden?",
    "Prontera is the closest city from here.": "Prontera es la ciudad mas cercana desde aqui.",
    "Go to Prontera and find an Eden Group Teleporter.": "Ve a Prontera y encuentra un Teleportador del Grupo Eden.",
    "You've completed 'Conquer the Culvert'.": "Completaste 'Conquista la Alcantarilla'.",
    "Go back to the Eden Group headquarters to report to Boya.": "Regresa al cuartel general del Grupo Eden para reportarte con Boya.",
    "Boya might eat my tuna while he is waiting for you.": "Boya podria comerse mi atun mientras te espera.",
    "How are you meeow?": "Como estas, miau?",
    "Did you volunteer to conquer the Culvert?": "Te ofreciste como voluntario para conquistar la Alcantarilla?",
    "You are a member of the Edgen Group for sure.": "Eres miembro del Grupo Eden seguro.",
    "You are helping to make the world a better place.": "Estas ayudando a hacer del mundo un lugar mejor.",
}

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    original_count = len(lines)
    new_lines = []
    translated = 0
    untranslated_list = []

    for line in lines:
        stripped = line.strip()

        if stripped.startswith('//') or not stripped:
            new_lines.append(line)
            continue

        # Process mes "..." lines (no + concatenation)
        mes_match = re.match(r'^(\s*mes\s+)"(.*)";(\s*)$', stripped)
        if mes_match and '+' not in stripped.split('mes ')[1] if 'mes ' in stripped else False:
            pass  # handled below

        # Better approach: check if the line is a simple mes line
        simple_mes = re.match(r'^(\s*)mes "(.*)";$', line.rstrip())
        if simple_mes:
            indent = simple_mes.group(1)
            inner = simple_mes.group(2)

            # Skip NPC names
            if re.match(r'^\[.+\]$', inner):
                new_lines.append(line)
                continue

            # Skip non-text
            clean = re.sub(r'\^[0-9a-fA-F]{6}', '', inner)
            if not re.search(r'[a-zA-Z]', clean):
                new_lines.append(line)
                continue

            tr = translate_text(inner)
            tr = tr.replace('"', "'")
            if tr != inner:
                translated += 1
            elif not is_likely_spanish(inner) and re.search(r'[a-zA-Z]', clean):
                untranslated_list.append(inner)

            new_lines.append(indent + 'mes "' + tr + '";')
            continue

        # Process select lines
        if 'select(' in stripped:
            sel_match = re.search(r'select\(\s*"([^"]+)"\s*\)', line)
            if sel_match:
                options_str = sel_match.group(1)
                options = options_str.split(':')
                tr_options = []
                any_changed = False
                for opt in options:
                    tr = translate_text(opt)
                    tr = tr.replace('"', "'").replace(':', '')
                    if tr != opt:
                        any_changed = True
                    else:
                        if not is_likely_spanish(opt) and opt.strip() and re.search(r'[a-zA-Z]', opt):
                            untranslated_list.append('SEL:' + opt)
                    tr_options.append(tr)
                new_options = ':'.join(tr_options)
                if any_changed:
                    translated += 1
                new_line = line.replace('"' + options_str + '"', '"' + new_options + '"')
                new_lines.append(new_line)
                continue

        new_lines.append(line)

    assert len(new_lines) == original_count, f"Line count mismatch! {len(new_lines)} vs {original_count}"

    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        f.write('\n'.join(new_lines))

    unique_untranslated = sorted(set(untranslated_list))
    print(f"Processed {filepath}")
    print(f"  Lines: {original_count}, Translated: {translated}, Untranslated: {len(unique_untranslated)}")

    return unique_untranslated

if __name__ == '__main__':
    files = sys.argv[1:]
    all_ut = []
    for f in files:
        ut = process_file(f)
        all_ut.extend(ut)

    unique = sorted(set(all_ut))
    with open('untranslated.txt', 'w', encoding='utf-8') as f:
        for s in unique:
            f.write(s + '\n')
    print(f"\nTotal unique untranslated: {len(unique)}")
