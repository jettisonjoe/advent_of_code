import argparse
import collections
import functools
import operator


Creds = collections.namedtuple('Creds',
                              ('lower', 'upper', 'letter', 'passwd'))


def _parse_input():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument('infile',
                        type=argparse.FileType('r'),
                        help='Input text file for this puzzle')
    args = parser.parse_args()
    entries = []
    text = args.infile.read()
    for entry_data in text.split('\n\n'):
        entry = {}
        for field in entry_data.split():
            key, val = field.split(':')
            entry[key] = val
        entries.append(entry)
    return entries


def valid_for_part_one(entry):
    required_fields = ('byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid')
    for field in required_fields:
        if field not in entry:
            return False
    return True


def valid_for_part_two(entry):
    if not valid_for_part_one(entry):
        return False
    field_validations = (
        validate_byr(entry['byr']),
        validate_iyr(entry['iyr']),
        validate_eyr(entry['eyr']),
        validate_hgt(entry['hgt']),
        validate_hcl(entry['hcl']),
        validate_ecl(entry['ecl']),
        validate_pid(entry['pid']),
    )
    if not all(field_validations):
        return False
    return True


def validate_byr(data):
    try:
        return 1920 <= int(data) <= 2002
    except ValueError:
        return False


def validate_iyr(data):
    try:
        return 2010 <= int(data) <= 2020
    except ValueError:
        return False


def validate_eyr(data):
    try:
        return 2020 <= int(data) <= 2030
    except ValueError:
        return False


def validate_hgt(data):
    try:
        units = data[-2:]
        if units == 'cm':
            return 150 <= int(data[:-2]) <= 193
        if units == 'in':
            return 59 <= int(data[:-2]) <= 76
    except ValueError:
        return False
    return False


def validate_hcl(data):
    if len(data) != 7:
        return False
    if not data[0] == '#':
        return False
    for char in data[1:]:
        if char not in ('0123456789abcdef'):
            return False
    return True


def validate_ecl(data):
    return data in ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth')


def validate_pid(data):
    if len(data) != 9:
        return False
    try:
        int(data)
    except ValueError:
        return False
    return True


def main(input):
    valid = [entry for entry in input if valid_for_part_one(entry)]
    answer_one = len(valid)
    print(f'Part One: {answer_one}')
    valid = [entry for entry in input if valid_for_part_two(entry)]
    answer_two = len(valid)
    print(f'Part Two: {answer_two}')    


if __name__ == '__main__':
    main(_parse_input())