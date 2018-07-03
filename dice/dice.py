from random import randint


def roll(dice_count, dice_size, explode=0, implode=0):
    if explode + implode >= dice_size:
        implode = 0
        explode = 0
    rolls = []
    for i in range(dice_count):
        die = randint(1, dice_size)
        rolls.append(die)
        loop_is_sane = 31  # Arbitrary limit on number of dice gained by explosions
        while (die > (dice_size - explode) or die <= implode) and loop_is_sane:  # Duck typing logic gates ftw
            die = randint(1, dice_size)
            rolls.append(die)
            loop_is_sane -= 1
    return rolls


def parse(string):
    unparsed = string.split("d")
    if len(unparsed) == 0:
        output = 0
    elif len(unparsed) == 1:
        output = int(unparsed[0])
    else:
        explode_criteria = len([x for x in unparsed[1] if x == "!"])
        implode_criteria = len([x for x in unparsed[1] if x == "?"])
        drop_lowest = len([x for x in unparsed[1] if x == "+"])
        drop_highest = len([x for x in unparsed[1] if x == "-"])
        if explode_criteria or implode_criteria or drop_lowest or drop_highest:
            output = roll(
                            int(unparsed[0]),
                            int(unparsed[1][:-(explode_criteria + implode_criteria + drop_lowest + drop_highest)]),
                            explode_criteria,
                            implode_criteria
                        )
        else:
            output = roll(int(unparsed[0]), int(unparsed[1]))
        if drop_lowest or drop_highest:
            output.sort()
            output = output[drop_lowest:len(output)-drop_highest]
    return output


def preparse(string):
    to_check = string.split(" ")
    rolls = []
    negative = False
    for i in range(len(to_check)):
        if to_check[i] == "-":
            negative = True
        elif to_check[i] != "+":  # TODO? Exception handling for weird inputs ("*", "/", etc)
            temp_rolls = parse(to_check[i])
            if negative:
                temp_rolls = [-i for i in temp_rolls]
            negative = False
            for j in temp_rolls:
                rolls.append(j)
    return rolls


def prepreparse(string):
    check = string.split(" ")
    if check[0][:3] == "hit":
        hit_criteria = int(check[0][3:])
        dice = preparse(" ".join(check[1:]))
    else:
        hit_criteria = 0
        dice = preparse(string)
    if hit_criteria:
        score = len([x for x in dice if x >= hit_criteria])
    else:
        score = sum(dice)
    return "Rolled a " + str(score) + ".\n    " + str(dice)

