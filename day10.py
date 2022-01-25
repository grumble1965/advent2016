import sys

inits, bots, outs = [], {}, {}

def main():
    if len(sys.argv) != 2:
        sys.exit("Please provide a file name for input data")

    global inits, bots, outs

    filename = sys.argv[1]
    with open(filename, "r") as inputfile:
        while True:
            line = inputfile.readline()
            if not line:
                break
            tmp = line.strip()
            #print(f"{tmp}")
            words = line.split()
            if words[0] == 'value':
                inits.append((int(words[5]), int(words[1])))
            elif words[0] == 'bot':
                bot_num = int(words[1])
                low_dest, low_num = words[5], int(words[6])
                high_dest, high_num = words[10], int(words[11])
                bots[bot_num] = {'chips': [], 'low_dest': low_dest, 'low_num': low_num,
                                 'high_dest': high_dest, 'high_num': high_num}
            else:
                print(f"Unknown input {tmp}")

    changes = False

    # initialization
    for bot, value in inits:
        store_chip('bot', bot, value)
        changes = True

    # step
    while changes:
        changes = False
        bots_to_execute = [bot for bot, prog in bots.items() if len(prog['chips']) == 2]
        for bot in bots_to_execute:
            low = min(bots[bot]['chips'])
            high = max(bots[bot]['chips'])
            if low == 17 and high == 61:
                print(f"Part A: bot {bot} compared 17 and 71")

            bots[bot]['chips'] = []
            store_chip(bots[bot]['low_dest'], bots[bot]['low_num'], low)
            store_chip(bots[bot]['high_dest'], bots[bot]['high_num'], high)
            changes = True
    print(f"Part B: product is {outs[0] * outs[1] * outs[2]}")


def store_chip(dest_kind, dest_num, chip):
    global bots, outs
    if dest_kind == 'bot':
        bots[dest_num]['chips'].append(chip)
    elif dest_kind == 'output':
        outs[dest_num] = chip
    else:
        print(f"Unknown destination {dest_kind}")


if __name__ == '__main__':
    main()
