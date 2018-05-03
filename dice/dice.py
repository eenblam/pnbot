from random import randint


def roll(dice_count, dice_size, features=(0, 0, 0, 0)):
    for i in [features[0], features[1], features[0] + features[1]]:
        if i >= dice_size:
            features[0] = 0
            features[1] = 0
            break
    for i in [features[2], features[3], features[2] + features[3]]:
        if i >= dice_count:
            features[2] = 0
            features[3] = 0
            break
    EXPLODE = dice_size - features[0]
    IMPLODE = features[1]
    CAP_MIN = features[2]
    CAP_MAX = features[3]
    rolls = []
    for i in range(dice_count):
        die = randint(1, dice_size)
        rolls.append(die)
        while die > EXPLODE or die <= IMPLODE:
            die = randint(1, dice_size)
            rolls.append(die)
    if CAP_MIN or CAP_MAX:
        rolls.sort()
        return rolls[CAP_MIN:(len(rolls) - CAP_MAX)]
    else:
        return rolls


def parse(string):
    UNPARSED = string.split("d")
    if len(UNPARSED) == 0:
        OUTPUT = 0
    elif len(UNPARSED) == 1:
        OUTPUT = int(UNPARSED[0])
    else:
        EXCLAMATIONS = len([x for x in UNPARSED[1] if x == "!"])
        QUESTIONS = len([x for x in UNPARSED[1] if x == "?"])
        PLUSES = len([x for x in UNPARSED[1] if x == "+"])
        MINUSES = len([x for x in UNPARSED[1] if x == "-"])
        if EXCLAMATIONS or QUESTIONS or PLUSES or MINUSES:
            OUTPUT = roll(int(UNPARSED[0]), int(UNPARSED[1][:-(EXCLAMATIONS + QUESTIONS + PLUSES + MINUSES)]),
                          [EXCLAMATIONS, QUESTIONS, PLUSES, MINUSES])
        else:
            OUTPUT = roll(int(UNPARSED[0]), int(UNPARSED[1]))
    return OUTPUT


def preparse(string):
    CHECK = string.split(" ")
    rolls = []
    score = 0
    negative = False
    if CHECK[0][:3] == "hit":
        COUNTER = int(CHECK[0][3:])
        TRUE_START = 1
    else:
        COUNTER = 0
        TRUE_START = 0
    for i in range(TRUE_START, len(CHECK)):
        if CHECK[i] == "-":
            negative = True
        elif CHECK[i] not in ["-", "+"]:
            rolls.append(parse(CHECK[i]))
            if negative:
                rolls[-1] = [-i for i in rolls[-1]]
            negative = False
    if COUNTER:
        for i in rolls:
            score += len([x for x in i if x >= COUNTER])
    else:
        for i in rolls:
            score += sum(i)
    return [score, rolls]
