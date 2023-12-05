"""Advent of Code 2021

Day 17:
  https://adventofcode.com/2021/day/17
"""

import argparse
from pathlib import Path
import re

import aoc


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--infile',
                        type=Path,
                        default=None,
                        help='Optional input text file for this puzzle')
    parser.add_argument('--part',
                        type=int,
                        default=None,
                        help='Solve just one part of the puzzle (1|2)')
    
    return parser.parse_args()


class Area():
    """A rectangular area."""
    RE = re.compile(r'target area: '
                    r'x=(?P<x1>\-?[0-9]+)..(?P<x2>\-?[0-9]+), '
                    r'y=(?P<y1>\-?[0-9]+)..(?P<y2>\-?[0-9]+)')

    def __init__(self, x_range, y_range):
        self.left = min(*x_range)
        self.right = max(*x_range)
        self.bottom = min(*y_range)
        self.top = max(*y_range)
    
    @property
    def width(self):
        return self.right - self.left
    
    @property
    def height(self):
        return self.top - self.bottom
    
    def contains(self, x, y):
        """True if the area contains the given point."""
        return self.left <= x <= self.right and self.bottom <= y <= self.top


class Probe():
    """A probe that follows an arc."""
    def __init__(self, dx, dy, target):
        self.x = 0
        self.y = 0
        self.dx = dx
        self.dy = dy
        self.target = target
        self.hit = False
        self.max_y = float('-inf')
    
    def simulate_launch(self):
        while not self.on_target and not self.missed:
            self.step()
        return self.on_target
    
    def step(self):
        self.x += self.dx
        self.y += self.dy
        self.max_y = max(self.y, self.max_y)
        if self.dx > 0:
            self.dx -= 1
        if self.dx < 0:
            self.dx += 1
        self.dy -= 1
        if self.on_target:
            self.hit = True
    
    @property
    def on_target(self):
        return self.target.contains(self.x, self.y)
    
    @property
    def missed(self):
        if self.hit:
            return False
        return self.x > self.target.right or self.y < self.target.bottom


def solve_part_1(puzzle_input):
    """Solve part 1 of today's puzzle."""
    highest_height = float('-inf')
    solution = None
    for dx in range(0, puzzle_input.right + 1):
        for dy in range(puzzle_input.bottom, 3 * abs(puzzle_input.top + 1)):
            probe = Probe(dx, dy, puzzle_input)
            if probe.simulate_launch() and probe.max_y > highest_height:
                highest_height = probe.max_y
                solution = (dx, dy)

    return highest_height


def solve_part_2(puzzle_input):
    """Solve part 2 of today's puzzle."""
    solutions = []
    for dx in range(0, puzzle_input.right + 1):
        for dy in range(puzzle_input.bottom, 3 * abs(puzzle_input.top + 1)):
            probe = Probe(dx, dy, puzzle_input)
            if probe.simulate_launch():
                solutions.append((dx, dy))
    
    return len(solutions)


def run_tests():
    """Run regression tests."""
    target = Area((20, 30), (-10, -5))
    assert 45 == solve_part_1(target)
    assert 112 == solve_part_2(target)


def format_input(puzzle_input):
    """Format the puzzle input."""
    match = Area.RE.match(puzzle_input.strip())
    return Area((int(match.group('x1')), int(match.group('x2'))),
                (int(match.group('y1')), int(match.group('y2'))))


def main(infile=None, part=None):
    """Solves for the given input."""
    solution_1 = None
    solution_2 = None

    if infile:
        puzzle_input = format_input(infile.read_text())
        if part in (None, 1):
            solution_1 = solve_part_1(puzzle_input)
        if part in (None, 2):
            solution_2 = solve_part_2(puzzle_input)

    return solution_1, solution_2


if __name__ == '__main__':
    run_tests()
    solution_1, solution_2 = main(**vars(parse_args()))
    print(f'Part One: {solution_1}')
    print(f'Part Two: {solution_2}')
