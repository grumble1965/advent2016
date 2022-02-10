import sys
import time
from datetime import timedelta, datetime


def main():
    if len(sys.argv) != 2:
        sys.exit("Please provide a file name for input data")

    total_elves = None
    filename = sys.argv[1]
    with open(filename, "r") as inputfile:
        while True:
            line = inputfile.readline()
            if not line:
                break
            tmp = line.strip()
            # print(f"{tmp}")
            total_elves = int(tmp)

    winner = old_game_rules(total_elves)
    print(f"Part A: winner is {winner}")

    winner = new_game_rules(total_elves)
    print(f"Part B: winner is {winner}")


def old_game_rules(total_elves):
    elves = [ee for ee in range(1, total_elves + 1)]

    while len(elves) > 1:
        new = [elves[idx] for idx in range(0, len(elves), 2)]
        if len(elves) % 2 == 1:
            del new[0]
        # print(f"{elves} becomes {new}")
        elves = new

    return elves[0]


def new_game_rules(total_elves, debug=False):
    elves = [ee for ee in range(1, total_elves + 1)]

    time_start = time.monotonic()
    while len(elves) > 1:
        if debug and len(elves) % 10000 == 0:
            time_now = time.monotonic()
            rate = 10000 / (time_now - time_start)
            est_sec = rate * (len(elves)/10000)
            delta = timedelta(seconds=est_sec)
            est_time = datetime.now() + delta
            print(f"remaining elves: {len(elves)}  Estimate {est_time.ctime()} complete.")
            time_start = time.monotonic()
        mid_idx = len(elves) // 2
        # print(f"{elves[0]} steals from {elves[mid_idx]}")
        # new = elves[1:mid_idx] + elves[mid_idx+1:]
        # new.append(elves[0])
        #elves.pop(mid_idx)
        del elves[mid_idx]
        tmp = elves[0]
        del elves[0]
        elves.append(tmp)
    return elves[0]


if __name__ == '__main__':
    main()
