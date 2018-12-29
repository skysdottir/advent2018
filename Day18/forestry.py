# Okay, we're going to be quick and dirty with this one.
# Coords are going to be [y][x] because we're doing nested lists.
# and that's the easy way to read them in from a file.

from collections import Counter

board = []
line_len = 0
board_len = 0

with open("input.txt", "r") as infile:
    for line in infile:
        board_len += 1
        board.append([char for char in line if char in {".", "#", "|"}])
        line_len = len(line) - 1

def print_board():
    for line in board:
        print("".join(line))

def neighbors(y, x):
    count = Counter()
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if (0 <= (x + dx) < line_len) and (0 <= (y + dy) < board_len) and (dy != 0 or dx != 0):
                count[board[y+dy][x+dx]] += 1
    # print("Found neighbors for {},{}: {}".format(x, y, count))
    return count

def tick(old_board):
    new_board = []
    for y in range(board_len):
        new_row = []
        for x in range(line_len):
            cell = old_board[y][x]
            neigh = neighbors(y, x)

            if cell == ".":
                # empty space
                if neigh["|"] >= 3:
                    # if there's three or more adjacent acres of forest, this one becomes a forest
                    new_row.append("|")
                else:
                    # otherwise nothing happens
                    new_row.append(cell)
            elif cell == "|":
                # a forest!
                if neigh["#"] >= 3:
                    # this becomes a lumberyard
                    new_row.append("#")
                else:
                    # nothing happens
                    new_row.append(cell)
            elif cell == "#":
                if neigh["#"] >= 1 and neigh["|"] >= 1:
                    # working lumberyard, nothing happens
                    new_row.append(cell)
                else:
                    # lumberyard closes
                    new_row.append(".")
            else:
                raise RuntimeError("I don't know what to do with {} at {},{}".format(cell, x, y))
        # print("Adding new row: " + str(new_row))
        new_board.append(new_row)
    return new_board

def score():
    count = Counter()
    for row in board:
        for cell in row:
            count[cell] += 1
    
    #print("Counts: " + str(count))
    #print("Final score: " +str(count["#"] * count["|"]))
    return count["#"] * count["|"]

def loop_math(i, start_score):
    global board
    # we're probably looping. Find how long the loop is, and then work out what 1bn will be
    rounds = []
    local_iter = 0
    new_score = 0
    print("looking for loop starting at " + str(i))

    while new_score != start_score and local_iter < 100:
        board = tick(board)
        local_iter += 1
        new_score = score()
        rounds.append(new_score)
    
    print("Found loop of length {}, {}" .format(len(rounds), rounds))
    
    loop_len = len(rounds)
    offset = i % loop_len
    bn_offset = 1000000000 % loop_len
    bn_index = bn_offset - offset
    bn_normal = (bn_index + loop_len if bn_index < 0 else bn_index)

    print("For score at 1bn of {} at offset {}".format(rounds[bn_normal], bn_normal))


scores = Counter()
#print_board()
for i in range(1000000000):
    # I bet this is going to converge before 1bn seconds
    s = score()
    print("{}: {}".format(i, s))
    scores[s] += 1

    if scores[s] >= 5:
        # almost certainly converging
        loop_math(i, s)
        break

    #throwaway = input()
    board = tick(board)
    #print_board()

# ...okay, so I ended up overshooting by one. Right answer was 227608, one before the
# 226080 my math came up with. Whoops.