#!/usr/bin/env python3
"""
Part 2: Translate remaining English mes strings in quests_moscovia.txt
Covers: Island triggers, Help Mikhail, Acorn Exchange, Banish Winter,
Shafka Hat, Koshei the Immortal, and all remaining sections.
"""
import re

INPUT = r"D:\Xponzy Network\Ragnarok-Server\rathena\npc\quests\quests_moscovia.txt"

with open(INPUT, 'r', encoding='utf-8') as f:
    content = f.read()

orig_lines = content.count('\n')
lines = content.split('\n')
new_lines = []

# Comprehensive translation dictionary for remaining English strings
trans = {
    # ========== ISLAND TRIGGER / DOCKS ==========
    "-Watching the sea from the docks,": "-Mirando el mar desde los muelles,",
    "it suddenly dawns upon you that you": "de repente te das cuenta de que",
    "have memories from Whale Island.-": "tienes recuerdos de Whale Island.-",
    "Stop by the whale island?": "Pasar por la isla ballena?",
    "-Slowly, your hands are on the": "-Lentamente, tus manos estan sobre el",
    "Gusli, and the playing starts...": "Gusli, y la musica comienza...",
    "reminding you of the melody which": "recordandote la melodia que",
    "the aged stranger had played...-": "el anciano habia tocado...-",
    "So...something is rising from the sea!!!": "Asi que... algo esta surgiendo del mar!!!",
    "What...What is that...??": "Que...Que es eso...??",
    "Ojojoh!... That's the whale": "Ojojoh!... Esa es la isla",
    "island...!!! Someday, I hope to go there! Jajaja.": "ballena...!!! Algun dia, espero ir ahi! Jajaja.",
    "Oh my goodness... Slipped right out": "Oh cielos... Se me olvido",
    "of my mind... to forget equipping the Gusli.": "por completo... equipar el Gusli.",
    "The aged stranger said that when I": "El anciano dijo que cuando",
    "want to go to Whale Island again, I": "quiera ir a Whale Island de nuevo,",
    "should play the Gusli from this place...": "debo tocar el Gusli desde este lugar...",
    "I can go some other time.": "Puedo ir en otro momento.",
    "I will do other work now.": "Hare otras cosas ahora.",

    # ========== SHIP TRIGGERS ==========
    "seeewaaaaaaaaaaa": "maaaaaaaaarrrrr",
    "It's dangerous! Hide! Hurry!": "Es peligroso! Escondete! Rapido!",
    "That... that is...": "Eso... eso es...",
    "Something... something is rising...": "Algo... algo esta surgiendo...",
    "Ah... That... That is... What...": "Ah... Eso... Eso es... Que...",
    "Now that all the monsters are gone,": "Ahora que todos los monstruos se fueron,",
    "we can start sailing again": "podemos empezar a navegar de nuevo",
    "normally.": "normalmente.",

    # ========== HELP MIKHAIL - GALLINA ==========
    "Oh, where the heck is he?": "Oh, donde demonios esta?",
    "I'll teach him a lesson.": "Le dare una leccion.",
    "He's timid like Dad.": "Es timido como Papa.",
    "Mikhail, he's a coward, a crybaby.": "Mikhail, es un cobarde, un lloron.",
    "It's because you didn't look after your brother. So you clean the house, Anna?": "Es porque no cuidaste a tu hermano. Asi que limpia la casa, Anna?",
    "Oh, my................": "Oh, no................",
    "Oh, God!": "Oh, Dios!",
    "I didn't see you there. Sorry!": "No te vi ahi. Disculpa!",
    "You want to buy a hotcake, don't you?": "Quieres comprar un hotcake, verdad?",
    "I'm sorry but we're not ready to open the store..": "Lo siento pero no estamos listos para abrir la tienda..",
    "No, that's ok.": "No, esta bien.",
    "Is there something that I can help with? What's the matter?": "Hay algo en lo que pueda ayudar? Que pasa?",
    "Oh, well...": "Oh, bueno...",
    "My son, Mikhail broke our Matrushka while I was away from home.": "Mi hijo, Mikhail rompio nuestra Matrushka mientras yo no estaba en casa.",
    "He's afraid that I would punish him. So he ran away.": "Tiene miedo de que lo castigue. Asi que se escapo.",
    "How timid the boy is!": "Que timido es ese nino!",
    "I doubt that he'd be able to be a great general in the future": "Dudo que pueda ser un gran general en el futuro",
    "He used to come home at this time.": "Solia llegar a casa a esta hora.",
    "I'm worried that something bad has happened to him.": "Me preocupa que algo malo le haya pasado.",
    "You look anxious. I'd like to help you to find your son.": "Te ves ansiosa. Me gustaria ayudarte a encontrar a tu hijo.",
    "Did you say I'm anxious?": "Dijiste que estoy ansiosa?",
    "I'm just anxious for him to get home.": "Solo estoy ansiosa de que llegue a casa.",
    "...So I can punish him for what he did.": "...Para poder castigarlo por lo que hizo.",
    "But it's not good that I refuse your kindness": "Pero no esta bien que rechace tu amabilidad",
    "Will you find Mikhail for me?": "Encontraras a Mikhail por mi?",
    "You meanie! I'm not in the mood for jokes.": "Malvado! No estoy de humor para bromas.",
    "Oh, God, You're so kind": "Oh, Dios, eres tan amable",
    "Mikhail is such a timid boy. I guess he didn't leave this village.": "Mikhail es un nino muy timido. Supongo que no salio de esta aldea.",
    "Please bring him to me, then~": "Por favor traemelo, entonces~",
    "Mikhail, my timid son must still be in this village.": "Mikhail, mi timido hijo debe seguir en esta aldea.",
    "I'm sorry if he's shy and timid like his father.": "Lo siento si es timido y miedoso como su padre.",
    "Mikhail hasn't come yet?": "Mikhail aun no ha llegado?",
    "No, where on earth is he?": "No, donde demonios esta?",
    "He came back with my Matrushka roughly pasted together and just left...": "Regreso con mi Matrushka torpemente pegada y se fue...",
    "I'm sorry that I treated the little boy badly.": "Lamento haber tratado mal al pequeno.",
    "He did his best in his own way.": "Hizo lo mejor que pudo a su manera.",
    "Yes. I'm sure I will. jojo..": "Si. Estoy segura de que lo hare. jojo..",
    "Anna, my daughter made a mistake. She laid the blame upon her brother alone. I'll punish her too.": "Anna, mi hija cometio un error. Le echo toda la culpa a su hermano. Tambien la castigare.",
    "I appreciate your effort. You went to a dangerous place to find my son": "Agradezco tu esfuerzo. Fuiste a un lugar peligroso para encontrar a mi hijo",
    "It often happens to me, jeje.": "Me pasa seguido, jeje.",
    "I can't afford to reward you with much but... I'll let you know how to make a delicious hotcake!": "No puedo recompensarte con mucho pero... te ensenare como hacer un delicioso hotcake!",
    "I have to work now but Larissa will tell you about that. She's our maid..": "Tengo que trabajar ahora pero Larissa te contara sobre eso. Es nuestra sirvienta..",
    "She's really a nice cook.": "Es muy buena cocinera.",
    "Hotcakes of Moscovia are so delicious!": "Los hotcakes de Moscovia son deliciosos!",
    "Once you make it, I bet you that you'll love it.": "Una vez que lo hagas, apuesto a que te encantara.",
    "Well, now I have to get to work!": "Bueno, ahora tengo que ponerme a trabajar!",
    "I'll make you my hotcakes someday. Please visit me later": "Te hare mis hotcakes algun dia. Por favor visitame despues",
    "I'm always trying to prepare a new dish.": "Siempre estoy tratando de preparar un nuevo platillo.",
    "What do you think of 'the most spicy chili hotcake in the world'?": "Que piensas de 'el hotcake de chile mas picante del mundo'?",
    "I think that will be great!": "Creo que sera genial!",

    # ========== ANNA ==========
    "Why are you here?": "Por que estas aqui?",
    "Where is Mikhail?": "Donde esta Mikhail?",
    "Do you know where he is?": "Sabes donde esta?",
    "If I had known that, I would have already found him, you fool.": "Si lo hubiera sabido, ya lo habria encontrado, tonto.",
    "Jajaja, you're right.": "Jajaja, tienes razon.",
    "How's your relationship with your brother?": "Como es tu relacion con tu hermano?",
    "Mikhail always stays behind me and asks me to read books!": "Mikhail siempre se queda detras de mi y me pide que le lea libros!",
    "And he cries too much.": "Y llora demasiado.",
    "It annoys me.": "Me molesta.",
    "And he only wants to play with me. That's why he has no friends.": "Y solo quiere jugar conmigo. Por eso no tiene amigos.",
    "You seem very courageous.": "Pareces muy valiente.",
    "I can understand why your mother worries about him.": "Puedo entender por que tu madre se preocupa por el.",
    "What were you doing when Mikhail broke your mother's Matrushka?": "Que estabas haciendo cuando Mikhail rompio la Matrushka de tu madre?",
    "I was there.": "Yo estaba ahi.",
    "Oh were you?": "Oh en serio?",
    "When my parents were out, they asked me to take care of Mikhail.": "Cuando mis padres salieron, me pidieron que cuidara a Mikhail.",
    "I didn't want to do that but I'm his sister so I was reading a book next to him.": "No queria hacerlo pero soy su hermana asi que estaba leyendo un libro a su lado.",
    "He began to tease me to read a book for him and later, he annoyed me saying that he's hungry!": "Empezo a molestarme para que le leyera un libro y luego, me fastidio diciendo que tenia hambre!",
    "I was so bothered with him and I pretended not to hear him and kept reading. I guess it made him mad and so he broke the Matrushka.": "Estaba tan molesta con el que fingi no escucharlo y segui leyendo. Creo que eso lo enfurecio y por eso rompio la Matrushka.",
    "He made trouble and began to cry!": "Causo problemas y empezo a llorar!",
    "He's such a timid boy...": "Es un nino tan timido...",
    "(giggling)": "(risita)",
    "And then I told him that we should glue the pieces together before Mom came back, so Mikhail went to get ^3131FFpaste^000000 but he hasn't come back yet.": "Y entonces le dije que deberiamos pegar las piezas antes de que Mama regresara, asi que Mikhail fue a buscar ^3131FFpegamento^000000 pero aun no ha regresado.",
    "Where can you get it?": "Donde puedes conseguirlo?",
    "Why didn't you go with him?": "Por que no fuiste con el?",
    "Do you think we kids know that?": "Crees que los ninos sabemos eso?",
    "He broke it and should get the thing by himself!": "El lo rompio y debe conseguirlo el solo!",
    "And Mom said that he should do his work for himself to become a great general.": "Y Mama dijo que debe hacer sus cosas solo para convertirse en un gran general.",
    "Don't you have any idea of where he might be?": "No tienes ni idea de donde podria estar?",
    "No.": "No.",
    "Is there anyone who is close to him?": "Hay alguien cercano a el?",
    "(giggle) He's a fool and has no friends.": "(risita) Es un tonto y no tiene amigos.",
    "But among our villagers, the lady of ^3131FFInn 'Sticky Herb Tree'^000000 has held Mikhail dear.": "Pero entre nuestros aldeanos, la senora de la ^3131FFPosada 'Sticky Herb Tree'^000000 le tiene carino a Mikhail.",
    "I have no idea anymore.": "Ya no tengo mas ideas.",
    "- Anna sticks her tongue out. -": "- Anna saca la lengua. -",
    "It's the only clue, I guess I'll go to ^3131FFInn 'Sticky Herb Tree'^000000?": "Es la unica pista, supongo que ire a la ^3131FFPosada 'Sticky Herb Tree'^000000?",
    "What am I going to ask her?": "Que le voy a preguntar?",
    "Anna,": "Anna,",
    "Do you know what this is?": "Sabes que es esto?",
    "I know that they have a game called RAGNAROK Online 2... and they like... what am I saying now... right?": "Se que tienen un juego llamado RAGNAROK Online 2... y les gusta... que estoy diciendo ahora... verdad?",
    "Mom's hotcakes are so delicious! Oh, it's sweet flavor!": "Los hotcakes de Mama son deliciosos! Oh, su sabor dulce!",
    "Everyone in this village likes Mom's hotcakes. Jeje.": "Todos en esta aldea les gustan los hotcakes de Mama. Jeje.",
    "Mikhail is a timid fool!": "Mikhail es un tonto timido!",
    "I have no idea about that thing.": "No tengo idea sobre eso.",
    "Hmm ~ ~ ~ ~ ": "Hmm ~ ~ ~ ~ ",
    "- Anna frowns at me and sticks out her tongue.": "- Anna me mira con el ceno fruncido y saca la lengua.",
    "She doesn't want to talk to me -": "No quiere hablar conmigo -",
    "Ok, I got a clue from Anna and one thing that I have to do is go to ^3131FFInn 'Sticky Herb Tree'^000000.": "Bien, tengo una pista de Anna y lo que debo hacer es ir a la ^3131FFPosada 'Sticky Herb Tree'^000000.",
    "Mikhail is foolish, timid and a coward!": "Mikhail es tonto, timido y cobarde!",
    "Mik..ha..il": "Mik..ha..il",
    "He tattled on me to mom...": "Le fue con el chisme a mama...",
    "Anna!": "Anna!",
    "....I'm sorry.": "....Lo siento.",
    "....I'm bored.": "....Estoy aburrida.",

    # ========== BED / FIRE POT ==========
    "- There are sheets and a pillow which seem so neat and soft that I'll probably fall asleep as soon as I lie down on them. -": "- Hay sabanas y una almohada que parecen tan limpias y suaves que probablemente me dormire tan pronto como me acueste. -",
    "- You'll examine the bed later -": "- Examinaras la cama despues -",
    "- You come near the bed to look it over. -": "- Te acercas a la cama para examinarla. -",
    "- You didn't find anything -": "- No encontraste nada -",
    "- It's a fire pot to heat the room or bake something -": "- Es un fogon para calentar la habitacion u hornear algo -",
    "- It's a fire pot that is used when Gallina bakes hotcakes.": "- Es un fogon que se usa cuando Gallina hornea hotcakes.",
    "It seems that this has not been used for a long time.": "Parece que no se ha usado en mucho tiempo.",
    "I think I should ask his family where he might have fun off to -": "Creo que deberia preguntar a su familia a donde podria haber ido -",
    "It seems that it was used a long time ago. -": "Parece que se uso hace mucho tiempo. -",
    "- You decide to check out other things -": "- Decides revisar otras cosas -",
    "- You come near the pot to look it over. -": "- Te acercas al fogon para examinarlo. -",
    "- As you look it over very carefully, you find some pieces of bread on the floor around the fire pot! -": "- Al examinarlo cuidadosamente, encuentras pedazos de pan en el suelo alrededor del fogon! -",
    "I finally found him.": "Finalmente lo encontre.",
    "- You put your arm into the hole of the fire pot. -": "- Metes tu brazo en el agujero del fogon. -",
    "- Something makes a rustling sound. -": "- Algo hace un sonido crujiente. -",
    "- You call Mikhail with a low voice. -": "- Llamas a Mikhail en voz baja. -",
    "Mik-ha-il-.": "Mik-ha-il-.",
    "- .......................... -": "- .......................... -",
    "Mikhail.": "Mikhail.",
    "I know you're there, please come out.": "Se que estas ahi, por favor sal.",
    "Your mom and sister are worried about you.": "Tu mama y tu hermana estan preocupadas por ti.",
    ".......hey.": ".......oye.",
    "?????": "?????",
    ".......No, I can't............": ".......No, no puedo............",
    "I'll.... be punished........": "Me van a.... castigar........",
    "No, you won't, Mikhail.": "No, no lo haran, Mikhail.",
    "Your mom is worried about you so much.": "Tu mama esta muy preocupada por ti.",
    "Your sister, too.": "Tu hermana tambien.",
    "You broke your mom's Matrushka by mistake, didn't you?": "Rompiste la Matrushka de tu mama por accidente, verdad?",
    "I'll tell her about your mistake. Please come out.": "Le contare sobre tu error. Por favor sal.",
    "Oh.. ma.. matrushka..": "Oh.. ma.. matrushka..",
    "I didn't break..it.. it..wasn't.. just me!": "No la rompi..yo.. no..fui.. solo yo!",
    "And?": "Y?",
    "Anna pushed me and bumped me......": "Anna me empujo y me golpeo......",
    "But she told Mom that it was just me who broke it....": "Pero le dijo a Mama que solo yo la rompi....",
    "Oh, dear! You and Anna did that but she put all the blame on you?": "Oh, cielos! Tu y Anna hicieron eso pero ella te echo toda la culpa?",
    "Yes.....": "Si.....",
    "You should come out and tell your mom the truth! Let's go Mikhail.": "Deberias salir y decirle la verdad a tu mama! Vamos Mikhail.",
    "No! No, I can't!!": "No! No, no puedo!!",
    "- A small-white hand comes out of the fire pot and grabs your ankle -": "- Una pequena mano blanca sale del fogon y agarra tu tobillo -",
    "No...I'm afraid that Mom will punish me...": "No...tengo miedo de que Mama me castigue...",
    "Because Grandma's Matrushka is broken......": "Porque la Matrushka de la Abuela esta rota......",
    "Oh, my. Please don't cry little boy.": "Oh, no llores pequeno.",
    "There's no way. I'll get a paste to bond all the pieces together. And then you can bring it back to your mom and apologize to her.": "No te preocupes. Conseguire un pegamento para unir todas las piezas. Y luego puedes devolversela a tu mama y disculparte.",
    "Can you... get... a paste?": "Puedes... conseguir... pegamento?",
    "You don't believe me?": "No me crees?",
    "Ok, stay here. I'll be right back with the paste.": "Ok, quedate aqui. Volvere enseguida con el pegamento.",
    "- I need to know what's required for the paste.": "- Necesito saber que se requiere para el pegamento.",
    "I'll ask that guy ^3131FFMr. Victor^000000 about them. -": "Le preguntare a ^3131FFMr. Victor^000000 sobre eso. -",
    "- Ok, what I have to do first is ask Mr. Victor what I need for the paste. -": "- Ok, lo primero que debo hacer es preguntarle a Mr. Victor que necesito para el pegamento. -",
    "Hey, Mikhail. I've got the paste!.": "Oye, Mikhail. Consegui el pegamento!.",
    "......Really? are you serious?": "......En serio? hablas en serio?",
    "- You hand over the paste from Victor to Mikhail. -": "- Le entregas el pegamento de Victor a Mikhail. -",
    "Wow! Great!": "Wow! Genial!",
    "- He begins working on the broken Matrushka as if he was piecing together a puzzle. -": "- Comienza a trabajar en la Matrushka rota como si estuviera armando un rompecabezas. -",
    "I've done it!!!!!!!": "Lo logre!!!!!!!",
    "You're welcome, jaja.": "De nada, jaja.",
    "Anyway, can you promise me one thing?": "De todas formas, puedes prometerme algo?",
    "What?": "Que?",
    "Bring back the Matrushka to your mother, and promise me that you will be a brave general in the future.": "Devuelve la Matrushka a tu madre, y prometeme que seras un general valiente en el futuro.",
    ".............": ".............",
    "OK, I will!": "OK, lo hare!",
    "Hoohoo, you're good boy.": "Joojoo, eres un buen chico.",
    "Now I'm gonna give this back to Mom.": "Ahora voy a devolverle esto a Mama.",
    "- It's a fire pot to heat the room or bake something -": "- Es un fogon para calentar la habitacion u hornear algo -",

    # ========== STICKY HERB TREE INN ==========
    "Oh, welcome to the Inn 'Sticky Herb Tree'.": "Oh, bienvenido a la Posada 'Sticky Herb Tree'.",
    "It is the most comfortable and calmest place in all of Moscovia.": "Es el lugar mas comodo y tranquilo de toda Moscovia.",
    "You're up already?": "Ya despertaste?",
    "Well since you're young you've probably already recovered all of your strength.": "Bueno, como eres joven probablemente ya recuperaste todas tus fuerzas.",
    "Jojojo.": "Jojojo.",

    # ========== SWAMP ==========
    "- You feel sticky just looking at this swamp. -": "- Te sientes pegajoso solo con mirar este pantano. -",
    "- Gas bubbles are rising. The atmosphere here is pretty scary -": "- Burbujas de gas suben. El ambiente aqui es bastante aterrador -",
    "I don't see any traces of Mikhail. I think I should go back and check his house one more time.": "No veo rastros de Mikhail. Creo que deberia regresar y revisar su casa una vez mas.",
    "- You can see a small muddy swamp -": "- Puedes ver un pequeno pantano fangoso -",
    "- You feel sticky just looking at the swamp. -": "- Te sientes pegajoso solo con mirar el pantano. -",
    "- You stretch out to find sticky herbs. -": "- Te estiras para encontrar hierbas pegajosas. -",
    "- You have pricked your finger on a Sticky Herb. -": "- Te pinchaste el dedo con una Sticky Herb. -",
    "- You have pricked your finger on a Green Herb. -": "- Te pinchaste el dedo con una Green Herb. -",
    "- You can see a small swamp which seems very muddy. -": "- Puedes ver un pequeno pantano que parece muy fangoso. -",

    # ========== ACORN EXCHANGE ==========
    "We have very fresh acorns. Everyone will like them!": "Tenemos bellotas muy frescas. A todos les gustaran!",
    "You can buy one acorn for 100zeny!": "Puedes comprar una bellota por 100zeny!",
    "Well uh...": "Bueno eh...",
    "You can grind them to make": "Puedes molerlas para hacer",
    "something to eat and you can feed squirrels.": "algo de comer y puedes alimentar ardillas.",
    "Someone can decorate their house": "Alguien puede decorar su casa",
    "with them but I don't know how...": "con ellas pero no se como...",
    "they've got to be highly talented.": "deben ser muy talentosos.",
    "Jaja.": "Jaja.",
    "I'll bet you that they are very fresh!": "Te apuesto a que estan muy frescas!",
    "How many acorns do you need?": "Cuantas bellotas necesitas?",
    "Do you want to cancel this trade?": "Quieres cancelar este intercambio?",
    "You can't buy more than 500.": "No puedes comprar mas de 500.",
    "Hello, I think you can't get acorns": "Hola, creo que no puedes recibir bellotas",
    "now. You're carrying too many": "ahora. Estas cargando demasiados",
    "items!": "objetos!",
    "Please use Kafra service. I'll be": "Por favor usa el servicio Kafra. Estare",
    "right here.": "justo aqui.",
    "Hello? You've turned pale! Are you ok??": "Hola? Te pusiste palido! Estas bien??",
    "Do you have enough money?": "Tienes suficiente dinero?",
    "Oh, thank you...": "Oh, gracias...",
    "What do you think of them? They're fresh, aren't they?": "Que te parecen? Estan frescas, verdad?",
    "- It's an extraordinary big squirrel. -": "- Es una ardilla extraordinariamente grande. -",
    "- When the animal comes across you, it starts to sniffle and purse up its lips. -": "- Cuando el animal se te acerca, empieza a olfatear y fruncir los labios. -",
    "- You take one of acorns out and hold it out to the squirrel. -": "- Sacas una bellota y se la ofreces a la ardilla. -",
    "- It cocked it's ears up and begins to nibble the acorn quickly. -": "- Levanta las orejas y empieza a mordisquear la bellota rapidamente. -",
    "- It makes a crunching sound -": "- Hace un sonido crujiente -",
    "- After eating the acorn up, the squirrel dances around wildly. Suddenly it curls its body and throws something up with a spit-spit sound -": "- Despues de comerse la bellota, la ardilla baila alrededor salvajemente. De repente enrolla su cuerpo y escupe algo con un sonido de escupir -",
    "It's so cute.": "Es tan lindo.",
    "Is it bigger than an ordinary one?": "Es mas grande que una normal?",
    "I found it one day and was barely able to save it...": "La encontre un dia y apenas pude salvarla...",
    "I felt that heaven had sent me a friend so that my life wouldn't be so lonely.": "Senti que el cielo me habia enviado un amigo para que mi vida no fuera tan solitaria.",
    "But I didn't know that it eats so much, it won't give me any attention if I give anything ^3131FFbelow 20 acorns^000000.": "Pero no sabia que come tanto, no me presta atencion si le doy menos de ^3131FF20 bellotas^000000.",
    "That's why it's bigger than ordinary ones jajaja.": "Por eso es mas grande que las normales jajaja.",
    "- The squirrel looks at the acorn which you held for a while but it turned its head with indifference. -": "- La ardilla mira la bellota que sostienes por un momento pero voltea la cabeza con indiferencia. -",

    # ========== SHAFKA HAT ==========
    "Wait a moment!!": "Espera un momento!!",
    "You have too many items.": "Tienes demasiados objetos.",
    "You can't receive this.": "No puedes recibir esto.",
    "Lighten your weight and": "Reduce tu peso y",
    "try again.": "intenta de nuevo.",
    "Hello, foreign traveler!": "Hola, viajero extranjero!",
    "Have you had good day": "Has tenido un buen dia",
    "in Moscovia?": "en Moscovia?",
    "A special souvenir for visiting Moscovia...?": "Un recuerdo especial por visitar Moscovia...?",
    "For you, let's make a Shafka hat.": "Para ti, hagamos un gorro Shafka.",
    "The Shafka has practicality and": "El Shafka tiene practicidad y",
    "it's spruce! Do you want one?": "es elegante! Quieres uno?",
    "When I look at you, you seem to": "Cuando te miro, pareces querer",
    "want to put on something of a thick": "ponerte algo como un grueso",
    "fur hat on your head, out in this": "gorro de piel en la cabeza, con esta",
    "temperature. A Shafka!": "temperatura. Un Shafka!",
    "If you've come here for the first": "Si vienes aqui por primera",
    "time, you might not know... that": "vez, quizas no sepas... que",
    "winter here is famous for being so": "el invierno aqui es famoso por ser tan",
    "long and cold in Moscovia.": "largo y frio en Moscovia.",
    "A Shafka hat is especially": "Un gorro Shafka es especialmente",
    "necessary to live here during the": "necesario para vivir aqui durante las",
    "cold seasons. Without this hat, you": "estaciones frias. Sin este gorro,",
    "may not endure a winter!": "quizas no soportes un invierno!",
    "Now, the long, long winter has": "Ahora, el largo, largo invierno ha",
    "ended and the sun is shining... But": "terminado y el sol brilla... Pero",
    "someday the winter will come again.": "algun dia el invierno volvera.",
    "So, for preparation, you should": "Asi que, como preparacion, deberias",
    "keep a Shafka hat handy.": "tener un gorro Shafka a mano.",
    "Don't worry about keeping warm if": "No te preocupes por mantenerte caliente si",
    "you're wearing a Shafka hat. Even": "llevas puesto un gorro Shafka. Incluso",
    "during the coldest weather... You": "durante el clima mas frio... Puedes",
    "can roll around in the snow and the": "revolcarte en la nieve y el",
    "Shafka still keeps you warm!": "Shafka aun te mantiene caliente!",
    "Do you want to make a Shafka hat?": "Quieres hacer un gorro Shafka?",
    "Jejeh. Good idea!": "Jejeh. Buena idea!",
    "That's a good task.": "Esa es una buena tarea.",
    "You will be grateful forever.": "Estaras agradecido para siempre.",
    "If you bring the materials,": "Si traes los materiales,",
    "we can make one immediately!": "podemos hacer uno de inmediato!",
    "The materials are: ^0000FFNine Tails 20, Yarn 10, Soft Silk 10, Sea-otter Fur 20, Spool 1^000000.": "Los materiales son: ^0000FFNine Tails 20, Yarn 10, Soft Silk 10, Sea-otter Fur 20, Spool 1^000000.",
    "You did well.": "Lo hiciste bien.",
    "Give me the materials. I will make the Shafka.": "Dame los materiales. Hare el Shafka.",
    "Good, I made it. So, how about it?": "Bien, lo hice. Y, que te parece?",
    "Do you like it?": "Te gusta?",
    "If you need a Shafka hat,": "Si necesitas un gorro Shafka,",
    "come to me whenever,": "ven conmigo cuando quieras,",
    "with the materials.": "con los materiales.",
    "I will make it.": "Lo hare.",
    "Okay?": "Ok?",
    "Okay, so... Bye-bye!~": "Ok, entonces... Bye-bye!~",
    "Ah... You lack some materials. We": "Ah... Te faltan algunos materiales. No",
    "can't make the Shafka hat with just": "podemos hacer el gorro Shafka solo con",
    "these materials.": "estos materiales.",
    "If you bring the right materials, I": "Si traes los materiales correctos,",
    "will make a Shafka immediately.": "hare un Shafka de inmediato.",

    # ========== ANNOUNCE / MAPANNOUNCE ==========
    "Koshei, the Immortal : Keeeek, you, cursed human.. I'll never give up!!! We'll see who's smiling in the end!!!": "Koshei, the Immortal : Keeeek, tu, humano maldito.. Nunca me rendire!!! Veremos quien rie al final!!!",
    "Koshei, the Immortal : I will kill all who disturb me!! Cry in terror weak humans!!!": "Koshei, the Immortal : Matare a todos los que me molesten!! Lloren de terror debiles humanos!!!",
    "Koshei, the Immortal : You worms, you mere monsters... I will curse all who are in my way!!": "Koshei, the Immortal : Gusanos, simples monstruos... Maldecire a todos los que esten en mi camino!!",
    "Koshei, the Immortal : Mankind! Cry in terror!! Hahahahahahahhahahah!!!": "Koshei, the Immortal : Humanidad! Lloren de terror!! Jajajajajajjajajaj!!!",
    "Marozka's Guard : Invader! Search the whole cave!!": "Guardia de Marozka : Invasor! Busquen en toda la cueva!!",
    "Mazroka : You are truly brave. When you get the cookies and apples, come to see me.": "Mazroka : Eres verdaderamente valiente. Cuando consigas las galletas y manzanas, ven a verme.",

    # ========== WARNING SIGNS ==========
    " WARNING !! ": " ADVERTENCIA !! ",
    "No Swimming": "No Nadar",
}

# Process each line
for i, line in enumerate(lines):
    stripped = line.strip()

    # Handle mes "..." lines
    mes_match = re.match(r'^(\s*)mes\s+"(.*)";(.*)$', line.rstrip('\r\n'))
    if mes_match:
        indent = mes_match.group(1)
        content_str = mes_match.group(2)
        suffix = mes_match.group(3)

        # Skip NPC names in brackets
        if content_str.startswith('[') and content_str.endswith(']'):
            new_lines.append(line)
            continue

        # Skip lines with string concatenation (dynamic content)
        if '"+' in content_str or '"+' in line:
            # But still check for translatable parts
            pass

        if content_str in trans:
            translated = trans[content_str]
            translated = translated.replace('"', "'")
            new_lines.append(f'{indent}mes "{translated}";{suffix}\n' if line.endswith('\n') else f'{indent}mes "{translated}";{suffix}')
            continue

    # Handle select("...") lines - translate option text
    # Handle announce/mapannounce lines
    announce_match = re.search(r'(announce|mapannounce)\s+"[^"]*","([^"]*)"', line)
    if announce_match:
        ann_content = announce_match.group(2)
        if ann_content in trans:
            translated = trans[ann_content].replace('"', "'")
            line = line.replace(f'"{ann_content}"', f'"{translated}"', 1)

    new_lines.append(line)

result = ''.join(new_lines) if lines[-1].endswith('\n') else '\n'.join(new_lines)

new_count = result.count('\n')
print(f"Original lines: {orig_lines}")
print(f"New lines: {new_count}")
if orig_lines != new_count:
    print("WARNING: Line count mismatch!")
else:
    print("Line count matches - OK")

with open(INPUT, 'w', encoding='utf-8') as f:
    f.write(result)

print("Translation part 2 complete!")
print(f"Applied translations from dictionary of {len(trans)} entries")
