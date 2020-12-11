import argparse
import functools
import itertools


def _parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument('infile',
                        type=argparse.FileType('r'),
                        help='Input text file for this puzzle')
    args = parser.parse_args()
    return args.infile.read()


def uniques_in_group(group):
    return len(set(itertools.chain.from_iterable(group)) - {'\n'})


def intersection(a, b):
    return set(a).intersection(set(b))


def intersection_size_in_group(group):
    return len(functools.reduce(intersection, group))


def main(input):
    groups = [group.split('\n') for group in input.split('\n\n')]
    answer_one = sum(uniques_in_group(group) for group in groups)
    answer_two = sum(intersection_size_in_group(group) for group in groups)
    return answer_one, answer_two


if __name__ == '__main__':
    answer_one, answer_two = main(_parse_args())
    print(f'Part One: {answer_one}')
    print(f'Part Two: {answer_two}')
