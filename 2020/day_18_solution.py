import argparse
import operator

OPERATIONS = {
    '+': operator.add,
    '*': operator.mul,
}


def _parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument('infile',
                        type=argparse.FileType('r'),
                        help='Input text file for this puzzle')
    args = parser.parse_args()
    return args.infile.read().splitlines()


def tokens_from_str(expr):
    """Parse math nouveau tokens from a string."""
    expr = expr.replace('(', ' ( ')
    expr = expr.replace(')', ' ) ')
    return expr.split()


def pop_subexpr(tokens):
    """Pop and return the full subexpr."""
    result = []
    nesting = 1
    while nesting > 0:
        token = tokens.pop(0)
        if token == '(':
            nesting += 1
        if token == ')':
            nesting -= 1
        result.append(token)
    return result[:-1]


def evaluate(tokens):
    """Evaluate the math nouveau expression."""
    acc = None
    op = None
    while tokens:
        val = None
        token = tokens.pop(0)
        if token in OPERATIONS:
            op = OPERATIONS[token]
            continue
        elif token == '(':
            subexpr_tokens = pop_subexpr(tokens)
            val = evaluate(subexpr_tokens)
        else:
            val = int(token)
        if acc is None:
            acc = val
            continue
        acc = op(acc, val)
    return acc


def pop_right_val(tokens):
    while tokens and tokens[0] is not '*':
        token = token.pop(0)



def adv_eval(tokens):
    """Evaluate the math nouveau expression with "advanced" rules."""
    stack = []
    while tokens:
        token = tokens.pop(0)
        if not stack:
            if token == '(':
                stack.append(adv_eval(pop_subexpr(tokens)))
            else:
                stack.append(int(token))
            continue
        if token in OPERATIONS:
            stack.append(token)
            continue
        if token == '(':
            val = adv_eval(pop_subexpr(tokens))
        else:
            val = int(token)
        if stack[-1] == '+':
            stack.pop()
            temp = stack.pop()
            stack.append(temp + val)
            continue
        if stack[-1] == '*':
            stack.append(val)
            continue

    acc = stack.pop(0)
    while stack:
        stack.pop(0)
        acc = acc * stack.pop(0)
    return acc


def run_tests():
    assert 71 == evaluate(tokens_from_str('1 + 2 * 3 + 4 * 5 + 6'))
    assert 51 == evaluate(tokens_from_str('1 + (2 * 3) + (4 * (5 + 6))'))
    assert 26 == evaluate(tokens_from_str('2 * 3 + (4 * 5)'))
    assert 437 == evaluate(tokens_from_str('5 + (8 * 3 + 9 + 3 * 4 * 3)'))
    assert 12240 == evaluate(
        tokens_from_str('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))'))
    assert 13632 == evaluate(
        tokens_from_str('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2'))
    assert 231 == adv_eval(tokens_from_str('1 + 2 * 3 + 4 * 5 + 6'))
    assert 51 == adv_eval(tokens_from_str('1 + (2 * 3) + (4 * (5 + 6))'))
    assert 46 == adv_eval(tokens_from_str('2 * 3 + (4 * 5)'))
    assert 1445 == adv_eval(tokens_from_str('5 + (8 * 3 + 9 + 3 * 4 * 3)'))
    assert 669060 == adv_eval(
        tokens_from_str('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))'))
    assert 23340 == adv_eval(
        tokens_from_str('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2'))


def main(input_lines):
    run_tests()
    answer_one = sum(evaluate(tokens_from_str(line)) for line in input_lines)
    answer_two = sum(adv_eval(tokens_from_str(line)) for line in input_lines)
    return answer_one, answer_two


if __name__ == '__main__':
    answer_one, answer_two = main(_parse_args())
    print(f'Part One: {answer_one}')
    print(f'Part Two: {answer_two}')
