def get_lines():
    with open("day4_input.txt") as f:
        for line in f:
            yield [
                list(map(int, i.split("-")))
                for i
                in line.strip().split(",")
            ]


def part_one():
    c = 0
    for line in get_lines():
        start, stop = line[0]
        s1 = set(range(start, stop + 1))
        start, stop = line[1]
        s2 = set(range(start, stop + 1))
        intersection = s1 & s2
        if intersection == s1 or intersection == s2:
            c += 1
    return c


def part_two():
    c = 0
    for line in get_lines():
        start, stop = line[0]
        s1 = set(range(start, stop + 1))
        start, stop = line[1]
        s2 = set(range(start, stop + 1))
        intersection = s1 & s2
        if len(intersection) > 0:
            c += 1
    return c


def main():
    # print(part_one())
    print(part_two())


if __name__ == '__main__':
    main()