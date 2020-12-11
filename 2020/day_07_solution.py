import argparse


def _parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument('infile',
                        type=argparse.FileType('r'),
                        help='Input text file for this puzzle')
    args = parser.parse_args()
    return args.infile.read().splitlines()


def parse_rules(input):
    rules = {}
    for line in input:
        left, right = line.split(' bags contain ')
        if right == 'no other bags.':
            rules[left] = None
            continue
        options = []
        for piece in right.split(', '):
            words = piece.split()
            number = int(words[0])
            name = ' '.join(words[1:-1])
            options.append((number, name))
        rules[left] = options
    return rules


def can_hold(outer, inner, rules):
    if rules[outer] is None:
        return False
    options = [name for number, name in rules[outer]]
    if inner in options:
        return True
    return any(can_hold(option,inner, rules) for option in options)


def origins_for(color, rules):
    origins = set()
    for outer in rules:
        if outer != color and can_hold(outer, color, rules):
            origins.add(outer)
    return origins


def total_inner_bags(color, rules):
    if rules[color] == None:
        return 0
    total = 0
    for number, name in rules[color]:
        total += number
        total += number * (total_inner_bags(name, rules))
    return total


def main(input):
    rules = parse_rules(input)
    answer_one = len(origins_for('shiny gold', rules))
    answer_two = total_inner_bags('shiny gold', rules)
    return answer_one, answer_two


if __name__ == '__main__':
    answer_one, answer_two = main(_parse_args())
    print(f'Part One: {answer_one}')
    print(f'Part Two: {answer_two}')
