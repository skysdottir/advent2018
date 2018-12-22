# The plan!
# we're going to simulate the universe until t=10000 in fast-forward
# and then iterate through it step by step on user input
# because the time it will take to recognize words in the sky is probably larger than the time
# it'll take to page through it.
# Although it should be relatively simple to spot characters formed by star count per row...
# and the size of the universe is going to be big. Hm.
# Or I could just page through it and adjust render window by hand. That's not bad.

import re
line_regex = re.compile("^position=< *([-0-9]*), *([-0-9]*)> velocity=< *([-0-9]*), *([-0-9]*)>$")

def manhattan(point):
    return abs(point[0]) + abs(point[1])

def add(list, list2):
    return [list[i]+list2[i] for i in range(2)]

positions = []
velocities = []
time = 0

with open("input.txt", "r") as input:
    for line in input:
        match = line_regex.match(line)

        positions.append([int(match.group(1)), int(match.group(2))])
        velocities.append([int(match.group(3)), int(match.group(4))])

def tick():
    global time
    time += 1

    for i in range(len(positions)):
        new_position = add(positions[i], velocities[i])
        positions[i][0] = new_position[0]
        positions[i][1] = new_position[1]


for i in range(10124):
    tick()

# total swag at board size
min_x = 50
max_x = 250
min_y = 100
max_y = 150

def write():
    for y in range(min_y, max_y):
        row = [" "] * max_x
        for star in positions:
            if star[1] == y and star[0] >= min_x and star[0] < max_x:
                row[star[0]] = "X"
        print("".join(row))

write()
