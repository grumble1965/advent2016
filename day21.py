import sys


def main():
    if len(sys.argv) != 2:
        sys.exit("Please provide a file name for input data")

    steps = []
    filename = sys.argv[1]
    with open(filename, "r") as inputfile:
        while True:
            line = inputfile.readline()
            if not line:
                break
            tmp = line.strip()
            # print(f"{tmp}")
            words = tmp.split()
            inst = None
            if words[0] == 'swap' and words[1] == 'position':
                inst = ['swap_position', int(words[2]), int(words[5])]
            elif words[0] == 'swap' and words[1] == 'letter':
                inst = ['swap_letter', words[2], words[5]]
            elif words[0] == 'rotate' and words[1] in ['left', 'right']:
                inst = [f"{words[0]}{words[1]}", int(words[2])]
            elif words[0] == 'rotate' and words[1] == 'based':
                inst = ['rotate', words[6]]
            elif words[0] == 'reverse':
                inst = ['reverse', int(words[2]), int(words[4])]
            elif words[0] == 'move':
                inst = ['move', int(words[2]), int(words[5])]
            else:
                print(f"Invalid instruction {tmp}")

            steps.append(inst)

    # start = 'abcde'
    # res = run_steps(steps, start, debug=False)
    # print(f"Part A: Scrambling {start} yields {res}")
    #
    # start = res
    # res = run_backwards(steps, start, debug=True)
    # print(f"Part B: Unscrambling {start} yields {res}")
    # start2 = run_steps(steps, res)
    # print(f"Part B: Scrambling {res} yields {start2}")

    start = 'abcdefgh'
    res = run_steps(steps, start)
    print(f"Part A: Scrambling {start} yields {res}\n")

    start = 'fbgdceah'
    res = run_backwards(steps, start)
    print(f"Part B: Unscrambling {start} yields {res}")
    start2 = run_steps(steps, res)
    print(f"Part B: Scrambling {res} yields {start2}")


def run_steps(steps, input_string, debug=False):
    ii = input_string
    for step in steps:
        oo = None
        if step[0] == 'swap_position':
            oo = ii
            l1 = min(step[1], step[2])
            l2 = max(step[1], step[2])
            oo = ii[:l1] + ii[l2] + ii[l1+1:l2] + ii[l1] + ii[l2+1:]
        elif step[0] == 'swap_letter':
            oo = ii
            l1 = min(ii.index(step[1]), ii.index(step[2]))
            l2 = max(ii.index(step[1]), ii.index(step[2]))
            oo = ii[:l1] + ii[l2] + ii[l1+1:l2] + ii[l1] + ii[l2+1:]
        elif step[0] == 'rotateleft':
            oo = rotate_left(ii, step[1])
        elif step[0] == 'rotateright':
            oo = rotate_right(ii, step[1])
        elif step[0] == 'rotate':
            oo = rotate_letter(ii, step[1])
        elif step[0] == 'reverse':
            oo = reverse_substring(ii, step[1], step[2])
        elif step[0] == 'move':
            src = step[1]
            dst = step[2]
            oo = ii[:src] + ii[src+1:]
            oo = oo[:dst] + ii[src] + oo[dst:]
        else:
            print("Bad instruction {step}")
        if debug:
            print(f"{ii} -> {oo} {step}")
        ii = oo
    return ii


def rotate_left(ii, steps):
    oo = ii
    for ctr in range(steps):
        oo = oo[1:] + oo[:1]
    return oo


def rotate_right(oo, steps):
    for ctr in range(steps):
        oo = oo[-1] + oo[:-1]
    return oo


def rotate_letter(ii, letter):
    oo = ii
    l1 = ii.index(letter)
    tr = 1 + l1
    tr += 1 if l1 >= 4 else 0
    for ctr in range(tr):
        oo = oo[-1] + oo[:-1]
    return oo


def reverse_substring(ii, src, dst):
    left, middle, right = ii[:src], ii[src:dst+1], ii[dst+1:]
    oo = left + middle[::-1] + right
    return oo


def run_backwards(steps, input_string, debug=False):
    steps.reverse()
    ii = input_string
    for step in steps:
        oo = None
        if step[0] == 'swap_position':
            l1 = min(step[1], step[2])
            l2 = max(step[1], step[2])
            oo = ii[:l1] + ii[l2] + ii[l1+1:l2] + ii[l1] + ii[l2+1:]
        elif step[0] == 'swap_letter':
            l1 = min(ii.index(step[1]), ii.index(step[2]))
            l2 = max(ii.index(step[1]), ii.index(step[2]))
            oo = ii[:l1] + ii[l2] + ii[l1+1:l2] + ii[l1] + ii[l2+1:]
        elif step[0] == 'rotateleft':
            oo = rotate_right(ii, step[1])
        elif step[0] == 'rotateright':
            oo = rotate_left(ii, step[1])
        elif step[0] == 'rotate':
            ll = step[1]
            tries = [rotate_left(ii, ss) for ss in range(len(ii))]
            tmp = [tt for tt in tries if rotate_letter(tt, ll) == ii]
            outcomes = set(tmp)
            if len(outcomes) == 0 or len(outcomes) > 1:
                print(f"Oops: {outcomes}")
            oo = outcomes.pop()
        elif step[0] == 'reverse':
            oo = reverse_substring(ii, step[1], step[2])
        elif step[0] == 'move':
            src = step[2]
            dst = step[1]
            oo = ii[:src] + ii[src+1:]
            oo = oo[:dst] + ii[src] + oo[dst:]
        else:
            print("Bad instruction {step}")
        if debug:
            print(f"{ii} -> {oo} {step}")
        ii = oo
    return ii


if __name__ == '__main__':
    main()
