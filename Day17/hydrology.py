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
import re

with open("testinput.txt", "r") as raw_scan:
    # sample scan line: x=495, y=2..7
    line_re = re.compile(r"(.)=([0-9]*), (.)=([0-9]*)..([0-9]*)")
    scan = []
    min_x = 500
    max_x = 500
    max_y = 0
    # min_y is going to be 0, that's ground level

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
            
            # saving these as raw coords because I don't yet know the ID space
            scan.append(((x, top), (x, base)))
        else:
            # horizontal line!
            y = int(scan_line.group(2))
            left = int(scan_line.group(4))
            right = int(scan_line.group(5))

            if y > max_y: max_y = y
            if left < min_x: min_x = left
            if right > max_x: max_x = right

            scan.append(((left, y), (right, y)))
    
    # and pad the sides
    min_x -= 1
    max_x += 1
    x_size = max_x - min_x
    y_size = max_y + 1

# and now we make us some globals!
board = ["."] * (x_size * (y_size+1))

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
    for y in range(0, y_size):
        print("".join([board[loc(x, y)] for x in range(min_x, max_x+1)]))

# and some debugging. Looks good!
print("x: ({}..{}), y: ({}..{})".format(min_x, max_x, 0, max_y))
print_board()