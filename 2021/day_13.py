"""Advent of Code 2021

Day 13:
  https://adventofcode.com/2021/day/13
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


def apply_fold(x_fold, y_fold, points):
    """Apply the fold and return the new set of points."""
    new_points = set()
    if x_fold is not None:
        for x, y in points:
            if x > x_fold:
                new_points.add((2 * x_fold - x, y))
                continue
            new_points.add((x, y))
    
    if y_fold is not None:
        for x, y in points:
            if y > y_fold:
                new_points.add((x, 2 * y_fold - y))
                continue
            new_points.add((x, y))
    
    return new_points


def points_to_str(points):
    """Return a string representation of the points."""
    max_row = 0
    max_col = 0
    for x, y in points:
        if y > max_row:
            max_row = y
        if x > max_col:
            max_col = x
    
    rows = [list(' ' * (max_col + 1)) for _ in range(max_row + 1)]
    for x, y in points:
        rows[y][x] = '#'

    return '\n'.join(''.join(row) for row in rows)


def solve_part_1(puzzle_input):
    """Solve part 1 of today's puzzle."""
    points, folds = puzzle_input
    points = apply_fold(*folds[0], points)
    return len(points)


def solve_part_2(puzzle_input):
    """Solve part 2 of today's puzzle."""
    points, folds = puzzle_input
    for fold in folds:
        points = apply_fold(*fold, points)
    return '\n' + points_to_str(points)


def run_tests():
    """Run regression tests."""
    sample_points = set((
        (6, 10),
        (0, 14),
        (9, 10),
        (0, 3),
        (10 ,4),
        (4, 11),
        (6, 0),
        (6, 12),
        (4, 1),
        (0, 13),
        (10 ,12),
        (3, 4),
        (3, 0),
        (8, 4),
        (1, 10),
        (2, 14),
        (8, 10),
        (9, 0),
    ))
    sample_folds = ((None, 7), (5, None))

    assert 17 == solve_part_1((sample_points, sample_folds))


def format_input(puzzle_input):
    """Format the puzzle input."""
    points = set()
    folds = []
    preamble = 'fold along '
    for line in puzzle_input.splitlines():
        if not line:
            continue
        if line.startswith(preamble):
            coord, value = line[len(preamble):].split('=')
            if coord == 'x':
                folds.append((int(value), None))
            elif coord == 'y':
                folds.append((None, int(value)))
            continue
        x, y = line.split(',')
        points.add((int(x), int(y)))
    
    return points, folds


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
