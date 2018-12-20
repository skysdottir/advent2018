# brute force time
# Challenge is to find the largest non-infinite space that's closest to one point
# Edges are interesting - three points in a single column will each have an infinite space
# but if the edge is concave, it creates a finite space for the inner point.
# Worst case, origin at top left, goes like: (2,1),(2,2),(1,n) for some big n.
# Thanks to manhattan distance, the line between (0) and (1)'s territory will be horizontal, at Y=2
# But the line between (1) and (2) will be a diagonal, Y = X + (n/2) (+/- 1 or so, because of the horizontal offset)
# Which won't cross Y=2 until -(n/2)
# If the space around (1) is bound on the positive side by additional points, we'll need to compute
# (n/2)+1 units beyond each limit to ensure spaces are closed.
# All that to say! Coords are in the range (43, 358), 
# and I'm just going to round that up to (0, 400) and compute (-200, 600).
# and for extra fun, because I like positive numbers, I'm actually going to add 200 to everything
# so I can work in (0,800) space.

# And we're going to flatten things even more: a cell's ID will be X + 800*Y

from collections import Counter

# declare us some constants so we can run test data
offset = 200 # 200 for prod data
edge_length = 800 # 800 for prod data
maxid = 640000 # 640000 for prod data

#Utils:
def pid(x, y):
    return x + edge_length*y

def pair(id):
    x = id % edge_length
    y = int(id / edge_length)

    return(x, y)

def manhattan(source_id, dest_id):
    source = pair(source_id)
    dest = pair(dest_id)
    x_dist = abs(source[0]-dest[0])
    y_dist = abs(source[1]-dest[1])
    return x_dist + y_dist

#Let's ingest some points
with open("input.txt", "r") as input:
    rawpoints = input.readlines()
    
    points = list()
    
    for point in rawpoints:
        coord_string = point.split(", ")
        coords = (int(coord_string[0]) + offset, int(coord_string[1]) + offset)
        id = pid(coords[0], coords[1])
        points.append(id)

        # and some test logic
        t_coords = pair(id)
        assert t_coords[0] == coords[0]
        assert t_coords[1] == coords[1]

print(points)

map = dict()
count = Counter()

#why do we have unique numeric point IDs, you ask?
for id in range(maxid):
    #evil laughter goes here
    closest = -1
    shortest_dist = edge_length * 2

    for point in points:
        dist = manhattan(id, point)
        if (dist < shortest_dist):
            closest = point
            shortest_dist = dist
        elif (dist == shortest_dist):
            closest = -1
        # else do nothing, this isn't the closest point
    
    map[id] = closest
    count[closest] += 1

    if (id % 1000 == 0):
        print(str(id))

print("count: " + str(count))

# And now for my next trick!
# Because we know any finite spaces will have closed before they reached my edges,
# any id that appears in an edge space is part of an infinite space.
# Collect those, filter them out of the counter, and the biggest space remaining is the one we want.

infinites = set()

for id in range(edge_length):
    top = pid(id, 0)
    left = pid(0, id)
    right = pid(edge_length-1, id)
    bottom = pid(id, edge_length-1)

    infinites.add(map[top])
    infinites.add(map[left])
    infinites.add(map[right])
    infinites.add(map[bottom])

for id in list(count):
    if id not in infinites:
        print("Set {} contains {}".format(id, count[id]))