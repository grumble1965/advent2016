import sys


def main():
    if len(sys.argv) != 2:
        sys.exit("Please provide a file name for input data")

    seq = []
    filename = sys.argv[1]
    with open(filename, "r") as inputfile:
        while True:
            line = inputfile.readline()
            if not line:
                break
            tmp = line.strip()
            # print(f"{tmp}")
            seq = tmp.replace(',', '').split()

    # print(seq)
    compass = ['N', 'E', 'S', 'W']

    loc_x, loc_y = 0, 0
    facing = 'N'
    for step in seq:
        turn = step[0:1]
        dist = int(step[1:])

        new_facing = None
        if turn == 'R':
            new_facing = compass[(compass.index(facing) + 1) % 4]
        elif turn == 'L':
            new_facing = compass[(compass.index(facing) - 1) % 4]
        else:
            print(f"Invalid turning {turn}")

        if new_facing is not None:
            if new_facing == 'N':
                loc_y += dist
            elif new_facing == 'E':
                loc_x += dist
            elif new_facing == 'S':
                loc_y -= dist
            elif new_facing == 'W':
                loc_x -= dist
            facing = new_facing

        # print(f"Facing {facing} at location ({loc_x},{loc_y})")
    distance = abs(loc_x) + abs(loc_y)
    print(f"Part A: Final location ({loc_x},{loc_y}) and distance {distance}")

    visits = set()
    loc_x, loc_y = 0, 0
    visits.add((loc_x, loc_y))
    facing = 'N'
    duplicate = None
    for step in seq:
        turn = step[0:1]
        dist = int(step[1:])

        new_facing = None
        if turn == 'R':
            new_facing = compass[(compass.index(facing) + 1) % 4]
        elif turn == 'L':
            new_facing = compass[(compass.index(facing) - 1) % 4]
        else:
            print(f"Invalid turning {turn}")

        path = None
        if new_facing is not None:
            if new_facing == 'N':
                path = [(loc_x, y) for y in range(loc_y + 1, loc_y + dist + 1)]
                loc_y += dist
            elif new_facing == 'E':
                path = [(x, loc_y) for x in range(loc_x + 1, loc_x + dist + 1)]
                loc_x += dist
            elif new_facing == 'S':
                path = [(loc_x, y) for y in range(loc_y - 1, loc_y - dist - 1, -1)]
                loc_y -= dist
            elif new_facing == 'W':
                path = [(x, loc_y) for x in range(loc_x - 1, loc_x - dist - 1, -1)]
                loc_x -= dist
            facing = new_facing

        # print(path)
        for pp in path:
            if pp in visits:
                duplicate = pp
                break
            else:
                visits.add(pp)
        if duplicate is not None:
            break

    distance = abs(duplicate[0]) + abs(duplicate[1])
    print(f"Part B: First location visited twice is {duplicate} at distance {distance}")


if __name__ == '__main__':
    main()
