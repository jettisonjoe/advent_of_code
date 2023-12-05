"""https://adventofcode.com/2022/day/3"""

import logging
import textwrap
from typing import List, Tuple


def run_tests() -> None:
    """Runs regression tests using example inputs."""
    test_input = textwrap.dedent(
        """\
        vJrwpWtwJgWrhcsFMMfFFhFp
        jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
        PmmdzqPrVvPwwTWBwg
        wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
        ttgJtRGJQctTZtZT
        CrZsJsPPZsGzwwsLwLmpwMDw
    """
    )
    sacks = sacks_from_string(test_input)
    assert sum_priorities(find_repeats(sacks)) == 157
    assert sum_priorities(find_badges(sacks)) == 70


def sacks_from_string(sack_str: str) -> List[Tuple[str, str]]:
    """Turns puzzle input str into a list of sacks."""
    result = []
    for line in sack_str.splitlines():
        result.append((line[: len(line) // 2], (line[len(line) // 2 :])))

    return result


def find_repeats(sacks: List[Tuple[str, str]]) -> str:
    """Returns all the repeat items from each sack in order of sacks."""
    repeats = ""
    for first_compartment, second_compartment in sacks:
        intersection = set(first_compartment) & set(second_compartment)
        assert len(intersection) == 1
        repeats += intersection.pop()

    return repeats


def find_badges(sacks: List[Tuple[str, str]]) -> str:
    """Returns the badges for each group of three sacks in order of groups."""
    badges = ""
    for group_idx in range(len(sacks) // 3):
        set_1 = set.union(*(set(half) for half in sacks[group_idx * 3]))
        set_2 = set.union(*(set(half) for half in sacks[group_idx * 3 + 1]))
        set_3 = set.union(*(set(half) for half in sacks[group_idx * 3 + 2]))
        badge_set = set_1 & set_2 & set_3
        assert len(badge_set) == 1
        badges += badge_set.pop()

    return badges


def priority(item: str) -> int:
    """Finds the priority of the given item."""
    if 65 <= ord(item) <= 90:
        return ord(item) - 65 + 27
    return ord(item) - 97 + 1


def sum_priorities(items: str) -> int:
    """Returns the sum of the priorities of all the items."""
    return sum(priority(item) for item in items)


def solve_part_1(puzzle_input: str) -> int:
    """Solves part 1 of today's puzzle."""
    sacks = sacks_from_string(puzzle_input)
    return sum_priorities(find_repeats(sacks))


def solve_part_2(puzzle_input: str) -> int:
    """Solves part 2 of today's puzzle."""
    sacks = sacks_from_string(puzzle_input)
    return sum_priorities(find_badges(sacks))
