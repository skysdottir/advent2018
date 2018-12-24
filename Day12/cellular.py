# Almost disappointed in this one, because I've seen one-dimensional cellular automata before.
# we're going to represent the rules as numbers, because numbers are easy: ##..# -> 11001
# Which we'll stuff in a set. 
# If it's present it means the result is a 1, if it's absent the result is a 0

from collections import defaultdict

rules = {101, 1111, 11110, 10101, 11101, 10, 10110, 1011, 10011, 1100, 11001, 1000, 1110, 10001}
start = "##....#.#.#...#.#..#.#####.#.#.##.#.#.#######...#.##....#..##....#.#..##.####.#..........#..#...#"

# test data
# rules = {11, 100, 1000, 1010, 1011, 1100, 1111, 10101, 10111, 11010, 11011, 11100, 11101, 11110}
# start = "#..#.#..##......###...###"

board = defaultdict(lambda : 0)

i = 0
for char in start:
    if (char == "#"):
        board[i] = 1
    i += 1

first_plant = 0
last_plant = 100

def state(cell_index):
    # calculate the rule that should apply to this cell
    rule = (board[cell_index-2] * 10000) + \
        (board[cell_index-1] * 1000) + \
        (board[cell_index] * 100) + \
        (board[cell_index+1] * 10) + \
        (board[cell_index+2])
    return 1 if rule in rules else 0

last_count = 0

# and now the simulator itself
for generation in range(1000):
    new_board = defaultdict(lambda : 0)
    for i in range(first_plant - 2, last_plant + 3):
        is_plant = state(i)
        new_board[i] = is_plant
        if i < first_plant and is_plant == 1:
            first_plant = i

        if i > last_plant and is_plant == 1:
            last_plant = i
    
    board = new_board

    count = sum([k for k,v in board.items() if v == 1])
    print("{}: ({}) for {}".format(generation, count - last_count, count))
    last_count = count

# cheated a bit and checked Reddit - rulesets and initial data were chosen to converge
# to a nice easy monotonic increase. Found that increase state (999: (42) for 43168),
# calculated out the answer