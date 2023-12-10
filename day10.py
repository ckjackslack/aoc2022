from abc import ABC, abstractmethod
from collections import deque

PIXEL_LIT = "#"
PIXEL_DARK = "."


class Instruction(ABC):
    def __init__(self, no_of_cycles, arg1=None):
        self.no_of_cycles = no_of_cycles
        self.finished = False
        self.arg1 = arg1
        self.current_cycle = 0
        self.cpu = None

    def set_cpu(self, cpu):
        assert isinstance(cpu, CPU)
        self.cpu = cpu

    @abstractmethod
    def action(self, cpu):
        pass

    def is_finished(self):
        return self.current_cycle == self.no_of_cycles


class NoopInstruction(Instruction):
    def __init__(self):
        super().__init__(no_of_cycles=1)

    def action(self):
        self.current_cycle += 1


class AddxInstruction(Instruction):
    def __init__(self, arg1):
        super().__init__(no_of_cycles=2, arg1=arg1)

    def action(self):
        self.current_cycle += 1
        if self.current_cycle == 2:
            self.cpu.registerX += self.arg1


class LineParser:
    @staticmethod
    def get_lines(filename):
        with open(filename) as f:
            for line in f:
                yield line.strip()

    @classmethod
    def parse_all(cls, filename):
        return [cls.parse(line) for line in cls.get_lines(filename)]

    @classmethod
    def parse(cls, line):
        if line == "noop":
            return NoopInstruction()
        elif line.startswith("addx"):
            _, value = line.split()
            return AddxInstruction(int(value))
        raise ValueError("Unrecognized instruction.")


class CPU:
    def __init__(self, instructions):
        assert all(isinstance(i, Instruction) for i in instructions)

        self.registerX = 1
        self.current_cycle = 1
        self.current_instr = None
        self.instructions = instructions

    def execute_part1(self):
        s = 0

        while len(self.instructions) > 0:

            if self.current_instr is None:
                self.current_instr = self.instructions.pop(0)
                self.current_instr.set_cpu(self)
            while not self.current_instr.is_finished():
                self.current_cycle += 1
                self.current_instr.action()

                if self.current_cycle in (20, 60, 100, 140, 180, 220):
                    ss = self.signal_strength()
                    # print(f"adding {ss} on cycle {self.current_cycle}")
                    s += ss

            self.current_instr = None

        return s

    def execute_part2(self):
        initial_position = "###....................................."
        sprite_position = deque(initial_position, maxlen=len(initial_position))
        col_max = len(initial_position) - 1
        cur_col = 0
        crt = []
        line = []

        while len(self.instructions) > 0:

            if self.current_instr is None:
                self.current_instr = self.instructions.pop(0)
                self.current_instr.set_cpu(self)
            while not self.current_instr.is_finished():
                self.current_cycle += 1
                self.current_instr.action()

                if cur_col > col_max:
                    cur_col = 0

                if sprite_position[cur_col] == PIXEL_LIT:
                    line.append(PIXEL_LIT)
                else:
                    line.append(PIXEL_DARK)

                if len(line) == len(sprite_position):
                    crt.append("".join(line))
                    line = []

                cur_col += 1

            if isinstance(self.current_instr, AddxInstruction):
                sprite_position.rotate(self.current_instr.arg1)

            self.current_instr = None

        return crt

    def signal_strength(self):
        return self.current_cycle * self.registerX


def main():
    filename = "day10_input.txt"
    for part in ("part1", "part2"):
        instructions = LineParser.parse_all(filename)
        cpu = CPU(instructions)
        fn = getattr(cpu, f"execute_{part}")
        result = fn()
        if type(result) == int:
            print(result)
        else:
            for line in result:
                print(line)

if __name__ == '__main__':
    main()