import time

input = open("input.txt", "r")

lines = dict()

for line in input:
    stamp = time.strptime(line[1:17], "%Y-%m-%d %H:%M")
    lines[stamp]=line

input.close()

sort = sorted(lines)

sorted = open("sortedinput.txt", "w")

for time in sort:
    sorted.write(lines[time])

sorted.close()