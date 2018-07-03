from random import randint
from math import ceil
from PIL import Image  # ! DEPENDENCY ! Pillow module is not standard!


def map_parse(split_string):
    try:
        output = [int(x) for x in split_string]
    except:
        output = []
    if len(output) > 2:
        output = output[:2]
    elif len(output) == 1:
        output.append(500)
    elif len(output) == 0:
        output = [500, 500]
    return output


def build(xy_coordinates_as_list):
    width = xy_coordinates_as_list[0]
    height = xy_coordinates_as_list[1]
    empty_map = []
    row = []
    for x in range(max(50, min(999, width)) + 2):
        row.append(0)
    for y in range(max(50, min(999, height)) + 2):
        empty_map.append(row)
    return empty_map


def walk(empty_map):
    walked_map = empty_map
    HEIGHT = len(empty_map)
    WIDTH = len(empty_map[0])
    walker_x = int(WIDTH / 2)
    walker_y = int(HEIGHT / 2)
    for n in range(WIDTH * HEIGHT * 2):
        direction = randint(1, 4)
        if direction == 1:
            walker_y += 1
        elif direction == 2:
            walker_x += 1
        elif direction == 3:
            walker_y -= 1
        else:
            walker_x -= 1
        if (walker_x < 1) or (walker_x > WIDTH - 2) or (walker_y < 1) or (walker_y > HEIGHT - 2):
            # Cuts off before hitting the edge in order for the blur function to work optimally
            walker_x = int(WIDTH / 2)
            walker_y = int(HEIGHT / 2)
        walked_map[walker_y][walker_x] += 1
    return walked_map


def normalize(walked_map):
    highest = max([max(x) for x in walked_map])
    normal_map = []
    for y in range(len(walked_map)):
        row = []
        for x in range(len(walked_map[y])):
            row.append(int((ceil(pow(walked_map[y][x], 2)/highest)+walked_map[y][x])/2))
        normal_map.append(row)
    return normal_map


def blur(normal_map):
    blurred_map = []
    for y in range(len(normal_map)):
        row = []
        for x in range(len(normal_map[y])):
            if y in [0, len(normal_map) - 1] or x in [0, len(normal_map[y]) - 1]:
                row.append(0)
            else:
                row.append(
                    int(
                        (normal_map[y + 1][x] 
                         + normal_map[y - 1][x] 
                         + normal_map[y][x + 1] 
                         + normal_map[y][x - 1] 
                         + 4 * normal_map[y][x])
                        / 8
                    )
                )
        blurred_map.append(row)
    return blurred_map


def delake(blurred_map):
    lakeless_map = []
    for y in range(len(blurred_map)):
        row = []
        for x in range(len(blurred_map[y])):
            row.append(blurred_map[y][x] + 1)
        lakeless_map.append(row)
    for y in range(len(lakeless_map)):
        lakeless_map[y][0] = 0
        lakeless_map[y][-1] = 0
    for x in range(len(lakeless_map[0])):
        lakeless_map[0][x] = 0
        lakeless_map[-1][x] = 0
    for n in range(4):
        for y in range(1, len(lakeless_map) - 1):
            for x in range(1, len(lakeless_map[y]) - 1):
                if 0 in [lakeless_map[y + 1][x], 
                         lakeless_map[y - 1][x], 
                         lakeless_map[y][x + 1],
                         lakeless_map[y][x - 1]
                        ] and lakeless_map[y][x] == 1:
                    lakeless_map[y][x] = 0
        for x in range(1, len(lakeless_map[0]) - 1)[::-1]:
            for y in range(1, len(lakeless_map) - 1):
                if 0 in [lakeless_map[y + 1][x],
                         lakeless_map[y - 1][x],
                         lakeless_map[y][x + 1],
                         lakeless_map[y][x - 1]
                        ] and lakeless_map[y][x] == 1:
                    lakeless_map[y][x] = 0
        for y in range(1, len(lakeless_map) - 1)[::-1]:
            for x in range(1, len(lakeless_map[y]) - 1)[::-1]:
                if 0 in [lakeless_map[y + 1][x],
                         lakeless_map[y - 1][x],
                         lakeless_map[y][x + 1],
                         lakeless_map[y][x - 1]
                        ] and lakeless_map[y][x] == 1:
                    lakeless_map[y][x] = 0
        for x in range(1, len(lakeless_map[0]) - 1):
            for y in range(1, len(lakeless_map) - 1)[::-1]:
                if 0 in [lakeless_map[y + 1][x],
                         lakeless_map[y - 1][x],
                         lakeless_map[y][x + 1],
                         lakeless_map[y][x - 1]
                        ] and lakeless_map[y][x] == 1:
                    lakeless_map[y][x] = 0
    return lakeless_map


"""
def rainshadow(lakeless_map): # Split into right2left and left2right passes as seperate functions
    pass1 = []
    pass2 = []
    cap = 0
    for y in range(len(lakeless_map)):
        row1 = []
        row2 = []
        for x in range(len(lakeless_map[0])):
            if y in [0, 1, len(lakeless_map)-2, len(lakeless_map)-1]:
                row1.append(0)
            elif x in [0, 1, len(lakeless_map[0])-2, len(lakeless_map[0])-1]:
                row1.append(0)
            else:
                cap = max(cap, lakeless_map[y][x])
                if 0 in [lakeless_map[y][x], lakeless_map[y-1][x], lakeless_map[y+1][x], lakeless_map[y][x-1], lakeless_map[y][x+1]]:
                    cap = 0
                    row1.append(0)
                elif lakeless_map[y][x] < cap:
                    row1.append(cap)
                else:
                    row1.append(0)
        pass1.append(row1)
        for x in list(range(len(lakeless_map[0])))[::-1]:
            if y in [0, 1, len(lakeless_map)-2, len(lakeless_map)-1]:
                row2.append(0)
            elif x in [0, 1, len(lakeless_map[0])-2, len(lakeless_map[0])-1]:
                row2.append(0)
            else:
                cap = max(cap, lakeless_map[y][x])
                if 0 in [lakeless_map[y][x], lakeless_map[y-1][x], lakeless_map[y+1][x], lakeless_map[y][x-1], lakeless_map[y][x+1]]:
                    cap = 0
                    row2.append(0)
                elif lakeless_map[y][x] < cap:
                    row2.append(cap)
                else:
                    row2.append(0)
        pass2.append(row2[::1])
    output = []
    for y in range(len(pass1)):
        row = []
        for x in range(len(pass1[0])):
            row.append(max(pass1[y][x], pass2[y][x]))
        output.append(row)
    return output
"""


def colorize(finished_map):
    def RGB(red, green, blue):
        return red + 256*green + 256*256*blue

    finished_map = finished_map[1:-1]
    for n in range(len(finished_map)):
        finished_map[n] = finished_map[n][1:-1]
    shadow = rainshadow(finished_map)
    width = len(finished_map[0])
    height = len(finished_map)
    highpoint = max([max(y) for y in finished_map])
    cutoff = 64
    multiplier = 1
    for number in [16, 8, 4]: # This loop scales up the color gradient of short landmasses to match tall ones.
        if highpoint < number:
            cutoff /= 2
            multiplier *= 2
    colored_map = []
    for y in range(height):
        row = []
        for x in range(width):
            if finished_map[y][x] == 0: # Ocean
                row.append(RGB(0, 32, 64))  # 4202496 in decimal.
            elif finished_map[y][x] > cutoff: # Mountain Caps
                row.append(RGB(240, 240, 240)) # 15790320 in decimal. Previously 12644576
            else:
                dryness = shadow[y][x]
                row.append(
                    RGB(dryness, 32, 0)
                    + RGB(3, 3, 2) * multiplier * finished_map[y][x]
                )
                # 8192, 131843, ??? in decimal
        colored_map.append(row)
    return colored_map


def generate(split_string, file_location):
    output = colorize(
            delake(
                    blur(
                        normalize(
                            walk(
                                build(
                                    map_parse(
                                    split_string
                                    )
                                )
                            )
                        )
                    )
                )
            )
    to_image = Image.new("RGB", (len(output[0]), len(output)))
    to_image.putdata(tuple([x for y in output for x in y]))
    to_image.save(file_location)
