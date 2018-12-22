# okay, this is going to be a fascinating recursive problem...

from collections import deque

with open("input.txt", "r") as input:
    data = input.readline().split()
    queue = deque([int(x) for x in data])

print("data length: " + str(len(data)))
meta_sum = 0

# define a recursive function...
def ingest_node(queue):
    global meta_sum
    # magic happens here

    child_count = queue.popleft()
    metadata_count = queue.popleft()

    children = [ingest_node(queue) for i in range(child_count)]
    metadata = [queue.popleft() for i in range(metadata_count)]

    # solving part 1
    meta_sum += sum(metadata)

    # debug!
    # print("Node metadata: {}".format(metadata))

    # and pass back the node
    return (children, metadata)

#And now call the unbound recursive monstrosity. This'll be great!
root = ingest_node(queue)

print("Done with part 1! meta_sum = " + str(meta_sum))

# part two, recursive traversal with different rules

def score(node):
    # node here is a tuple, ([children], [metadata])

    # end condition: leaf node, just return the sum of the metadata entries
    if len(node[0]) == 0:
        return sum(node[1])
    
    # otherwise, sum the scores of each existing child node specified in the metadata
    child_count = len(node[0])
    return sum([score(node[0][child-1]) for child in node[1] if child > 0 and child <= child_count])

print("Done with part 2! Score = {}".format(score(root)))