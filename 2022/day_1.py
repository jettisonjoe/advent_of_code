"""https://adventofcode.com/2022/day/1"""

import logging
import textwrap
from typing import List


def run_tests() -> None:
    """Run regression tests."""
    test_input = textwrap.dedent(
        """\
        1000
        2000
        3000

        4000

        5000
        6000

        7000
        8000
        9000

        10000
    """
    )
    assert solve_part_1(test_input) == 24000
    assert solve_part_2(test_input) == 45000


def parse_input(puzzle_input: str) -> List[List[int]]:
    result = []
    current_list: List[int] = []
    for line in puzzle_input.splitlines():
        if not line:
            result.append(current_list)
            current_list = []
            continue
        current_list.append(int(line))
    result.append(current_list)

    return result


def solve_part_1(puzzle_input: str) -> int:
    """Solve part 1."""
    calorie_counts = parse_input(puzzle_input)
    calorie_totals = [sum(count) for count in calorie_counts]
    return max(calorie_totals)


def solve_part_2(puzzle_input: str) -> int:
    """Solve part 2."""
    calorie_counts = parse_input(puzzle_input)
    calorie_totals = [sum(count) for count in calorie_counts]
    calorie_totals.sort()
    logging.debug("Totals: %s", calorie_totals)
    result = sum(calorie_totals[-1:-4:-1])
    logging.debug("Result: %s", result)
    return result
