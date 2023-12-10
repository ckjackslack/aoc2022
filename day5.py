import math
import re
from collections import namedtuple
from itertools import islice
from pprint import pp

Move = namedtuple("Move", "n src dest")
move_pattern = r"move (\d+) from (\d+) to (\d+)"
crate_pattern = r"\[(\w)\]"
crate_offset = 4


def get_lines():
    with open("day5_input.txt") as f:
        for line in f:
            yield line.rstrip()


def get_initial_stack_repr():
    return list(islice(get_lines(), 0, 9))


def determine_bucket(match, stack_index_ranges):
    startpos = match.start()
    for idx, (beg, end) in enumerate(stack_index_ranges):
        if beg <= startpos <= end:
            return idx


def parse_columns(stack_repr):
    no_of_columns = max(map(int,
        re.split(r'\s+', stack_repr[-1].strip())))
    stack_index_ranges = [
        (i*crate_offset, i*crate_offset+crate_offset-2)
        for i
        in range(no_of_columns)
    ]
    stacks = [[] for _ in range(no_of_columns)]
    for line in stack_repr[:-1]:
        crates_in_line = list(re.finditer(crate_pattern, line))
        for crate in crates_in_line:
            idx = determine_bucket(crate, stack_index_ranges)
            stacks[idx].insert(0, crate.group(1))
    return stacks


def parse_moves():
    for line in get_lines():
        if match := re.search(move_pattern, line):
            args = [int(g) for g in match.groups()]
            # alter for indices
            args[-1] -= 1
            args[-2] -= 1
            yield Move(*args)


def part_one(stacks):
    for move in parse_moves():
        for _ in range(move.n):
            stacks[move.dest].append(stacks[move.src].pop())
    result = "".join(stack[-1] for stack in stacks)
    return result


def part_two(stacks):
    for c, move in enumerate(parse_moves()):
        if move.n == 1:
            for _ in range(move.n):
                stacks[move.dest].append(stacks[move.src].pop())
        else:
            to_be_moved = stacks[move.src][-move.n:]
            stacks[move.src] = stacks[move.src][:-move.n]
            stacks[move.dest].extend(to_be_moved)
    result = "".join(stack[-1] for stack in stacks)
    return result


def main():
    stack_repr = get_initial_stack_repr()
    # print("\n".join(stack_repr))
    stacks = parse_columns(stack_repr)
    # pp(stacks)
    # print(part_one(stacks))
    print(part_two(stacks))


if __name__ == '__main__':
    main()