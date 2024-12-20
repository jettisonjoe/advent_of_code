"""Solver for Advent of Code 2024, day 2."""

import textwrap


def run_tests():
    test_input = textwrap.dedent(
        """\
        7 6 4 2 1
        1 2 7 8 9
        9 7 6 2 1
        1 3 2 4 5
        8 6 4 4 1
        1 3 6 7 9
    """
    )
    assert 2 == solve_part_1(test_input)
    assert 4 == solve_part_2(test_input)


class Report:
    def __init__(self, levels):
        self.levels = tuple(levels)

    def __len__(self):
        return len(self.levels)

    @property
    def deltas(self):
        result = []
        for i in range(len(self.levels) - 1):
            result.append(self.levels[i + 1] - self.levels[i])

        return tuple(result)

    @property
    def delta_mags(self):
        return tuple(abs(d) for d in self.deltas)

    @property
    def polarities(self):
        result = []
        for d in self.deltas:
            if d == 0:
                result.append(0)
            else:
                result.append(d // abs(d))
        return tuple(result)

    @property
    def monotonic(self):
        polarities = self.polarities
        if 0 in polarities:
            return False
        return len(set(polarities)) == 1

    @property
    def safe(self):
        if self.monotonic:
            return all(Report.delta_ok(d) for d in self.delta_mags)

    @staticmethod
    def delta_ok(delta):
        return 1 <= delta <= 3

    @staticmethod
    def damp(report):
        if report.safe:
            return report
        for i in range(len(report)):
            candidate_levels = list(report.levels)
            candidate_levels.pop(i)
            candidate = Report(candidate_levels)
            if candidate.safe:
                return candidate
        return report


def make_reports(puzzle_input):
    reports = []
    for line in puzzle_input.splitlines():
        reports.append(Report(int(x) for x in line.split()))

    return tuple(reports)


def solve_part_1(puzzle_input):
    reports = make_reports(puzzle_input)
    return len([r for r in reports if r.safe])


def solve_part_2(puzzle_input):
    reports = make_reports(puzzle_input)
    reports = tuple(Report.damp(r) for r in reports)
    return len([r for r in reports if r.safe])
