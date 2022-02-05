import sys
import numpy as np
import itertools
import queue

favorite_number = None


def main():
    global favorite_number
    if len(sys.argv) != 2:
        sys.exit("Please provide a file name for input data")

    favorite_number = None
    filename = sys.argv[1]
    with open(filename, "r") as inputfile:
        while True:
            line = inputfile.readline()
            if not line:
                break
            tmp = line.strip()
            #print(f"{tmp}")
            favorite_number = int(tmp)

    steps = dijkstra_solution((1, 1), (31, 39), "Part A")
    print(f"Part A: shorted path is {steps} steps")

    max_steps = 50
    locs = bfs_solution((1, 1), max_steps)
    print(f"Part B: in {max_steps} steps we can reach {locs} locations")


def dijkstra_solution(initial_state, goal_state, tag, debug=False):
    q = queue.PriorityQueue()
    q.put((0, initial_state))

    best_steps = None
    seen = {}
    ctr = 0
    while not q.empty():
        steps, here = q.get()

        if ctr % 10000 == 0 and debug:
            print(f"{tag}: Ctr = {ctr}, Q has {q.qsize()}, Seen has {len(seen)}")
        ctr += 1

        if best_steps is not None and steps > best_steps:
            if debug:
                print(f"Skipping this state: steps = {steps} but best_steps = {best_steps}")
            continue

        if here == goal_state:
            if debug:
                print(f"{tag}: found a solution with {steps} steps")
            if best_steps is None or steps < best_steps:
                best_steps = steps
            continue

        if here in seen:
            if debug:
                print(f"Skipping this state: already seen")
            if seen[here] < steps:
                seen[here] = steps
            continue

        seen[here] = steps

        for v in get_neighbors(here):
            if valid_state(v):
                new_pri = steps + 1
                q.put((steps + 1, v))

    return best_steps


def bfs_solution(initial_state, max_steps):
    q = queue.SimpleQueue()
    q.put((initial_state, max_steps))

    seen = set()
    while not q.empty():
        here, steps = q.get()

        if here in seen:
            continue

        seen.add(here)

        if steps > 0:
            for v in get_neighbors(here):
                if valid_state(v):
                    q.put((v, steps-1))

    return len(seen)


def get_neighbors(tt):
    x, y = tt[0], tt[1]
    return [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]


def valid_state(tt):
    x, y = tt[0], tt[1]
    return x >= 0 and y >= 0 and fill_cubicles(x, y) == '.'


def fill_cubicles(x, y):
    global favorite_number
    # print(x, y, end='')
    f = (x * x) + (3 * x) + (2 * x * y) + y + (y * y)
    f += favorite_number
    bit_list = [(f >> shift) & 1 for shift in range(32)]
    sbl = sum(bit_list)
    if sbl % 2 == 0:
        return '.'
    else:
        return '#'


if __name__ == '__main__':
    main()
