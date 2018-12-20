import string

#Design approach: The problem looks a lot like a context-free grammar
# In which each symbol has an antisymbol that it must be next to to remove.
# "abba" reduces "bb" first and then "aa"
# While "abab" doesn't have any reducable pairs
# This is manageable with a stack, popping every time we find a reducable pair.
# And the result is just the length of the ending stack, which is fine by me!

#ingestion
with open("input.txt", "r") as input:
    rawdata = input.readline()
    data = list(rawdata)

# the reducing operation:
def isPair(first, second):
    isFirstCap = first in string.ascii_uppercase
    isSecondCap = second in string.ascii_uppercase
    pair = (first.lower() == second.lower()) and isFirstCap is not isSecondCap

    #print(first + " " + second + (" are " if pair else " are not ") + "a pair")

    return pair

def reduce(polymer):
    stack = []

    for char in polymer:
        if len(stack) > 0:
            last = stack[-1]
            if isPair(char, last):
                stack.pop(-1)
            else:
                stack.append(char)
        else:
            stack.append(char)
        #print("Stack: " + str(stack))

    return stack

# And the actual logic
def remove(polymer, target):
    tgt_lower = target.lower()
    tgt_upper = target.upper()

    return [i for i in polymer if (i != tgt_lower and i != tgt_upper)]

for char in string.ascii_lowercase:
    print("Without pair " + char + " : " + str(len(reduce(remove(data, char)))))