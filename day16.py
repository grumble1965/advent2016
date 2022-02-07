import sys


def main():
    if len(sys.argv) != 2:
        sys.exit("Please provide a file name for input data")

    filename = sys.argv[1]
    with open(filename, "r") as inputfile:
        while True:
            line = inputfile.readline()
            if not line:
                break
            tmp = line.strip()
            # print(f"{tmp}")
            words = tmp.split()
            input_data = tmp

    checksum = calculate_checksum(input_data, 272)
    print(f"Part A: final checksum is {checksum} ")

    checksum = calculate_checksum(input_data, 35651584)
    print(f"Part A: final checksum is {checksum} ")


def calculate_checksum(input_data, length):
    data = input_data
    while len(data) < length:
        data = dragon_curve(data)
    # print(f"Padded data is now {len(data)} {data}")
    data = data[:length]
    # print(f"Data is truncated to {len(data)} {data}")
    checksum = get_sum(data)
    while len(checksum) % 2 == 0:
        # print(f"checksum is now {len(checksum)} {checksum}")
        checksum = get_sum(checksum)
    # print(f"Final Checksum is {len(checksum)} {checksum}")
    return checksum


def dragon_curve(in_str):
    res = in_str + "0" + ''.join(['0' if ch == '1' else '1' for ch in (reversed(in_str))])
    return res


def get_sum(in_str):
    def get_bit(a, b):
        return '1' if a == b else '0'
    out_str = ''
    for idx in range(0, len(in_str), 2):
        out_str += get_bit(in_str[idx], in_str[idx+1])
    return out_str


if __name__ == '__main__':
    main()
