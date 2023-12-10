from itertools import zip_longest


def get_lines(filename):
    with open(filename) as f:
        i = 0
        pair = []
        for line in f:
            line = line.strip()
            if i == 2:
                yield pair
                pair = []
                i = 0
            else:
                pair.append(eval(line))
                i += 1


def main():
    filename = "day13_example.txt"
    for pair in get_lines(filename):
        f, s = pair
        print(f, s)

# https://adventofcode.com/2022/day/13

# [[4, 4], 4, 4]
# 0a
# 01v
# 02v
# 1v
# 2v

# [[1, 4, [5, [3], 5], 3], 4, 5]
# 0a
# 00v
# 01v
# 02a
# 020v
# 021a
# 0210v
# 022v
# 03v
# 1v
# 2v

if __name__ == '__main__':
    main()