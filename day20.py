import sys


def main():
    if len(sys.argv) != 2:
        sys.exit("Please provide a file name for input data")

    ints = []
    filename = sys.argv[1]
    with open(filename, "r") as inputfile:
        while True:
            line = inputfile.readline()
            if not line:
                break
            tmp = line.strip()
            #print(f"{tmp}")
            words = tmp.split('-')
            lo, hi = int(words[0]), int(words[1])
            ints.append((lo, hi))

    ints.sort()
    cooked, raw = coalesce(ints.copy()), ints
    clean_ints = cooked

    lowest = clean_ints[0][1] + 1 if clean_ints[0][0] != 0 else 0
    print(f"Part A: lowest unblocked address is {lowest}")

    blocked = count_included(clean_ints)
    print(f"Part B: total blocked is {blocked} which allows {2**32 - blocked}")


def coalesce(ints):
    if not ints:
        return []
    res, ff = [], ints.pop(0)
    while ints:
        nn = ints.pop(0)
        if ff[0] <= nn[0] <= ff[1]:
            # overlapping range
            ff = ff[0], max(ff[1], nn[1])
        elif ff[1] + 1 == nn[0]:
            # adjacent range
            ff = ff[0], nn[1]
        else:
            res.append(ff)
            ff = nn
    res.append(ff)
    return res


def count_included(ints):
    total = 0
    for ii in ints:
        lo, hi = ii
        total += (hi - lo + 1)
    return total


if __name__ == '__main__':
    main()
