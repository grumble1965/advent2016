import sys


def main():
    if len(sys.argv) != 2:
        sys.exit("Please provide a file name for input data")

    lines = []
    filename = sys.argv[1]
    with open(filename, "r") as inputfile:
        while True:
            line = inputfile.readline()
            if not line:
                break
            tmp = line.strip()
            #print(f"{tmp}")
            lines.append(tmp)

    for ll in lines:
        print(f"Part A: Uncompressed length = {uncompressed_length_1(ll)}")
        print(f"Part B: Uncompressed length = {uncompressed_length_2(ll)}")


def uncompressed_length_1(ss):
    def calc_len(ss, length):
        left_paren = ss.find('(')
        if left_paren == 0:
            rparen = ss.find(')')
            marker = ss[1:rparen]
            m_words = marker.split('x')
            n_char, n_repeat = int(m_words[0]), int(m_words[1])
            repeat_str = ss[rparen + 1: rparen + n_char + 1]
            return calc_len(ss[rparen + n_char + 1:], length + (n_char*n_repeat))
        elif left_paren > 0:
            return calc_len(ss[left_paren:], length + left_paren)
        else:
            return len(ss) + length
    return calc_len(ss, 0)


def uncompressed_length_2(ss):
    def calc_len(ss, length):
        left_paren = ss.find('(')
        if left_paren == 0:
            rparen = ss.find(')')
            marker = ss[1:rparen]
            m_words = marker.split('x')
            n_char, n_repeat = int(m_words[0]), int(m_words[1])
            repeat_str = ss[rparen + 1: rparen + n_char + 1]
            return calc_len(ss[rparen + n_char + 1:], length + (uncompressed_length_2(repeat_str) * n_repeat))
        elif left_paren > 0:
            return calc_len(ss[left_paren:], length + left_paren)
        else:
            return len(ss) + length
    return calc_len(ss, 0)


if __name__ == '__main__':
    main()
