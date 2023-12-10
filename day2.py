from abc import ABC, abstractmethod
from enum import IntEnum, Enum, auto
from functools import lru_cache


class Who(Enum):
    OPPONENT = auto()
    YOU = auto()
    TIE = auto()

    @classmethod
    def get_outcome_from_letter(cls, letter):
        if letter == "X":
            return cls.OPPONENT
        elif letter == "Y":
            return cls.TIE
        elif letter == "Z":
            return cls.YOU
        else:
            raise ValueError("Unrecognized outcome.")


class Shape(IntEnum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

    @staticmethod
    @lru_cache
    def get_beats():
        return {
            Shape.ROCK: Shape.SCISSORS,
            Shape.PAPER: Shape.ROCK,
            Shape.SCISSORS: Shape.PAPER,
        }

    @classmethod
    def get_shape_from_letter(cls, letter):
        if letter in {"A", "X"}:
            return cls.ROCK
        elif letter in {"B", "Y"}:
            return cls.PAPER
        elif letter in {"C", "Z"}:
            return cls.SCISSORS
        else:
            raise ValueError("Unrecognized shape.")


class Strategy(ABC):
    def apply(self, game, opponent, you):
        opponent = Shape.get_shape_from_letter(opponent)

        you = self.get_you(game, opponent, you)

        winner, shape = game.decide_who_wins(opponent, you)
        game.calculate_points(winner, shape, opponent, you)

    @abstractmethod
    def get_you(self, game, opponent, you):
        pass


class PartOneStrategy(Strategy):
    def get_you(self, game, opponent, you):
        return Shape.get_shape_from_letter(you)


class PartTwoStrategy(Strategy):
    def get_you(self, game, opponent, you):
        outcome = Who.get_outcome_from_letter(you)
        return game.decide_the_figure(opponent, outcome)


class Game:
    def __init__(self, filename, strategy):
        self.filename = filename
        self.opponent_points = 0
        self.your_points = 0
        self.strategy = strategy

    def decide_who_wins(self, opponent, you):
        if opponent == you:
            return Who.TIE, opponent
        elif (opponent, you) == (Shape.ROCK, Shape.SCISSORS):
            return Who.OPPONENT, Shape.ROCK
        elif (opponent, you) == (Shape.SCISSORS, Shape.ROCK):
            return Who.YOU, Shape.ROCK
        elif (opponent, you) == (Shape.SCISSORS, Shape.PAPER):
            return Who.OPPONENT, Shape.SCISSORS
        elif (opponent, you) == (Shape.PAPER, Shape.SCISSORS):
            return Who.YOU, Shape.SCISSORS
        elif (opponent, you) == (Shape.PAPER, Shape.ROCK):
            return Who.OPPONENT, Shape.PAPER
        elif (opponent, you) == (Shape.ROCK, Shape.PAPER):
            return Who.YOU, Shape.PAPER
        else:
            raise ValueError("Unrecognized combination.")

    def decide_the_figure(self, opponent, outcome):
        if outcome == Who.TIE:
            return opponent
        elif outcome == Who.YOU:
            return {
                v: k
                for k, v
                in Shape.get_beats().items()
            }[opponent]
        else:
            return Shape.get_beats()[opponent]

    def calculate_points(self, winner, shape, opponent, you):
        if winner == Who.TIE:
            self.opponent_points += shape.value + 3
            self.your_points += shape.value + 3
        elif winner == Who.YOU:
            self.opponent_points += opponent.value
            self.your_points += shape.value + 6
        else:
            self.opponent_points += shape.value + 6
            self.your_points += you.value

    def play(self):
        with open(self.filename) as f:
            for line in f:
                opponent, you = line.strip().split(" ")
                self.strategy.apply(self, opponent, you)
        return (self.opponent_points, self.your_points)


def main():
    input_path = "day2_input.txt"

    for strategy in (PartOneStrategy, PartTwoStrategy):
        g = Game(input_path, strategy())
        result = g.play()[1]
        print(result)


if __name__ == '__main__':
    main()