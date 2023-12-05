"""Solver for Advent of Code 2023, day 5."""

import dataclasses
import logging
import re
import sys
import textwrap
from typing import Iterable, List, Optional, Tuple


@dataclasses.dataclass
class Seed:
    seed: Optional[int] = None
    soil: Optional[int] = None
    fertilizer: Optional[int] = None
    water: Optional[int] = None
    light: Optional[int] = None
    temperature: Optional[int] = None
    humidity: Optional[int] = None
    location: Optional[int] = None


@dataclasses.dataclass
class SeedRange:
    seed: Seed
    size: int


class Almanac:
    """An Island Island Almanac."""
    SECTION_HEADER_RE = re.compile(
        r"(?P<intype>[a-z]+)-to-(?P<outtype>[a-z]+) map:")

    def __init__(self, section_strs: Iterable[str]):
        self.data = dict()

        for section_str in section_strs:
            section_lines = section_str.splitlines()
            header_match = self.SECTION_HEADER_RE.fullmatch(section_lines[0])
            lookup_func = self.make_lookup_func(header_match.group("outtype"),
                                                section_lines[1:])
            self.data[header_match.group("intype")] = lookup_func
    
    @staticmethod
    def make_lookup_func(outtype: str, table: Iterable[str]):
        """Makes a lookup function based on a table of ranges.
        
        The lookup function uses the table to compute the output value and
        returns the str output type followed by the value. Example:
            "light", 46

        But wait, there's more. The lookup function also returns the size of
        remaining output range starting at the looked-up value. This is useful
        for figuring out where a possible range of seeds has to end because a
        jump in one of the lookup tables was encountered. I know this sounds
        vague, but go with it. It's nearly 1am and I can't stop to explain in
        more detail right now.
        """
        ranges = []
        for line in table:
            dest_start, src_start, size = line.split()
            ranges.append((int(src_start),
                           int(src_start) + int(size),
                           int(dest_start) - int(src_start)))
        ranges = tuple(sorted(ranges))
        def lookup_func(val):
            first_start = ranges[0][0]
            if val < first_start:
                return outtype, val, first_start - val
            for i in range(len(ranges)):
                start, end, offset = ranges[i]
                if start <= val < end:
                    return outtype, val + offset, end - val
                if i < len(ranges) - 1:
                    next_start = ranges[i + 1][0]
                    if val < next_start:
                        return outtype, val, next_start - val
            return outtype, val, float("inf")
        
        return lookup_func
    
    def lookup(self, seed_number: int) -> Seed:
        seed = Seed()
        next_lookup: Tuple[str, int] = ("seed", seed_number)
        while True:
            key, val = next_lookup
            setattr(seed, key, val)
            if key not in self.data:
                break
            next_key, next_val, _ = self.data[key](val)
            next_lookup = (next_key, next_val)
        
        logging.debug(f"Found seed {seed}.")
        return seed
    
    def lookup_range(self, seed_number: int) -> SeedRange:
        start_seed = Seed()
        smallest_range_size = float("inf")
        next_lookup: Tuple[str, int] = ("seed", seed_number)
        while True:
            key, val = next_lookup
            setattr(start_seed, key, val)
            if key not in self.data:
                break
            next_key, next_val, range_size = self.data[key](val)
            smallest_range_size = min(range_size, smallest_range_size)
            next_lookup = (next_key, next_val)
        
        logging.debug(f"Found seed range starting with {start_seed}.")
        return SeedRange(start_seed, smallest_range_size)


def parse_input(input: str) -> Tuple[Tuple[int], Almanac]:
    sections = input.split("\n\n")
    seed_spec = tuple(int(n) for n in sections[0].split(":")[1].split())
    almanac = Almanac(sections[1:])

    return seed_spec, almanac


def run_tests():
    test_input = textwrap.dedent("""\
        seeds: 79 14 55 13

        seed-to-soil map:
        50 98 2
        52 50 48

        soil-to-fertilizer map:
        0 15 37
        37 52 2
        39 0 15

        fertilizer-to-water map:
        49 53 8
        0 11 42
        42 0 7
        57 7 4

        water-to-light map:
        88 18 7
        18 25 70

        light-to-temperature map:
        45 77 23
        81 45 19
        68 64 13

        temperature-to-humidity map:
        0 69 1
        1 0 69

        humidity-to-location map:
        60 56 37
        56 93 4
    """)

    _, almanac = parse_input(test_input)

    seed_1 = almanac.lookup(79)
    assert 82 == seed_1.location, seed_1.location

    lowest_1 = solve_part_1(test_input)
    assert 35 == lowest_1, lowest_1

    lowest_2 = solve_part_2(test_input)
    assert 46 == lowest_2, lowest_2


def solve_part_1(puzzle_input: str):
    seed_spec, almanac = parse_input(puzzle_input)
    seed_records = tuple(almanac.lookup(s) for s in seed_spec)
    lowest_loc_seed = min(seed_records, key=lambda s: s.location)
    return lowest_loc_seed.location


def solve_part_2(puzzle_input: str):
    """Look, I'm not proud of this solution, but it's late, and it works."""
    seed_spec, almanac = parse_input(puzzle_input)
    lowest_location = float("inf")
    for i in range(0, len(seed_spec), 2):
        start, end = seed_spec[i], seed_spec[i] + seed_spec[i + 1]
        while start < end:
            seed_range = almanac.lookup_range(start)
            lowest_location = min(lowest_location, seed_range.seed.location)
            start += seed_range.size
    return lowest_location
    

