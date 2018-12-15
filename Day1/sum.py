file = open("input.txt", "r")
i = 0
for line in file:
    i += int(line)

print(i)
file.close