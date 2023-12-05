"""Advent of Code 2021

Day 1:
  https://adventofcode.com/2021/day/1
"""

import argparse
from pathlib import Path
from typing import Iterable, Tuple


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


def solve_part_1(puzzle_input: Iterable[int]) -> int:
    """Solve part 1 of today's puzzle."""
    number_of_increases = 0
    for idx, value in enumerate(puzzle_input):
        if idx == 0:
            continue
        if value > puzzle_input[idx - 1]:
            number_of_increases += 1
    
    return number_of_increases


def solve_part_2(puzzle_input):
    """Solve part 2 of today's puzzle."""
    window_values = []
    for i in range(len(puzzle_input) - 2):
        window_values.append(sum((puzzle_input[i],
                                  puzzle_input[i+1],
                                  puzzle_input[i+2])))
    
    return solve_part_1(window_values)


def run_tests():
    """Run regression tests."""
    sample_input = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]
    assert(7 == solve_part_1(sample_input))
    assert(5 == solve_part_2(sample_input))


def format_input(puzzle_input: str):
    """Format the puzzle input."""
    return [int(x) for x in puzzle_input.splitlines()]


def main(infile: Path = None, part: int = None) -> Tuple[int, int]:
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

