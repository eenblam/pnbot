from random import randint
from PIL import Image  # ! DEPENDENCY ! Pillow module is not standard!


def build(width=500, height=500):
	empty_map = []
	for y in range(max(50, min(999, height))+1):
		row = []
		for x in range(max(50, min(999, width))+1):
				row.append(0)
		empty_map.append(row)
	return empty_map


def walk(empty_map):
	walked_map = empty_map
	HEIGHT = len(empty_map)
	WIDTH = len(empty_map[0])
	walker_x = int(WIDTH/2)
	walker_y = int(HEIGHT/2)
	for n in range(WIDTH*HEIGHT*2):
		direction = randint(1, 4)
		if direction == 1:
			walker_y += 1
		elif direction == 2:
			walker_x += 1
		elif direction == 3:
			walker_y -= 1
		else:
			walker_x -= 1
		if (walker_x < 1) or (walker_x > WIDTH-2) or (walker_y < 1) or (walker_y > HEIGHT-2):  # Cuts off before hitting the edge in order for the blur function to work optimally
			walker_x = int(WIDTH/2)
			walker_y = int(HEIGHT/2)
		walked_map[walker_y][walker_x] += 1
	return walked_map


def blur(walked_map):
	blurred_map = []
	for y in range(len(walked_map)):
		row = []
		for x in range(len(walked_map[y])):
			if y in [0, len(walked_map)-1] or x in [0, len(walked_map[y])-1]:
				row.append(0)
			else:
				row.append(int((walked_map[y+1][x]+walked_map[y-1][x]+walked_map[y][x+1]+walked_map[y][x-1]+4*walked_map[y][x])/8))
		blurred_map.append(row)
	return blurred_map


def delake(blurred_map):
	lakeless_map = []
	for y in range(len(blurred_map)):
		row = []
		for x in range(len(blurred_map[y])):
			row.append(blurred_map[y][x]+1)
		lakeless_map.append(row)
	for y in range(len(lakeless_map)):
		lakeless_map[y][0] = 0
		lakeless_map[y][-1] = 0
	for x in range(len(lakeless_map[0])):
		lakeless_map[0][x] = 0
		lakeless_map[-1][x] = 0
	for n in range(4):
		for y in range(1, len(lakeless_map)-1):
			for x in range(1, len(lakeless_map[y])-1):
				if 0 in [lakeless_map[y+1][x], lakeless_map[y-1][x], lakeless_map[y][x+1], lakeless_map[y][x-1]] and lakeless_map[y][x] == 1:
					lakeless_map[y][x] = 0
		for x in range(1, len(lakeless_map[0])-1)[::-1]:
			for y in range(1, len(lakeless_map)-1):
				if 0 in [lakeless_map[y+1][x], lakeless_map[y-1][x], lakeless_map[y][x+1], lakeless_map[y][x-1]] and lakeless_map[y][x] == 1:
					lakeless_map[y][x] = 0
		for y in range(1, len(lakeless_map)-1)[::-1]:
			for x in range(1, len(lakeless_map[y])-1)[::-1]:
				if 0 in [lakeless_map[y+1][x], lakeless_map[y-1][x], lakeless_map[y][x+1], lakeless_map[y][x-1]] and lakeless_map[y][x] == 1:
					lakeless_map[y][x] = 0
		for x in range(1, len(lakeless_map[0])-1):
			for y in range(1, len(lakeless_map)-1)[::-1]:
				if 0 in [lakeless_map[y+1][x], lakeless_map[y-1][x], lakeless_map[y][x+1], lakeless_map[y][x-1]] and lakeless_map[y][x] == 1:
					lakeless_map[y][x] = 0
	return lakeless_map


def save_to_image(finished_map, location, name):
	finished_map = finished_map[1:-1]
	for n in range(len(finished_map)):
		finished_map[n] = finished_map[n][1:-1]
	WIDTH = len(finished_map[0])
	HEIGHT = len(finished_map)
	HIGHPOINT = max([max(y) for y in finished_map])
	cutoff = 64
	multiplier = 1
	for number in [16, 8, 4]:
		if HIGHPOINT < number:
			cutoff /= 2
			multiplier *= 2
	to_image = Image.new("RGB", (WIDTH, HEIGHT))
	output = []
	for y in range(HEIGHT):
		for x in range(WIDTH):
			if finished_map[y][x] == 0:
				output.append(4202496)  # RGB hex -> decimal. Plz no touchy
			elif finished_map[y][x] > cutoff:
				output.append(12644576)
			else:
				output.append(8192 + 131843*multiplier*finished_map[y][x])
	to_image.putdata(tuple(output))  # I don't know the details of how Pillow handles data...
	to_image.save(location+name+".png")  # ...Or how to save said data arbitrarily to a database or whatever we decide on.
