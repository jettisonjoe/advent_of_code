"""Advent of Code 2021

Day 11:
  https://adventofcode.com/2021/day/11
"""

import argparse
import copy
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


def get_neighbors(row, col, max_row=9, max_col=9):
    """Returns an iterable of the cell's neighbors."""
    possible_neighbors = set()
    possible_neighbors.add((row - 1, col - 1))
    possible_neighbors.add((row - 1, col))
    possible_neighbors.add((row - 1, col + 1))
    possible_neighbors.add((row, col - 1))
    possible_neighbors.add((row, col + 1))
    possible_neighbors.add((row + 1, col - 1))
    possible_neighbors.add((row + 1, col))
    possible_neighbors.add((row + 1, col + 1))

    invalid_cells = set()
    for possibility in possible_neighbors:
        n_row, n_col = possibility
        if n_row < 0 or n_col < 0 or n_row > max_row or n_col > max_col:
            invalid_cells.add(possibility)
    
    return possible_neighbors - invalid_cells


def step(grid_state):
    """Mutate the grid state to complete a step, returning number of flashes."""
    to_flash = set()
    max_row = len(grid_state) - 1
    max_col = len(grid_state[0]) - 1
    for row in range(len(grid_state)):
        for col in range(len(grid_state[0])):
            grid_state[row][col] += 1
            if grid_state[row][col] > 9:
                to_flash.add((row, col))
    
    has_flashed = set()
    while to_flash:
        row, col = to_flash.pop()
        has_flashed.add((row, col))
        grid_state[row][col] = 0
        for n_row, n_col in get_neighbors(row, col, max_row, max_col):
            if (n_row, n_col) not in has_flashed:
                grid_state[n_row][n_col] += 1
                if grid_state[n_row][n_col] > 9:
                    to_flash.add((n_row, n_col))
    
    return len(has_flashed)


def solve_part_1(puzzle_input):
    """Solve part 1 of today's puzzle."""
    grid_state = copy.deepcopy(puzzle_input)
    num_flashes = 0
    for i in range(100):
        num_flashes += step(grid_state)
    
    return num_flashes


def solve_part_2(puzzle_input):
    """Solve part 2 of today's puzzle."""
    grid_state = copy.deepcopy(puzzle_input)
    step_count = 0
    while True:
        num_flashes = step(grid_state)
        step_count += 1
        if num_flashes == len(grid_state) * len(grid_state[0]):
            return step_count


def run_tests():
    """Run regression tests."""
    small_input = [
        [1, 1, 1, 1, 1],
        [1, 9, 9, 9, 1],
        [1, 9, 1, 9, 1],
        [1, 9, 9, 9, 1],
        [1, 1, 1, 1, 1],
    ]
    small_expected_step = [
        [3, 4, 5, 4, 3],
        [4, 0, 0, 0, 4],
        [5, 0, 0, 0, 5],
        [4, 0, 0, 0, 4],
        [3, 4, 5, 4, 3],
    ]
    step(small_input)
    assert small_input == small_expected_step

    sample_input = [
        [5, 4, 8, 3, 1, 4, 3, 2, 2, 3],
        [2, 7, 4, 5, 8, 5, 4, 7, 1, 1],
        [5, 2, 6, 4, 5, 5, 6, 1, 7, 3],
        [6, 1, 4, 1, 3, 3, 6, 1, 4, 6],
        [6, 3, 5, 7, 3, 8, 5, 4, 7, 8],
        [4, 1, 6, 7, 5, 2, 4, 6, 4, 5],
        [2, 1, 7, 6, 8, 4, 1, 7, 2, 1],
        [6, 8, 8, 2, 8, 8, 1, 1, 3, 4],
        [4, 8, 4, 6, 8, 4, 8, 5, 5, 4],
        [5, 2, 8, 3, 7, 5, 1, 5, 2, 6],
    ]
    assert 1656 == solve_part_1(sample_input)
    assert 195 == solve_part_2(sample_input)


def format_input(puzzle_input):
    """Format the puzzle input."""
    formatted_input = []
    for line in puzzle_input.splitlines():
        formatted_input.append([int(x) for x in line])
    
    return formatted_input


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

