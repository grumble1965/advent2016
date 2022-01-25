import numpy as np
import sys


def main():
    if len(sys.argv) != 2:
        sys.exit("Please provide a file name for input data")

    program = []
    filename = sys.argv[1]
    with open(filename, "r") as inputfile:
        while True:
            line = inputfile.readline()
            if not line:
                break
            tmp = line.strip()
            #print(f"{tmp}")
            words = tmp.split()
            command, arg1, arg2 = None, None, None
            if words[0] == 'rect':
                command = 'rect'
                args = words[1].split('x')
                arg1, arg2 = int(args[0]), int(args[1])
            elif words[0] == 'rotate' and words[1] == 'row':
                command = 'rotate_row'
                arg1 = int(words[2].split('=')[1])
                arg2 = int(words[4])
            elif words[0] == 'rotate' and words[1] == 'column':
                command = 'rotate_column'
                arg1 = int(words[2].split('=')[1])
                arg2 = int(words[4])
            else:
                print(f"Unknown input {words}")
            program.append((command, arg1, arg2))

    screen_shape = (6, 50)
    screen = np.zeros(screen_shape, dtype=np.str_)
    screen.fill('.')
    for command, arg1, arg2 in program:
        if command == 'rect':
            for c in range(0, arg1):
                for r in range(0, arg2):
                    screen[r, c] = '#'
        elif command == 'rotate_column':
            column = screen[:, arg1]
            for counter in range(arg2):
                nc = np.zeros_like(column)
                nc[0] = column[-1]
                nc[1:] = column[:-1]
                column = nc
            screen[:, arg1] = column
        elif command == 'rotate_row':
            row = screen[arg1, :]
            for counter in range(arg2):
                nr = np.zeros_like(row)
                nr[0] = row[-1]
                nr[1:] = row[:-1]
                row = nr
            screen[arg1, :] = row
        else:
            print(f"Unknown command {command}")
    # print(screen)
    lit = 0
    for xx in np.nditer(screen):
        if xx == '#':
            lit += 1
    print(f"Part A: {lit} pixels are lit")

    print(f"Part B:")
    for r in range(screen.shape[0]):
        line = ''.join(screen[r, :]).replace('.', ' ')
        print(f"{''.join(line)}")


if __name__ == '__main__':
    main()
