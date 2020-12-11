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
    return args.infile.readlines()


def partition(operations, left_op, right_op, start, end):
    lower = start
    upper = end
    for op in operations:
        mid = (lower + upper) // 2
        if op == left_op:
            upper = mid
            continue
        if op == right_op:
            lower = mid + 1
            continue
        raise ValueError(f'Invalid paritioning operation: {op}')
    if lower != upper:
        raise RuntimeError(f'Binary partitioning fail: {lower}, {upper}')
    return lower


def seat_from_code(code):
    row = partition(code[:7], 'F', 'B', 0, 127)
    col = partition(code[-3:], 'L', 'R', 0, 7)
    seat_id = (8 * row) + col
    return row, col, seat_id


def main(input):
    seats = [seat_from_code(line.rstrip()) for line in input]
    seat_ids = [seat_id for _, _, seat_id in seats]
    answer_one = max(seat_ids)
    print(f'Part One: {answer_one}')
    all_seats = [x for x in range(min(seat_ids), max(seat_ids) + 1)]
    for seat in seat_ids:
        all_seats.remove(seat)
    if len(all_seats) != 1:
        raise RuntimeError(f'Failed to locate seat: {all_seats}')
    answer_two = all_seats[0]
    print(f'Part Two: {answer_two}')


if __name__ == '__main__':
    main(_parse_input())
