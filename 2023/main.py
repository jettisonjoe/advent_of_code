"""Main entry point for Advent of Code 2023."""

import argparse
import logging
import importlib
import pathlib
from typing import Any, Optional, Tuple


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-d",
                        "--day",
                        help="day number to solve",
                        type=int,
                        required=True)
    parser.add_argument("-i",
                        "--infile",
                        help="puzzle input as a text file",
                        type=pathlib.Path)
    parser.add_argument("-v",
                        "--verbose",
                        help="enable verbose output",
                        action="store_true")
    return parser.parse_args()


def main(day: int,
         infile: Optional[pathlib.Path],
         verbose: bool) -> Tuple[Any, Any]:
    """Import the solver for the given day and run it on the input."""
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
    
    module_name = f"day_{day}"
    solver = importlib.import_module(module_name)

    infile = infile or pathlib.Path(f"day_{day}.txt")
    if not infile.exists():
        raise IOError(f"Puzzle input file {infile.name} doesn't exist.")
    puzzle_input = infile.read_text()
    if puzzle_input.strip() == "":
        raise ValueError("Puzzle input file has no contents.")

    if hasattr(solver, "run_tests"):
        logging.debug("Running tests...")
        solver.run_tests()
        logging.debug("...Done running tests.")

    logging.debug("Solving puzzles...")
    solution_1 = solver.solve_part_1(puzzle_input)
    solution_2 = solver.solve_part_2(puzzle_input)
    logging.debug("...Done solving puzzles.")

    return solution_1, solution_2


if __name__ == "__main__":
    solution_1, solution_2 = main(**vars(parse_args()))
    print(f"Part 1: {solution_1}")
    print(f"Part 2: {solution_2}")