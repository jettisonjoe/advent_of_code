import argparse


def _parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument('infile',
                        type=argparse.FileType('r'),
                        help='Input text file for this puzzle')
    args = parser.parse_args()
    return [int(x) for x in args.infile.read().splitlines()]


class AdapterChain:
    def __init__(self, chain=None, max_diff=3):
        self._max_diff = max_diff
        if chain is None:
            chain = [0]
        self._chain = chain

    def __repr__(self):
        result = f'[({self.head()})'
        if len(self._chain) > 2:
            result += ', '
            result += ', '.join(str(x) for x in self._chain[1:-1])
        result += f', ({self.tail()})]'
        return result

    def __len__(self):
        return len(self._chain)

    def add(self, val):
        if 0 < val - self.tail() > self._max_diff:
            return None
        self._chain.append(val)
        return self

    def copy(self):
        return self.__class__(self._chain[:], self._max_diff)

    def is_valid(self):
        return all(0 <= x <= self._max_diff for x in self.diffs())

    def diffs(self):
        result = []
        for i in range(1, len(self._chain)):
            result.append(self._chain[i] - self._chain[i-1])
        return result

    def head(self):
        return self._chain[0]

    def tail(self):
        return self._chain[len(self._chain) - 1]

    def valid_partials(self, start=0, end=None, copy_class=None):
        """Returns all valid sequences that can be made with our adapters.

        NOTE: Slooowwwwww! Try to reduce the number of times this runs,
        because it's O(n^2) at best, even when copying with stub chains.
        """
        if copy_class is None:
            copy_class = self.__class__
        if end is None:
            end = len(self._chain)
        in_progress = {copy_class([self._chain[start]], self._max_diff)}
        for i in range(start + 1, end):
            to_add = set()
            to_remove = set()
            for start in in_progress:
                candidate = start.copy()
                if candidate.add(self._chain[i]):
                    to_add.add(candidate)
                else:
                    to_remove.add(start)
            for valid in to_add:
                in_progress.add(valid)
            for invalid in to_remove:
                in_progress.remove(invalid)
        return [p for p in in_progress if p.tail() == self._chain[end-1]]


class StubAdapterChain(AdapterChain):
    def __init__(self, chain=None, max_diff=3):
        if chain is None:
            chain = [0]
        super().__init__([chain[0], chain[-1]], max_diff)

    def add(self, val):
        if 0 < val - self.tail() > self._max_diff:
            return None
        self._chain[-1] = val
        return self


def main(input):
    chain = AdapterChain([0] + sorted(input) + [max(input) + 3])
    diffs = chain.diffs()
    answer_one = diffs.count(1) * diffs.count(3)
    # Break the input down into sub-problems. This helps when there are some
    # adapters in the chain that can never be removed because the gaps on one
    # or the other side of them are too great. Pragmatically, this approach
    # works for my input, but it would still have terrible performace on
    # very large inputs or inputs with few or no always-included adapters.
    end = 0
    partial_count = 1
    while end < len(diffs):
        start = end
        end = diffs.index(3, end) + 1
        valids = chain.valid_partials(start=start, end=end)
        partial_count *= len(valids)
    answer_two = partial_count
    return answer_one, answer_two


if __name__ == '__main__':
    answer_one, answer_two = main(_parse_args())
    print(f'Part One: {answer_one}')
    print(f'Part Two: {answer_two}')
