# Okay, this is going to be a big problem. Let's just see how close these girls will get to the origin
# using our trusty manhattan distance algorithm

import re
line_regex = re.compile("^position=< *([-0-9]*), *([-0-9]*)> velocity=< *([-0-9]*), *([-0-9]*)>$")

count = -1

def manhattan(point):
    return abs(point[0]) + abs(point[1])

def add(list, list2):
    return [list[i]+list2[i] for i in range(2)]

with open("input.txt", "r") as input:
    for line in input:
        match = line_regex.match(line)
        count += 1

        position = [int(match.group(1)), int(match.group(2))]
        velocity = [int(match.group(3)), int(match.group(4))]

        last_dist = manhattan(position)
        distance = manhattan(position)
        improving = True

        time = 0

        while improving:
            # print("coords: {}".format(position))
            last_dist = distance
            position = add(position, velocity)
            distance = manhattan(position)
            time += 1

            improving = (distance < last_dist)
        
        print("Closest approach for {}: {} at time {}".format(count, last_dist, time))

# All this to say that all the points seem to pass within a manhattan distance of 300 of the origin
# mostly between times 10000 and 10200