# Okay, going to try this one the dumb way first, assuming paths don't cross (and thus there are no loops)
# and thus the given route to any given room is the shortest one.
# This may bite me in the ass, but it's true for all examples given.
# This means the map is really a tree
# In which there are nodes (strings of moves), and children (parenthetically, |-divided)
# This gets weird with the empty-option option, in which each child route reverses itself
# But, some quick regexing across the input file finds that all empty-option nodes have no options
# inside them. Which means they're effectively leaf nodes with len (len/2) because they all reverse
# themselves.
# Second thing that could have screwed us up - a regex fragment like N(E|W)N
# in which (E|W) create branches that both can then continue N. None of those exist.
# All close-paren groups are either preceeded by or followed by a |
# Which means they're either leaves or closing a child to step up to a parent's options (or both)

max_dist = 0
dist_stack = []
dir_stack = []
op = {"N": "S", "S": "N", "E": "W", "W": "E"}

# part 2 variable!
count = 0

with open("input.txt", "r") as infile:
    map_re = infile.readline()

for char in map_re:
    if char in ("^", "$"):
        # file ends, do nothing
        continue
    if char in {"N", "E", "W", "S"}:
        if (len(dir_stack) > 0) and (dir_stack[-1] == op[char]): 
            dir_stack.pop()
        else: 
            dir_stack.append(char)
            dist = len(dir_stack)
            if dist >= 1000: count += 1
            if dist > max_dist: max_dist = dist
    if char == "(":
        dist_stack.append(len(dir_stack))
    if char == "|":
        # We already saved max_dist last time
        # so just back up a level
        dir_stack = dir_stack[:dist_stack[-1]]
    if char == ")":
        dir_stack = dir_stack[:dist_stack.pop()]

    # test code
    #debug_str.append(char)
    #print("Seen: {} dirs: {} dists: {}".format("".join(debug_str), "".join(dir_stack), dist_stack))

print("Max dist was: " + str(max_dist))
print("And I found {} rooms more than 1k doors away".format(count))

# Okay, looking around on the internets, it looks like my assumption for part 1, that it's all a tree
# doesn't work for part 2.