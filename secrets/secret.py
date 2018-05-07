from random import randint

LIST_OF_SECRETS = [
    "An octopus is just a boneless spider.",
    "10 = 10, but not in base 1.",
    "A hippopotamus is just a really cool Opotamus.",
    "You can toggle the [Jog] ability by pressing the [Walk] key while already walking.",
    "The human colon actually has a second sphincter muscle.",
    "Taxation is theft.",
    "When fermented, grapes of wrath become unpleasant whine.",
    "The term 'childbirth' is either redundant or has frightening implications.",
    "Despite their name, dragons rarely drag things onto other things.",
    "Babies are neither insects nor can they often be found in bays."
]

def secret():
    return LIST_OF_SECRETS[randint(0, len(LIST_OF_SECRETS)-1)]
