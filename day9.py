from collections import namedtuple
from dataclasses import dataclass
from enum import IntEnum, auto
from typing import Optional

Move = namedtuple("Move", "direction steps")

@dataclass
class Cell:
    value: Optional[str] = None

HEAD_CELL = Cell(value="H")
TAIL_CELL = Cell(value="T")

#T T
# H
#T T

# (row - 1, col - 1), (row - 1, col + 1)
# (row + 1, col - 1), (row + 1, col + 1)

@dataclass
class Position:
    x: int
    y: int

    def as_tuple(self):
        return (self.x, self.y)

    def is_on_diagonal(self, other):
        return (
            (self.x + 1 == other.x and self.y + 1 == other.y)
            or
            (self.x + 1 == other.x and self.y - 1 == other.y)
            or
            (self.x - 1 == other.x and self.y + 1 == other.y)
            or
            (self.x - 1 == other.x and self.y - 1 == other.y)
        )

    def get_position_before(self, move, other):
        if move.direction == Direction.UP:
            return Position(other.x, other.y - 1)
        elif move.direction == Direction.DOWN:
            return Position(other.x, other.y + 1)
        elif move.direction == Direction.LEFt:
            return Position(other.x + 1, other.y)
        elif move.direction == Direction.RIGHT:
            return Position(other.x - 1, other.y)

    def __add__(self, other):
        assert isinstance(other, Position)
        return Position(self.x + other.x, self.y + other.y)

class Direction(IntEnum):
    RIGHT = auto()
    UP = auto()
    LEFT = auto()
    DOWN = auto()

    @classmethod
    def from_string(cls, string):
        for opt in list(cls):
            if string == opt.name[0]:
                return opt
        raise ValueError("Unrecognized option.")

    @classmethod
    def get_position_mask(cls, move):
        assert isinstance(move, Move)
        if move.direction == cls.RIGHT:
            change = (0, 1)
        elif move.direction == cls.LEFT:
            change = (0, -1)
        elif move.direction == cls.UP:
            change = (-1, 0)
        elif move.direction == cls.DOWN:
            change = (1, 0)
        change = tuple(n * move.steps for n in change)
        return Position(*change)

class Board:
    def __init__(self, rows, cols, head_pos=None, tail_pos=None):
        self.board = [
            [
                Cell()
                for _
                in range(cols)
            ]
            for _
            in range(rows)
        ]
        self.current_head_pos = head_pos
        self.current_tail_pos = tail_pos
        if head_pos:
            self.board[head_pos.x][head_pos.y] = HEAD_CELL
        if tail_pos:
            self.board[tail_pos.x][tail_pos.y] = TAIL_CELL
        self.tail_positions_visited = []

    def set_cell(self, position, cell=None):
        if cell is not None:
            assert isinstance(cell, Cell)
            self.board[position.x][position.y] = cell
        else:
            self.board[position.x][position.y] = Cell()

    def determine_new_head_position(self, move):
        assert isinstance(move, Move)
        mask = Direction.get_position_mask(move)
        return self.current_head_pos + mask

    def determine_tail_position(self, move, new_head_pos):
        if self.current_tail_pos:
            if self.current_tail_pos.is_on_diagonal(new_head_pos):
               # 1
               # first move is
               # if pos == TL and dir == DOWN -> col + 1
               # if pos == TR and dir == DOWN -> col - 1
               # if pos == BL and dir == UP -> col + 1
               # if pos == BR and dir == UP -> col - 1
               pass
            else:
                return self.current_tail_pos.get_position_before(
                    move, new_head_pos
                )
        else:
            return self.current_tail_pos.get_position_before(
                move, new_head_pos
            )
        # 1) check if tail is positioned diagonally from head
        # (1, 1), (1, -1), (-1, 1), (-1, -1)
        # 2) otherwise, it's either covered or one cell before
        # and it will be one move before the head in the same direction
        # after move
        pass

    def move(self, move):
        new_head_pos = self.determine_new_head_position(move)
        new_tail_pos = self.determine_tail_position(move, new_head_pos)
        self.set_cell(self.current_head_pos)
        self.current_head_pos = new_head_pos
        self.set_cell(self.current_head_pos, HEAD_CELL)

    def display(self):
        for row in self.board:
            for cell in row:
                print(f"[{' ' if not cell.value else cell.value}]", end="")
            print()

def get_moves():
    with open("day9_example.txt") as f:
        for line in f:
            direction, steps = line.strip().split(" ")
            direction = Direction.from_string(direction)
            yield Move(direction=direction, steps=int(steps))

def main():
    b = Board(5, 6, head_pos=Position(x=4, y=0))
    # b.display()
    for m in get_moves():
        b.move(m)
    # b.display()

if __name__ == '__main__':
    main()