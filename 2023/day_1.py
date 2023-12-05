"""Solve Advent of Code 2023, day 1."""

import textwrap


def run_tests():
    assert calibration_value("1abc2") == 12
    assert calibration_value("pqr3stu8vwx") == 38
    assert calibration_value("a1b2c3d4e5f") == 15
    assert calibration_value("treb7uchet") == 77

    test_input_1 = textwrap.dedent(
        """\
        1abc2
        pqr3stu8vwx
        a1b2c3d4e5f
        treb7uchet
    """
    )
    assert solve_part_1(test_input_1) == 142

    test_input_2 = textwrap.dedent(
        """\
        two1nine
        eightwothree
        abcone2threexyz
        xtwone3four
        4nineeightseven2
        zoneight234
        7pqrstsixteen
    """
    )

    assert solve_part_2(test_input_2) == 281


def calibration_value(line: str):
    """Returns the two-digit number formed by the first and last digit."""
    digits = [c for c in line if c in "0123456789"]
    return int(digits[0] + digits[-1])


def replace_text_digits(line: str) -> str:
    """Replaces spelled digits with numerical digits.

    Preserves the first and last letter in case some letters contribute to
    multiple spelled digits, as in "eightwothree".
    """
    result = line
    result = result.replace("zero", "z0o")
    result = result.replace("one", "o1e")
    result = result.replace("two", "t2o")
    result = result.replace("three", "t3r")
    result = result.replace("four", "f4r")
    result = result.replace("five", "f5e")
    result = result.replace("six", "s6x")
    result = result.replace("seven", "s7n")
    result = result.replace("eight", "e8t")
    result = result.replace("nine", "n9e")
    return result


def solve_part_1(puzzle_input: str) -> int:
    return sum(calibration_value(l) for l in puzzle_input.splitlines())


def solve_part_2(puzzle_input: str):
    return sum(
        calibration_value(replace_text_digits(l)) for l in puzzle_input.splitlines()
    )


if __name__ == "main":
    main(**vars(parse_args()))
