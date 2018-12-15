from collections import Counter

def dig (id):
    "Digests an id string into a map of frequencies per letter"
    dig = Counter()

    for char in id:
        dig[char] += 1
    
    return dig

def has3 (digest):
    "Checks if an item has a triple character repeat"

    for pair in digest.items():
        if pair[1] == 3:
            return True
    
    return False

def has2 (digest):
    "Checks if an item has a triple character repeat"

    for pair in digest.items():
        if pair[1] == 2:
            return True
    
    return False

file = open("input.txt", "r")

twos = 0
threes = 0

for line in file:
    d = dig(line)
    if has2(d):
        twos += 1
    if has3(d):
        threes += 1

print("twos: " + str(twos))
print("threes: " + str(threes))
print("checksum: " + str(twos * threes))
file.close