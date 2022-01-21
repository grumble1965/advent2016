import sys


def main():
    if len(sys.argv) != 2:
        sys.exit("Please provide a file name for input data")

    triangles = []

    filename = sys.argv[1]
    with open(filename, "r") as inputfile:
        while True:
            line = inputfile.readline()
            if not line:
                break
            tmp = line.strip()
            # print(f"{tmp}")
            triangles.append([int(ss) for ss in tmp.split()])

    total, possible = 0, 0
    for tt in triangles:
        total += 1
        if possible_triangle(tt):
            possible += 1
    print(f"Part A: Of {total} triangles, {possible} are possible")

    total, possible = 0, 0
    for idx in range(0, len(triangles), 3):
        for jdx in range(3):
            tt = [triangles[idx][jdx], triangles[idx + 1][jdx], triangles[idx + 2][jdx]]
            total += 1
            if possible_triangle(tt):
                possible += 1
    print(f"Part B: Of {total} triangles, {possible} are possible")


def possible_triangle(tt):
    st = sorted(tt)
    s1, s2, s3 = st[0], st[1], st[2]
    return s1 + s2 > s3


if __name__ == '__main__':
    main()
