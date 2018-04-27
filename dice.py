from random import randint


def roll(dice_count, dice_size=0, explode_criteria=0):
	if dice_size == 0:
		return dice_count
	else:
		if explode_criteria >= dice_size:
			explode_criteria = 0
		rolls = []
		for i in range(dice_count):
			die = randint(1, dice_size)
			rolls.append(die)
			while die > (dice_size - explode_criteria):
				die = randint(1, dice_size)
				rolls.append(die)
		return rolls


def drop_low(rolls, count=1)
	if count >= len(rolls):
		return []
	else:
		rolls.sort()
		return rolls[count:]


def drop_high(rolls, count=1)
	if count >= len(rolls):
		return []
	else:
		rolls.sort()
		return rolls[:-count]


def count(rolls, hit)
	return len([i for i in rolls if i >= hit])


def parse(string)  # WIP
	unparsed = string.split("d")
	EXPLOSIONS = len([x for x in unparsed[1] if x == "!"])
	# unparsed[1] = str
	roll(INPUT[0], INPUT[1], EXPLOSIONS)


def preparse(string)  #WIP
	to_sum = string.split(" + ")
	asdf = [parse(i) for i in to_sum]
	


