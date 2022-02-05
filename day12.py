import sys


def main():
    if len(sys.argv) != 2:
        sys.exit("Please provide a file name for input data")

    program = []
    filename = sys.argv[1]
    with open(filename, "r") as inputfile:
        while True:
            line = inputfile.readline()
            if not line:
                break
            tmp = line.strip()
            #print(f"{tmp}")
            words = tmp.split()
            if words[0] == 'cpy' or words[0] == 'jnz':
                if words[1].isdigit():
                    words[1] = int(words[1])
            if words[0] == 'jnz':
                words[2] = int(words[2])
            program.append(words)

    # a, b, c, d = python_program()
    # print(f"Part A: a reg value is {a}")
    #
    # a, b, c, d = python_program(c=1)
    # print(f"Part B: a reg value is {a}")

    regs = {'a': 0, 'b': 0, 'c': 0, 'd': 0}
    new_regs = run_cpu(program, regs)
    print(f"Part A: a reg value is {new_regs['a']}")

    regs = {'a': 0, 'b': 0, 'c': 1, 'd': 0}
    new_regs = run_cpu(program, regs)
    print(f"Part B: a reg value is {new_regs['a']}")


def run_cpu(program, regs, pc=0, debug=False):
    cycles = 0
    while 0 <= pc < len(program):
        inst = program[pc]
        if debug and cycles % 1000000 == 0:
            print(cycles, pc, regs, inst)
        cycles += 1

        if inst[0] == 'cpy':
            src, dest = get_value(inst[1], regs), inst[2]
            regs[dest] = src
            pc += 1
        elif inst[0] == 'inc':
            dest = inst[1]
            regs[dest] += 1
            pc += 1
        elif inst[0] == 'dec':
            dest = inst[1]
            regs[dest] -= 1
            pc += 1
        elif inst[0] == 'jnz':
            test, offset = get_value(inst[1], regs), inst[2]
            if not (test == 0):
                pc += offset
            else:
                pc += 1
        else:
            print(f"PC = {pc}: Unknown opcode {inst[0]}")
    return regs


def get_value(src, regs):
    if isinstance(src, str) and src in regs:
        return regs[src]
    else:
        return src


#
# so...  I had a bug in the code for 'cpy' (+= instead of =)
# so I implemented the raw bunnyasm in C++, including the gotos,
# then refactored it into something Python can run.  That helped
# me locate the first bug.
#
def python_program(a=0, b=0, c=0, d=0):
    a = 1
    b = 1
    d = 26
    if c != 0:
        d = 33
        c = 0
    loop = True
    while loop:
        c = a
        a += b
        b = c
        d -= 1
        loop = (d != 0)
    a += 198
    return a, b, c, d


if __name__ == '__main__':
    main()
