from random import randint

LIST_OF_SECRETS = [
    "An octopus is just a boneless spider.",
    "10 = 10, but not in base 1.",
    "A hippopotamus is just a really cool Opotamus.",
    "You can toggle the [Jog] ability by double tapping the [Walk] key.",
    "The human colon actually has a second sphincter muscle.",
    "Taxation is theft.",
    "If left long enough to ferment, grapes of wrath become a bitter whine.",
    "The term 'childbirth' is either redundant, or has concerning implications.",
    "Despite their name, dragons rarely drag things onto other things.",
    "Babies are not actually a type of bee, nor are they native the bay area.",
    "You can ask me to !eval python 3 expressions"
]

def sneakret():
    return LIST_OF_SECRETS[randint(0, len(LIST_OF_SECRETS)-1)]
