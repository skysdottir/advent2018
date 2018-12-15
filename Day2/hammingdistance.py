from collections import defaultdict

def hamming(left, right):
    "Computes the hamming distance between two strings"
    assert len(left) == len(right)
    return sum(c1 != c2 for c1, c2 in zip(left, right))

def test(candidate, previous):
    "Tests to see if the candidate string has a hamming distance of 1 from any of the previously-seen strings in this set"
    for seen in previous:
        if (hamming(candidate, seen) == 1):
            print(candidate)
            print(seen)

file = open("input.txt", "r")
ref = defaultdict(set)

for line in file:
    first = line[0:12]
    last = line[12:]

    if(first in ref):
        test(line, ref[first])
    
    ref[first].add(line)

    if(last in ref):
        test(line, ref[last])
    
    ref[last].add(line)

file.close