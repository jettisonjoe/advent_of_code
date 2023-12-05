import argparse
import sys


def _parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument('sequence',
                        type=str,
                        help='String of digits to use as puzzle input.')
    return parser.parse_args()


class Cup:
    def __init__(self, val):
        self.val = val
        self.left = self
        self.right = self

    def __repr__(self):
        return self.stringify(delimiter=' ', include_self=True)

    def pop(self, n):
        """Removes n cups from the circle and returns the new head"""
        head = self
        for _ in range(n):
            head = head.right
        popped_tail = head.left
        popped_tail.right = self
        head.left = self.left
        self.left.right = head
        self.left = popped_tail
        return head

    def insert(self, cup):
        """Insert the ring of cups to our right."""
        old_right = self.right
        self.right = cup
        cup.left.right = old_right
        old_right.left = cup.left
        cup.left = self

    def stringify(self, delimiter=None, include_self=False):
        """Returns a string representation of the linked list."""
        result = []
        if delimiter is None:
            delimiter = ''
        if include_self:
            result.append(f'({self.val})')
        cur = self
        while cur != self.left:
            result.append(str(cur.right.val))
            cur = cur.right
        return delimiter.join(result)


def play_crab_cups(sequence, num_moves, debug=False):
    cup_map = {}
    lowest, highest = min(sequence), max(sequence)
    first = Cup(sequence[0])
    cup_map[first.val] = first

    prev = first
    for i in range(1, len(sequence)):
        cup = Cup(sequence[i])
        prev.insert(cup)
        cup_map[cup.val] = cup
        prev = cup

    current = first
    for move in range(num_moves):
        if debug:
            sys.stdout.write(f'move {move}/{num_moves}                \r')
            sys.stdout.flush()
        pickup = current.right
        pickup.pop(3)
        pickup_vals = [pickup.val, pickup.right.val, pickup.right.right.val]
        dest = current.val
        while dest == current.val or dest in pickup_vals or dest not in cup_map:
            dest -= 1
            if dest < lowest:
                dest = highest
        cup_map[dest].insert(pickup)
        current = current.right

    return cup_map


def run_tests():
    sample_input = [int(x) for x in '389125467']
    assert '92658374' == play_crab_cups(sample_input, 10)[1].stringify()
    assert '67384529' == play_crab_cups(sample_input, 100)[1].stringify()
    highest = max(sample_input)
    sample_input.extend(range(highest + 1, 1000001))
    cup_map = play_crab_cups(sample_input, 10000000)
    assert 149245887792 == cup_map[1].right.val * cup_map[1].right.right.val


def main(sequence):
    run_tests()
    puzzle_input = [int(x) for x in sequence]
    answer_one = play_crab_cups(puzzle_input, 100)[1].stringify()
    highest = max(puzzle_input)
    puzzle_input.extend(range(highest + 1, 1000001))
    cup_map = play_crab_cups(puzzle_input, 10000000)
    answer_two = cup_map[1].right.val * cup_map[1].right.right.val
    return answer_one, answer_two


if __name__ == '__main__':
    answer_one, answer_two = main(**vars(_parse_args()))
    print(f'Part One: {answer_one}')
    print(f'Part Two: {answer_two}')
