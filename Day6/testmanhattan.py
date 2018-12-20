# declare us some constants so we can run test data
offset = 0 # 200 for prod data
ysize = 10 # 800 for prod data

#Utils:
def pid(x, y):
    return x + ysize*y

def pair(id):
    x = id % ysize
    y = int(id / ysize)

    return(x, y)

def manhattan(source_id, dest_id):
    source = pair(source_id)
    dest = pair(dest_id)

    x_dist = abs(source[0] - dest[0])
    print("X distances: {} to {} was {}".format(source[0], dest[0], x_dist))

    y_dist = abs(source[1] - dest[1])
    print("Y distances: {} to {} was {}".format(source[1], dest[1], y_dist))

    return x_dist + y_dist

def test(source_id, dest_id, expect):
    print("distance between {} and {} expected {} was {}".format(source_id, dest_id, expect, manhattan(source_id, dest_id)))

#some identity tests
test(0, 0, 0)
test(10, 10, 0)
test(11, 11, 0)
test(1, 1, 0)

# one column difference
test(12, 15, 3)
test(21, 51, 3)

# two column difference
test(12, 23, 2)