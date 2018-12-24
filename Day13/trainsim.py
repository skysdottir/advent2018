# Okay, time to do more simulation
# There's six possible board cells: " ", "-", "|", "\", "/", and "+"
# And four possible train directions: "^", "v", "<" and ">".
# Directions will be stored as (0, 4), with 0 north, one east, two south, three west
# so train turn status will cycle through (-1, 0, 1) which we can just add to direction every
# time we hit a +.
# trains are a four-vector: x, y, direction, turn state

x_size = 0
y_size = 0
board = []
trains = []

train_chars = ["^", ">", "v", "<"]

#and now some cleverness: each direction indexes to its change in [x,y] pairs
velocity_deltas = [[0, -1], [1, 0], [0, 1], [-1, 0]]

# For the "\" track, which we'll call a left turn: this[old_dir] = new_dir
left_turns=[3, 2, 1, 0]

# for the "/" track, which we'll call a right turn
right_turns=[1, 0, 3, 2]

# load us a board!
with open("input.txt", "r") as input:
    for line in input:
        y_size += 1
        x_size = max([x_size, len(line)])
    
    input.seek(0)

    for x in range(x_size):
        board.append([" " for y in range(y_size)])

    for y, line in enumerate(input):
        for x, char in enumerate(line):
            if char in train_chars:
                dir = train_chars.index(char)
                trains.append([x, y, dir, -1])
                char = "|" if (dir % 2 == 0) else "-"
            
            board[x][y] = char

def train_at(x, y):
    for train in trains:
        if train[0] == x and train[1] == y:
            return train

def is_train_at(x, y):
    for train in trains:
        if train[0] == x and train[1] == y:
            return True
    
    return False

# And now a test method
def print_state():
    for y in range(y_size):
        row = []
        for x in range(x_size):
            char = board[x][y]
            if is_train_at(x, y):
                char = train_chars[train_at(x, y)[2]]    
            
            row.append(char)
        print("".join(row))

    print("")
    print("trains: " + str(trains))

def sort(train_list):
    return sorted(train_list, key=lambda train: train[0]+train[1]*x_size).reverse()

# And now a tick method
def tick():
    global trains
    for train in sorted(trains):
        # pull it all into local variables
        x = train[0]
        y = train[1]
        dir = train[2]
        turn = train[3]

        if x == -1 and y == -1:
            #means this train got hit this tick.
            continue

        # Find the new location
        vel = velocity_deltas[dir]
        new_x = x + vel[0]
        new_y = y + vel[1]
        
        # check for collisions
        if is_train_at(new_x, new_y):
            # for part 1:
            # raise Exception("Collision at!", new_x, new_y)

            # means we need to drop this train and the one it hit.
            victim = train_at(new_x, new_y)
            train[0] = -1
            train[1] = -1
            victim[0] = -1
            victim[1] = -1
            continue
        
        # And find the new direction
        track = board[new_x][new_y]

        if track == " ":
            raise Exception("Train off track!", new_x, new_y)
        elif track == "-" and dir % 2 == 1:
            # we're going east or west, track runs east-west, all good
            new_dir = dir
        elif track == "|" and dir % 2 == 0:
            # same, with north-south
            new_dir = dir
        elif track == "\\":
            new_dir = left_turns[dir]
        elif track == "/":
            new_dir = right_turns[dir]
        elif track == "+":
            #intersection!
            new_dir = (dir + turn)%4 # good news! this'll bring -1 up to 3, correctly
            turn += 1
            if turn > 1:
                turn = -1
        else:
            raise Exception("Something went wrong!", train)
        
        # and actually update the board
        train[0] = new_x
        train[1] = new_y
        train[2] = new_dir
        train[3] = turn
    # end for train in trains

    # and now clean up trains that got hit this round
    new_trains = [train for train in trains if (train[0] != -1 and train[1] != -1)]
    trains = new_trains
# end tick

for i in range(1000000):
    #print_state()
    tick()
    if (len(trains) == 1):
        print("End! " + str(trains))
        break

        