from random import randint


def roll(dice_count, dice_size, explode_criteria=0):
    if explode_criteria >= dice_size:
        explode_criteria = 0
    rolls = []
    for i in range(dice_count):
        die = randint(1, dice_size)
        rolls.append(die)
        while die > (dice_size-explode_criteria):
            die = randint(1, dice_size)
            rolls.append(die)
    return rolls


def drop_low(rolls, number=1):
    if number >= len(rolls):
        return []
    else:
        rolls.sort()
        return rolls[number:]


def drop_high(rolls, number=1):
    if number >= len(rolls):
        return []
    else:
        rolls.sort()
        return rolls[:-number]


def count(rolls, hit):
    return len([i for i in rolls if i >= hit])


def parse(string):
    UNPARSED = string.split("d")
    if len(UNPARSED) == 1:
        OUTPUT = int(UNPARSED[0])
    else:
        EXPLOSIONS = len([x for x in UNPARSED[1] if x == "!"])
        if EXPLOSIONS:
            OUTPUT = roll(int(UNPARSED[0]), int(UNPARSED[1][:-EXPLOSIONS]), EXPLOSIONS)
        else:
            OUTPUT = roll(int(UNPARSED[0]), int(UNPARSED[1]))
    return OUTPUT


def preparse(string):
    check = string.split(" ")
    sums = []
    rolls = []
    negative = False
    for i in range(len(check)):
        if check[i] == "-":
            negative = True
        elif check[i] not in ["-", "+"]:
            rolls.append(parse(check[i]))
            sums.append(sum(rolls[-1])*((-1)**negative))
            negative = False
    return [sum(sums), rolls]
