"""Solver for Advent of Code 2023, day 3."""

import dataclasses
import re
import textwrap
from typing import Iterable, Tuple

NONSYMBOL_RE = re.compile(r"[0-9\.]")
NUMBER_RE = re.compile(r"[0-9]")


@dataclasses.dataclass(frozen=True)
class Part:
    number: int
    location: Tuple[int, int]


class EngineSchematic:
    def __init__(self, rows: Iterable[str]):
        self.rows = rows

        symbols = []
        gears = []
        for i, row in enumerate(self.rows):
            for j, c in enumerate(row):
                if not NONSYMBOL_RE.fullmatch(c):
                    symbols.append((i, j))
                if c == "*":
                    gears.append((i, j))
        self.symbols = tuple(symbols)
        self.gears = tuple(gears)

    @classmethod
    def from_str(cls, str_form_schematic: str):
        return cls(str_form_schematic.rstrip().splitlines())
    
    @property
    def part_numbers(self) -> Tuple[int]:
        parts = set()
        for row, col in self.symbols:
            parts.update(self.parts_adjacent(row, col))
        return tuple(p.number for p in parts)
    
    @property
    def gear_ratios(self) -> Tuple[int]:
        ratios = []
        for row, col in self.gears:
            adjacent_parts = self.parts_adjacent(row, col)
            if len(adjacent_parts) == 2:
                ratios.append(adjacent_parts[0].number * adjacent_parts[1].number)
        return tuple(ratios)
    
    @staticmethod
    def numerical_prefix(s: str) -> str:
        """Returns the longest fully numerical prefix on the input string."""
        result = ""
        idx = 0
        while idx < len(s) and NUMBER_RE.fullmatch(s[idx]):
            result += s[idx]
            idx += 1
        return result

    @staticmethod
    def numerical_suffix(s: str) -> str:
        """Returns the longest fully numerical suffix on the input string."""
        result = ""
        idx = len(s) - 1
        while idx >= 0 and NUMBER_RE.fullmatch(s[idx]):
            result += s[idx]
            idx -= 1
        return result[::-1]
    
    def parts_adjacent(self, row: int, col: int) -> Tuple[Part]:
        """Returns a tuple of all parts adjacent to the given coordinates.
        
        Parts are always layed out horizontally from left to right, which means
        a few things:
        
          - There can be at most one part directly W, and one directly E.
        
          - If there is a part touching directly N, then there's only one part
            to the N, since the N spot is adjacent to both the NW and NE spots.
            Same goes for the S spot.

          - If the N spot is empty, there could be two parts to the N, one
            touching the NW spot, and one touching the NE spot.
        """
        parts = []

        # Check if there's a part to the W.
        if col > 0 and NUMBER_RE.fullmatch(self.rows[row][col - 1]):
            part_str = self.numerical_suffix(self.rows[row][:col])
            parts.append(Part(number=int(part_str),
                              location=(row, col - len(part_str))))
        
        # Check if there's a part to the E.
        if col < len(self.rows[row]) - 1 and NUMBER_RE.fullmatch(self.rows[row][col + 1]):
            part_str = self.numerical_prefix(self.rows[row][col + 1:])
            parts.append(Part(number=int(part_str),
                              location=(row, col + 1)))
        
        # Check if there's a part to the N, or parts to the NW and NE.
        if row > 0 and NUMBER_RE.fullmatch(self.rows[row - 1][col]):
            left_str = self.numerical_suffix(self.rows[row - 1][:col])
            right_str = self.numerical_prefix(self.rows[row - 1][col:])
            parts.append(Part(number=int(left_str + right_str),
                              location=(row - 1, col - len(left_str))))
        else:
            if row > 0 and col > 0 and NUMBER_RE.fullmatch(self.rows[row - 1][col - 1]):
                part_str = self.numerical_suffix(self.rows[row - 1][:col])
                parts.append(Part(number=int(part_str),
                             location=(row, col - len(part_str))))
            if (row > 0 and col < len(self.rows[row])
                    and NUMBER_RE.fullmatch(self.rows[row - 1][col + 1])):
                part_str = self.numerical_prefix(self.rows[row -  1][col + 1:])
                parts.append(Part(number=int(part_str),
                                  location=(row - 1, col + 1)))
        
        # Check if there's a part to the S, or parts to the SW and SE.
        if row < len(self.rows) - 1 and NUMBER_RE.fullmatch(self.rows[row + 1][col]):
            left_str = self.numerical_suffix(self.rows[row + 1][:col])
            right_str = self.numerical_prefix(self.rows[row + 1][col:])
            parts.append(Part(number=int(left_str + right_str),
                              location=(row + 1, col - len(left_str))))
        else:
            if (row < len(self.rows) - 1 and col > 0
                    and NUMBER_RE.fullmatch(self.rows[row + 1][col - 1])):
                part_str = self.numerical_suffix(self.rows[row + 1][:col])
                parts.append(Part(number=int(part_str),
                             location=(row, col - len(part_str))))
            if (row < len(self.rows) and col < len(self.rows[row])
                    and NUMBER_RE.fullmatch(self.rows[row + 1][col + 1])):
                part_str = self.numerical_prefix(self.rows[row +  1][col + 1:])
                parts.append(Part(number=int(part_str),
                                  location=(row + 1, col + 1)))
        
        return tuple(parts)


def run_tests():
    """Runs some basic tests of solver logic using example inputs."""
    prefix_1 = EngineSchematic.numerical_prefix("123...")
    assert "123" == prefix_1, prefix_1

    prefix_2 = EngineSchematic.numerical_prefix("42*")
    assert "42" == prefix_2, prefix_2

    suffix_1 = EngineSchematic.numerical_suffix("......420")
    assert "420" == suffix_1, suffix_1

    suffix_2 = EngineSchematic.numerical_suffix("*1701")
    assert "1701" == suffix_2, suffix_2

    test_input = textwrap.dedent("""\
        467..114..
        ...*......
        ..35..633.
        ......#...
        617*......
        .....+.58.
        ..592.....
        ......755.
        ...$.*....
        .664.598..                     
    """)

    schematic = EngineSchematic.from_str(test_input)
    sum_of_parts = sum(schematic.part_numbers)
    assert 4361 == sum_of_parts, sum_of_parts

    sum_of_gear_ratios = sum(schematic.gear_ratios)
    assert 467835 == sum_of_gear_ratios, sum_of_gear_ratios


def solve_part_1(puzzle_input: str) -> int:
    """Sums the part numbers from a schematic in str form."""
    schematic = EngineSchematic.from_str(puzzle_input)
    return sum(schematic.part_numbers)


def solve_part_2(puzzle_input: str) -> int:
    schematic = EngineSchematic.from_str(puzzle_input)
    return sum(schematic.gear_ratios)