"""Advent of Code 2021

Day ?:
  https://adventofcode.com/2021/day/
"""

import argparse
from pathlib import Path
import textwrap


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


class UnmatchedError(Exception):
    """Unmatched chunk closing character."""


CHUNK_TYPES = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>',
}

ERROR_POINTS = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}

SYNTAX_POINTS = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
}


def validate_line(line):
    """Validate the chunks on the given line."""
    stack = []
    for char in line:
        if char in CHUNK_TYPES:
            stack.append(CHUNK_TYPES[char])
            continue
        if char != stack[-1]:
            err = UnmatchedError(f'Expected "{stack[-1]}", found "{char}"')
            err.closing_char = char
            raise err
        stack.pop()
    
    return stack[::-1]


def solve_part_1(puzzle_input):
    """Solve part 1 of today's puzzle."""
    error_points = 0
    for line in puzzle_input:
        try:
            validate_line(line)
        except UnmatchedError as err:
            error_points += ERROR_POINTS[err.closing_char]
    
    return error_points


def solve_part_2(puzzle_input):
    """Solve part 2 of today's puzzle."""
    syntax_scores = []
    for line in puzzle_input:
        try:
            unmatched = validate_line(line)
            syntax_score = 0
            for char in unmatched:
                syntax_score *= 5
                syntax_score += SYNTAX_POINTS[char]
            syntax_scores.append(syntax_score)
        except UnmatchedError:
            continue
    
    return sorted(syntax_scores)[len(syntax_scores) // 2]


def run_tests():
    """Run regression tests."""
    sample_input = textwrap.dedent("""\
        [({(<(())[]>[[{[]{<()<>>
        [(()[<>])]({[<{<<[]>>(
        {([(<{}[<>[]}>{[]{[(<()>
        (((({<>}<{<{<>}{[]{[]{}
        [[<[([]))<([[{}[[()]]]
        [{[{({}]{}}([{[{{{}}([]
        {<[[]]>}<{[{[{[]{()[[[]
        [<(<(<(<{}))><([]([]()
        <{([([[(<>()){}]>(<<{{
        <{([{{}}[<[[[<>{}]]]>[]]
    """).splitlines()

    assert 26397 == solve_part_1(sample_input)
    assert 288957 == solve_part_2(sample_input)


def format_input(puzzle_input):
    """Format the puzzle input."""
    return puzzle_input.splitlines()


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

