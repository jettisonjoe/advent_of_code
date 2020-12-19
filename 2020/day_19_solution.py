import argparse
import collections


def _parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument('infile',
                        type=argparse.FileType('r'),
                        help='Input text file for this puzzle')
    args = parser.parse_args()
    return args.infile.read().splitlines()


Partial = collections.namedtuple('Partial', ('head', 'remainder'))


def can_gen(msg, rule, grammar):
    """True if the msg can be produced by the rule from the grammar."""
    stack = []
    for choice in rule:
        stack.append(Partial('', list(choice)))
    while stack:
        partial = stack.pop()
        next_part = grammar[partial.remainder.pop(0)]
        if isinstance(next_part, str):
            new_head = partial.head + next_part
            if not msg.startswith(new_head):
                continue
            if not partial.remainder:
                if new_head == msg:
                    return True
                continue
            stack.append(Partial(new_head, list(partial.remainder)))
            continue
        for choice in next_part:
            stack.append(Partial(partial.head,
                                 list(choice) + list(partial.remainder)))
    return False


def run_tests():
    grammar = {
        0: ((4, 1, 5),),
        1: ((2, 3), (3, 2)),
        2: ((4, 4), (5, 5)),
        3: ((4, 5), (5, 4)),
        4: "a",
        5: "b",
    }
    messages = (
        "ababbb",
        "bababa",
        "abbbab",
        "aaabbb",
        "aaaabbb",
    )
    assert 2 == len([m for m in messages if can_gen(m, grammar[0], grammar)])


def grammar_and_msgs(input_lines):
    """Returns (grammar, messages) from puzzle input lines."""
    grammar = {}
    messages = []
    for line in input_lines:
        if ':' in line:
            num, expn = line.split(':')
            if '"' in expn:
                grammar[int(num)] = expn[2:3]
                continue
            choices = []
            for choice in expn.split('|'):
                choices.append(tuple(int(x) for x in choice.split()))
            grammar[int(num)] = tuple(choices)
            continue
        elif line:
            messages.append(line)
    return grammar, messages


def main(input_lines):
    run_tests()
    grammar, messages = grammar_and_msgs(input_lines)
    answer_one = len([m for m in messages if can_gen(m, grammar[0], grammar)])
    grammar[8] = ((42,), (42, 8))
    grammar[11] = ((42, 31), (42, 11, 31))
    answer_two = len([m for m in messages if can_gen(m, grammar[0], grammar)])
    return answer_one, answer_two


if __name__ == '__main__':
    answer_one, answer_two = main(_parse_args())
    print(f'Part One: {answer_one}')
    print(f'Part Two: {answer_two}')
