"""Advent of Code 2021

Day 3:
  https://adventofcode.com/2021/day/3
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
    totals = []
    for _ in puzzle_input[0]:
        totals.append({'0': 0, '1': 0})

    for line in puzzle_input:
        for pos in range(len(line)):
            bit = line[pos]
            totals[pos][bit] += 1
    
    gamma_list = []
    epsilon_list = []
    for bits in totals:
        gamma_list.append('0' if bits['0'] > bits['1'] else '1')
        epsilon_list.append('1' if bits['0'] > bits['1'] else '0')
    
    gamma = int(''.join(gamma_list), 2)
    epsilon = int(''.join(epsilon_list), 2)
    return gamma * epsilon


def most_common_value(corpus, idx):
    """Return the character most commonly found at the given index."""
    counts = {'0': 0, '1': 0}
    for entry in corpus:
        character = entry[idx]
        counts[character] = counts.get(character, 0) + 1
    
    return '0' if counts['0'] > counts['1'] else '1'
    

def solve_part_2(puzzle_input):
    """Solve part 2 of today's puzzle."""
    oxy_gen_rating = None
    c02_scrubber_rating = None

    candidates = set(puzzle_input)
    for idx in range(len(puzzle_input[0])):
        target_value = most_common_value(candidates, idx)
        to_remove = set()
        for candidate in candidates:
            if candidate[idx] != target_value:
                to_remove.add(candidate)
        candidates = candidates - to_remove
        if len(candidates) == 1:
            oxy_gen_rating = candidates.pop()
    
    candidates = set(puzzle_input)
    for idx in range(len(puzzle_input[0])):
        inverse_value = most_common_value(candidates, idx)
        to_remove = set()
        for candidate in candidates:
            if candidate[idx] == inverse_value:
                to_remove.add(candidate)
        candidates = candidates - to_remove
        if len(candidates) == 1:
            c02_scrubber_rating = candidates.pop()
    
    return int(oxy_gen_rating, 2) * int(c02_scrubber_rating, 2)



def run_tests():
    """Run regression tests."""
    sample_input = ['00100',
                    '11110',
                    '10110',
                    '10111',
                    '10101',
                    '01111',
                    '00111',
                    '11100',
                    '10000',
                    '11001',
                    '00010',
                    '01010']
    assert(198 == solve_part_1(sample_input))
    assert(230 == solve_part_2(sample_input))


def format_input(puzzle_input: str):
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

