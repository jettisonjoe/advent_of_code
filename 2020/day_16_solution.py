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
    return args.infile.read().splitlines()


def field_and_validator(field_line):
    """Returns a field name and validator function for that field, or None"""
    try:
        field_name, ranges_string = field_line.split(': ')
    except ValueError:
        return None, None
    ranges = ranges_string.split(' or ')
    range_tuples = []
    for r in ranges:
        start, end = r.split('-')
        range_tuples.append((int(start), int(end)))

    def validator_func(value):
        for start, end in range_tuples:
            if start <= value <= end:
                return True
        return False

    return field_name, validator_func


def rules_tickets_from_lines(lines):
    """Parse a rules dict and ticket tuples from input lines."""
    your_ticket = None
    rules = {}
    nearby_tickets = []
    for line in lines:
        field_name, validator = field_and_validator(line)
        if field_name is not None:
            rules[field_name] = validator
            continue
        try:
            fields = [int(field) for field in line.split(',')]
        except ValueError:
            continue
        if your_ticket is None:
            your_ticket = fields
            continue
        nearby_tickets.append(fields)
    return rules, your_ticket, nearby_tickets


def invalidate_ticket(rules, ticket):
    errors = []
    for val in ticket:
        validated = False
        if not any(validator(val) for _, validator in rules.items()):
            errors.append(val)
    return errors


def error_rate(rules, tickets):
    total_errors = []
    for ticket in tickets:
        total_errors.extend(invalidate_ticket(rules, ticket))
    return sum(total_errors)


def determine_ticket_fields(rules, tickets):
    """Given a rules dict and an iterable of tickets, return field names."""
    fields = [set(rules.keys()) for _ in rules]
    for i in range(len(tickets[0])):
        for ticket in tickets:
            for field_name, validator in rules.items():
                if not validator(ticket[i]):
                    fields[i].remove(field_name)
                    if len(fields[i]) == 1:
                        uniquefy_fields(*fields[i], i, fields)
    return [f.pop() for f in fields]


def uniquefy_fields(field_name, unique_idx, field_sets):
    for i in range(len(field_sets)):
        if i != unique_idx and field_name in field_sets[i]:
            field_sets[i].remove(field_name)
            if len(field_sets[i]) == 1:
                uniquefy_fields(*field_sets[i], i, field_sets)


def run_tests():
    rules, _, _ = rules_tickets_from_lines((
        'class: 1-3 or 5-7',
        'row: 6-11 or 33-44',
        'seat: 13-40 or 45-50'))
    assert not invalidate_ticket(rules, (7,1,14))
    assert not invalidate_ticket(rules, (7,3,47))
    assert invalidate_ticket(rules, (40,4,50))
    assert invalidate_ticket(rules, (55,2,20))
    assert invalidate_ticket(rules, (38,6,12))
    rules, yours, nearby = rules_tickets_from_lines((
        'class: 0-1 or 4-19',
        'row: 0-5 or 8-19',
        'seat: 0-13 or 16-19',
        '11,12,13',
        '3,9,18',
        '15,1,5',
        '5,14,9'))
    fields = ['row', 'class', 'seat']
    assert determine_ticket_fields(rules, [yours] + nearby) == fields


def main(data):
    run_tests()
    rules, your_ticket, nearby_tickets = rules_tickets_from_lines(data)
    all_tickets = [your_ticket] + nearby_tickets
    answer_one = error_rate(rules, all_tickets)
    invalidator = functools.partial(invalidate_ticket, rules)
    valid_tickets = list(itertools.filterfalse(invalidator, all_tickets))
    field_names = determine_ticket_fields(rules, valid_tickets)
    print(field_names)
    answer_two = 1
    for i in range(len(field_names)):
        if field_names[i].startswith('departure'):
            answer_two *= your_ticket[i]
    return answer_one, answer_two


if __name__ == '__main__':
    answer_one, answer_two = main(_parse_args())
    print(f'Part One: {answer_one}')
    print(f'Part Two: {answer_two}')
