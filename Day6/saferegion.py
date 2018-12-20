# See commentary in manhattan.py, this problem is honestly simpler
# All that to say! Coords are in the range (43, 358), 
# and I'm just going to round that up to (0, 400)

# And we're going to flatten things even more: a cell's ID will be X + edge_length*Y

from collections import Counter

# declare us some constants so we can run test data
offset = 0 # We're working in (0-400) now
edge_length = 400 # 400 for prod data
maxid = edge_length * edge_length # 640000 for prod data

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

count = 0

#why do we have unique numeric point IDs, you ask?
for id in range(maxid):
    distance = 0

    for point in points:
        distance += manhattan(id, point)
    
    if(distance < 10000):
        count += 1

    if( id % 1000 == 0):
        print(id)

print(count)