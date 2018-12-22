# Okay, more math. Yay math.
# Initial bet: part 2 of this problem is going to be blowing the problem up to a scale where 
# o(n^2) solutions just don't work.

def power(x, y):
    serial = 4455
    rack_id = x + 10
    charge = rack_id * y
    charge += serial
    charge *= rack_id

    charge = charge % 1000
    charge = int(charge / 100)

    charge -= 5
    return charge

# assemble the grid!
min_x = 1
max_x = 300
min_y = 1
max_y = 300

grid = [[0 for i in range(max_y)] for j in range(max_x)]

for x in range(min_x, max_x):
    for y in range(min_y, max_y):
        grid[x][y] = power(x, y)

# and now find the most powerful square

best = 0
best_coords = [0, 0, 0]

def sum_power(x, y, size):
    count = 0
    for z in range(size):
        count += sum(grid[x+z][y:y+size])
    return count

for z in range(1, max_x):
    print("Z: " + str(z))
    for x in range(min_x, (max_x - z)):
        for y in range(min_y, (max_y - z)):
            score = sum_power(x, y, z)
            if (score > best):
                best = score
                best_coords = [x, y, z]
                print("Found better! {} at {}".format(best, best_coords))

print("best power: {} at {}".format(best, best_coords))