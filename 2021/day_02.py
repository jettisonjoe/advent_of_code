"""Advent of Code 2021

Day 2:
  https://adventofcode.com/2021/day/2
"""

import argparse
from pathlib import Path


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
    depth = 0
    horizontal_pos = 0
    for direction, magnitude in puzzle_input:
        if direction == 'forward':
            horizontal_pos += magnitude
        if direction == 'up':
            depth -= magnitude
        if direction == 'down':
            depth += magnitude
    
    return depth * horizontal_pos


def solve_part_2(puzzle_input):
    """Solve part 2 of today's puzzle."""
    depth = 0
    horizonal_pos = 0
    aim = 0
    for direction, magnitude in puzzle_input:
        if direction == 'forward':
            horizonal_pos += magnitude
            depth += (aim * magnitude)
        if direction == 'up':
            aim -= magnitude
        if direction == 'down':
            aim += magnitude
    
    return depth * horizonal_pos


def run_tests():
    """Run regression tests."""
    sample_input = [('forward', 5),
                    ('down', 5),
                    ('forward', 8),
                    ('up', 3),
                    ('down', 8),
                    ('forward', 2)]
    assert(150 == solve_part_1(sample_input))
    assert(900 == solve_part_2(sample_input))


def format_input(puzzle_input: str):
    """Format the puzzle input."""
    data = []
    for line in puzzle_input.splitlines():
        direction, magnitude = line.split()
        data.append((direction, int(magnitude)))

    return data


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

