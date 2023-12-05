"""Advent of Code 2021

Day 7:
  https://adventofcode.com/2021/day/7
"""

import argparse
from pathlib import Path
import statistics
import collections


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


def multimode(data):
    freqs = collections.defaultdict(lambda: 0)
    for x in data:
        freqs[x] += 1
    
    max_freq = max(freqs.values())
    modes = []
    for k, v in freqs.items():
        if v == max_freq:
            modes.append(k)
    
    return modes


def solve_part_1(puzzle_input):
    """Solve part 1 of today's puzzle."""
    sorted_input = sorted(puzzle_input)
    min_fuel = sum(sorted_input)
    partition = 0
    for target_pos in range(1, sorted_input[-1]):
        while sorted_input[partition] < target_pos:
            partition += 1
        fuel = min_fuel + partition
        fuel -= len(sorted_input) - partition
        if fuel < min_fuel:
            min_fuel = fuel
    
    return min_fuel


def solve_part_2(puzzle_input):
    """Solve part 2 of today's puzzle."""
    min_fuel = None
    for target_pos in range(min(puzzle_input), max(puzzle_input) + 1):
        fuel = 0
        for crab in puzzle_input:
            fuel += sum(range(abs(crab - target_pos) + 1))
        if min_fuel is None or fuel < min_fuel:
            min_fuel = fuel
    
    return min_fuel


def run_tests():
    """Run regression tests."""
    sample_input = [16, 1, 2, 0, 4, 2, 7, 1, 2, 14]
    assert(37 == solve_part_1(sample_input))
    assert(168 == solve_part_2(sample_input))


def format_input(puzzle_input):
    """Format the puzzle input."""
    return [int(x) for x in puzzle_input.strip().split(',')]


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
