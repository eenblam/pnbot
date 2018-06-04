from random import randint

LIST_OF_SECRETS = [
    "An octopus is just a boneless spider.",
    "10 = 10, but not in base 1.",
    "A hippopotamus is just a really cool Opotamus.",
    "You can toggle the [Jog] ability by pressing the [Walk] key while already walking.",
    "The human colon actually has a second sphincter muscle.",
    "Taxation is theft.",
    "If left long enough to ferment, grapes of wrath become a bitter whine.",
    "The term 'childbirth' is either redundant or has frightening implications.",
    "Despite their name, dragons rarely drag things onto other things.",
    "Babies are neither commonly found in bays, nor are they a type of bee.",
    "You can ask me to !eval python 3 expressions"
]

def sneakret():
    return LIST_OF_SECRETS[randint(0, len(LIST_OF_SECRETS)-1)]
