import collections
from operator import itemgetter
import sys


def main():
    if len(sys.argv) != 2:
        sys.exit("Please provide a file name for input data")

    rooms = []

    filename = sys.argv[1]
    with open(filename, "r") as inputfile:
        while True:
            line = inputfile.readline()
            if not line:
                break
            tmp = line.strip()
            # print(f"{tmp}")
            rooms.append(tmp)

    valid_rooms = []
    for rr in rooms:
        name, sector_id, checksum = parse_room_line(rr)
        if valid_checksum(checksum, name):
            valid_rooms.append((name, sector_id))
    sums = sum([sid for _, sid in valid_rooms])
    print(f"Part A: sum of valid checksums is {sums}")

    letters = 'abcdefghijklmnopqrstuvwxyz'
    for cipher_name, sector_id in valid_rooms:
        clear_name = "".join([letters[(letters.find(c) + sector_id) % 26] for c in cipher_name])
        if 'north' in clear_name:
            print(f"Part B: {clear_name} in {sector_id}")


def valid_checksum(checksum, name):
    c = collections.Counter([ch for ch in name if ch.isalpha()])
    foo = c.most_common()
    foo.sort(key=itemgetter(0))
    foo.sort(key=itemgetter(1), reverse=True)
    calc = "".join([ch for (ch, _) in foo])[:5]
    return calc == checksum


def parse_room_line(rr):
    l_bracket = rr.index('[')
    checksum = rr[l_bracket + 1: -1]
    last_hyphen = rr.rfind('-')
    sector_id = int(rr[last_hyphen + 1: l_bracket])
    name = rr[:last_hyphen]
    return name, sector_id, checksum


if __name__ == '__main__':
    main()
