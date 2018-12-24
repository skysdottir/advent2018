# Woo, queues
# Sadly, not actually a genetic algorithm, there's no fitness function

from collections import deque

board = deque([3, 7])

# not values but indexes into the board
elves = [0, 1]

def combine():
    raw_score = board[elves[0]] + board[elves[1]]

    if raw_score > 9:
        board.append(1)
    
    board.append(raw_score%10)

def advance():
    for i in range(2):
        elf = elves[i]
        elves[i] = (elf + 1 + board[elf])%len(board)

def print_state():
    state = []
    for i, score in enumerate(board):
        state.append("({})".format(score) if i == elves[0] else "[{}]".format(score) if i == elves[1] else " {} ".format(score))
    print("".join(state))

# and now let's actually run it!
prediction = 704321

while(len(board) < prediction + 11):
    combine()
    advance()
    # print_state()

# and now just print the last ten
print("".join([str(i) for i in list(board)[prediction:prediction+10]]))