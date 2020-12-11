import argparse
import collections


Passwd = collections.namedtuple('Passwd',
                               ('lower', 'upper', 'letter', 'passwd'))


def _parse_input():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument('infile',
                        type=argparse.FileType('r'),
                        help='Input text file for this puzzle')
    args = parser.parse_args()
    result = []
    for line in args.infile.readlines():
        first, middle, passwd = line.split()
        lower, upper = first.split('-')
        letter = middle[:-1]
        result.append(Passwd(int(lower), int(upper), letter, passwd))
    return result


def validate_for_part_one(input):
    valid = []
    invalid = []
    for entry in input:
        occurences = entry.passwd.count(entry.letter)
        if entry.lower <= occurences <= entry.upper:
            valid.append(entry)
            continue
        invalid.append(entry)
    return valid, invalid


def validate_for_part_two(input):
    valid = []
    invalid = []
    for entry in input:
        occurences = (entry.passwd[entry.lower - 1] == entry.letter,
                      entry.passwd[entry.upper - 1] == entry.letter)
        if any(occurences) and not all(occurences):
            valid.append(entry)
            continue
        invalid.append(entry)
    return valid, invalid


if __name__ == '__main__':
    valid, invalid = validate_for_part_one(_parse_input())
    answer_one = len(valid)
    print(f'Part One: {answer_one}')
    valid, invalid = validate_for_part_two(_parse_input())
    answer_two = len(valid)
    print(f'Part Two: {answer_two}')