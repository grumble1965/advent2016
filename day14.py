import sys
import hashlib


md5_cache = {}
stretched_md5_cache = {}


def main():
    if len(sys.argv) != 2:
        sys.exit("Please provide a file name for input data")

    salt = None
    filename = sys.argv[1]
    with open(filename, "r") as inputfile:
        while True:
            line = inputfile.readline()
            if not line:
                break
            tmp = line.strip()
            #print(f"{tmp}")
            salt = tmp

    # test0 = make_pad('abc', 0)
    # print(test0)
    # test1 = make_stretched_pad('abc', 0)
    # print(test1)
    # exit()

    final_pad = 64
    idx = find_index(salt, final_pad, make_pad)
    print(f"Part A: index {idx} produces key {final_pad}")

    final_pad = 64
    idx = find_index(salt, final_pad, make_stretched_pad)
    print(f"Part B: index {idx} produces key {final_pad}")


def find_index(salt, final_pad, pad_function):
    idx = 0
    for pad_counter in range(final_pad):
        while True:
            new_pad = pad_function(salt, idx)
            if not valid_pad(new_pad, salt, idx, pad_function):
                idx += 1
            else:
                # print(f"Pad # {pad_counter} with index # {idx}")
                idx += 1
                break
    return idx-1


def make_pad(salt, idx):
    global md5_cache
    hash_string = salt + str(idx)
    if hash_string in md5_cache:
        return md5_cache[hash_string]
    else:
        result = hashlib.md5(hash_string.encode()).hexdigest()
        md5_cache[hash_string] = result
        return result


def make_stretched_pad(salt, idx):
    global stretched_md5_cache
    hash_string = salt + str(idx)
    if hash_string in stretched_md5_cache:
        return stretched_md5_cache[hash_string]
    else:
        result = hashlib.md5(hash_string.encode()).hexdigest()
        for i in range(2016):
            result = hashlib.md5(result.encode()).hexdigest()
        stretched_md5_cache[hash_string] = result
        return result


def valid_pad(pad, salt, idx, pad_function):
    triple = find_triple(pad)
    if triple is None:
        return False
    for offset in range(1, 1001):
        new_pad = pad_function(salt, idx + offset)
        if has_quint(new_pad, triple):
            return True
    return False


def find_triple(pad):
    tts = [pad[idx] for idx in range(len(pad)-2) if pad[idx] == pad[idx+1] and pad[idx] == pad[idx+2]]
    if tts:
        return tts[0]
    else:
        return None


def has_quint(pad, target):
    return target*5 in pad


if __name__ == '__main__':
    main()
