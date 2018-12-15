file = open("input.txt", "r")

changes = []

for line in file:
    changes.append(int(line))

states = set()

now = 0
i = 0

while (now not in states):
    states.add(now)
    now += changes[i]
    i += 1
    if (i >= len(changes)):
        i = 0

print(now)
file.close