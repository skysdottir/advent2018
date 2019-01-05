# Copying the CPU itself from day 19
# each opcode gets to be its own function, f(instruction, registers) -> new_registers
# without changing registers, so we can just spin through them all
# The instruction will be complete, including the opcode in [0] which will just be ignored.

import re

# because there's an awful lot of repetition of copy and return
def lambda_op(instructions, registers, result_lambda):
    reg = registers.copy()
    reg[instructions[3]] = result_lambda(instructions, registers)
    # print("lambda_op {}, {}, {} -> {}".format(instructions, registers, result_lambda, reg))
    return reg

# addition
def addr(i, reg): return lambda_op(i, reg, lambda i, reg: reg[i[1]] + reg[i[2]])

def addi(i, reg): return lambda_op(i, reg, lambda i, reg: reg[i[1]] + i[2])

# multiplication
def mulr(i, reg): return lambda_op(i, reg, lambda i, reg: reg[i[1]] * reg[i[2]])

def muli(i, reg): return lambda_op(i, reg, lambda i, reg: reg[i[1]] * i[2])

# binary and
def banr(i, reg): return lambda_op(i, reg, lambda i, reg: reg[i[1]] & reg[i[2]])

def bani(i, reg): return lambda_op(i, reg, lambda i, reg: reg[i[1]] & i[2])

# binary or
def borr(i, reg): return lambda_op(i, reg, lambda i, reg: reg[i[1]] | reg[i[2]])

def bori(i, reg): return lambda_op(i, reg, lambda i, reg: reg[i[1]] | i[2])

# set ops
def setr(i, reg): return lambda_op(i, reg, lambda i, reg: reg[i[1]])

def seti(i, reg): return lambda_op(i, reg, lambda i, reg: i[1])

# comparison ops
def gtir(i, reg): return lambda_op(i, reg, lambda i, reg: 1 if i[1] > reg[i[2]] else 0)

def gtri(i, reg): return lambda_op(i, reg, lambda i, reg: 1 if reg[i[1]] > i[2] else 0)

def gtrr(i, reg): return lambda_op(i, reg, lambda i, reg: 1 if reg[i[1]] > reg[i[2]] else 0)

# equality ops
def eqir(i, reg): return lambda_op(i, reg, lambda i, reg: 1 if i[1] == reg[i[2]] else 0)

def eqri(i, reg): return lambda_op(i, reg, lambda i, reg: 1 if reg[i[1]] == i[2] else 0)

def eqrr(i, reg): return lambda_op(i, reg, lambda i, reg: 1 if reg[i[1]] == reg[i[2]] else 0)

ops = {"addr": addr, "addi": addi, "mulr": mulr, \
        "muli": muli, "banr": banr, "bani": bani, "borr": borr, \
        "bori": bori, "setr": setr, "seti": seti, "gtir": gtir, \
        "gtri": gtri, "gtrr": gtrr, "eqir": eqir, "eqri": eqri, "eqrr": eqrr}

line_re = re.compile(r"^([a-z]{4}) ([0-9]*) ([0-9]*) ([0-9]*)$")

# just hard-coding this in, for now
ip_reg = 1

with open("program.txt", "r") as infile:
    pgm = []
    for line in infile:
        m = line_re.match(line)
        pgm.append([m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4))])

ip = 0
clock = 0
max_clock = 100000000
regs = [0, 0, 0, 0, 0, 0]
pgm_len = len(pgm)

while ip >= 0 and ip < pgm_len and clock < max_clock:
    # one instruction evaluation!
    throwaway = input()
    clock += 1
    regs[ip_reg] = ip
    instr = pgm[ip]
    new_regs = ops[instr[0]](instr, regs)
    new_ip = new_regs[ip_reg] + 1

    # and debug!
    print("IP+1: {} {} {} {}".format(ip+1, regs, instr, new_regs))

    ip = new_ip
    regs = new_regs

print("Program halted " + ("before" if clock < max_clock else "at") + " max clock, with registers: " + str(regs))