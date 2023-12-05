"""https://adventofcode.com/2022/day/2"""

import dataclasses
import logging
import textwrap
from typing import List, Optional


@dataclasses.dataclass
class Shape:
    name: str
    score: int
    beats: Optional[Shape] = None
    beaten_by: Optional[Shape] = None

    def score_against(self, other_shape: "Shape") -> int:
        """Score a game of Rock, Paper, Scissors according to elvish rules."""
        if self.beats is other_shape:
            return self.score + 6
        if self is other_shape:
            return self.score + 3
        return self.score


PAPER = Shape("Paper", 1)
SCISSORS = Shape("Scissors", 2)
ROCK = Shape("Rock", 3)

PAPER.beats = ROCK
SCISSORS.beats = PAPER
ROCK.beats = SCISSORS

PAPER.beaten_by = SCISSORS
SCISSORS.beaten_by = ROCK
ROCK.beaten_by = PAPER


def shape_for_name(name: str) -> Shape:
    """Return the Shape desginated by name."""
    if name.upper() in ("PAPER", "A", "X"):
        return PAPER
    if name.upper() in ("SCISSORS", "B", "Y"):
        return SCISSORS
    if name.upper() in ("ROCK", "C", "Z"):
        return ROCK
    raise ValueError(f"Invalid shape name: {name}")


def run_tests() -> None:
    """Run regression tests."""
    test_input = textwrap.dedent(
        """\
        A Y
        B X
        C Z
    """
    )
    test_solution_1 = solve_part_1(test_input)
    logging.debug("Test solution 1: %s", test_solution_1)
    assert test_solution_1 == 15

    test_solution_2 = solve_part_2(test_input)
    logging.debug("Test solution 2: %s", test_solution_2)
    assert test_solution_2 == 12


def parse_input(puzzle_input: str) -> List[List[str]]:
    """Parse the input strategy guide str."""
    return [line.split() for line in puzzle_input.splitlines()]


def solve_part_1(puzzle_input: str) -> int:
    """Solve part 1."""
    total_score = 0
    for their_shape_name, our_shape_name in parse_input(puzzle_input):
        their_shape = shape_for_name(their_shape_name)
        our_shape = shape_for_name(our_shape_name)
        total_score += our_shape.score_against(their_shape)

    return total_score


def solve_part_2(puzzle_input: str):
    """Solve part 2."""
    total_score = 0
    for their_shape_name, outcome in parse_input(puzzle_input):
        their_shape = shape_for_name(their_shape_name)
        assert isinstance(their_shape.beats, Shape)
        assert isinstance(their_shape.beaten_by, Shape)
        our_shape = their_shape
        if outcome == "X":
            logging.debug("Their shape: %s; we need to lose.", their_shape.name)
            our_shape = their_shape.beats
        elif outcome == "Y":
            logging.debug("Their shape: %s; we need to draw.", their_shape.name)
        elif outcome == "Z":
            logging.debug("Their shape: %s; we need to win.", their_shape.name)
            our_shape = their_shape.beaten_by
        logging.debug("Our shape: %s", our_shape.name)
        total_score += our_shape.score_against(their_shape)

    return total_score
