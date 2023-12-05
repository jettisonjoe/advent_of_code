"""Advent of Code 2021

Day 4:
  https://adventofcode.com/2021/day/4
"""

import argparse
from collections import defaultdict
from pathlib import Path
import textwrap
from typing import DefaultDict


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


class Board():
    def __init__(self, rows):
        self.rows = rows
        self.cols = []
        for i in range(5):
            col = []
            for row in rows:
                col.append(row[i])
            self.cols.append(col)
    
    def has_bingo(self, game_state):
        for row in self.rows:
            if all(game_state[r] for r in row):
                return True
        for col in self.cols:
            if all(game_state[c] for c in col):
                return True
        return False
    
    def unmarked_numbers(self, game_state):
        return [r for row in self.rows for r in row if not game_state[r]]


def solve_part_1(puzzle_input):
    """Solve part 1 of today's puzzle."""
    call, boards = puzzle_input
    game_state = defaultdict(lambda: False)
    for num in call:
        game_state[num] = True
        for board in boards:
            if board.has_bingo(game_state):
                sum_of_unmarked = sum(board.unmarked_numbers(game_state))
                return sum_of_unmarked * num


def solve_part_2(puzzle_input):
    """Solve part 2 of today's puzzle."""
    call, boards = puzzle_input
    game_state = defaultdict(lambda: False)
    boards_left = set(boards)
    for num in call:
        game_state[num] = True
        for board in boards:
            if board not in boards_left:
                continue
            if board.has_bingo(game_state):
                boards_left.remove(board)
                if len(boards_left) == 0:
                    sum_of_unmarked = sum(board.unmarked_numbers(game_state))
                    return sum_of_unmarked * num


def run_tests():
    """Run regression tests."""
    sample_input = textwrap.dedent("""\
        7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

        22 13 17 11  0
         8  2 23  4 24
        21  9 14 16  7
         6 10  3 18  5
         1 12 20 15 19

         3 15  0  2 22
         9 18 13 17  5
        19  8  7 25 23
        20 11 10 24  4
        14 21 16 12  6

        14 21 17 24  4
        10 16 15  9 19
        18  8 23 26 20
        22 11 13  6  5
         2  0 12  3  7
    """)

    assert (4512 == solve_part_1(format_input(sample_input)))


def format_input(puzzle_input: str):
    """Format the puzzle input."""
    lines = puzzle_input.splitlines()
    call = [int(x) for x in lines[0].split(',')]

    boards = []
    next_board_start = 2
    while True:
        board_lines = lines[next_board_start:next_board_start + 5]
        board_rows = []
        for board_line in board_lines:
            board_rows.append([int(x) for x in board_line.split()])
        boards.append(Board(board_rows))
        try:
            next_board_start = lines.index('', next_board_start + 1) + 1
        except ValueError:
            break

    return call, boards


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

