"""Main entry point for Advent of Code 2022 (https://adventofcode.com/2022).

Takes care of most of the boiler plate of handling command line arguments,
configuring logging, reading input files, and printing results so that the code
for each day can focus purely on solving the puzzle at hand.

The code for each day should be placed in a file called "day_<NUM>.py", while
the puzzle input text for that day should be placed in a corresponding file
called "day_<NUM>.txt". For example, the code and puzzle input for December 12th
should be placed in the files "day_12.py" and "day_12.txt" respectively.

The main entry point code will look for the following functions to be defined by
each day's code:

    solve_part_1: Takes puzzle input str as the sole argument and returns the
        solution to part 1 of that day's puzzle.

    solve_part_2: Takes puzzle input str as the sole argument and returns the
        solution to part 2 of that day's puzzle.

    run_tests: Optional test function to call (with no arguments) before
        attempting to call the solve_part_* functions.

Invocation:
  python main.py --day <DAY NUMBER>
"""

import argparse
import importlib
import logging
import pathlib
from typing import Any, Optional, Tuple


DEFAULT_DAY = 1
DEFAULT_MODULE = None
DEFAULT_INFILE = None
DEFAULT_PART = None


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--day",
        type=int,
        default=DEFAULT_DAY,
        help="which number day to solve (default=1)",
    )
    parser.add_argument(
        "--module",
        type=str,
        default=DEFAULT_MODULE,
        help="solve using a specific module instead of --day",
    )
    parser.add_argument(
        "--infile",
        type=pathlib.Path,
        default=DEFAULT_INFILE,
        help="solve for specific input input instead of --day",
    )
    parser.add_argument(
        "--part",
        type=int,
        default=DEFAULT_PART,
        help="solve just one part of the puzzle (1|2)",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="turn on verbose logging"
    )

    return parser.parse_args()


def main(
    day: int = DEFAULT_DAY,
    module: Optional[str] = DEFAULT_MODULE,
    infile: Optional[pathlib.Path] = DEFAULT_INFILE,
    part: Optional[int] = DEFAULT_PART,
    verbose: bool = False,
) -> Tuple[Optional[Any], Optional[Any]]:
    """Imports and runs puzzle solvers."""
    if verbose:
        logging.basicConfig(level=logging.DEBUG)

    solver = importlib.import_module(f"day_{day}")
    if module is not None:
        solver = importlib.import_module(module)
    logging.debug("Solving with module '%s'.", solver.__name__)

    infile = infile or pathlib.Path(f"day_{day}.txt")
    puzzle_input = infile.read_text()
    logging.debug("Solving for input '%s'.", infile.name)

    if hasattr(solver, "run_tests"):
        logging.debug("Running regression tests.")
        solver.run_tests()
        logging.debug("Regression tests complete.")
    else:
        logging.debug("No regression tests to run.")

    solution_1 = None
    solution_2 = None

    if part in (None, 1) and hasattr(solver, "solve_part_1"):
        logging.debug("Solving part 1.")
        solution_1 = solver.solve_part_1(puzzle_input)
        logging.debug("Done solving part 1:\n  %s", solution_1)
    if part in (None, 2) and hasattr(solver, "solve_part_2"):
        logging.debug("Solving part 2.")
        solution_2 = solver.solve_part_2(puzzle_input)
        logging.debug("Done solving part 2:\n  %s", solution_2)

    return solution_1, solution_2


if __name__ == "__main__":
    solution_1, solution_2 = main(**vars(parse_args()))
    print(f"Part One: {solution_1}")
    print(f"Part Two: {solution_2}")
