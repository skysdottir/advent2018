from collections import Counter

playercount = 477
rounds = 7085100
score = Counter()

class Node:
    """A doubly-linked list node. Starts in a loop with itself."""

    def __init__(self, value):
        self.value = value
        self.right = self
        self.left = self
    
    def insert_right(self, value):
        new = Node(value)

        righter = self.right
        new.left = self
        new.right = righter
        self.right = new
        righter.left = new
    
    def remove_left(self):
        left = self.left
        lefter = left.left

        self.left = lefter
        lefter.right = self

        return left.value

board = Node(0)
zero = board

def make_list(start_node):
    list = [start_node.value]
    traversal = start_node.right

    while traversal is not start_node:
        list.append(traversal.value)
        traversal = traversal.right
    
    return list

for round in range(1, rounds+1):
    player = (round % playercount)

    if (round % 23 == 0):
        score[player] += round

        for i in range(6):
            board = board.left

        score[player] += board.remove_left()

    else:
        board = board.right
        board.insert_right(round)
        board = board.right

    # debug
    # print("{}: {}".format(player, make_list(zero)))

    # status
    if round%100000 == 0:
        print(round)

# and highscore!

# print(score)

print("Max: {}".format(max([count[1] for count in score.items()])))