"""Advent of Code 2021

Day 9:
  https://adventofcode.com/2021/day/9
"""

import argparse
import functools
import operator
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


def get_neighbor_locs(rows, r, c):
    """Returns an iterable of neighbor locations of the given cell."""
    neighbors = []
    if r > 0:
        neighbors.append((r - 1, c))  # North
    if r < len(rows) - 1:
        neighbors.append((r + 1, c))  # South
    if c < len(rows[r]) - 1:
        neighbors.append((r, c + 1))  # East
    if c > 0:
        neighbors.append((r, c - 1))  # West

    return neighbors


def get_values(rows, locations):
    """Returns an iterable of values in the given locations."""
    return [rows[r][c] for r, c in locations]


def get_low_points(rows):
    """Returns a list of all the low points in rows."""
    low_points = []
    for r, row in enumerate(rows):
        for c, cell in enumerate(row):
            neighbor_locs = get_neighbor_locs(rows, r, c)
            if all(cell < n for n in get_values(rows, neighbor_locs)):
                low_points.append((r, c))
    
    return low_points

def get_basin_size(rows, row, col):
    """Returns the size of the basin at the low point."""
    to_visit = get_neighbor_locs(rows, row, col)
    visited = {(row, col)}
    basin_size = 1
    while to_visit:
        curr_r, curr_c = to_visit.pop()
        if rows[curr_r][curr_c] == 9:
            continue
        basin_size += 1
        for neighbor in get_neighbor_locs(rows, curr_r, curr_c):
            if neighbor in visited or neighbor in to_visit:
                continue
            to_visit.append(neighbor)
        visited.add((curr_r, curr_c))
    
    return basin_size



def solve_part_1(puzzle_input):
    """Solve part 1 of today's puzzle."""
    low_points = get_low_points(puzzle_input)
    return sum(get_values(puzzle_input, low_points)) + len(low_points)


def solve_part_2(puzzle_input):
    """Solve part 2 of today's puzzle."""
    low_points = get_low_points(puzzle_input)
    basin_sizes = [get_basin_size(puzzle_input, r, c) for r, c in low_points]
    sorted_sizes = sorted(basin_sizes)
    result = functools.reduce(operator.mul, sorted_sizes[-3:], 1)
    return result


def run_tests():
    """Run regression tests."""
    sample_input = [
        [2, 1, 9, 9, 9, 4, 3, 2, 1, 0],
        [3, 9, 8, 7, 8, 9, 4, 9, 2, 1],
        [9, 8, 5, 6, 7, 8, 9, 8, 9, 2],
        [8, 7, 6, 7, 8, 9, 6, 7, 8, 9],
        [9, 8, 9, 9, 9, 6, 5, 6, 7, 8],
    ]
    
    assert 15 == solve_part_1(sample_input)
    assert 1134 == solve_part_2(sample_input)


def format_input(puzzle_input):
    """Format the puzzle input."""
    rows = []
    for line in puzzle_input.splitlines():
        rows.append([int(x) for x in line])
    
    return rows


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

