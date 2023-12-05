"""Solve Advent of Code 2023, day 2."""

import dataclasses
import re
import textwrap
from typing import Iterable


GAME_RE = re.compile(r"Game (?P<id>[0-9]+)")
COLOR_COUNT_RE = re.compile(r"(?P<count>[0-9]+) (?P<color>[a-z]+)")


@dataclasses.dataclass
class CubeSet:
    """A single set of colored cubes from the cube game."""
    red: int
    green: int
    blue: int

    @classmethod
    def from_record(cls, record: str):
        red, green, blue = 0, 0, 0
        color_counts = record.split(", ")
        for color_count in color_counts:
            match = COLOR_COUNT_RE.fullmatch(color_count)
            if match.group("color") == "red":
                red = int(match.group("count"))
            if match.group("color") == "green":
                green = int(match.group("count"))
            if match.group("color") == "blue":
                blue = int(match.group("count"))
        
        return cls(red, green, blue)
    
    @property
    def power(self) -> int:
        return self.red * self.green * self.blue


class CubeGame:
    def __init__(self, id: int, rounds: Iterable[CubeSet]):
        self.id = id
        self.rounds = rounds

        red_max_seen = 0
        green_max_seen = 0
        blue_max_seen = 0
        for round in self.rounds:
            red_max_seen = max(red_max_seen, round.red)
            green_max_seen = max(green_max_seen, round.green)
            blue_max_seen = max(blue_max_seen, round.blue)
        self.max_seen = CubeSet(red=red_max_seen,
                                green=green_max_seen,
                                blue=blue_max_seen)
    
    @classmethod
    def from_record(cls, record: str):
        id_segment, rounds_segment = record.split(": ")

        id_match = GAME_RE.fullmatch(id_segment)
        id = int(id_match.group("id"))

        round_records = rounds_segment.split("; ")
        rounds = [CubeSet.from_record(r) for r in round_records]

        return cls(id, rounds)
    
    def possible_with_bag(self, bag: CubeSet) -> bool:
        """True if this game would be possible with the given bag."""
        return all((self.max_seen.red <= bag.red,
                   self.max_seen.green <= bag.green,
                   self.max_seen.blue <= bag.blue))


def run_tests():
    test_input_1 = textwrap.dedent("""\
        Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
        Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
        Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
        Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
        Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
    """)
    assert solve_part_1(test_input_1) == 8

    test_game = CubeGame.from_record("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green")
    assert test_game.max_seen == CubeSet(red=4, green=2, blue=6)
    assert test_game.max_seen.power == 48

    assert solve_part_2(test_input_1) == 2286


def solve_part_1(puzzle_input: str):
    games = [CubeGame.from_record(r) for r in puzzle_input.splitlines()]
    return sum(int(g.id) for g in games if g.possible_with_bag(CubeSet(12, 13, 14)))


def solve_part_2(puzzle_input:str):
    games = [CubeGame.from_record(r) for r in puzzle_input.splitlines()]
    return sum(g.max_seen.power for g in games)
