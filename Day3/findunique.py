# the dumbest solution
# Like, I could fold all this stuff into a four-tree?
# But /ugh, why/?
# It's just 1m cells, this'll work fine

mem = list(list(0 for i in range(1000)) for j in range(1000))

file = open("input.txt", "r")

for line in file:
    # Fear my terrible string-processing powers
    line.strip
    line = line.replace(" ", "")

    at = line.find("@")
    cm = line.find(",")
    co = line.find(":")
    x = line.find("x")

    id = int(line[1:at])
    left = int(line[at+1:cm])
    top = int(line[cm+1:co])
    width = int(line[co+1:x])
    height = int(line[x+1:])

    for i in range(left, left+width):
        for j in range(top, top+height):
            mem[i][j] += 1

# And now it gets really ugly.
file.seek(0, 0)

for line in file:
    #this will look very familiar...
    line.strip
    line = line.replace(" ", "")

    at = line.find("@")
    cm = line.find(",")
    co = line.find(":")
    x = line.find("x")

    id = int(line[1:at])
    left = int(line[at+1:cm])
    top = int(line[cm+1:co])
    width = int(line[co+1:x])
    height = int(line[x+1:])

    found = True
    for i in range(left, left+width):
        for j in range(top, top+height):
            if mem[i][j] > 1:
                found = False

    if found:
        print("Found it! " + str(id))

file.close()