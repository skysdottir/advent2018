# Sadly, not actually a genetic algorithm, there's no fitness function
# okay, because my target value ends with a 1, that's either coming from the 10 of a >10 answer,
# or a 1 from a 0+1. Tested both those cases and my code catches it, which means
# it's just an optimization problem. I bet deque[i] is an o(n) function.
# elf position is relative, which means I can bring in my dll code from good old marbles

# ...and switch to 64-bit Python because I needed to go beyond 2 gigs of memory to solve it.
# not by much, but I was a good 6m iterations short

from collections import deque

class Node:
    """A singly-linked list node. Starts in a loop with itself."""

    def __init__(self, value):
        self.value = value
        self.right = self
    
    def insert_right(self, value):
        new = Node(value)
        
        righter = self.right
        new.right = righter
        self.right = new

start = Node(3)
start.insert_right(7)
board = start.right
board_size = 2

# going to keep the end of the queue in a separate deque for faster serialization
# rather than needing to slice up the entire queue time after time
last = deque([3, 7])

# test data
target = 704321
target_len = 6

# not values but pointers at the board
elves = [board.right, board]

def test_done():
    # trim it down
    while len(last) > target_len:
        last.popleft()
    
    # and now, see if we're done
    last_score = sum([last[i]*(10**(target_len-(i+1))) for i in range(len(last))])

    if(last_score == target):
        return True
    
    return False

def add_score(score):
    global board, board_size
    board.insert_right(score)
    board = board.right
    board_size += 1
    last.append(score)

def combine():
    raw_score = elves[0].value + elves[1].value

    if raw_score > 9:
        add_score(1)
        if test_done():
            return
    
    add_score(raw_score%10)

def advance():
    for i in range(2):
        elf = elves[i]
        advance = 1 + elf.value

        for j in range(advance):
            elf = elf.right
        
        elves[i] = elf

def print_state():
    state = []
    iter = start
    esc = True
    while esc:
        if(elves[0] is iter):
            state.append("({})".format(iter.value))
        elif(elves[1] is iter):
            state.append("[{}]".format(iter.value))
        else:
            state.append(" {} ".format(iter.value))

        iter = iter.right
        esc = iter is not start

    print("".join(state))


# and now let's actually run it!

for j in range(30000000):
    if j % 100000 == 0:
        print(j)

    combine()
    advance()
    # print_state()

    if test_done():
        print("Found result! " + str(board_size - target_len))
        break

