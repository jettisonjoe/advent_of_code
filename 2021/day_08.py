"""Advent of Code 2021

Day 8:
  https://adventofcode.com/2021/day/8
"""

import argparse
import itertools
from os import supports_follow_symlinks
from pathlib import Path

DIG_TO_SEG = {
    0: 'abcefg',
    1: 'cf',
    2: 'acdeg',
    3: 'acdfg',
    4: 'bcdf',
    5: 'abdfg',
    6: 'abdefg',
    7: 'acf',
    8: 'abcdefg',
    9: 'abcdfg',
}

SEG_TO_DIG = {seg: dig for dig, seg in DIG_TO_SEG.items()}


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


def generate_decoder(patterns):
    """Return a decoder dict for the given set of patterns.
    
    1, 4, 7, 8 can be known by lengths alone.

    set(7) - set(1) -> a
    if len(set(4).intersect(x)) == 4 -> x == 9
    set(8) - set(9) -> e
    2 is 5 segs and has e in it
    f is in 3 and 5 but not in 2
    c is the other thing in 1 besides f
    0 - acefg -> b
    3 - acfg -> d
    """
    patterns = sorted(patterns, key=len)
    by_len = {k: tuple(g) for k, g in itertools.groupby(patterns, len)}
    solution = {}
    
    one_set = set(by_len[2][0])
    four_set = set(by_len[4][0])
    seven_set = set(by_len[3][0])
    eight_set = set(by_len[7][0])

    a_set = seven_set - one_set
    solution[a_set.copy().pop()] = 'a'

    for nine_candidate in by_len[6]:
        if len(four_set & set(nine_candidate)) == 4:
            nine_set = set(nine_candidate)
    e_set = eight_set - nine_set
    solution[e_set.copy().pop()] = 'e'
    
    three_and_five = []
    for two_candidate in by_len[5]:
        if e_set.copy().pop() in two_candidate:
            two_set = set(two_candidate)
        else:
            three_and_five.append(set(two_candidate))
    three_intersect_five = three_and_five[0] & three_and_five[1]
    f_set = three_intersect_five - two_set
    solution[f_set.copy().pop()] = 'f'

    c_set = one_set - f_set
    solution[c_set.copy().pop()] = 'c'

    b_and_d_set = four_set - c_set - f_set

    b_set = b_and_d_set - two_set
    solution[b_set.copy().pop()] = 'b'

    d_set = b_and_d_set - b_set
    solution[d_set.copy().pop()] = 'd'

    g_set = eight_set - a_set - b_set - c_set - d_set - e_set - f_set
    solution[g_set.copy().pop()] = 'g'

    return solution


def solve_part_1(puzzle_input):
    """Solve part 1 of today's puzzle."""
    num_sentinels = 0
    for _, output_val in puzzle_input:
        for digit in output_val:
            if len(digit) in (2, 3, 4, 7):
                num_sentinels += 1
    
    return num_sentinels


def solve_part_2(puzzle_input):
    """Solve part 2 of today's puzzle."""
    final_sum = 0
    for pattern, out_val in puzzle_input:
        decoder = generate_decoder(pattern)
        num_str = ''
        for digit in out_val:
            seg_str = ''.join(sorted(decoder[c] for c in digit))
            num_str += str(SEG_TO_DIG[seg_str])
        final_sum += int(num_str)

    return final_sum


def run_tests():
    """Run regression tests."""
    sample_input = (
        ('be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb'.split(),
         'fdgacbe cefdb cefbgd gcbe'.split()),
        ('edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec'.split(),
         'fcgedb cgb dgebacf gc'.split()),
        ('fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef'.split(),
         'cg cg fdcagb cbg'.split()),
        ('fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega'.split(),
         'efabcd cedba gadfec cb'.split()),
        ('aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga'.split(),
         'gecf egdcabf bgf bfgea'.split()),
        ('fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf'.split(),
         'gebdcfa ecba ca fadegcb'.split()),
        ('dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf'.split(),
         'cefg dcbef fcge gbcadfe'.split()),
        ('bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd'.split(),
         'ed bcgafe cdgba cbgef'.split()),
        ('egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg'.split(),
         'gbdfcae bgc cg cgb'.split()),
        ('gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc'.split(),
         'fgae cfgab fg bagce'.split()),
    )
    assert 26 == solve_part_1(sample_input)


def format_input(puzzle_input):
    """Format the puzzle input."""
    result = []
    for line in puzzle_input.splitlines():
        patterns, out_val = line.split('|')
        result.append((patterns.split(), out_val.split()))

    return result



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
