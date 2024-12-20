"""Solver for Advent of Code 2024, day 6."""

import logging
import textwrap


def run_tests():
    test_input = textwrap.dedent(
        """\
        ....#.....
        .........#
        ..........
        ..#.......
        .......#..
        ..........
        .#..^.....
        ........#.
        #.........
        ......#...
    """
    )
    assert 41 == solve_part_1(test_input)
    assert 6 == solve_part_2(test_input)


class PathLoopError(Exception):
    """Patrol path looped!"""


class Guard:
    ROTATIONS = ((0, -1), (1, 0), (0, 1), (-1, 0))

    def __init__(self, x, y):
        self.start_x = x
        self.start_y = y
        self.reset()

    @property
    def dest(self):
        return (self.x + self.heading[0], self.y + self.heading[1])

    def rotate(self):
        current_idx = self.ROTATIONS.index(self.heading)
        self.heading = self.ROTATIONS[(current_idx + 1) % len(self.ROTATIONS)]

    def step(self):
        x, y = self.dest
        self.x = x
        self.y = y
        self.path.append(((x, y), self.heading))
        if ((x, y), self.heading) in self.path[:-1]:
            raise PathLoopError()

    def reset(self):
        self.x = self.start_x
        self.y = self.start_y
        self.heading = (0, -1)
        self.path = [((self.x, self.y), self.heading)]


class Lab:
    def __init__(self, text):
        lines = text.splitlines()
        self.rows = []
        for row_idx, line in enumerate(lines):
            if "^" in line:
                self.guard = Guard(line.index("^"), row_idx)
                line = line.replace("^", ".")
            self.rows.append(line)

    def __getitem__(self, pos):
        x, y = pos
        return self.rows[y][x]

    def __setitem__(self, pos, val):
        x, y = pos
        old_row = self.rows[y]
        new_row = old_row[:x] + val + old_row[x + 1 :]
        self.rows[y] = new_row

    def in_bounds(self, x, y):
        return 0 <= x < len(self.rows[0]) and 0 <= y < len(self.rows)

    def obstructed(self, x, y):
        return self[(x, y)] != "." or (x, y) == (self.guard.x, self.guard.y)

    def resolve_patrol(self):
        while self.in_bounds(*self.guard.dest):
            if self.obstructed(*self.guard.dest):
                self.guard.rotate()
            else:
                self.guard.step()

    def empty_spaces(self):
        result = []
        for row_idx, row in enumerate(self.rows):
            for col_idx, marker in enumerate(row):
                if (self.guard.x, self.guard.y) == (col_idx, row_idx):
                    continue
                if marker == ".":
                    result.append((col_idx, row_idx))

        return tuple(result)


def solve_part_1(puzzle_input):
    lab = Lab(puzzle_input)
    lab.resolve_patrol()
    return len(set(pos for pos, _ in lab.guard.path))


def solve_part_2(puzzle_input):
    lab = Lab(puzzle_input)
    lab.resolve_patrol()
    candidates = set(pos for pos, _ in lab.guard.path[1:])
    lab.guard.reset()

    loop_makers = set()
    for idx, pos in enumerate(candidates):
        logging.debug("Trying obstruction at {}.", pos)
        logging.info("%3.2f%% complete.", (idx / len(candidates)) * 100)
        lab[pos] = "O"
        try:
            lab.resolve_patrol()
        except PathLoopError:
            loop_makers.add(pos)
            continue
        finally:
            lab[pos] = "."
            lab.guard.reset()

    return len(loop_makers)
