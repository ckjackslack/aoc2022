from functools import reduce
from string import ascii_letters

PRIORITIES = {
    letter: i
    for i, letter
    in enumerate(ascii_letters, start=1)
}


def get_lines_for_part_one():
    with open("day3_input.txt") as f:
        for line in f:
            yield line.strip()


def get_lines_for_part_two():
    i = 0
    with open("day3_input.txt") as f:
        group = []
        for line in f:
            if i == 3:
                yield group
                group = []
                i = 0
            group.append(line.strip())
            i += 1
        if group:
            yield group


# only works for part one
def get_item_type_1(line):
    midpoint = len(line) // 2
    comp1, comp2 = set(line[:midpoint]), set(line[midpoint:])
    return next(iter(comp1 & comp2))


# more generic
def get_item_type_2(line, parts=2):
    midpoint = len(line) // parts
    groups = [
        set(
            line[i*midpoint:i*midpoint+midpoint]
        )
        for i
        in range(parts)
    ]
    return next(iter(reduce(set.__and__, groups)))


# only works for part two
def get_item_type_3(group):
    return next(iter(reduce(set.__and__, map(set, group))))


def part_one(get_item_type):
    return sum(
        PRIORITIES.get(get_item_type(line))
        for line
        in get_lines_for_part_one()
    )


def part_two(get_item_type):
    total = 0
    for group in get_lines_for_part_two():
        item_type = get_item_type(group)
        total += PRIORITIES.get(item_type)
    return total


def main():
    print(part_one(get_item_type_1))
    print(part_two(get_item_type_3))


if __name__ == "__main__":
    main()