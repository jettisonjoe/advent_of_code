"""Solver for Advent of Code 2024, day 3."""

import re

DO = "do()"
DONT = "don't()"


class Mul:
    PATTERN = re.compile(r"mul\((?P<x>\d{1,3}),(?P<y>\d{1,3})\)")

    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

    @property
    def value(self):
        return self.x * self.y

    @classmethod
    def from_str(cls, s):
        muls = cls.PATTERN.findall(s)
        if len(muls) == 1:
            return Mul(*muls[0])
        return tuple(Mul(*m) for m in muls)


def run_tests():
    assert 2024 == Mul.from_str("mul(44,46)").value

    test_input = (
        "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
    )
    assert 161 == solve_part_1(test_input)

    test_input = (
        "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
    )
    assert 48 == solve_part_2(test_input)


def remove_donts(raw_input):
    result = []
    segments = raw_input.split(DONT)
    result.append(segments[0])
    for segment in segments[1:]:
        if DO in segment:
            enabled = segment.split(DO)[1:]
            result.extend(enabled)
    return "".join(result)


def solve_part_1(puzzle_input):
    muls = Mul.from_str(puzzle_input)
    return sum(m.value for m in muls)


def solve_part_2(puzzle_input):
    puzzle_input = remove_donts(puzzle_input)
    return solve_part_1(puzzle_input)
