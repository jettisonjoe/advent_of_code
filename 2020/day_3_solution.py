import argparse
import functools
import operator


def _parse_input():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument('infile',
                        type=argparse.FileType('r'),
                        help='Input text file for this puzzle')
    args = parser.parse_args()
    return args.infile.readlines()


def trees_for_slope(dx, dy, field):
    trees = 0
    x, y = 0, 0
    while y < len(field):
        if field[y][x] == '#':
            trees += 1
        x = (x + dx) % (len(field[0]) - 1)
        y += dy
    return trees


if __name__ == '__main__':
    answer_one = trees_for_slope(3, 1, _parse_input())
    print(f'Part One: {answer_one}')
    field = _parse_input()
    slopes_to_try = ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2))
    tree_counts = (trees_for_slope(x, y, field) for x, y in slopes_to_try)
    answer_two = functools.reduce(operator.mul, tree_counts, 1)
    print(f'Part Two: {answer_two}')