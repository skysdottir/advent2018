# Okay, day 15 (of doom)
# We're going to use single IDs for each square, id = x + row_size*y
# because all selection happens in page order (left to right, top row first), that just means
# we'll pick the lowest ID

row_size = 32
filename = "input.txt"

# Initialize the board with closed space so extra volume just doesn't get used
board=["#"] * row_size**2
elf_dps = 20
max_dps = 30

# We're going to store elves and goblins as loc_id -> (health, name)
elves = dict()
goblins = dict()
elf_count = 0
round = 0

def id(x, y):
    return x + row_size*y

def coord(id):
    return[id % row_size, int(id/row_size)]

# ingest a map
with open(filename, "r") as mapfile:
    file_lines = mapfile.readlines()

def init():
    global elf_count, round

    elves.clear()
    goblins.clear()
    round = 0

    for y, line in enumerate(file_lines):
        for x, char in enumerate(line):
            if char == "\n":
                continue
            # yes, we're going to stick units onto the map directly
            # because they are blocking objects
            board[id(x, y)] = char
            if char == "E":
                elves[id(x, y)] = [200, "E{}{}".format(x, y)]
            elif char == "G":
                goblins[id(x, y)] = [200, "G{}{}".format(x, y)]

    elf_count = len(elves)

# Turn steps, as functions to be coordinated later:

# 1) we see if there are existing enemies - this'll happen in tick()

# 2) if we're adjacent to any enemies - if so, no moving

# no filtering, just get all of the adjacent squares
def adjacent(id):
    neighbors = [id-row_size, id-1, id+1, id+row_size]
    return [i for i in neighbors if i > 0 and i < row_size**2]

# and get all neighboring enemies
def adjacent_enemies(id, is_elf):
    return [i for i in adjacent(id) if board[i] == ("G" if is_elf else "E")]

# 3) we find all the possible spaces we might move to
def open_adjacent(id):
    return [i for i in adjacent(id) if board[i] == "."]

def attack_locations(is_elf):
    locs = [i for l in (goblins.keys() if is_elf else elves.keys()) for i in open_adjacent(l)]

    #if is_elf:
    #    print("places to attack: {}".format(locs))

    return locs

# 4) we find the set of closest spaces
def bfs(start_id, locations):
    active = set([start_id])
    closed = set()
    distance = 0

    if start_id in locations:
        # Great! We're already there!
        # print("Already in {} of {}".format(start_id, locations))
        return [start_id]

    # Safe assumption: there's no routes longer than the board size
    while distance < row_size**2:
        distance += 1
        closed.update(active)
        new_active = {i for n in active for i in open_adjacent(n) if i not in closed}
        active = new_active

        if len(new_active.intersection(locations)) > 0:
            break
    
    return [i for i in active if i in locations]

# 5) find the first
def pick_dest(start_id, locations):
    dests = bfs(start_id, locations)

    if len(dests) == 0:
        return -1

    dest = sorted(dests)[0]

    # print("Moving to {} out of {}".format(dest, dests))

    return dest

# 6) and pick the next step towards it.
# Fortunately for us, this is solvable with the same code backwards - we want to move to the space
# closest to the target, in reading order, so we'll just pick_dest from our selected destination
# "to" open_adjacent(start_id), and that'll be the space we move to.

#7 ) and move the piece
def manhattan(from_id, to_id):
    from_coord = coord(from_id)
    to_coord = coord(to_id)

    return abs(from_coord[0]-to_coord[0]) + abs(from_coord[1]-to_coord[1])

def move(from_id, to_id, is_elf):
    # some sanity tests
    assert board[from_id] in ["E", "G"]
    assert board[to_id] == "."
    assert manhattan(from_id, to_id) == 1

    # print("Moving {} to {}".format(coord(from_id), coord(to_id)))

    # and the move itself
    board[to_id] = board[from_id]
    board[from_id] = "."

    if is_elf:
        health = elves.pop(from_id)
        elves[to_id] = health
    else:
        health = goblins.pop(from_id)
        goblins[to_id] = health
    
    return to_id
    

# Phew! And now it's time for combat

# 8) get all adjacent enemies, pick weakest
def select_target(id, is_elf):
    foes = adjacent_enemies(id, is_elf)
    all_foes = (goblins if is_elf else elves)

    # print("Unit at {} found foes {}".format(id, foes))

    if len(foes) == 0:
        return -1
    elif len(foes) == 1:
        id = foes[0]
        return [id, all_foes[id][0], all_foes[id][1]]
    else:
        # this will be (location, health, name) triples
        triples = [[i, all_foes[i][0], all_foes[i][1]] for i in foes]

        # magic sort! We want the weakest, and then the lowest ID if there's more than one
        triples.sort(key = lambda foe: foe[1]*1000 + foe[0])
        return triples[0]

# 9) attack!
# Bug discovered in part 2: also need to remove the dead unit from the move order
# to prevent phantom moves if someone else moves in on top of them
def kill(id, is_elf):
    pop = (elves if is_elf else goblins)
    # print("Killing unit {} at {} from pop {}".format(id, coord(id), pop))
    pop.pop(id)
    board[id] = "."

def attack(attacker_id, target_id, is_elf):
    # print("{} attacking {}!".format(coord(attacker_id), coord(target_id)))
    # sanity test
    assert board[attacker_id] == ("E" if is_elf else "G")

    foes = (goblins if is_elf else elves)

    # adjustable attack power for part 2
    foes[target_id][0] -= (elf_dps if is_elf else 3)
    if foes[target_id][0] <= 0:
        return True
    
    return False

# Coordination time! What does a move look like?
def unit_move_phase(id, is_elf):
    # print("Beginning move phase for {} at {}".format(("elf" if is_elf else "gob"), id))

    if len(adjacent_enemies(id, is_elf)) > 0:
        # There's an enemy here! No need to move
        return id
    
    goal = pick_dest(id, attack_locations(is_elf))

    if goal == -1:
        # Couldn't find a reachable attack space
        return id
    
    next = pick_dest(goal, open_adjacent(id))

    if next == -1:
        # Couldn't find a route to the desired attack space
        return id

    return move(id, next, is_elf)

# what does a win look like?
def test_victory():
    if len(elves) == 0 or len(goblins) == 0:
        elves_win = (len(elves) > 0)
        winners = (elves if elves_win else goblins)
        remaining_health = sum([v[0] for k,v in winners.items()])

        print("And that's a wrap! Last finished round: {} Winner: {}".format(round, "Elves" if elves_win else "Goblins"))
        print("Surviving elves: {} of {}".format(len(elves), elf_count))
        print("Answer: {}".format(remaining_health * round))
        return True
    
    return False

# and the tick function itself
def tick():
    dead = []
    # get move order - triple: (location, name, is_elf)
    move_order = [(id, val[1], True) for id, val in elves.items()]
    move_order.extend([(id, val[1], False) for id, val in goblins.items()])
    move_order.sort(key=lambda pair:pair[0])

    # print("Round {} move order: {}".format(round, [coord(unit[0]) for unit in move_order]))

    for unit_triple in move_order:
        # print("Ticking {} at {}".format(("elf" if unit_triple[2] else "gob"), coord(unit_triple[0])))
        # zeroth, does this unit still exist?
        if unit_triple[1] in dead:
            # print("Unit {} at {} died this round and cannot move".format(unit_triple[1], coord(unit_triple[0])))
            continue

        char = board[unit_triple[0]]
        if char not in ["E", "G"]:
            # print("Missing unit at {}".format(coord(unit[0])))
            continue
        
        # first, are we done?
        if test_victory():
            # print("Unit {} declares victory!".format(coord(unit_triple[0])))
            return False

        # second, do we need to move?
        loc = unit_move_phase(unit_triple[0], unit_triple[2])

        # (location, health, name)
        target_triple = select_target(loc, unit_triple[2])

        # okay this is getting hideous - now that units have names and locations
        # what's what is getting hard to juggle and needs structural fixes
        # Fortunately I only need this to work once
        if target_triple != -1:
            if attack(loc, target_triple[0], unit_triple[2]):
                # target died
                dead.append(target_triple[2])
                kill(target_triple[0], not unit_triple[2])

    return True

def print_board():
    print("After round {}:".format(round))
    for y in range(row_size):
        row = "".join([board[id(x, y)] for x in range(row_size)])

        units = [(id, elves[id], True) for id in elves.keys() if coord(id)[1] == y]
        units.extend([(id, goblins[id], False) for id in goblins.keys() if coord(id)[1] == y])
        units.sort(key=lambda unit: unit[0])

        health = ", ".join(["{}{}({})".format(("E" if unit[2] else "G"), coord(unit[0]), unit[1]) for unit in units])

        print("{}  {}".format(row, health))

# spun through all the possibilities to find the win condition
# seems to happen at elf_dps = 25
while elf_dps < max_dps:
    print("Running sim at elf_dps " + str(elf_dps))
    init()
    fight = True
    while fight:
        # print_board()
        fight = tick()
        round += 1

    elf_dps += 1
# print_board()