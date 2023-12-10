import os
from dataclasses import dataclass


@dataclass
class Position:
    x: int # right
    y: int # down

    @classmethod
    def from_string(cls, string, sep=","):
        return cls(*map(int, string.split(sep)))

    def as_tuple(self):
        return (self.x, self.y)

    @classmethod
    def convert_path(cls, line, sep=" -> "):
        return [cls.from_string(part) for part in line.split(sep)]


@dataclass
class Thing:
    pos: Position
    symbol: str

    def __str__(self):
        return self.symbol

@dataclass
class Air(Thing):
    symbol: str = "."

@dataclass
class SandSource(Thing):
    pos: Position = Position(x=500, y=0)
    symbol: str = "+"

@dataclass
class Sand(Thing):
    symbol: str = "o"

@dataclass
class Rock(Thing):
    symbol: str = "#"


def get_input():
    name, ext = os.path.splitext(__file__)
    with open(f"{name}_input.txt") as f:
        yield from [Position.convert_path(line.strip()) for line in f]


def main():
    cave = [
        [
            Air(pos=Position(x=i, y=j)) for i in range(494, 503)
        ] for j in range(10)
    ]
    for row in cave:
        for col in row:
            print(col, end="")
        print()

    # for trace in get_input():
    #     print(trace)
    #     break


if __name__ == '__main__':
    main()