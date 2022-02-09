import sys


def main():
    if len(sys.argv) != 2:
        sys.exit("Please provide a file name for input data")

    rows = []
    filename = sys.argv[1]
    with open(filename, "r") as inputfile:
        while True:
            line = inputfile.readline()
            if not line:
                break
            tmp = line.strip()
            # print(f"{tmp}")
            tmp_row = [ch == '^' for ch in tmp]
            rows.append(tmp_row)

    ts = count_safes(rows[0], 40)
    print(f"Part A: After {40} rows, there are {ts} safe tiles")

    ts = count_safes(rows[0], 400000)
    print(f"Part B: After {400000} rows, there are {ts} safe tiles")


def count_safes(seed, total_rows, debug = False):
    if debug:
        print("".join(['^' if trap else '.' for trap in seed]))
    total_safe = seed.count(False)
    this = seed
    for cnt in range(total_rows - 1):
        new_row = []
        for idx in range(len(this)):
            left = this[idx-1] if idx > 0 else False
            center = this[idx]
            right = this[idx+1] if idx < len(this)-1 else False

            square = None
            if left and center and not right:
                square = True
            elif center and right and not left:
                square = True
            elif left and not center and not right:
                square = True
            elif right and not center and not left:
                square = True
            else:
                square = False
            new_row.append(square)
        if debug:
            print("".join(['^' if trap else '.' for trap in new_row]))
        total_safe += new_row.count(False)
        this = new_row
    return total_safe


if __name__ == '__main__':
    main()
