"""https://adventofcode.com/2022/day/5"""

import copy
import logging
import textwrap
from typing import List, Tuple


def run_tests() -> None:
    """Run regression tests using sample input."""
    test_input = textwrap.dedent(
        """\
            [D]    
        [N] [C]    
        [Z] [M] [P]
         1   2   3 

        move 1 from 2 to 1
        move 3 from 1 to 3
        move 2 from 2 to 1
        move 1 from 1 to 2
    """
    )
    stacks, moves = parse_input(test_input)
    apply_moves(stacks, moves)
    logging.debug(stacks)
    assert sample_stacks(apply_moves(stacks, moves)) == "CMZ"
    assert sample_stacks(apply_moves_9001(stacks, moves)) == "MCD"


def parse_input(
    puzzle_input: str,
) -> Tuple[List[List[str]], List[Tuple[int, int, int]]]:
    """Turn str puzzle input into initial stacks and a list of moves."""
    stack_str, move_str = puzzle_input.split("\n\n")

    stack_lines = stack_str.splitlines()
    column_labels = stack_lines[-1].split()
    num_columns = len(column_labels)
    assert num_columns == int(column_labels[-1])

    stacks: List[List[str]] = [[] for _ in range(num_columns)]
    for line in stack_str.splitlines():
        for idx in range(num_columns):
            if line[idx * 4] != " ":
                stacks[idx].append(line[idx * 4 + 1])

    for stack in stacks:
        stack.reverse()

    moves = []
    for line in move_str.splitlines():
        _, num, __, src, ___, dest = line.split()
        moves.append((int(num), int(src) - 1, int(dest) - 1))

    return stacks, moves


def apply_moves(
    stacks: List[List[str]], moves: List[Tuple[int, int, int]]
) -> List[List[str]]:
    """Apply classic crane style moves and return the result."""
    result = copy.deepcopy(stacks)
    for num, src, dest in moves:
        for _ in range(num):
            result[dest].append(result[src].pop())

    return result


def apply_moves_9001(
    stacks: List[List[str]], moves: List[Tuple[int, int, int]]
) -> List[List[str]]:
    """Apply crane model 9001 style moves and return the result."""
    result = copy.deepcopy(stacks)
    for num, src, dest in moves:
        lifted_chunk = []
        for _ in range(num):
            lifted_chunk.append(result[src].pop())

        for _ in range(num):
            result[dest].append(lifted_chunk.pop())

    return result


def sample_stacks(stacks: List[List[str]]) -> str:
    """Return the str formed by the top crate in each stack."""
    return "".join(stack[-1] for stack in stacks)


def solve_part_1(puzzle_input: str) -> str:
    """Solve part 1 of today's puzzle."""
    stacks, moves = parse_input(puzzle_input)
    return sample_stacks(apply_moves(stacks, moves))


def solve_part_2(puzzle_input: str) -> str:
    """Solve part 2 of today's puzzle."""
    stacks, moves = parse_input(puzzle_input)
    return sample_stacks(apply_moves_9001(stacks, moves))
