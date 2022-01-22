from hashlib import md5
import sys


def main():
    if len(sys.argv) != 2:
        sys.exit("Please provide a file name for input data")

    door_id = None

    filename = sys.argv[1]
    with open(filename, "r") as inputfile:
        while True:
            line = inputfile.readline()
            if not line:
                break
            tmp = line.strip()
            # print(f"{tmp}")
            door_id = tmp

    # print(f"Door ID is {door_id}")
    password_digits = []
    index = 0
    while len(password_digits) < 8:
        m = md5()
        m.update(bytes(f"{door_id}{index}", 'utf-8'))
        try_hash = m.digest()
        if try_hash[0] == 0x00 and try_hash[1] == 0x00 and try_hash[2] < 0x10:
            password_digits.append(f"{try_hash[2]:x}")
        index += 1
    print(f"Part A: password for Door ID {door_id} is {''.join(password_digits)}")

    password_digits = [None, None, None, None, None, None, None, None]
    index = 0
    while None in password_digits:
        m = md5()
        m.update(bytes(f"{door_id}{index}", 'utf-8'))
        try_hash = m.digest()
        if try_hash[0] == 0x00 and try_hash[1] == 0x00 and try_hash[2] < 0x08:
            pos = try_hash[2]
            value = try_hash[3] // 16
            if password_digits[pos] is None:
                password_digits[pos] = f"{value:x}"
        index += 1
    print(f"Part B: password for Door ID {door_id} is {''.join(password_digits)}")


if __name__ == '__main__':
    main()
