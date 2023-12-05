"""Advent of Code 2021

Day ?:
  https://adventofcode.com/2021/day/
"""

import argparse
from pathlib import Path

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


def solve_part_1(puzzle_input):
    """Solve part 1 of today's puzzle."""


def solve_part_2(puzzle_input):
    """Solve part 2 of today's puzzle."""


def run_tests():
    """Run regression tests."""


def format_input(puzzle_input):
    """Format the puzzle input."""
    return [int(x) for x in puzzle_input.splitlines()]


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
