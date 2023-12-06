"""Solver for Advent of Code 2023, day 6.

I'm trying today's without type annotations just to remind myself how it used to feel to
write Python in the dark ages.

I did have more dumb bugs today that took a second to figure out than previous days, but
unclear whether it was because of using fewer type annotations and shorter variable
names, or because I was more tired today.

My initial solution is brute forcey but it still runs in (several) seconds on my
(pretty fast) machine. I could probably come up with a faster solution if I did some
algebra, but also kinda why have computers if you're still gonna have to do algebra?
"""

import functools
import logging
import operator
import textwrap


class RaceDoc:
    def __init__(self, races):
        self.races = races

    @classmethod
    def from_str(cls, s):
        time_line, dist_line = s.splitlines()
        times = (int(t) for t in time_line.split(":")[1].split())
        dists = (int(d) for d in dist_line.split(":")[1].split())
        return cls(tuple(zip(times, dists)))

    @classmethod
    def from_kerny_str(cls, s):
        time_line, dist_line = s.splitlines()
        time = int("".join(time_line.split(":")[1].split()))
        dist = int("".join(dist_line.split(":")[1].split()))
        return cls(((time, dist),))

    @staticmethod
    def ways_to_win(r):
        time, dist = r
        ways = []
        for t in range(1, time + 1):
            our_dist = t * (time - t)
            logging.debug(f"hold for {t}, travel {our_dist}")
            if our_dist > dist:
                ways.append(t)
        return tuple(ways)


def run_tests():
    test_input = textwrap.dedent(
        """\
        Time:      7  15   30
        Distance:  9  40  200
    """
    )

    race_doc = RaceDoc.from_str(test_input)
    assert ((7, 9), (15, 40), (30, 200)) == race_doc.races, race_doc.races

    solution_1 = solve_part_1(test_input)
    assert 288 == solution_1, solution_1

    race_doc_2 = RaceDoc.from_kerny_str(test_input)
    assert ((71530, 940200),) == race_doc_2.races, race_doc_2.races

    solution_2 = solve_part_2(test_input)
    assert 71503 == solution_2, solution_2


def solve_part_1(puzzle_input):
    race_doc = RaceDoc.from_str(puzzle_input)
    return functools.reduce(
        operator.mul, (len(RaceDoc.ways_to_win(r)) for r in race_doc.races), 1
    )


def solve_part_2(puzzle_input):
    race_doc = RaceDoc.from_kerny_str(puzzle_input)
    return len(RaceDoc.ways_to_win(race_doc.races[0]))
