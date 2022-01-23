from collections import Counter
import sys


def main():
    if len(sys.argv) != 2:
        sys.exit("Please provide a file name for input data")

    messages = []
    filename = sys.argv[1]
    with open(filename, "r") as inputfile:
        while True:
            line = inputfile.readline()
            if not line:
                break
            tmp = line.strip()
            # print(f"{tmp}")
            messages.append(tmp)

    counters = [Counter() for ch in messages[0]]
    for mm in messages:
        for idx in range(len(mm)):
            counters[idx].update(mm[idx])
    most_common = [cc.most_common(1)[0][0] for cc in counters]
    print(f"Part A: Most common message is {''.join(most_common)}")

    least_common = [cc.most_common()[-1][0] for cc in counters]
    print(f"Part B: Least common message is {''.join(least_common)}")


if __name__ == '__main__':
    main()
