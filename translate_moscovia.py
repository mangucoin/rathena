#!/usr/bin/env python3
"""
Translate quests_moscovia.txt from English to LATAM Spanish.
Processes entire file, translating mes/select/announce strings.
"""
import re
import sys

INPUT = r"D:\Xponzy Network\Ragnarok-Server\rathena\npc\quests\quests_moscovia.txt"

with open(INPUT, 'r', encoding='utf-8') as f:
    content = f.read()

# Count original lines
orig_lines = content.count('\n')

# We'll do exact string replacements for all English mes/select/announce strings.
# This is a comprehensive mapping of all remaining English strings in the file.

replacements = [
    # === Aged Stranger remaining English (lines ~1685, 1694-1700, 1800-1836) ===
    ('mes "Well, well... Do as you please.";\n\tmes "If so, I will take a rest.";',
     'mes "Bueno, bueno... Haz lo que quieras.";\n\tmes "Si es asi, descansare.";'),

    # S_AS_3 subroutine
    ('mes "-The old man starts to play";\n\tmes "his instrument, with eyes closed.";\n\tmes "He is unresponsive...";\n\tmes "like having fallen into a world";\n\tmes "only his own.-";',
     'mes "-El viejo comienza a tocar";\n\tmes "su instrumento, con los ojos cerrados.";\n\tmes "No responde...";\n\tmes "como si hubiera caido en un mundo";\n\tmes "solo suyo.-";'),

    # Lines 1800-1828 Aged Stranger case 3
    ('mes "Ya veo. Okay, let\'s go.";', 'mes "Ya veo. Bueno, vamonos.";'),
    ('mes "Whenever you want to come back here";\n\t\t\tmes "again, play the Gusli at the docks";\n\t\t\tmes "of Moscovia.";',
     'mes "Cuando quieras volver aqui";\n\t\t\tmes "de nuevo, toca el Gusli en los muelles";\n\t\t\tmes "de Moscovia.";'),
    ("mes \"Even if it's difficult to play it\";\n\t\t\tmes \"well, because you may not yet know\";\n\t\t\tmes \"how to play it, it's not a problem.\";\n\t\t\tmes \"Just make a sound.\";",
     'mes "Aunque sea dificil tocarlo";\n\t\t\tmes "bien, porque quizas aun no sepas";\n\t\t\tmes "como tocarlo, no es un problema.";\n\t\t\tmes "Solo haz un sonido.";'),
    ('mes "This island... this whale... can";\n\t\t\tmes "perceive the sound of a Gusli from";\n\t\t\tmes "an endless distance away.";',
     'mes "Esta isla... esta ballena... puede";\n\t\t\tmes "percibir el sonido de un Gusli desde";\n\t\t\tmes "una distancia infinita.";'),
    ('mes "If you play this instrument,";\n\t\t\tmes "wherever you are, I\'ll go to you";\n\t\t\tmes "with this island. Only if you are a";\n\t\t\tmes "friend... jejeh.";',
     'mes "Si tocas este instrumento,";\n\t\t\tmes "donde sea que estes, ire hacia ti";\n\t\t\tmes "con esta isla. Solo si eres un";\n\t\t\tmes "amigo... jejeh.";'),

]

# Apply targeted replacements
for old, new in replacements:
    content = content.replace(old, new)

# Now let's do the massive bulk translation using a line-by-line approach
# We process each line, and for mes "..." lines that contain English text, we translate them

lines = content.split('\n')
new_lines = []

# Build a comprehensive translation dictionary for individual mes string contents
# Format: exact English string content -> Spanish translation
trans = {
    # ========== CSAR ALEXSAY III SECTION ==========
    "You!!!": "Tu!!!",
    "So many people saw you": "Mucha gente te vio",
    "meet with Baba Yaga!": "reunirte con Baba Yaga!",
    "The guilt which must be felt, when": "La culpa que se debe sentir, al",
    "meeting secretly with a witch...": "reunirse en secreto con una bruja...",
    "For that, we indict capital": "Por eso, dictamos castigo",
    "punishment without any just trial!": "capital sin un juicio justo!",
    "But you are a stranger to these": "Pero eres un extrano en estas",
    "lands... So I will hold you in special trial.": "tierras... Asi que te dare un juicio especial.",
    "If you have anything to say...": "Si tienes algo que decir...",
    "spare me no detail.": "no me escatimes ningun detalle.",
    "-Talk about what happened with Baba": "-Habla sobre lo que paso con Baba",
    "Yaga, and move forward with the plan.-": "Yaga, y avanza con el plan.-",
    "Hm-hm, that's an embarrassing story...": "Hm-hm, esa es una historia vergonzosa...",
    "But if you are telling the": "Pero si estas diciendo la",
    "truth, my people will be pleased.": "verdad, mi pueblo estara complacido.",
    "Okay, Bring to me": "Bien, traeme",
    "any evidence, to believe": "alguna evidencia, para creer",
    "what you are saying.": "lo que estas diciendo.",
    "You killed the Baba Yaga!!": "Mataste a la Baba Yaga!!",
    "If this is true, bring": "Si esto es verdad, traeme",
    "me Yaga's Pestles.": "las Mazas de Yaga.",
    "If you do, I will make": "Si lo haces, me asegurare",
    "sure no one ever doubts you.": "de que nadie dude de ti.",
    "Yes, Here you are.": "Si, aqui tienes.",
    "-Offered the Yaga's Pestles.-": "-Ofreciste las Mazas de Yaga.-",
    "Hm.. You do have them.": "Hm.. Si las tienes.",
    "For the time being, I will admit": "Por el momento, admitire",
    "that you are coming and going to": "que vas y vienes para",
    "hunt Baba Yaga.": "cazar a Baba Yaga.",
    "But do not engage in doubtable": "Pero no te involucres en",
    "behavior that would instigate my": "comportamientos dudosos que inciten a mi",
    "people to act in a strange way!": "pueblo a actuar de manera extrana!",
    "If you do that, I will arrest you immediately!": "Si haces eso, te arrestare de inmediato!",
    "So take care of yourself.": "Asi que cuidate.",
    "And, when you succeed in": "Y, cuando logres",
    "banishing winter with magic,": "desterrar el invierno con magia,",
    "announce that to me immediately.": "anunciamelo de inmediato.",
    "I said to bring me": "Dije que me trajeras",
    "40 Yaga's Pestles": "40 Mazas de Yaga",
    "from the Baba Yaga.": "de la Baba Yaga.",
    "Did you bring some evidence to": "Trajiste alguna evidencia para",
    "resolve your issue of doubt, traveler?": "resolver tu problema de duda, viajero?",
    "Good,": "Bien,",
    "I won't doubt you anymore.": "Ya no dudare de ti.",
    "Because you've proven yourself,": "Porque has demostrado tu valentia,",
    "you can remain a free traveler.": "puedes seguir siendo un viajero libre.",
    "Surely, I hate cooperating with Baba Yaga.": "Sin duda, odio cooperar con Baba Yaga.",
    "But if my people are happy": "Pero si mi pueblo es feliz",
    "after the work you do,": "despues del trabajo que haces,",
    "I am also pleased.": "yo tambien estoy complacido.",
    "Your items do not match the": "Tus objetos no coinciden con la",
    "count of 40 Yaga's Pestles.": "cantidad de 40 Mazas de Yaga.",
    "Did you forget the amount,": "Olvidaste la cantidad,",
    "or did you wish to lie to me...": "o deseabas mentirme...",
    "I will treat that as a joke!": "Tratare eso como una broma!",
    "A kind of sarcasm!": "Una especie de sarcasmo!",
    "You go away now and bring some": "Vete ahora y trae alguna",
    "evidence to certify your innocence.": "evidencia para certificar tu inocencia.",
    "Are you here to tease me?": "Estas aqui para burlarte de mi?",
    "It'd be great if I stayed put, for": "Seria genial si me quedara quieto, por",
    "the good of both me and my people.": "el bien mio y de mi pueblo.",
    "I don't want to see the Baba Yaga": "No quiero ver a la Baba Yaga",
    "personally.": "personalmente.",
    "So, I want you to ": "Asi que, quiero que tu",
    "take my place for that.": "tomes mi lugar para eso.",
    "Please help Baba Yaga": "Por favor ayuda a Baba Yaga",
    "to seize the summer.": "a atrapar el verano.",
    "Are you here for...": "Estas aqui por...",
    "I already heard about the": "Ya escuche sobre el",
    "weather from the minister.": "clima del ministro.",
    "Actually, I was a little": "De hecho, estaba un poco",
    "dissatisfied with the doing": "insatisfecho con la realizacion",
    "of witchcraft at the center": "de brujeria en el centro",
    "of the square...": "de la plaza...",
    "But... I can admit it was good work.": "Pero... puedo admitir que fue un buen trabajo.",
    "Everyone hates the cold winter.": "Todos odian el frio invierno.",
    "Now, the winter will not": "Ahora, el invierno no",
    "come anymore! So, I'm very pleased.": "vendra mas! Asi que, estoy muy complacido.",
    "Right.": "Correcto.",
    "I want to give you something": "Quiero darte algo",
    "in the name of the people.": "en nombre del pueblo.",
    "Here, take it.": "Aqui, tomalo.",
    "I give it as an atonement": "Te lo doy como expiacion",
    "to make my people happy.": "para hacer feliz a mi pueblo.",
    "Stay here as long as you want, and": "Quedate aqui todo el tiempo que quieras, y",
    "enjoy yourself to the fullest this summer.": "disfruta al maximo este verano.",
    "I am the ruler, Csar Aleksay III, of Moscovia.": "Soy el gobernante, Csar Aleksay III, de Moscovia.",
    "Go back to your hometown and talk about the beauty of Moscovia! Talk about my great government to all the people of the lands!": "Regresa a tu ciudad natal y habla sobre la belleza de Moscovia! Habla sobre mi gran gobierno a toda la gente de las tierras!",
    "A foreign traveler...?": "Un viajero extranjero...?",
    "Do you have something to tell me?": "Tienes algo que decirme?",
    "If it is not important,": "Si no es importante,",
    "have an audience with the Prime Minister first.": "ten una audiencia con el Primer Ministro primero.",
    "Oh, are you the traveler who told me about an interesting adventure story...": "Oh, eres el viajero que me conto sobre una interesante historia de aventura...",
    "Not only are you not from Moscovia, but also... you have found the moving island, which only existed in legends! I want to hear details...": "No solo no eres de Moscovia, sino que ademas... encontraste la isla movil, que solo existia en leyendas! Quiero escuchar los detalles...",
    "Let's hear it...": "Escuchemos...",
    "Tell me quickly.": "Dime rapido.",
    "I'm anxious to know the truth about the island...": "Estoy ansioso por saber la verdad sobre la isla...",
    "Surely, an interesting story... But it sounds so unbelievable! What do you think, Prime Minister?": "Sin duda, una historia interesante... Pero suena tan increible! Que opinas, Primer Ministro?",
    "It doesn't sound like a lie,": "No suena como una mentira,",
    "but it's difficult to believe": "pero es dificil creerlo",
    "completely. I mean, I've known": "completamente. Digo, he sabido",
    "a whale to be huge, but...": "que una ballena es enorme, pero...",
    "a person living there...": "una persona viviendo ahi...",
    "water streaming...": "agua fluyendo...",
    "and a tree growing on it...!!!": "y un arbol creciendo en ella...!!!",
    "I agree. I have heard many kinds of mysterious adventure stories, but this sounds like an absurd story!": "Estoy de acuerdo. He escuchado muchos tipos de historias de aventura misteriosas, pero esta suena absurda!",
    "Not to mention that it's happened near my nation. Unbelievable!": "Sin mencionar que sucedio cerca de mi nacion. Increible!",
    "But Csar... In my memory,": "Pero Csar... En mi memoria,",
    "I heard that exactly, the": "escuche que exactamente, la",
    "last time a story was told": "ultima vez que se conto una historia",
    "about the mysterious moving island. But there was a musical instrument...which an old man played.": "sobre la misteriosa isla movil. Pero habia un instrumento musical... que tocaba un viejo.",
    "Really? Tell me the details.": "En serio? Dime los detalles.",
    "Surely, I have heard the same": "Sin duda, he escuchado la misma",
    "story, as told in the legends": "historia, como se cuenta en las leyendas",
    "of our ancestors; about an old man who lived there.": "de nuestros ancestros; sobre un viejo que vivia ahi.",
    "Hm. There are many doubtful points. Ordinarily, I would give you a big prize, but in this case, it is difficult to believe.": "Hm. Hay muchos puntos dudosos. Normalmente, te daria un gran premio, pero en este caso, es dificil de creer.",
    "Bring me something to prove": "Traeme algo para probar",
    "the existence of the whale.": "la existencia de la ballena.",
    "If you do, I will give you a big prize.": "Si lo haces, te dare un gran premio.",
    "But if you don't,": "Pero si no lo haces,",
    "I will punish you for your lies! Bring this instrument that supposedly an old man has.": "Te castigare por tus mentiras! Trae ese instrumento que supuestamente tiene un viejo.",
    "Csar... This is a foreigner...": "Csar... Este es un extranjero...",
    "No disrespect was meant to you.": "No se pretendia faltarte al respeto.",
    "Perhaps a little more generosity is in order?.": "Quizas un poco mas de generosidad seria apropiado?.",
    "No way! If the story is not true, many other foreign travelers who pass by this land will disrespect me like this... What would you have me do?": "De ninguna manera! Si la historia no es cierta, muchos otros viajeros que pasen por esta tierra me faltaran al respeto... Que harias tu?",
    "You got it, traveler?": "Entendiste, viajero?",
    "You have a heavy responsibility.": "Tienes una gran responsabilidad.",
    "Bring evidence of this whale island to me, to provide me with some relief. Now go.": "Traeme evidencia de esta isla ballena, para darme algo de tranquilidad. Ahora ve.",
    "I'm tired... I want to take a rest, so... leave.": "Estoy cansado... Quiero descansar, asi que... vete.",
    "Just think about finding the whale island...": "Solo piensa en encontrar la isla ballena...",
    "Oh. You've come back...": "Oh. Has vuelto...",
    "Hm. Did you find something to bring": "Hm. Encontraste algo para traerme",
    "to me from the whale island?": "de la isla ballena?",
    "Did you bring the instrument?": "Trajiste el instrumento?",
    "A Gooselri? Which only exists": "Un Gooselri? Que solo existe",
    "in the whale island? Let's see.": "en la isla ballena? Veamos.",
    "Oh... Is this instrument... a Gooselri?": "Oh... Este instrumento es... un Gooselri?",
    "Actually, Csar, I believe it is": "En realidad, Csar, creo que se",
    "called a Gusli.": "llama Gusli.",
    "Oh. Prime Minister, is this the": "Oh. Primer Ministro, es este el",
    "correct instrument from the": "instrumento correcto de las",
    "legends, then?": "leyendas, entonces?",
    "I can't be sure, but this is": "No puedo estar seguro, pero este es",
    "definitely an instrument never seen": "definitivamente un instrumento nunca visto",
    "in our lands before.": "en nuestras tierras antes.",
    "Hm. This is also my first time": "Hm. Esta es tambien mi primera vez",
    "seeing this kind of musical": "viendo este tipo de instrumento",
    "instrument. So mysterious... Hey!": "musical. Tan misterioso... Oye!",
    "Can you play it?": "Puedes tocarlo?",
    "You can play it!": "Puedes tocarlo!",
    "Good, play it right away!": "Bien, tocalo de inmediato!",
    "Um... What is this? Do you mock me?": "Um... Que es esto? Te burlas de mi?",
    "You are so impudent... You...!": "Eres tan descarado... Tu...!",
    "Csar... Calm down, please.": "Csar... Calmate, por favor.",
    "If you are quick to anger by such a": "Si te enfureces rapido por una",
    "lowly person, it will become a": "persona tan insignificante, sera un",
    "problem of prestige for you.": "problema de prestigio para ti.",
    "Agh... I agree with you.": "Agh... Estoy de acuerdo contigo.",
    "You. Give a proper prize to the": "Tu. Dale un premio apropiado al",
    "adventurer and send them on their way.": "aventurero y envialos en su camino.",
    "How can I re...reward...?": "Como puedo re...recompensar...?",
    "I ordered you instead Prime": "Te ordene a ti Primer",
    "Minister, to make this poor player": "Ministro, que hagas que este pobre musico",
    "disappear from in front of my eyes,": "desaparezca de frente a mis ojos,",
    "right now.": "ahora mismo.",
    "You should be grateful for the": "Deberias estar agradecido por la",
    "Csar's mercy... impudent": "misericordia del Csar... viajero",
    "traveler...": "descarado...",
    "Even though I regard as your effort for the time so, award you. Take it and go out.": "Aunque reconozco tu esfuerzo por ahora, te premiare. Tomalo y vete.",
    "Um... That's too bad.": "Um... Que lastima.",
    "Ya veo... Will I ever believe...": "Ya veo... Alguna vez creere...?",
    "Thanks for your efforts.": "Gracias por tus esfuerzos.",
    "Hey, Prime Minister,": "Oye, Primer Ministro,",
    "reward this traveler.": "recompensa a este viajero.",
    "How can I reward the traveler?": "Como puedo recompensar al viajero?",
    "I leave the matter in your hands;": "Dejo el asunto en tus manos;",
    "it's up to you. I will take a": "depende de ti. Voy a tomar un",
    "rest.": "descanso.",
    "The Csar didn't take pleasure in": "Al Csar no le gusto",
    "your story, as I expected.": "tu historia, como esperaba.",
    "Even though I regard as your effort for the time so, award you. Take it.": "Aunque reconozco tu esfuerzo por ahora, te premiare. Tomalo.",
    "What are you doing? Can you play it": "Que estas haciendo? Puedes tocarlo",
    "without even holding the musical instrument???": "sin siquiera sostener el instrumento musical???",
    "Don't be impudent with me! Do it right!": "No seas descarado conmigo! Hazlo bien!",
    "Oh you come...hum did you find": "Oh viniste...hum encontraste",
    "something to satisfy me": "algo para satisfacerme",
    "at the whale island?": "en la isla ballena?",
    "Actually, Csar, I believe it is called a Gusli.": "En realidad, Csar, creo que se llama Gusli.",
    "Yes. I learned how to play it at Whale Island.": "Si. Aprendi a tocarlo en Whale Island.",
    "Oh! Oh!... You can play it!": "Oh! Oh!... Puedes tocarlo!",
    "Play it right away. I wonder about its sound.": "Tocalo de inmediato. Me pregunto como suena.",
    "-When the music of the Gusli is": "-Cuando la musica del Gusli es",
    "played, all the people in the": "tocada, toda la gente en el",
    "Csar's Palace fall in with the tune.-": "Palacio del Csar se deja llevar por la melodia.-",
    "Oh! I can't hear without tears.": "Oh! No puedo escuchar sin llorar.",
    "That's a sad tune.": "Es una melodia triste.",
    "That's right, Csar.": "Asi es, Csar.",
    "I have never heard a sad tune such as this.": "Nunca habia escuchado una melodia tan triste.",
    "Kh-huk. Sniff.": "Kh-huk. Snif.",
    "Huk... You. Give a big prize to": "Huk... Tu. Dale un gran premio a",
    "this traveler!": "este viajero!",
    "Hukhuk... Sniff. How can I reward this?": "Hukhuk... Snif. Como puedo recompensar esto?",
    "I leave this matter in your hands.": "Dejo este asunto en tus manos.",
    "Give a proper prize to whom has": "Dale un premio apropiado a quien ha",
    "Shown me a great story and": "mostrado una gran historia y",
    "beautiful music.": "hermosa musica.",
    "I express thanks to you on behalf": "Te expreso mi agradecimiento en nombre",
    "of our dear Csar and all the people": "de nuestro querido Csar y toda la gente",
    "in his palace. I will reward your": "en su palacio. Recompensare tus",
    "efforts, in the name of the Csar.": "esfuerzos, en nombre del Csar.",
    "But you... Where do you keep the": "Pero tu... Donde guardas el",
    "instrument which you are to show me?": "instrumento que me ibas a mostrar?",
    "Don't you need to be holding the instrument, in order to play it???": "No necesitas estar sosteniendo el instrumento, para tocarlo???",
    "I'm sorry. I will be ready now, and try again to play it.": "Lo siento. Estare listo ahora, e intentare tocarlo de nuevo.",
    "What happen... If you have special things go out.": "Que pasa... Si no tienes nada especial, vete.",
    "Um... You are a traveler as I saw.": "Um... Eres un viajero como vi.",
    "If you have special things, don't interfere my rest.": "Si no tienes nada especial, no interrumpas mi descanso.",
    "Oh... You. ~": "Oh... Tu. ~",
    "Nice to see you again.": "Que bueno verte de nuevo.",
    "I want for you to sometimes stop by here and play some music for me. ~": "Quiero que a veces pases por aqui y toques algo de musica para mi. ~",
    "I am Csar Alexsay the Third.": "Soy el Csar Alexsay III.",
    "Go back to your hometown and tell everyone about the beauty of Moscovia,": "Regresa a tu ciudad natal y cuentale a todos sobre la belleza de Moscovia,",
    "and my great government.": "y mi gran gobierno.",

    # ========== PRIME MINISTER DMITREE ==========
    "You are in trouble if": "Estaras en problemas si",
    "you conspire against the Csar,": "conspiras contra el Csar,",
    "so, make your actions carefully,": "asi que, actua con cuidado,",
    "and if you want to clean yourself": "y si quieres limpiar tu nombre",
    "from suspicion... do everything you": "de sospechas... haz todo lo que",
    "can to prove your innocence.": "puedas para probar tu inocencia.",
    "You have just cleared your name,": "Acabas de limpiar tu nombre,",
    "but... we don't trust you wholly yet.": "pero... aun no confiamos completamente en ti.",
    "I can't trust you, but...": "No puedo confiar en ti, pero...",
    "if you succeed in taking hold of": "si logras apoderarte del",
    "the summer... I might be able to.": "verano... quizas pueda.",
    "We know that you mean well.": "Sabemos que tienes buenas intenciones.",
    "But we can't fully trust you,": "Pero no podemos confiar completamente en ti,",
    "so we kept an eye on your movements.": "asi que vigilamos tus movimientos.",
    "I heard that you performed": "Escuche que realizaste",
    "witchcraft at the palace square...": "brujeria en la plaza del palacio...",
    "so, I ordered scholars to": "asi que, ordene a los estudiosos",
    "investigate the weather.": "investigar el clima.",
    "The results from taking observation": "Los resultados de observar",
    "of the weather, are the reducing": "el clima, son la reduccion",
    "change of temperature, and that the": "del cambio de temperatura, y que la",
    "highest temperature is now stabilized.": "temperatura maxima ahora esta estabilizada.",
    "I don't know what this may mean, by": "No se lo que esto pueda significar, en",
    "way of principle, but I've decided": "terminos de principio, pero he decidido",
    "to admit the facts.": "admitir los hechos.",
    "Already, our dear Csar knows.": "Nuestro querido Csar ya lo sabe.",
    "I finished the report.": "Termine el informe.",
    "Go and announce it to him.": "Ve y anunciaselo.",
    "You are a foreign traveler. This is the Moscovia Palace, home of Csar Aleksay the Third. Extending your every courtesy here... is not bad manners.": "Eres un viajero extranjero. Este es el Palacio de Moscovia, hogar del Csar Aleksay III. Mostrar toda tu cortesia aqui... no es mala educacion.",
    "Traveler, why have you come to the Csar's Palace?": "Viajero, por que has venido al Palacio del Csar?",
    "If so... look around with caution. Do not bother the Csar.": "Si es asi... mira alrededor con cuidado. No molestes al Csar.",
    "Moscovia welcomes all travelers such as yourself!": "Moscovia da la bienvenida a todos los viajeros como tu!",
    "Marvelously, our dear Csar likes it very much when interesting stories are often told to him.": "Maravillosamente, a nuestro querido Csar le gusta mucho cuando le cuentan historias interesantes.",
    "Did you come to see our dear Csar? If so, tell me your business with him in advance.": "Viniste a ver a nuestro querido Csar? Si es asi, dime tu asunto con el por adelantado.",
    "I will tell him directly about your business. You don't need to worry yourself with the Csar.": "Le dire directamente sobre tu asunto. No necesitas preocuparte por el Csar.",
    "I wonder what sort of things have happened to you... The Csar will be very pleased to hear your stories.": "Me pregunto que cosas te habran pasado... El Csar estara muy complacido de escuchar tus historias.",
    "I will admit you. If our dear Csar is satisfied with your story, he will give you a big prize.": "Te dejare pasar. Si nuestro querido Csar queda satisfecho con tu historia, te dara un gran premio.",
    "I already announced you,": "Ya te anuncie,",
    "so go see him and speak to him directly.": "asi que ve a verlo y hablale directamente.",
    "Now, our dear Csar needs a rest.": "Ahora, nuestro querido Csar necesita descansar.",
    "You should do your duty and go find the whale island.": "Deberias cumplir tu deber e ir a buscar la isla ballena.",
    "Ah! You've come back.": "Ah! Has vuelto.",
    "I will request for you to see him immediately.": "Pedire que te reciba de inmediato.",
    "I don't want to hear your terrible ": "No quiero escuchar tu terrible ",
    "performance anymore so, go out away.": "actuacion nunca mas, asi que vete.",
    "What's up? Dear Chare is taking a rest.": "Que pasa? El querido Csar esta descansando.",
    "If you have nothing special, go out.": "Si no tienes nada especial, vete.",
    "Your Gusli performance was so touching.": "Tu interpretacion del Gusli fue tan conmovedora.",
    "Unforgettable! Whenever you are here, please allow us to hear that tune again.": "Inolvidable! Cuando estes aqui, por favor permitenos escuchar esa melodia de nuevo.",
    "You are a foreign traveler. This is a palace": "Eres un viajero extranjero. Este es un palacio",
    "which lives Alexei the Third.": "donde vive Alexei III.",
    "Extend you every courtesy don't not bad manner.": "Muestra toda tu cortesia, no seas maleducado.",
}

# Process each line
for i, line in enumerate(lines):
    stripped = line.strip()

    # Check if this is a mes "..." line
    mes_match = re.match(r'^(\s*)mes\s+"(.*)";(.*)$', line.rstrip('\r\n'))
    if mes_match:
        indent = mes_match.group(1)
        content_str = mes_match.group(2)
        suffix = mes_match.group(3)

        # Skip if it's a NPC name in brackets like [Name]
        if content_str.startswith('[') and content_str.endswith(']'):
            new_lines.append(line)
            continue

        # Skip if it contains variables/expressions (starts with " + or contains "+)
        # These are dynamic strings

        # Check if content is in our translation dictionary
        if content_str in trans:
            translated = trans[content_str]
            # Replace double quotes with single quotes in translated text
            translated = translated.replace('"', "'")
            new_lines.append(f'{indent}mes "{translated}";{suffix}\n' if line.endswith('\n') else f'{indent}mes "{translated}";{suffix}')
            continue

    new_lines.append(line)

result = ''.join(new_lines) if lines[-1].endswith('\n') else '\n'.join(new_lines)

# Verify line count
new_count = result.count('\n')
print(f"Original lines: {orig_lines}")
print(f"New lines: {new_count}")
if orig_lines != new_count:
    print("WARNING: Line count mismatch!")
else:
    print("Line count matches - OK")

with open(INPUT, 'w', encoding='utf-8') as f:
    f.write(result)

print("Translation complete!")
print(f"Applied translations from dictionary of {len(trans)} entries")
