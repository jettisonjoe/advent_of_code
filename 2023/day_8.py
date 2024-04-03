"""Solver for Advent of Code 2023, day 8."""

import dataclasses
import itertools
import logging
import re
import textwrap
from typing import Tuple


@dataclasses.dataclass
class Node:
    name: str
    L: str
    R: str


@dataclasses.dataclass
class Loop:
    prefix: Tuple[Node]
    loop: Tuple[Node]


class Network:
    NODE_RE = re.compile(
        r"(?P<name>[A-Z0-9]+) = \((?P<L>[A-Z0-9]+), (?P<R>[A-Z0-9]+)\)"
    )

    def __init__(self, lr, nodes):
        self.lr = lr
        self.nodes = nodes

    @staticmethod
    def possible_outs(steps):
        return tuple(i + 1 for i, n in enumerate(steps) if n.endswith("Z"))
    
    @classmethod
    def from_str(cls, s):
        lr, node_part = s.split("\n\n")
        nodes = dict()
        for n in node_part.splitlines():
            match = cls.NODE_RE.match(n)
            nodes[match.group("name")] = Node(
                match.group("name"), match.group("L"), match.group("R")
            )

        return cls(lr, nodes)

    def navigate(self, start="AAA", end="ZZZ"):
        move_loop = itertools.cycle(self.lr)
        n = self.nodes[start]
        steps = []
        for move in move_loop:
            n = self.nodes[getattr(n, move)]
            steps.append(n.name)
            if n.name == end:
                return tuple(steps)
    
    def find_loop(self, start="AAA"):
        n = self.nodes[start]
        steps = []
        step_set = set()
        move_loop = itertools.cycle(enumerate(self.lr))
        for i, move in move_loop:
            move_spec = (n.name, i)
            if move_spec in step_set:
                loop_start_i = steps.index(move_spec)
                return Loop(steps[:loop_start_i], steps[loop_start_i:])
            steps.append(move_spec)
            step_set.add(move_spec)
            n = self.nodes[getattr(n, move)]

    def ghostigate(self, start="A", end="Z"):
        start_nodes = tuple(n for n in self.nodes if n.endswith(start))
        loops = tuple(self.find_loop(start=n) for n in start_nodes)
        for loop in loops:
            print(" ".join(n for n, i in loop.prefix))
        return loops


def run_tests():
    test_input_1 = textwrap.dedent(
        """\
        RL

        AAA = (BBB, CCC)
        BBB = (DDD, EEE)
        CCC = (ZZZ, GGG)
        DDD = (DDD, DDD)
        EEE = (EEE, EEE)
        GGG = (GGG, GGG)
        ZZZ = (ZZZ, ZZZ)
    """
    )
    steps_1 = solve_part_1(test_input_1)
    assert 2 == steps_1, steps_1

    test_input_2 = textwrap.dedent(
        """\
        LLR

        AAA = (BBB, BBB)
        BBB = (AAA, ZZZ)
        ZZZ = (ZZZ, ZZZ)
    """
    )
    steps_2 = solve_part_1(test_input_2)
    assert 6 == steps_2, steps_2

    test_input_3 = textwrap.dedent(
        """\
        LR

        11A = (11B, XXX)
        11B = (XXX, 11Z)
        11Z = (11B, XXX)
        22A = (22B, XXX)
        22B = (22C, 22C)
        22C = (22Z, 22Z)
        22Z = (22B, 22B)
        XXX = (XXX, XXX)
    """
    )
    # steps_3 = solve_part_2(test_input_3)
    # assert 6 == steps_3, steps_3


def solve_part_1(puzzle_input):
    net = Network.from_str(puzzle_input)
    return len(net.navigate())


def solve_part_2(puzzle_input):
    net = Network.from_str(puzzle_input)
    return len(net.ghostigate())
