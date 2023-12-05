import argparse


def _parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument('infile',
                        type=argparse.FileType('r'),
                        help='Input text file for this puzzle')
    args = parser.parse_args()
    return args.infile.read().splitlines()


class SeatingSystem:
    DIRECTIONS = {
        'n':  (-1, 0),
        'ne': (-1, 1),
        'e':  (0, 1),
        'se': (1, 1),
        's':  (1, 0),
        'sw': (1, -1),
        'w':  (0, -1),
        'nw': (-1, -1),
    }

    def __init__(self, state):
        self._state = state
        self.ticks = 0

    def __repr__(self):
        return '\n'.join(self._state)

    @property
    def empty_seats(self):
        return sum(row.count('L') for row in self._state)

    @property
    def filled_seats(self):
        return sum(row.count('#') for row in self._state)

    def _in_bounds(self, x, y):
        return 0 <= x < len(self._state) and 0 <= y < len(self._state[0])

    def neighbors(self, i, j, r=1):
        result = []
        rows = len(self._state)
        cols = len(self._state[0])
        for row in range(max(0, i - r), min(rows, i + r + 1)):
            for col in range(max(0, j - r), min(cols, j + r + 1)):
                if row == i and col == j:
                    continue
                result.append(self._state[row][col])
        return result

    def visibles(self, i, j):
        result = []
        for direction, (dx, dy) in self.DIRECTIONS.items():
            x = i + dx
            y = j + dy
            while self._in_bounds(x, y):
                val = self._state[x][y]
                if val in ('L', '#'):
                    result.append(val)
                    break
                x += dx
                y += dy
        return result

    def advance(self, locator_func=None, crowded=4):
        if locator_func is None:
            locator_func = self.neighbors
        delta = 0
        rows = len(self._state)
        cols = len(self._state[0])
        result = []
        for i in range(rows):
            new_row = ''
            for j in range(cols):
                cur = self._state[i][j]
                seats_to_check = locator_func(i, j)
                if cur == 'L' and seats_to_check.count('#') == 0:
                    new_row += '#'
                    delta += 1
                    continue
                if cur == '#' and seats_to_check.count('#') >= crowded:
                    new_row += 'L'
                    delta += 1
                    continue
                new_row += cur
            result.append(new_row)
        self.ticks += 1
        self._state = result
        return delta


def main(data):
    system = SeatingSystem(data)
    while system.advance():
        continue
    answer_one = system.filled_seats
    system = SeatingSystem(data)
    while system.advance(locator_func=system.visibles, crowded=5):
        continue
    answer_two = system.filled_seats
    return answer_one, answer_two


if __name__ == '__main__':
    answer_one, answer_two = main(_parse_args())
    print(f'Part One: {answer_one}')
    print(f'Part Two: {answer_two}')
