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

count = 0

for i in range(1000):
    for j in range(1000):
        if mem[i][j] > 1:
            count += 1

print(count)

file.close()