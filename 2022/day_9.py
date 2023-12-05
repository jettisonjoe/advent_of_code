"""https://adventofcode.com/2022/day/9"""

import logging
import math
import textwrap
from typing import Iterable, List, Tuple


def run_tests() -> None:
    """Run simple tests using sample input."""
    test_input_1 = textwrap.dedent(
        """\
        R 4
        U 4
        L 3
        D 1
        R 4
        D 1
        L 5
        R 2
    """
    )
    test_input_2 = textwrap.dedent(
        """\
        R 5
        U 8
        L 8
        D 3
        R 17
        D 10
        L 25
        U 20
    """
    )
    moves_1 = parse_input(test_input_1)
    moves_2 = parse_input(test_input_2)

    rope = Rope()
    rope.apply_moves(moves_1)
    logging.debug("Tail visited in test case 1: %s", rope.tail_visited)
    assert len(rope.tail_visited) == 13

    rope = Rope(10)
    rope.apply_moves(moves_1)
    assert len(rope.tail_visited) == 1

    rope = Rope(10)
    rope.apply_moves(moves_2)
    logging.debug("Tail visited length in test case 3: %s", len(rope.tail_visited))
    assert len(rope.tail_visited) == 36


def parse_input(puzzle_input: str) -> List[Tuple[str, int]]:
    """Parses puzzle input and returns a list of moves."""
    moves = []
    for line in puzzle_input.splitlines():
        direction, distance = line.split()
        moves.append((direction, int(distance)))

    return moves


class Rope:
    """A simulated rope."""

    DIRECTIONS = {
        "U": (0, -1),
        "D": (0, 1),
        "L": (-1, 0),
        "R": (1, 0),
        "UL": (-1, -1),
        "UR": (1, -1),
        "DL": (-1, 1),
        "DR": (1, 1),
        "C": (0, 0),
    }

    def __init__(self, length=2):
        self.segments = [(0, 0) for _ in range(length)]
        self.tail_visited = {self.segments[-1]}

    def apply_moves(self, moves: Iterable[Tuple[str, int]]) -> None:
        """Applies a series of moves to the rope."""
        for direction, distance in moves:
            for _ in range(distance):
                self.move(self.add_points(self.segments[0], self.DIRECTIONS[direction]))

    def move(self, dest: Tuple[int, int], idx: int = 0) -> None:
        """Applies a single move to a rope segment."""
        if idx == len(self.segments) - 1:
            self.segments[-1] = dest
            self.tail_visited.add(dest)
            return

        self.segments[idx] = dest
        next_seg = self.segments[idx + 1]
        if not self.are_neighbors(dest, next_seg):
            dx = dest[0] - next_seg[0]
            x_incr = 0 if dx == 0 else int(math.copysign(1, dx))
            dy = dest[1] - next_seg[1]
            y_incr = 0 if dy == 0 else int(math.copysign(1, dy))
            self.move((next_seg[0] + x_incr, next_seg[1] + y_incr), idx + 1)

    @classmethod
    def are_neighbors(cls, x: Tuple[int, int], y: Tuple[int, int]) -> bool:
        """Returns True if the two points are neighbors."""
        for direction in cls.DIRECTIONS.values():
            if y == cls.add_points(x, direction):
                return True
        return False

    @staticmethod
    def add_points(x: Tuple[int, int], y: Tuple[int, int]) -> Tuple[int, int]:
        """Adds two points together."""
        return x[0] + y[0], x[1] + y[1]


def solve_part_1(puzzle_input: str) -> int:
    """Solves part 1 of today's puzzle."""
    rope = Rope()
    rope.apply_moves(parse_input(puzzle_input))
    return len(rope.tail_visited)


def solve_part_2(puzzle_input: str) -> int:
    """Solves part 2 of today's puzzle."""
    rope = Rope(10)
    rope.apply_moves(parse_input(puzzle_input))
    return len(rope.tail_visited)
