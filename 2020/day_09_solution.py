import argparse
import collections
import itertools


def _parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument('infile',
                        type=argparse.FileType('r'),
                        help='Input text file for this puzzle')
    parser.add_argument('preamble_len',
                        type=int,
                        help='Length of XMAS encryption preamble')
    args = parser.parse_args()
    return args.infile.read().splitlines(), args.preamble_len


class Validator:
    def __init__(self, preamble_len):
        self._preamble_len = preamble_len
        self._preamble = collections.deque()

    def validate(self, val):
        valids = [sum(x) for x in itertools.combinations(self._preamble, 2)]
        return val in valids

    def advance(self, val):
        if len(self._preamble) < self._preamble_len:
            self._preamble.append(val)
            return
        if not self.validate(val):
            return val
        self._preamble.append(val)
        self._preamble.popleft()

    def feed(self, sequence):
        for element in sequence:
            status = self.advance(element)
            if status is not None:
                return status


def weakness(val, seq):
    for length in range(1, len(seq)):
        for start in range(0, len(seq) - length):
            end = start + length
            sub_seq = seq[start:end + 1]
            if sum(sub_seq) == val:
                return min(sub_seq) + max(sub_seq)


def main(input, preamble_len):
    seq = [int(x) for x in input]
    validator = Validator(preamble_len)
    answer_one = validator.feed(seq)
    answer_two = weakness(answer_one, seq)
    return answer_one, answer_two


if __name__ == '__main__':
    answer_one, answer_two = main(*_parse_args())
    print(f'Part One: {answer_one}')
    print(f'Part Two: {answer_two}')
