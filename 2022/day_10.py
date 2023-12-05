"""https://adventofcode.com/2022/day/10"""

import logging
import textwrap
from typing import Callable, Dict, List


def run_tests() -> None:
    """Run simple tests using sample input."""
    small_input = textwrap.dedent(
        """\
        noop
        addx 3
        addx -5
    """
    )
    larger_input = textwrap.dedent(
        """\
        addx 15
        addx -11
        addx 6
        addx -3
        addx 5
        addx -1
        addx -8
        addx 13
        addx 4
        noop
        addx -1
        addx 5
        addx -1
        addx 5
        addx -1
        addx 5
        addx -1
        addx 5
        addx -1
        addx -35
        addx 1
        addx 24
        addx -19
        addx 1
        addx 16
        addx -11
        noop
        noop
        addx 21
        addx -15
        noop
        noop
        addx -3
        addx 9
        addx 1
        addx -3
        addx 8
        addx 1
        addx 5
        noop
        noop
        noop
        noop
        noop
        addx -36
        noop
        addx 1
        addx 7
        noop
        noop
        noop
        addx 2
        addx 6
        noop
        noop
        noop
        noop
        noop
        addx 1
        noop
        noop
        addx 7
        addx 1
        noop
        addx -13
        addx 13
        addx 7
        noop
        addx 1
        addx -33
        noop
        noop
        noop
        addx 2
        noop
        noop
        noop
        addx 8
        noop
        addx -1
        addx 2
        addx 1
        noop
        addx 17
        addx -9
        addx 1
        addx 1
        addx -3
        addx 11
        noop
        noop
        addx 1
        noop
        addx 1
        noop
        noop
        addx -13
        addx -19
        addx 1
        addx 3
        addx 26
        addx -30
        addx 12
        addx -1
        addx 3
        addx 1
        noop
        noop
        noop
        addx -9
        addx 18
        addx 1
        addx 2
        noop
        noop
        addx 9
        noop
        noop
        noop
        addx -1
        addx 2
        addx -37
        addx 1
        addx 3
        noop
        addx 15
        addx -21
        addx 22
        addx -6
        addx 1
        noop
        addx 2
        addx 1
        noop
        addx -10
        noop
        noop
        addx 20
        addx 1
        addx 2
        addx 2
        addx -6
        addx -11
        noop
        noop
        noop
    """
    )

    handheld = Handheld()
    handheld.load(small_input)
    handheld.run()
    assert handheld.x == -1

    handheld = Handheld()
    handheld.load(larger_input)
    signal_strengths = sample_signal_strength(handheld)
    logging.debug("Strengths: %s", signal_strengths)
    assert sum(signal_strengths) == 13140


class Handheld:
    """A simulated elvish handheld device."""

    def __init__(self):
        self.cycle: int = 0
        self.x: int = 1
        self.notify: Dict[int, Callable] = {}
        self._program: List[str] = []

    def __str__(self) -> str:
        """Returns the display state."""
        result = []
        for row in self.display:
            result.append("".join(row))
        return "\n".join(result)

    @property
    def signal_strength(self) -> int:
        """Returns the current signal strength."""
        return self.cycle * self.x

    def load(self, program: str) -> None:
        """Loads the program onto the handheld."""
        self.cycle = 0
        self.x = 1
        self._program = program.splitlines()
        self._program.reverse()
        self.display: List[List[str]] = [["." for _ in range(40)] for __ in range(6)]

    def run(self) -> None:
        """Run the currently loaded program."""
        while self._program:
            instruction = self._program.pop()
            if instruction == "noop":
                self.noop()
            elif instruction.startswith("addx"):
                _, val = instruction.split()
                self.addx(int(val))
            else:
                raise ValueError(f"Unknown instruction: {instruction}")

    def tick(self, t: int = 1) -> None:
        """Ticks the CPU by 1 cycle."""
        for _ in range(t):
            row = self.cycle // 40
            col = self.cycle % 40
            self.cycle += 1

            if col in (self.x - 1, self.x, self.x + 1):
                self.display[row][col] = "#"

            if self.cycle in self.notify:
                self.notify[self.cycle]()

    def subscribe(self, cycle: int, cb: Callable) -> None:
        """Adds the callback function to be called on the given cycle."""
        self.notify[cycle] = cb

    def noop(self) -> None:
        """No-op instruction; takes 1 cycle."""
        self.tick()

    def addx(self, val: int) -> int:
        """Adds value to x register and returns the new x; takes 2 cycles."""
        self.tick(2)
        self.x += val
        return self.x


def sample_signal_strength(handheld: Handheld) -> List[int]:
    """Samples signal strength at certain cycles."""
    samples = []

    def notify_cb():
        samples.append(handheld.signal_strength)

    for cycle in (20, 60, 100, 140, 180, 220):
        handheld.subscribe(cycle, notify_cb)

    handheld.run()

    return samples


def solve_part_1(puzzle_input: str) -> int:
    """Solves part 1 of today's puzzle."""
    handheld = Handheld()
    handheld.load(puzzle_input)
    return sum(sample_signal_strength(handheld))


def solve_part_2(puzzle_input: str) -> str:
    """Solves part 2 of today's puzzle."""
    handheld = Handheld()
    handheld.load(puzzle_input)
    handheld.run()
    return "\n" + str(handheld)
