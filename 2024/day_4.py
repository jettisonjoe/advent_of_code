"""Solver for Advent of Code 2024, day 4."""

import textwrap


def run_tests():
    test_input = textwrap.dedent(
        """\
        MMMSXXMASM
        MSAMXMSMSA
        AMXSXMAAMM
        MSAMASMSMX
        XMASAMXAMM
        XXAMMXXAMA
        SMSMSASXSS
        SAXAMASAAA
        MAMMMXMMMM
        MXMXAXMASX
    """
    )
    assert 18 == solve_part_1(test_input)
    assert 9 == solve_part_2(test_input)


def solve_part_1(puzzle_input):
    lines = puzzle_input.splitlines()
    rows = len(lines)
    cols = len(lines[0])
    count = 0
    for row in range(rows):
        for col in range(cols):
            if lines[row][col] != "X":
                continue
            # North
            if (
                row >= 3
                and lines[row - 1][col] == "M"
                and lines[row - 2][col] == "A"
                and lines[row - 3][col] == "S"
            ):
                count += 1

            # Northeast
            if (
                row >= 3
                and col <= cols - 4
                and lines[row - 1][col + 1] == "M"
                and lines[row - 2][col + 2] == "A"
                and lines[row - 3][col + 3] == "S"
            ):
                count += 1

            # East
            if (
                col <= cols - 4
                and lines[row][col + 1] == "M"
                and lines[row][col + 2] == "A"
                and lines[row][col + 3] == "S"
            ):
                count += 1

            # Southeast
            if (
                row <= rows - 4
                and col <= cols - 4
                and lines[row + 1][col + 1] == "M"
                and lines[row + 2][col + 2] == "A"
                and lines[row + 3][col + 3] == "S"
            ):
                count += 1

            # South
            if (
                row <= rows - 4
                and lines[row + 1][col] == "M"
                and lines[row + 2][col] == "A"
                and lines[row + 3][col] == "S"
            ):
                count += 1

            # Southwest
            if (
                row <= rows - 4
                and col >= 3
                and lines[row + 1][col - 1] == "M"
                and lines[row + 2][col - 2] == "A"
                and lines[row + 3][col - 3] == "S"
            ):
                count += 1

            # West
            if (
                col >= 3
                and lines[row][col - 1] == "M"
                and lines[row][col - 2] == "A"
                and lines[row][col - 3] == "S"
            ):
                count += 1

            # Nortwest
            if (
                row >= 3
                and col >= 3
                and lines[row - 1][col - 1] == "M"
                and lines[row - 2][col - 2] == "A"
                and lines[row - 3][col - 3] == "S"
            ):
                count += 1

    return count


def solve_part_2(puzzle_input):
    lines = puzzle_input.splitlines()
    rows = len(lines)
    cols = len(lines[0])
    count = 0
    for row in range(rows):
        for col in range(cols):
            if lines[row][col] != "A":
                continue
            if not 1 <= row <= rows - 2:
                continue
            if not 1 <= col <= cols - 2:
                continue
            corners = (
                lines[row - 1][col - 1]
                + lines[row + 1][col - 1]
                + lines[row + 1][col + 1]
                + lines[row - 1][col + 1]
            )
            if corners in ("MMSS", "MSSM", "SMMS", "SSMM"):
                count += 1

    return count
