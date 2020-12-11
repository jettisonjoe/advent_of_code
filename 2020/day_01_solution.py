import argparse
import functools
import itertools
import operator


def _parse_input():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument('infile',
                        type=argparse.FileType('r'),
                        help='Input text file for this puzzle')
    args = parser.parse_args()
    return (int(line) for line in args.infile.readlines())


def main(input, n):
    for combo in itertools.combinations(input, n):
        if sum(combo) == 2020:
            return functools.reduce(operator.mul, combo, 1)


if __name__ == '__main__':
    answer_one = main(_parse_input(), 2)
    print(f'Part One: {answer_one}')
    answer_two = main(_parse_input(), 3)
    print(f'Part Two: {answer_two}')