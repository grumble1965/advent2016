import heapq
import io
import sys
import copy
import queue
from itertools import chain, combinations, product, count
import cProfile, pstats


def main():
    if len(sys.argv) != 2:
        sys.exit("Please provide a file name for input data")

    config = {}
    rename = {'microchip': 'M', 'generator': 'G', 'hydrogen': 'H', 'lithium': 'L', 'strontium': 'S', 'plutonium': 'P',
              'thulium': 'T', 'ruthenium': 'R', 'curium': 'C'}
    filename = sys.argv[1]
    with open(filename, "r") as inputfile:
        while True:
            line = inputfile.readline()
            if not line:
                break
            tmp = line.strip()
            # print(f"{tmp}")
            words = tmp.split()
            while 'and' in words:
                words.remove('and')
            # print(words)
            fl = words[1]
            if 'nothing' in words:
                config[fl] = []
            else:
                contents = [(words[idx + 1], words[idx + 2]) for idx in range(4, len(words), 3)]
                mc = []
                for c1, c2 in contents:
                    t1 = c1.replace(',', '')
                    t2 = t1.replace('.', '')
                    nc1 = t2.replace('-compatible', '')
                    t3 = c2.replace(',', '')
                    nc2 = t3.replace('.', '')
                    if nc1 in rename:
                        mc.append(rename[nc1] + rename[nc2])
                    else:
                        print(f"Unknown element {nc1}")
                        exit()
                config[fl] = mc

    # print(config)
    initial_state = [config['first'], config['second'], config['third'], config['fourth']]
    initial_state[0].insert(0, 'E')
    # initial_state = [['E', 'HM', 'LM'], ['HG'], ['LG'], []]

    # pr = cProfile.Profile()
    # pr.enable()

    # answer_a = astar_solution(initial_state, "Part A")
    answer_a = dijkstra_solution(initial_state, "Part A")
    print(f"Part A: Best is {answer_a} steps")

    # pr.disable()
    # s = io.StringIO()
    # sortby = pstats.SortKey.CUMULATIVE
    # ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    # ps.print_stats()
    # print(s.getvalue())
    # exit()

    initial_state = [config['first'], config['second'], config['third'], config['fourth']]
    initial_state[0].extend(['YM', 'YG', 'DM', 'DG'])
    # answer_b = astar_solution(initial_state, "Part B", debug=False)
    answer_b = dijkstra_solution(initial_state, "Part B", debug=False)
    print(f"Part B: Best is {answer_b} steps")


def dijkstra_solution(initial_state, tag, debug=False):
    q = queue.PriorityQueue()
    q.put((0, 0, make_hashable(initial_state)))

    best_steps = None
    seen = {}
    ctr = 0
    while not q.empty():
        pri, steps, hs = q.get()

        if ctr % 10000 == 0 and debug:
            print(f"{tag}: Ctr = {ctr}, Q has {q.qsize()}, Seen has {len(seen)}")
        ctr += 1

        if best_steps is not None and steps > best_steps:
            if debug:
                print(f"Skipping this state: steps = {steps} but best_steps = {best_steps}")
            continue

        if end_state(hs):
            if debug:
                print(f"{tag}: found a solution with {steps} steps")
            if best_steps is None or steps < best_steps:
                best_steps = steps
            # for hh in history:
            #     print(hh)
            continue

        # hs = make_hashable(state)
        if hs in seen:
            if debug:
                print(f"Skipping this state: already seen")
            if seen[hs] < steps:
                seen[hs] = steps
            continue

        seen[hs] = steps

        for v in get_hashable_neighbors(hs):
            if valid_state(v):
                new_pri = steps + 1
                q.put((new_pri, steps + 1, v))

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

    return best_steps


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


def astar_solution(initial_state, tag, debug=False):
    infinity = 999999999
    path = {}
    seen = set()

    his = make_hashable(initial_state)
    estimate = get_estimate(initial_state)
    # f, g, h; distance, rootDistance, manhattanDistance
    dist = {his: (infinity, 0, estimate)}

    global pq, entry_finder
    pq = []
    entry_finder = {}

    add_task(his, 0)

    queue_ctr = 0
    try:
        while pq:
            tuple_state = pop_task()
            seen.add(tuple_state)
            state_d, state_rd, state_md = dist[tuple_state]

            for hv in [vv for vv in get_hashable_neighbors(tuple_state) if vv not in seen]:
                if hv not in dist:
                    estimate = get_estimate(hv)
                    # f, g, h; distance, rootDistance, manhattanDistance
                    dist[hv] = (infinity, infinity, estimate)
                v_d, v_rd, v_md = dist[hv]

                v_rd = min([v_rd, state_rd + 1])
                min_distance = min([v_d, v_rd + v_md])

                if min_distance != v_d:
                    v_d = min_distance
                    dist[hv] = (v_d, v_rd, v_md)
                    path[hv] = tuple_state
                add_task(hv, min_distance)
                queue_ctr += 1
    except KeyError:
        pass

    # pq is empty
    print(f"Queue checked {queue_ctr} items")
    d, rd, md = None, None, None
    for ss in dist:
        if end_state(ss):
            d, rd, md = dist[ss]
            print(f"{ss} {d} {rd} {md}")

    return rd


def get_hashable_neighbors(tuple_state):
    state = [(list(tuple_state[0])), (list(tuple_state[1])),
             (list(tuple_state[2])), (list(tuple_state[3]))]

    neighbors = []
    current_floor = [fl_idx + 1 for fl_idx in [0, 1, 2, 3] if 'E' in state[fl_idx]][0]
    possible_floors = [current_floor + dx for dx in [-1, +1] if current_floor + dx in [1, 2, 3, 4]]
    possible_stuff = [ss for ss in state[current_floor - 1] if ss != 'E']
    stuff_iter = chain.from_iterable([combinations(possible_stuff, 1), combinations(possible_stuff, 2)])
    for new_floor, stuff_to_move in product(possible_floors, stuff_iter):
        new_current_floor = state[current_floor - 1].copy()
        new_new_floor = state[new_floor - 1].copy()

        new_current_floor.remove('E')
        new_new_floor.append('E')
        for item in stuff_to_move:
            new_current_floor.remove(item)
            new_new_floor.append(item)
        tuple_new_current_floor = tuple(sorted(new_current_floor))
        tuple_new_new_floor = tuple(sorted(new_new_floor))

        res_list = []
        for floor in [1, 2, 3, 4]:
            if current_floor == floor:
                res_list.append(tuple_new_current_floor)
            elif new_floor == floor:
                res_list.append(tuple_new_new_floor)
            else:
                res_list.append(tuple_state[floor - 1])
        new_state = tuple(res_list)

        if valid_state(new_state):
            neighbors.append(new_state)
    return neighbors


def valid_state(state):
    # print("validating", state)
    for floor in state:
        chips_here, rtgs_here = [], []
        for item in floor:
            if item[-1] == 'M':
                chips_here.append(item)
            elif item[-1] == 'G':
                rtgs_here.append(item)
        # print(f"floor {floor} has {chips_here} and {rtg_here}")
        if rtgs_here:
            for chip in chips_here:
                matching_rtg = chip[0] + 'G'
                if matching_rtg not in rtgs_here:
                    # print(f"No RTG for {chip}!")
                    return False
    return True


def make_hashable(state):
    f1, f2, f3, f4 = state[0], state[1], state[2], state[3]
    sf1, sf2, sf3, sf4 = sorted(f1), sorted(f2), sorted(f3), sorted(f4)
    return tuple(sf1), tuple(sf2), tuple(sf3), tuple(sf4)


def end_state(state):
    f1, f2, f3, f4 = state[0], state[1], state[2], state[3]
    return len(f1) == 0 and len(f2) == 0 and len(f3) == 0


def get_estimate(state):
    f1, f2, f3, f4 = state[0], state[1], state[2], state[3]
    return 6 * len(f1) + 4 * len(f2) + 2 * len(f3)


if __name__ == '__main__':
    main()
