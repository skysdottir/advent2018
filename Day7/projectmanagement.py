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
done = []
running = []

# and stuff for task scheduling:
workers = 5
run_clock = 0
in_progress = defaultdict(lambda : []) #going to map finish time -> task IDs

print("found chars: " + str(chars))

def can_run(upstreams):
    #print("Testing list: " + str(upstreams))
    remaining = [upstream for upstream in upstreams if upstream not in done]
    #print("unsatisfied dependencies: " + str(remaining))
    return (len(remaining) == 0 and len(running) < workers)

def has_finished(char):
    return char in done

def finish_time(char):
    return run_clock + 61 + string.ascii_uppercase.find(char)

def start_task(char):
    # print("Running char " + char)
    in_progress[finish_time(char)].append(char)
    running.append(char)
    chars.remove(char)
    graph.pop(char)

def finish_task(char):
    # print("Finished char " + char)
    running.remove(char)
    done.append(char)

def tick():
    global run_clock
    print("Second {}: running: {} done: {}".format(run_clock, running, done))
    run_clock += 1

    for char in in_progress[run_clock]:
        finish_task(char)


# Let's not write an unbound loop
iter = 0
while(len(graph) > 0 and iter < 10000):
    iter += 1

    for char in chars:
        # print("checking char: " + char)
        if(can_run(graph[char])):
            start_task(char)
    
    tick()

# and now the question is just on what second the last task completes

if(len(graph) > 0):
    print("Woah! We aren't done yet!")

last = max(in_progress)
print("Final task ({}) ends at {}".format(in_progress[last], last))
