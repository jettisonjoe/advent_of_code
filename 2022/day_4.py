"""https://adventofcode.com/2022/day/4"""

import logging
import textwrap
from typing import List, Tuple


def run_tests() -> None:
    """Runs regression tests using sample input."""
    test_input = textwrap.dedent(
        """\
        2-4,6-8
        2-3,4-5
        5-7,7-9
        2-8,3-7
        6-6,4-6
        2-6,4-8
    """
    )
    section_pairs = parse_input(test_input)
    assert 2 == count_contained(section_pairs)
    assert 4 == count_overlapping(section_pairs)


def parse_input(puzzle_input: str) -> List[Tuple[List[int], List[int]]]:
    """Parses puzzle input into a list of pairs of sections."""
    result = []
    for line in puzzle_input.splitlines():
        first_range, second_range = line.split(",")
        first_min, first_max = first_range.split("-")
        second_min, second_max = second_range.split("-")
        first_sections = list(range(int(first_min), int(first_max) + 1))
        second_sections = list(range(int(second_min), int(second_max) + 1))
        result.append((first_sections, second_sections))

    return result


def has_full_overlap(x: List[int], y: List[int]) -> bool:
    """Returns True if one section range fully overlaps with the other."""
    x_set, y_set = set(x), set(y)
    logging.debug("Looking for overlap in:\n  %s\n  %s", x, y)
    overlap = x_set & y_set
    if overlap:
        logging.debug("Detected overlap: %s", overlap)
    return overlap == x_set or overlap == y_set


def has_any_overlap(x: List[int], y: List[int]) -> bool:
    """True if the two sections overlap at all."""
    x_set, y_set = set(x), set(y)
    logging.debug("Looking for overlap in:\n  %s\n  %s", x, y)
    overlap = x_set & y_set
    if overlap:
        logging.debug("Detected overlap: %s", overlap)
        return True
    return False


def count_contained(section_pairs: List[Tuple[List[int], List[int]]]) -> int:
    """Returns a count of section pairs where one fully contains the other."""
    num_contained = 0
    for x, y in section_pairs:
        if has_full_overlap(x, y):
            num_contained += 1

    return num_contained


def count_overlapping(section_pairs: List[Tuple[List[int], List[int]]]) -> int:
    """Returns a count of section pairs that have any overlap."""
    num_overlapping = 0
    for x, y in section_pairs:
        if has_any_overlap(x, y):
            num_overlapping += 1

    return num_overlapping


def solve_part_1(puzzle_input: str):
    """Solves part one of today's puzzle."""
    section_pairs = parse_input(puzzle_input)
    return count_contained(section_pairs)


def solve_part_2(puzzle_input: str) -> int:
    """Solves part two of today's puzzle."""
    section_pairs = parse_input(puzzle_input)
    return count_overlapping(section_pairs)
