from collections import defaultdict
import time
import re

# Don't mind me, just bringing a lot of stuff across from sleepiestguard

def parse_min (line):
    "Does the thing"
    timestamp = time.strptime(line[1:17], "%Y-%m-%d %H:%M")
    min = timestamp.tm_min
    if (timestamp.tm_hour == 23):
        min = 0
    
    # print("Parsed " + str(line) + " to minute " + str(min))

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

    for i in range(1, len(day)):
        print("line: " + day[i])
        last_event_min = parse_min(day[i-1])
        event_min = parse_min(day[i])

        print("last_event_min: " + str(last_event_min))
        print("event_min: " + str(event_min))

        if day[i].endswith("asleep\n"):
            # means the guard fell asleep, and thus was awake. Add these minutes to awakeness
            print("Guard was awake for: " + str(event_min - last_event_min))
            guards[guardnum][0] = (event_min - last_event_min)
        else:
            print("Guard was asleep for: " + str(event_min - last_event_min))
            guards[guardnum][1] = (event_min - last_event_min)
    
# and now we've got a map of guardnum -> [minutes awake, minutes asleep]

sleepy = dict()

for id, times in guards.items():
    # print("id: " + str(id))
    # print("times: " + str(times))

    if times[0] + times[1] > 0:
        sleepy[times[0]/(times[0]+times[1])] = id

for k in sorted(sleepy):
    print("Guard: " + str(sleepy[k]) + " slept for: " + str(k))