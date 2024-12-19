"""Solve Advent of Code 2024, day 1."""

import textwrap


def run_tests():
    test_input = textwrap.dedent(
        """\
        3   4
        4   3
        2   5
        1   3
        3   9
        3   3
    """
    )
    assert 11 == solve_part_1(test_input)
    assert 31 == solve_part_2(test_input)


def make_sorted_lists(puzzle_input):
    left_list = []
    right_list = []

    for line in puzzle_input.splitlines():
        left_entry, right_entry = line.split()
        left_list.append(int(left_entry))
        right_list.append(int(right_entry))

    return sorted(left_list), sorted(right_list)


def solve_part_1(puzzle_input):
    left_list, right_list = make_sorted_lists(puzzle_input)

    total_delta = 0
    for i in range(len(left_list)):
        total_delta += abs(left_list[i] - right_list[i])

    return total_delta


def solve_part_2(puzzle_input):
    left_list, right_list = make_sorted_lists(puzzle_input)

    total_similarity = 0

    for entry in left_list:
        total_similarity += entry * (right_list.count(entry))

    return total_similarity
