from collections import defaultdict
import time
import re

def parse_min (line):
    "Does the thing"
    timestamp = time.strptime(line[1:17], "%Y-%m-%d %H:%M")
    min = timestamp.minute
    if (timestamp.hour == 23):
        min = 0
    
    return min

with open("sortedinput.txt", "r") as input:

    # example snippet:
    #[1518-03-05 23:58] Guard #1543 begins shift
    #[1518-03-06 00:14] falls asleep
    #[1518-03-06 00:16] wakes up
    #[1518-03-06 00:43] falls asleep
    #[1518-03-06 00:50] wakes up

    #...thank goodness Python dates just handle dates in the 1500s.
    #... also what watcher was writing timestamps in parsable formats in the 1500s?

    # We're gonna be silly and just get the sleepiest guard here

    data = input.readlines()

days = list()

start = 0
for i in range(len(data)):
    line = data[i].strip()

    if line.endswith("shift") and start != i:
        #Everything from start to here (noninclusive) is a shift!
        days.append(data[start:i])
        start = i

#Lucky me, I don't actually care about the date itself
#just how much time each guard spends asleep during the magic hour
#and some quick grepping shows that nobody falls asleep before midnight
#and nothing happens after 1AM

guards = defaultdict(set)

for day in days:
    idline = day[0]
    guardnum = int(re.search(r"\d+", idline[18:]))

    for i, evt in enumerate(day, 1):
        last_event_min = parse_min(day[i-1])
        event_min = parse_min(evt)
        