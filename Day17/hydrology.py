# Wait, I got a coat in 1018? *checks previous days*
# All right, back to x/y grids and things moving upon them
# This day looks significantly easier than day 15 so I'm going to make the same dumb assumption:
# I can get away with just making changes on the map proper rather than trying to track
# exactly where each unit of water is.
# This is just a search with an interesting pattern - from start, down if possible,
# left and right until a barrier is reached or down is possible again,
# and call it a closed row and back up if barriers are on both sides
# some quick grepping suggests that x coords vary from >200 to <600
# and y coords go from 0 to <1650
# So we're going to use good old loc = (x-min_x)+row_size*y
# and simulate from (min_x, 0) to (max_x, max_y) (with an extra 1 on each side for overflow)
from collections import deque
import re

with open("input.txt", "r") as raw_scan:
    # sample scan line: x=495, y=2..7
    line_re = re.compile(r"(.)=([0-9]*), (.)=([0-9]*)..([0-9]*)")
    scan = []
    min_x = 500
    max_x = 500
    max_y = 0
    min_y = 99999 # we're going to simulate from y=0, of course, but we only score from min_y to max_y.

    for line in raw_scan:
        scan_line = line_re.match(line)
        # print("Scanned and reconstructed: {}={}, {}={}..{}".format(scan.group(1), scan.group(2), scan.group(3), scan.group(4), scan.group(5)))

        if scan_line.group(1) == "x":
            # vertical line!
            x = int(scan_line.group(2))
            top = int(scan_line.group(4))
            base = int(scan_line.group(5))

            if x < min_x: min_x = x
            if x > max_x: max_x = x
            if base > max_y: max_y = base
            if top < min_y: min_y = top
            
            # saving these as raw coords because I don't yet know the ID space
            scan.append(((x, top), (x, base)))
        else:
            # horizontal line!
            y = int(scan_line.group(2))
            left_edge = int(scan_line.group(4))
            right_edge = int(scan_line.group(5))

            if y < min_y: min_y = y
            if y > max_y: max_y = y
            if left_edge < min_x: min_x = left_edge
            if right_edge > max_x: max_x = right_edge

            scan.append(((left_edge, y), (right_edge, y)))
    
    # and pad the sides
    min_x -= 2
    max_x += 2
    x_size = (max_x - min_x + 1)
    y_size = max_y + 1
    max_id = (x_size * (y_size)) - 1

# and now we make us some globals!
board = ["."] * (x_size * (y_size))

# important terminology update: a single-digit board index is a loc, not an id
def loc(x, y):
    return (x - min_x)+(x_size*y)

def coord(here):
    y = here/x_size
    x = (here % x_size) + min_x
    return (x, y)

def connect(start_coord, end_coord):
    # I'm sure there's a clever way to do this with a double comprehension
    if start_coord[0] == end_coord[0]:
        return [(start_coord[0], i) for i in range(start_coord[1], end_coord[1]+1)]
    else:
        return [(i, start_coord[1]) for i in range(start_coord[0], end_coord[0]+1)]

# prep the board!
for scanline in scan:
    for cell in connect(*scanline):
        board[loc(*cell)] = "#"

board[loc(500, 0)] = "+"

# this will be more useful for tests than the thousand-line prod data
def print_board():
    with open("output.txt", "w") as output:
        for y in range(0, y_size):
            output.write("".join([board[loc(x, y)] for x in range(min_x, max_x+1)]) + "\n")

# and some debugging. Looks good!
# print("x: ({}..{}), y: ({}..{})".format(min_x, max_x, 0, max_y))
# print_board()

# All right! Let's set ourselves up for a search.

descent_blockers = {"#", "~"} # Descent stops and we move into lateral motion instead
descent_consumers = {"|"} # We've hit running water, this stream joins that one
descent_accepters = {"."}
lateral_blockers = {"#", "|", "~"} # sideways running has hit something, check for settling
settling_blockers = {"#"} # settled pool walls must be clay

# the search state, initialized to the spring
open_cells = deque([loc(500, 0)])

def below(here):
    return here + x_size

def above(here):
    return here - x_size

# no helical world here - if we go off the edge, complain
def left(here):
    if coord(here)[0] == min_x:
        raise RuntimeError("Attempting to simulate into negative space from " + str(here))
    return here-1

def right(here):
    if coord(here)[0] == max_x:
        raise RuntimeError("Attempting to simulate off right edge from " + str(here))
    return here+1

def iter_test_settling(here, dir, reopen):
        if board[below(here)] not in descent_blockers:
            # there's a drain, insta-fail
            return False

        if board[above(here)] == "|":
            # another entry point to reopen, if this is a valid settle
            reopen.append(above(here))

        if board[here] in settling_blockers:
            # we've found clay! This end is good.
            return True
        
        if board[here] in descent_accepters:
            # we've found empty air. This isn't good.
            return False

        next = here + dir
        if next == min_x or next == max_x:
            # little bit hacky, but we padded the sides so they'll both drain
            return False
        
        # So far, so good - check the next space!
        return iter_test_settling(next, dir, reopen)

def iter_settle(here, dir):
    if board[here] not in {"|", "~"}:
        return
    
    board[here] = "~"
    iter_settle(here+dir, dir)

def test_settling(here):
    # To settle, we need to be in a closed basin, "#" below
    # And it'll re-open all "|"s above the surface
    reopen = []
    if iter_test_settling(here, 1, reopen) and iter_test_settling(here, -1, reopen):
        open_cells.extend(reopen)
        iter_settle(here, 1)
        iter_settle(here, -1)

def flow(here):
    global wet_count
    down = below(here)
    if down > max_id or board[down] in descent_consumers:
        # bottom of the map or we're joining an existing flow.
        # do nothing, no need to explore further
        return
    elif board[down] in descent_accepters:
        board[down] = "|"
        open_cells.append(down)
    elif board[down] in descent_blockers:
        if board[left(here)] in lateral_blockers and board[right(here)] in lateral_blockers:
            test_settling(here)
        
        if board[left(here)] in descent_accepters:
            board[left(here)] = "|"
            open_cells.append(left(here))
        
        if board[right(here)] in descent_accepters:
            board[right(here)] = "|"
            open_cells.append(right(here))
    else:
        raise RuntimeError("I have no idea what to do with \"{}\" at {}".format(board[down], down))

while len(open_cells) > 0:
    flow(open_cells.popleft())

# and a final test to solve part 1
print_board()
count = len([i for i in board if i in {"~"}])
print("Part 1 answer: " + str(count))