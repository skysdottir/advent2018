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

ops = [addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr]

def test_ops(i, reg, end_reg):
    matches = [op for op in ops if op(i, reg) == end_reg]
    print("Matches: " + str(matches))
    return len(matches)

# shamelessly borrowed from StackOverflow
def block_iter(l, n):
    """Yields successive n-length blocks from l."""
    for i in range(0, len(l), n):
        yield l[i:i+n]

def parse_short(line):
    return [int(s) for s in line.split(" ")]

def parse_long(line):
    return [int(s) for s in line[9:-1].split(", ")]

# and the test code for part 1
# downloaded input_607.txt from the reddit: https://www.reddit.com/r/adventofcode/comments/a9rlgw/day_16_part_1_can_someone_validate_this_for_me/
# Because I'm getting way too low of answers - 90 for mine and 161 for this one (should have been 607!)
# ...am I misreading the question? I bet I'm misreading the question.
#... I'm misreading the question. "three _or more_", not "three"
def part_1(): 

    with open("input.txt", "r") as in_file:
        in_lines = in_file.readlines()
        threes_count = 0
        sample_count = 0

        for sample in block_iter(in_lines, 4):
            sample_count += 1
            print("Testing :" + str(sample))
            if 3 <= test_ops(parse_short(sample[1].strip()), parse_long(sample[0].strip()), parse_long(sample[2].strip())):
                threes_count += 1
    print(threes_count)
    print("{} lines cut into {} samples".format(len(in_lines), sample_count))

# and solve part 1
# part_1()

# Gotta track which op is which, and I'm not doing indexes -> names by hand.
ops_and_names = [("addr", addr), ("addi", addi), ("mulr", mulr), \
        ("muli", muli), ("banr", banr), ("bani", bani), ("borr", borr), \
        ("bori", bori), ("setr", setr), ("seti", seti), ("gtir", gtir), \
        ("gtri", gtri), ("gtrr", gtrr), ("eqir", eqir), ("eqri", eqri), ("eqrr", eqrr)]

def possible_ops_for(i, reg, end_reg):
    return {op[0] for op in ops_and_names if op[1](i, reg) == end_reg}

def find_opcodes():
    with open("input.txt", "r") as in_file:
        in_lines = in_file.readlines()
        opcode_possible_map = dict()

        for sample in block_iter(in_lines, 4):
            start_reg = parse_long(sample[0].strip())
            instr = parse_short(sample[1].strip())
            opcode = instr[0]
            end_reg = parse_long(sample[2].strip())
            
            sample_opcodes = possible_ops_for(instr, start_reg, end_reg)

            try:
                opcode_possible_map[opcode] = opcode_possible_map[opcode] & sample_opcodes
            except:
                opcode_possible_map[opcode] = sample_opcodes

    print("All possibilities: {}".format(opcode_possible_map))

    # and round two - I'm just going to solve this sucker mechanically and brute-force.

    certain_opcodes = []

    for i in range(15):
        single_options = [(k, v.pop()) for k, v in opcode_possible_map.items() if len(v) == 1]
        for code in single_options:
            del opcode_possible_map[code[0]]
            certain_opcodes.append(code)
            for k, v in opcode_possible_map.items():
                if code[1] in v: v.remove(code[1])
    
    print(certain_opcodes)

# and get opcodes -> names for part 2
# find_opcodes()
# All that to discover:
# [(12, 'eqir'), (14, 'gtrr'), (4, 'gtri'), (7, 'eqri'), (9, 'eqrr'), (15, 'gtir'), 
# (0, 'bani'), (11, 'setr'), (5, 'banr'), (8, 'seti'), (1, 'addr'), (2, 'mulr'), 
# (13, 'muli'), (3, 'addi'), (10, 'bori'), (6, 'borr')]

# and now lets actually solve this thing
opcodes = {12: eqir, 14: gtrr, 4: gtri, 7: eqri, 9: eqrr, 15: gtir, \
        0: bani, 11: setr, 5: banr, 8: seti, 1: addr, 2: mulr,  \
        13: muli, 3: addi, 10: bori, 6: borr}

def run_program():
    with open("testprogram.txt", "r") as program:
        reg = [0, 0, 0, 0]

        for line in program:
            line = line.strip()
            if len(line) == 0:
                continue
            
            instr = parse_short(line)
            reg = opcodes[instr[0]](instr, reg)
        
        print(reg)

run_program()