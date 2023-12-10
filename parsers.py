
# by char
# by n chars
# by line
# by several lines
# until empty line
# split on
# match regex
# several matchers
# as grid / matrix
# to counter
# horizontal parser
# vertical parser
# to set
# evaluated / as ast
# tree like / nested
# as chain / to 2d lines

import math
import re
from collections import Counter, defaultdict, namedtuple
from dataclasses import dataclass
from enum import IntEnum, auto
from functools import partial, reduce
from itertools import takewhile
from pprint import pp
from typing import Optional

import parse


def is_iterable(obj):
    try:
        iter(obj)
        return True
    except:
        return False


pp = partial(pp, width=100)


class When(IntEnum):
    BEFORE = auto()
    IN_BETWEEN = auto()
    AFTER = auto()


def apply(thing, *args):
    for arg in args:
        if isinstance(arg, list):
            for fn in arg:
                thing = fn(thing)
        else:
            thing = arg(thing)
    return thing


def _get_lines(filename):
    with open(filename) as f:
        for line in f:
            yield line


def line_parser(filename,
    skip_empty=False,
    strip_fn=None,
    process_fn=None,
    filter_fn=None,
    when_filter=None):
    # initial conditions
    assert isinstance(skip_empty, bool)
    assert process_fn is None or callable(process_fn)\
        or (isinstance(process_fn, list) and all(map(callable, process_fn)))
    if when_filter is not None:
        assert callable(filter_fn)
    if strip_fn is not None:
        assert callable(strip_fn)
    lines_generator = _get_lines(filename)
    while True:
        try:
            current_line = next(lines_generator)
            if when_filter == When.BEFORE and not filter_fn(current_line):
                continue
            if strip_fn:
                current_line = strip_fn(current_line)
            if skip_empty and not current_line.strip():
                continue
            if when_filter == When.IN_BETWEEN and not filter_fn(current_line):
                continue
            if process_fn is None:
                yield current_line
            elif when_filter == When.AFTER:
                altered_line = apply(current_line, process_fn)
                if filter_fn(altered_line):
                    yield altered_line
            else:
                yield apply(current_line, process_fn)
        except StopIteration:
            break


def split_on(generator, predicate):
        result = []
        sublist = []
        for item in generator:
            if predicate(item):
                sublist.append(item)
            else:
                result.append(sublist)
                sublist = []
        if sublist:
            result.append(sublist)
        return result


def traverse(nested, convert_fn=None):
    for item in nested:
        if is_iterable(item):
            yield from traverse(item, convert_fn=convert_fn)
        else:
            yield convert_fn(item) if convert_fn else item


def traverse_with_path(nested, path=""):
    for idx, item in enumerate(nested):
        if type(item) is list:
            yield from traverse(item, path=f"{path} {idx}")
        else:
            yield item, f"{path} {idx}"


def go_into(ds, indexes):
    thing = ds.copy()
    for i in indexes.split():
        thing = thing[int(i)]
    return thing


def test_traverse_paths(ds):
    for v, indexes in traverse(ds):
        print(v, indexes)
        assert v == go_into(ds, indexes)


def divide_chunks(_list, size):
    for start in range(0, len(_list), size):
        yield _list[start:start + size]


def iterator_to_chunks(it, size):
    while True:
        try:
            pack = []
            i = 0
            while i < size:
                pack.append(next(it))
                i += 1
            yield pack
        except StopIteration:
            break


# ds = [[["a", "a"], ["b", "b", "y", "y", "x", ["a", [chr(i) for i in range(98, 109)]]]], [["c", "c"], ["d", "d", "d", ["e", "f"]]]]
# test_traverse_paths(ds)


# TODO: add convert fn to leaf
def split_consecutive(thing, *separators):
    def wrapper(thing, separator):
        if type(thing) is str:
            return list(filter(None, re.split(separator, thing)))
        else:
            return [wrapper(chunk, separator) for chunk in thing]

    result = thing
    for separator in separators:
        result = wrapper(result, separator)

    return result


def get_until_ws(filename, predicate=str.isdigit, converter=None):
    for sublist in split_on(get_with_empty(filename), predicate):
        yield list(map(converter, sublist)) if converter else sublist


until_ws = lambda filename: get_until_ws(filename, converter=int)


def get_fmt_tuples(filename, fmt):
        for line in _get_lines(filename):
            line = line.strip()
            if line:
                result = parse.parse(fmt, line)
                if result:
                    yield result.fixed


def get_even_sized_blocks(filename, size=1):
        with open(filename) as f:
            while True:
                block = f.read(size).strip()
                if block:
                    yield block
                else:
                    break


def one_of(string, *fmts, as_tuple=False):
    for fmt in fmts:
        if result := parse.parse(fmt, string):
            return result if not as_tuple else result.fixed


def one_of_annotated(string, *pairs):
    for fmt, outcome in pairs:
        if result := parse.parse(fmt, string):
            return string, outcome, result.fixed


make = lambda fn: lambda seq: type(seq)(fn(item) for item in seq)
get_with_empty = partial(line_parser, strip_fn=str.strip)
get_cleaned = partial(line_parser, strip_fn=str.strip, skip_empty=True)
get_ints = partial(get_cleaned, process_fn=int)
get_comps = partial(get_cleaned, process_fn=[str.split, tuple])
get_sets = partial(get_cleaned, process_fn=[str.lower, set])
get_codes = partial(get_cleaned, process_fn=[str.lower, set, make(ord)])
get_splitted = partial(get_cleaned, process_fn=[split_consecutive(",", "-")])


def main():
    # filename = "day1_input.txt"
    # pp(list(get_ints(filename)))
    # pp(list(until_ws(filename)))

    # filename = "day2_input.txt"
    # pp(list(get_comps(filename)))

    # filename = "day3_input.txt"
    # pp(list(get_sets(filename)))
    # pp(list(get_codes(filename)))

    # filename = "day4_input.txt"
    # items_gen = traverse(
    #     split_consecutive("10-15,20-25", ",", "-", r""),
    #     convert_fn=int,
    # )
    # pp(list(iterator_to_chunks(items_gen, 2)))
    # pp(list(get_splitted(filename)))
    # for line in _get_lines(filename):
    #     print(line)

    filename = "day5_input.txt"


    def find_all_in_line(string, substring):
        result = []
        idx = 0
        while True:
            idx = string.find(substring, idx)
            if idx == -1:
                break
            result.append(idx)
            idx += len(substring)
        return result


    def get_stacks_in_line(line, beg_box="[", box_size=3, space_between=1, value_length=1):
        indexes = find_all_in_line(line, beg_box)
        for idx in indexes:
            # stack_no = math.floor(idx / (box_size + space_between) + 1)
            stack_no = idx // (box_size + space_between)
            beg_pos = idx + len(beg_box)
            if value_length == 1:
                value = line[beg_pos]
            else:
                value = line[beg_pos:beg_pos + value_length]
            yield stack_no, value


    def parse_all_stacks(_input, **kwargs):
        stacks = []

        if type(_input) is str:
            it = _get_lines(_input)
        else:
            it = _input
        for line in it:
            # print(line)
            found = list(get_stacks_in_line(line, **kwargs))
            if len(found) > 0:
                # s = " ".join(f"{t[0]}{t[1]}" for t in found)
                # print(f"{s:>30}")
                for stack_no, value in found:
                    print(stack_no, value)
                    for _ in range(stack_no - len(stacks)):
                        stacks.append([])
                    # stacks[stack_no - 1].insert(0, value)
                    # stacks[stack_no].insert(0, value)
            else:
                break

        return stacks

    lines = [
        "((o))   ((b))   ((c))",
        "((g))           ((d))",
        "((f))                   ((h))",
        "        ((t))",
    ]

    def determine_number_of_boxes(line):
        return len(list(filter(None, re.split(r"\s+", line))))

    def determine_free_space(line):
        return line.count(" ")

    def determine_occupied_space(line):
        return len(line) - determine_free_space(line)

    def determine_box_size(line):
        return determine_occupied_space(line) // determine_number_of_boxes(line)

    # def determine_can_fit(line):
    #     size = len(line)
    #     num_boxes = determine_number_of_boxes(line)
    #     total_spaces = determine_free_space(line)
    #     box_size = determine_box_size(line)
    #     can_fit = 0
    #     while True:
    #         total_spaces -= box_size
    #         if total_spaces % 2 != 0:
    #             break

    def determine_space_between(line):
        size = len(line)
        box_size = determine_box_size(line)
        total_spaces = determine_free_space(line)
        num_boxes = determine_number_of_boxes(line)
        occupied = size - total_spaces
        # can_fit = determine_can_fit(line)
        # return can_fit

        # occupied / total_spaces
        # occupied = num_boxes * box_size

        "((o))   ((b))   ((c))"         # 21 6 15 3
        "((g))           ((d))"         # 21 11 10 2
        "((f))                   ((h))" # 29 19 10 2
        "        ((t))"                 # 13 8 5 1

        # 0, 1, 2, 1

    def most_common(lst):
        data = Counter(lst)
        return data.most_common(1)[0][0]

    def determine_value_size(line):
        counter = Counter(line)
        del counter[" "]
        copy_counter = counter.copy()
        for key, value in list(counter.items()).copy():
            if value % 2 != 0:
                del counter[key]
        keys_to_delete = set()
        for (f1, v1), (f2, v2) in divide_chunks(sorted(counter.items()), 2):
            if abs(ord(f1) - ord(f2)) == 1:
                keys_to_delete.add(f1)
                keys_to_delete.add(f2)
                break
        for key in keys_to_delete:
            del copy_counter[key]
        return most_common(copy_counter.values())

    # print([determine_box_size(line) for line in lines])
    print([determine_space_between(line) for line in lines])
    # print([determine_value_size(line) for line in lines])

    print(parse_all_stacks(lines, beg_box="((", box_size=5, space_between=3, value_length=1))

    # pp([s[-1] for s in parse_all_stacks(filename)])

    # fmt = "move {:d} from {:d} to {:d}"
    # pp(list(get_fmt_tuples(filename, fmt)))

    # filename = "day6_input.txt"
    # pp(list(get_even_sized_blocks(filename, 4)))
    # pp(list(get_even_sized_blocks(filename, 14)))

    class Outcome(IntEnum):
        COMMAND_CD = auto()
        COMMAND_LS = auto()
        OUT_FILE = auto()
        OUT_DIR = auto()

    @dataclass
    class Command:
        name: str
        arg: Optional[str] = None

    @dataclass
    class Entry:
        name: str
        is_file: bool
        size: Optional[int] = None

    def thing_factory(outcome, args):
        if outcome == Outcome.COMMAND_CD:
            return Command("cd", *args)
        elif outcome == Outcome.COMMAND_LS:
            return Command("ls")
        elif outcome == Outcome.OUT_FILE:
            size, name = args
            return Entry(name, True, size)
        elif outcome == Outcome.OUT_DIR:
            name = args[0]
            return Entry(name, False)

    # fmts = [
    #     "$ cd {}",
    #     "$ ls",
    #     "{:d} {}",
    #     "dir {}",
    # ]

    # pairs = list(zip(
    #     fmts,
    #     list(Outcome),
    # ))

    # filename = "day7_input.txt"
    # not_identified = 0

    # for line in _get_lines(filename):
    #     line = line.strip()

    #     # print(one_of(line, *fmts))

    #     try:
    #         s, outcome, args = one_of_annotated(line, *pairs)
    #         # print(s, " -> ", outcome)
    #         # print(thing_factory(outcome, args))
    #     except:
    #         not_identified += 1

    # assert not_identified == 0

    def into_matrix(generator, with_position=False):
        for row, line in enumerate(generator):
            line = line.strip()
            if line:
                if with_position:
                    yield [(int(v), row, col) for col, v in enumerate(line)]
                else:
                    yield [int(c) for c in line]


    def check_dimensions(matrix):
        rows, cols = 0, 0
        for e in matrix:
            for t in e:
                _, r, c = t
                if r > rows:
                    rows = r
                if c > cols:
                    cols = c
        return rows + 1, cols + 1


    def display_matrix(matrix):
        for row in matrix:
            for col in row:
                if isinstance(col, tuple):
                    v, _, _ = col
                else:
                    v = col
                print(f"[{v}]", end="")
            print()


    # filename = "day8_input.txt"
    # m = list(into_matrix(_get_lines(filename), with_position=True))
    # m = list(into_matrix(_get_lines(filename)))
    # pp(m)
    # print(check_dimensions(m))
    # display_matrix(m)

    # filename = "day9_input.txt"
    # pp(list(get_comps(filename)))

    # generator = line_parser(
    #     filename,
    #     strip_fn=str.strip,
    #     skip_empty=True,
    #     process_fn=int,
    #     filter_fn=lambda v: v >= 10000 and v < 20000,
    #     when_filter=When.AFTER,
    # )
    # pp(list(generator))


if __name__ == '__main__':
    main()