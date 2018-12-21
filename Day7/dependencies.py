# First, we build the dependency graph
# This is (or had better be) a DAG.
# We're going to call the ends of a dependency connection "upstream" and "downstream"
# Continuing with the theme of brute force, we're going to store these in a dict
# "C" -> ["D", "E", "P"] for upstream dependencies D, E, and P
# Because the connection we're going to want to ask (over and over) is
# "Are all the dependencies satisfied for task X?"

from collections import defaultdict
import string
import re

raw_chars = set()
graph = defaultdict(lambda : [])
line_regex = re.compile("^Step (.) must be finished before step (.) can begin.$")

with open("input.txt", "r") as input:
    for line in input:
        match = line_regex.match(line)
        upstream = match.group(1)
        downstream = match.group(2)
        
        raw_chars.add(upstream)
        raw_chars.add(downstream)
        graph[downstream].append(upstream)

print(graph)
# And now, to resolve the dependencies.

chars = sorted(raw_chars)
order = []

print("found chars: " + str(chars))

def can_run(upstreams):
    print("Testing list: " + str(upstreams))
    remaining = [upstream for upstream in upstreams if upstream not in order]
    print("unsatisfied dependencies: " + str(remaining))
    return len(remaining) == 0

def has_run(char):
    return char in order

def run(char):
    print("Running char " + char)
    order.append(char)
    chars.remove(char)
    graph.pop(char)

    for node in graph:
        l = graph[node]

        if char in l:
            l.remove(char)


# Let's not write an unbound loop
iter = 0
while(len(graph) > 0 and iter < 100):
    iter += 1

    for char in chars:
        print("checking char: " + char)
        if(can_run(graph[char])):
            run(char)
            break

print("".join(order))