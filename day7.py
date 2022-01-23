import sys


def main():
    if len(sys.argv) != 2:
        sys.exit("Please provide a file name for input data")

    ip_addrs = []
    filename = sys.argv[1]
    with open(filename, "r") as inputfile:
        while True:
            line = inputfile.readline()
            if not line:
                break
            tmp = line.strip()
            # print(f"{tmp}")
            ip_addrs.append(tmp)

    supports_tls = 0
    for ip in ip_addrs:
        nonhyper, hyper = parse_ip(ip)
        # print(f"{ip} = {nonhyper} + {hyper}")
        if any(map(lambda x: find_abba(x) is not None, nonhyper)) \
                and not any(map(lambda x: find_abba(x) is not None, hyper)):
            supports_tls += 1
    print(f"Part A: {supports_tls} ip address support TLS")

    supports_ssl = 0
    for ip in ip_addrs:
        nonhyper, hyper = parse_ip(ip)
        found_aba_bab = False
        for nh in nonhyper:
            for aba in find_aba(nh):
                bab = aba[1]+aba[0]+aba[1]
                if any(map(lambda x: bab in x, hyper)):
                    found_aba_bab = True
                    break
            if found_aba_bab:
                supports_ssl += 1
                break
    print(f"Part B: {supports_ssl} ip address support SSL")



def find_abba(s):
    abba = None
    for idx in range(len(s) - 3):
        if s[idx] == s[idx + 3] and s[idx + 1] == s[idx + 2] and s[idx] != s[idx + 1]:
            abba = s[idx: idx + 4]
            break
    return abba


def find_aba(s):
    aba_list = []
    for idx in range(len(s) - 2):
        if s[idx] == s[idx + 2] and s[idx] != s[idx + 1]:
            aba_list.append(s[idx: idx + 3])
    return aba_list


def parse_ip(s):
    non_hyper = []
    hyper = []
    st = 0
    while True:
        lb = s.find('[', st)
        if lb == -1:
            break
        non_hyper.append(s[st: lb])
        rb = s.find(']', st + 1)
        hyper.append(s[lb + 1: rb])
        st = rb + 1
    non_hyper.append(s[st:])
    return non_hyper, hyper


if __name__ == '__main__':
    main()
