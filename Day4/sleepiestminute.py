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

guards = defaultdict(lambda :[])
guard_ids = set()

def addtime (guardnum, startmin, endmin, asleep) :
    for min in range(startmin, endmin):
        guards[str(guardnum) + ":" + str(min)].append(asleep)


for day in days:
    idline = day[0]
    guardnum = int(re.search(r"\d+", idline[18:]).group())
    guard_ids.add(guardnum)

    print("\nNew day: " + idline[0:len(idline) - 1])
    last_event_min = 0
    event_min = 0
    is_asleep = False

    for i in range(1, len(day)):
        print("line: " + day[i][0:len(day[i]) - 1])
        last_event_min = parse_min(day[i-1])
        event_min = parse_min(day[i])

        print("last_event_min: " + str(last_event_min))
        print("event_min: " + str(event_min))

        if day[i].endswith("asleep\n"):
            # means the guard fell asleep, and thus was awake. Add these minutes to awakeness
            print("Guard was awake for: " + str(event_min - last_event_min))
            addtime(guardnum, last_event_min, event_min, False)
            is_asleep = True
        else:
            print("Guard was asleep for: " + str(event_min - last_event_min))
            addtime(guardnum, last_event_min, event_min, True)
            is_asleep = False

    # And closing off until 1 AM
    print("End of day")
    print("Last event was at: " + str(event_min))
    print("Guard was " + ("asleep" if is_asleep else "awake") + " for: " + str(60 - event_min)) 
    addtime (guardnum, event_min, 60, is_asleep)
    
# and now we've got a map of guardnum:minute -> [awake, awake, asleep]
# Where asleep is TRUE
# Let's find the sleepiest guard/minute combo

# This'll hold [guard ID, minute, sleeprate]
sleepiest_guard = [0, 0, 0]

for guardnum in guard_ids:
    for min in range(0, 60):
        mins_asleep = 0
        mins_awake = 0
        guardmin = guards[str(guardnum) + ":" + str(min)]
        # This'll be a list of [awake, awake, asleep] for a single guard for a single minute
        # where asleep is TRUE

        for instance in guardmin:
            if (instance):
                mins_asleep += 1
            else:
                mins_awake += 1

        sleeprate = mins_asleep

        print("Guard " + str(guardnum) + " on min " + str(min) + " slept for " + str(sleeprate))

        if (sleeprate > sleepiest_guard[2]):
            sleepiest_guard[0] = guardnum
            sleepiest_guard[1] = min
            sleepiest_guard[2] = sleeprate

print("I believe the sleepiest guard to be " + str(sleepiest_guard[0]) +
         " who slept for " + str(sleepiest_guard[2]) +
         " of minute " + str(sleepiest_guard[1]))

print("Solution: " + str(sleepiest_guard[0] * sleepiest_guard[1]))