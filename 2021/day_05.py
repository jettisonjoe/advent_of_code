"""Advent of Code 2021

Day 5:
  https://adventofcode.com/2021/day/5
"""

import argparse
import collections
import math
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


def frequencies(corpus):
    """Compute the frequency of each element in the corpus."""
    freqs = collections.defaultdict(lambda: 0)
    for element in corpus:
        freqs[element] += 1
    
    return freqs


def all_points_from_endpoints(endpoints, skip_diags=True):
    """Given an iterable of endpoint pairs, return all points covered."""
    all_points = []
    for (x1, y1), (x2, y2) in endpoints:
        if skip_diags and x1 != x2 and y1 != y2:
            continue
        x = x1
        y = y1
        dx = 0 if x1 == x2 else math.copysign(1, x2 - x1)
        dy = 0 if y1 == y2 else math.copysign(1, y2 - y1)
        while x != x2 or y != y2:
            all_points.append((x, y))
            x += dx
            y += dy
        all_points.append((x2, y2))
    
    return all_points


def solve_part_1(puzzle_input):
    """Solve part 1 of today's puzzle."""
    all_points = all_points_from_endpoints(puzzle_input)
    freqs = frequencies(all_points)
    num_danger_points = 0
    for danger_level in freqs.values():
        if danger_level >= 2:
            num_danger_points += 1
    
    return num_danger_points


def solve_part_2(puzzle_input):
    """Solve part 2 of today's puzzle."""
    all_points = all_points_from_endpoints(puzzle_input, skip_diags=False)
    freqs = frequencies(all_points)
    num_danger_points = 0
    for danger_level in freqs.values():
        if danger_level >= 2:
            num_danger_points += 1
    
    return num_danger_points


def run_tests():
    """Run regression tests."""
    sample_input = (((0, 9), (5, 9)),
                    ((8, 0), (0, 8)),
                    ((9, 4), (3, 4)),
                    ((2, 2), (2, 1)),
                    ((7, 0), (7, 4)),
                    ((6, 4), (2, 0)),
                    ((0, 9), (2, 9)),
                    ((3, 4), (1, 4)),
                    ((0, 0), (8, 8)),
                    ((5, 5), (8, 2)))

    assert(5 == solve_part_1(sample_input))


def format_input(puzzle_input):
    """Format the puzzle input."""
    point_pairs = []
    for line in puzzle_input.splitlines():
        left, right = line.split('->')
        x1, y1 = left.strip().split(',')
        x2, y2 = right.strip().split(',')
        point_pairs.append(((int(x1), int(y1)), (int(x2), int(y2))))
    
    return point_pairs


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

