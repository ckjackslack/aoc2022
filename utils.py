from enum import IntEnum, auto


def dynamic_option(n):
    assert isinstance(n, int)
    n = n if n > 0 else 1
    opt = Option.CHARS
    opt.n = n
    return opt


class Option(IntEnum):
    CHAR = auto()
    CHARS = auto()
    LINE = auto()


class ByType(type):
    def __getattr__(self, name):
        if name not in list(map(lambda o: o.name, Option)):
            raise AttributeError
        if name == Option.CHAR.name:
            return Option.CHAR
        elif name == Option.LINE.name:
            return Option.LINE
        elif name == Option.CHARS.name:
            return dynamic_option


class By(metaclass=ByType):
    pass


def get_lines(filename, process_by=By.LINE, strip_ws=False, skip_empty=False):
    with open(filename) as f:
        if process_by == By.CHAR:
            for line in f:
                for char in line:
                    if char.isspace() and skip_empty:
                        continue
                    yield char
        elif process_by == By.LINE:
            for line in f:
                if not line.strip() and skip_empty:
                    continue
                yield line if not strip_ws else line.strip()
        else:
            while True:
                block = f.read(process_by.n)
                if not block:
                    break
                yield block


def main():
    # for o in get_lines("day1_input.txt", By.LINE, strip_ws=True, skip_empty=True):
    #     print(o)

    # for o in get_lines("day1_input.txt", By.CHAR):
    #     print(o)

    # for o in get_lines("day1_input.txt", By.CHAR, skip_empty=True):
    #     print(o)

    pass

if __name__ == '__main__':
    main()