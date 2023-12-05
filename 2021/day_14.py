"""Advent of Code 2021

Day 14:
  https://adventofcode.com/2021/day/14
"""

import argparse
import collections
from pathlib import Path
import pprint

import aoc


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


def apply_insertions(template, rules, rounds=1, debug=False):
    """Apply the insertion rules to the template and return the result."""
    polymer = template[:]
    for i in range(rounds):
        if debug:
            print(f'round {i}')
        result = [polymer[0]]
        for idx, char in enumerate(polymer):
            if idx == 0:
                continue
            pair = polymer[idx-1:idx+1]
            val = rules[pair]
            result.append(val)
            result.append(char)

        polymer = ''.join(result)
    
    return polymer

def find_growth_rates(template, rules, rounds=20, debug=False):
    """Find the stablized growth rates of each element in the system."""
    polymer = template[:]
    original_freqs = aoc.Frequencies(tuple(polymer))
    growth_rates = {}

    for i in range(1, rounds + 1):
        new_polymer = apply_insertions(polymer, rules)
        new_freqs = aoc.Frequencies(tuple(new_polymer))
        for element, count in new_freqs.freqs.items():
            growth_rates[element] = ((new_freqs.freqs[element]
                                      - original_freqs.freqs[element]) / i)
        polymer = new_polymer
        if debug:
            pprint.pprint(growth_rates['B'])


def solve_part_1(puzzle_input):
    """Solve part 1 of today's puzzle."""
    template, rules = puzzle_input
    result = apply_insertions(template, rules, 10)
    freqs = aoc.Frequencies(result)
    return freqs[freqs.most_common] - freqs[freqs.least_common]


def solve_part_2(puzzle_input):
    """Solve part 2 of today's puzzle."""
    template, rules = puzzle_input
    # result = apply_insertions(template, rules, 40, debug=True)
    # freqs = aoc.Frequencies(result)
    # return freqs[freqs.most_common] - freqs[freqs.least_common]
    # find_growth_rates(template, rules, rounds=40, debug=True)
    polymer = 'BC'
    for _ in range(8):
        print(polymer)
        polymer = apply_insertions(polymer, rules)



def run_tests():
    """Run regression tests."""
    sample_template = 'NNCB'
    sample_rules = {
        'CH': 'B',
        'HH': 'N',
        'CB': 'H',
        'NH': 'C',
        'HB': 'C',
        'HC': 'B',
        'HN': 'C',
        'NN': 'C',
        'BH': 'H',
        'NC': 'B',
        'NB': 'B',
        'BN': 'B',
        'BB': 'N',
        'BC': 'B',
        'CC': 'N',
        'CN': 'C',
    }
    assert 1588 == solve_part_1((sample_template, sample_rules))
    assert 2188189693529 == solve_part_2((sample_template, sample_rules))


def format_input(puzzle_input):
    """Format the puzzle input."""
    lines = puzzle_input.splitlines()
    template = lines[0]
    
    rules = {}
    for line in lines[2:]:
        key, val = line.split(' -> ')
        rules[key] = val
    
    return template, rules


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
