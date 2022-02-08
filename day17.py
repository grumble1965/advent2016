import hashlib
import heapq
from itertools import count
import queue
import sys


def main():
    if len(sys.argv) != 2:
        sys.exit("Please provide a file name for input data")

    passcodes = []
    filename = sys.argv[1]
    with open(filename, "r") as inputfile:
        while True:
            line = inputfile.readline()
            if not line:
                break
            tmp = line.strip()
            # print(f"{tmp}")
            passcodes.append(tmp)

    for pc in passcodes:
        path1 = dijkstra_algorithm(pc, "Part A", shortest=True)
        print(f"Part A: for passcode {pc}, the shortest path is {path1}")
        path2 = dijkstra_algorithm(pc, "Part B", shortest=False)
        print(f"Part B: for passcode {pc}, the longest path has length {len(path2)}")


def dijkstra_algorithm(passcode, tag, debug=False, shortest=True):
    q = queue.PriorityQueue()
    # queue entry is priority, path_so_far
    q.put((0, ''))

    best_steps = None
    best_path = None
    seen = {}
    ctr = 0
    while not q.empty():
        pri, path = q.get()

        if ctr % 10000 == 0 and debug:
            print(f"{tag}: Ctr = {ctr}, Q has {q.qsize()}, Seen has {len(seen)}")
        ctr += 1

        steps = len(path)
        if shortest and best_steps is not None and steps > best_steps:
            if debug:
                print(f"Skipping this state: steps = {steps} but best_steps = {best_steps}")
            continue

        if end_state(path):
            if debug:
                print(f"{tag}: found a solution with {steps} steps")
            if shortest and (best_steps is None or steps < best_steps):
                best_steps = steps
                best_path = path
            elif not shortest and (best_steps is None or steps > best_steps):
                best_steps = steps
                best_path = path
            # for hh in history:
            #     print(hh)
            continue

        # hs = make_hashable(state)
        if path in seen:
            if debug:
                print(f"Skipping this state: already seen")
            if seen[path] < steps:
                seen[path] = steps
            continue

        seen[path] = steps

        r, c, directions = get_valid_neighbors(passcode, path)
        for d in directions:
            new_path = path + d
            q.put((len(new_path), new_path))

        # current_floor = [fl_idx + 1 for fl_idx in [0, 1, 2, 3] if 'E' in state[fl_idx]][0]
        # floors = [current_floor + dx for dx in [-1, +1] if current_floor + dx in [1, 2, 3, 4]]
        # stuff = [ss for ss in state[current_floor - 1] if ss != 'E']
        # stuff_iter = chain.from_iterable([combinations(stuff, 1), combinations(stuff, 2)])
        # for new_floor, stuff_to_move in product(floors, stuff_iter):
        #     new_state = copy.deepcopy(state)
        #     # move the elevator to the new floor
        #     new_state[current_floor - 1].remove('E')
        #     new_state[new_floor - 1].append('E')
        #     # move the stuff to the new floor
        #     for item in stuff_to_move:
        #         new_state[current_floor - 1].remove(item)
        #         new_state[new_floor - 1].append(item)
        #
        #     if valid_state(new_state):
        #         new_pri = steps + 1
        #         q.put((new_pri, steps + 1, new_state))

    return best_path


def end_state(path):
    row = 1 + path.count('D') - path.count('U')
    col = 1 + path.count('R') - path.count('L')
    return row == 4 and col == 4


pq = []
entry_finder = {}
REMOVED = '<removed-task>'
counter = count()


def add_task(task, priority=0):
    global pq, entry_finder, counter
    if task in entry_finder:
        remove_task(task)
    entry = [priority, (next(counter)), task]
    entry_finder[task] = entry
    heapq.heappush(pq, entry)


def remove_task(task):
    global entry_finder, REMOVED
    entry = entry_finder.pop(task)
    entry[-1] = REMOVED


def pop_task():
    global pq, entry_finder, REMOVED
    while pq:
        _, _, task = heapq.heappop(pq)
        if task is not REMOVED:
            del entry_finder[task]
            return task
    raise KeyError('pop from empty priority queue')


def find_shortest_path(passcode):
    path = 'DUR'
    col, row, valid = get_valid_neighbors(passcode, path)
    print(f"neighbors of {passcode}+{path} location({row},{col}): {valid}")


def get_valid_neighbors(passcode, path):
    def ok(ch):
        return ch in 'bcdef'
    hash_string = passcode + path
    vv = hashlib.md5(hash_string.encode()).hexdigest()[:4]
    unlocked = {}
    for idx in range(len(vv)):
        unlocked['UDLR'[idx]] = ok(vv[idx])
    row = 1 + path.count('D') - path.count('U')
    col = 1 + path.count('R') - path.count('L')
    if row == 1:
        del unlocked['U']
    elif row == 4:
        del unlocked['D']
    if col == 1:
        del unlocked['L']
    elif col == 4:
        del unlocked['R']
    valid = [k for k, v in unlocked.items() if v]
    return col, row, valid


if __name__ == '__main__':
    main()
