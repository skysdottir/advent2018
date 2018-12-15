from collections import defaultdict
import time
import re

def parse_min (line):
    "Does the thing"
    timestamp = time.strptime(line[1:17], "%Y-%m-%d %H:%M")
    min = timestamp.tm_min
    if (timestamp.tm_hour == 23):
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

guards = defaultdict(lambda :[0,0])

for day in days:
    idline = day[0]
    guardnum = int(re.search(r"\d+", idline[18:]).group())

    for i, evt in enumerate(day, 1):
        last_event_min = parse_min(day[i-1])
        event_min = parse_min(evt)

        if evt.endswith("asleep"):
            # means the guard fell asleep, and thus was awake. Add these minutes to awakeness
            guards[guardnum][0] += (event_min - last_event_min)
        else:
            guards[guardnum][1] += (event_min - last_event_min)
    
# and now we've got a map of guardnum -> [minutes awake, minutes asleep]

print(len(guards))

sleepy = dict()

for id, times in guards.items():
    if times[0] + times[1] > 0:
        sleepy[times[0]/(times[0]+times[1])] = id

print("first: " + str(sorted(sleepy)[0]))
print("last: " + str(sorted(sleepy)[len(sleepy)-1]))