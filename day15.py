import sys


def main():
    if len(sys.argv) != 2:
        sys.exit("Please provide a file name for input data")

    discs = {}
    filename = sys.argv[1]
    with open(filename, "r") as inputfile:
        while True:
            line = inputfile.readline()
            if not line:
                break
            tmp = line.strip()
            # print(f"{tmp}")
            tmp = tmp.replace('#', '')
            tmp = tmp.replace('.', '')
            words = tmp.split()
            number, slots, offset = int(words[1]), int(words[3]), int(words[-1])
            print(f"disk {number}: total slots {slots}  current position {offset}")
            discs[number] = (offset, slots)

    success_time = 0
    while not drop_ball(success_time, discs):
        success_time += 1
    print(f"Part A: earliest time to get a capsule is {success_time}")

    last_disc = max(discs.keys())
    discs[last_disc + 1] = (0, 11)
    second_time = success_time
    while not drop_ball(second_time, discs):
        second_time += 1
    print(f"Part B: next time to get a capsule is {second_time}")


def drop_ball(t, discs, debug=False):
    local_time = t
    for disc in sorted(discs.keys()):
        local_time += 1
        off, slots = discs[disc]
        rotation = (local_time + off) % slots
        if debug:
            print(f"at time {local_time}, disc {disc} is in position {rotation}")
        if rotation != 0:
            return False
        else:
            if debug:
                print(f"Ball passes through disc {disc}")
    return True


if __name__ == '__main__':
    main()
