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


class Ship:
    DIRECTIONS = collections.OrderedDict(
        E=(1, 0),
        S=(0, 1),
        W=(-1, 0),
        N=(0, -1)
    )

    ROTATIONS = {
        'R': 1,
        'L': -1,
    }

    def __init__(self):
        self.x = 0
        self.y = 0
        self.rot = 'E'

    def navigate(self, steps):
        for step in steps:
            op = step[0]
            mag = int(step[1:])
            if op in self.ROTATIONS:
                self.rotate(op, mag)
                continue
            if op in self.DIRECTIONS:
                self.move(op, mag)
                continue
            if op == 'F':
                self.forward(mag)
                continue

    def rotate(self, hand, degrees):
        dirs = [x for x in self.DIRECTIONS]
        turns = degrees // 90
        idx = dirs.index(self.rot)
        idx = (idx + (turns * self.ROTATIONS[hand])) % len(dirs)
        self.rot = dirs[idx]

    def move(self, direction, mag):
        dx, dy = self.DIRECTIONS[direction]
        self.x += mag * dx
        self.y += mag * dy

    def forward(self, mag):
        self.move(self.rot, mag)


class WaypointShip(Ship):
    def __init__(self, waypoint=(10, -1)):
        super().__init__()
        self.wx, self.wy = waypoint

    def move(self, direction, mag):
        dx, dy = self.DIRECTIONS[direction]
        self.wx += mag * dx
        self.wy += mag * dy

    def rotate(self, hand, degrees):
        degrees = degrees % 360
        if hand == 'L':
            degrees = 360 - degrees
        turns = degrees // 90
        for turn in range(turns):
            sy = 1 if self.wx >= 0 else -1
            sx = 1 if self.wy < 0 else -1
            old_wx = self.wx
            self.wx = abs(self.wy) * sx
            self.wy = abs(old_wx) * sy

    def forward(self, mag):
        self.x += self.wx * mag
        self.y += self.wy * mag


def main(data):
    ship = Ship()
    ship.navigate(data)
    answer_one = abs(ship.x) + abs(ship.y)
    ship = WaypointShip()
    ship.navigate(data)
    answer_two = abs(ship.x) + abs(ship.y)
    return answer_one, answer_two


if __name__ == '__main__':
    answer_one, answer_two = main(_parse_args())
    print(f'Part One: {answer_one}')
    print(f'Part Two: {answer_two}')
