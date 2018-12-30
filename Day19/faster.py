bignum = 10551432
sum = 0

for i in range(1, bignum+1):
    if bignum % i == 0:
        sum += i

print("And done. Sum = " + str(sum))