"""https://adventofcode.com/2022/day/11"""


import collections
import logging
import math
import operator
import re
import textwrap
from typing import Callable, Iterable, List, Optional, Tuple

MONKEY_PATTERN = re.compile(
    r"Monkey (?P<idx>\d+:)\n"
    r"  Starting items: (?P<items>(\d+)(, \d+)*)\n"
    r"  Operation: new = (?P<op>\w+ [*+] \w+)\n"
    r"  Test: divisible by (?P<divisor>\d+)\n"
    r"    If true: throw to monkey (?P<cohort_0>\d+)\n"
    r"    If false: throw to monkey (?P<cohort_1>\d+)"
)

OPS = {
    "*": operator.mul,
    "+": operator.add,
}


def run_tests() -> None:
    """Runs simple tests using sample inputs."""
    test_input = textwrap.dedent(
        """\
        Monkey 0:
          Starting items: 79, 98
          Operation: new = old * 19
          Test: divisible by 23
            If true: throw to monkey 2
            If false: throw to monkey 3

        Monkey 1:
          Starting items: 54, 65, 75, 74
          Operation: new = old + 6
          Test: divisible by 19
            If true: throw to monkey 2
            If false: throw to monkey 0
        
        Monkey 2:
          Starting items: 79, 60, 97
          Operation: new = old * old
          Test: divisible by 13
            If true: throw to monkey 1
            If false: throw to monkey 3
        
        Monkey 3:
          Starting items: 74
          Operation: new = old + 3
          Test: divisible by 17
            If true: throw to monkey 0
            If false: throw to monkey 1
    """
    )
    monkeys = [Monkey.from_str(s) for s in test_input.split("\n\n")]
    sim = MonkeySim(monkeys)
    sim.run(rounds=1)
    logging.debug("Monkey 0 items: %s", monkeys[0].items)
    assert list(monkeys[0].items) == [20, 23, 27, 26]

    assert solve_part_1(test_input) == 10605
    assert solve_part_2(test_input) == 2713310158


class Monkey:
    """A monkey that inspects items and causes worry."""

    def __init__(
        self,
        items: Iterable[int],
        operation: str,
        divisor: int,
        cohorts: Tuple[int, int],
        mitigation: Callable[[int], int] = lambda x: x // 3,
    ):
        self.items = collections.deque(items)
        self.operation = operation
        self.divisor = divisor
        self.cohorts = cohorts
        self.mitigation = mitigation
        self.inspections = 0

    @classmethod
    def from_str(cls, s: str) -> "Monkey":
        match = MONKEY_PATTERN.match(s)
        if not match:
            raise ValueError(f"Unable to parse Monkey from text: {s}")
        return cls(
            items=[int(item) for item in match.group("items").split(", ")],
            operation=match.group("op"),
            divisor=int(match.group("divisor")),
            cohorts=(int(match.group("cohort_0")), int(match.group("cohort_1"))),
        )

    def test_worry(self):
        """Tests worry level to decide who to toss to."""
        return bool(self.items[0] % self.divisor == 0)

    def resolve(self, operand: str) -> int:
        """Resolve an operand in operation namespace."""
        if operand == "old":
            return self.items[0]
        return int(operand)

    def inspect_item(self) -> int:
        """Monkey inspects and returns the ID of the monkey to toss it to."""
        self.inspections += 1
        x, op, y = self.operation.split()
        self.items[0] = OPS[op](self.resolve(x), self.resolve(y))
        self.items[0] = self.mitigation(self.items[0])
        if self.test_worry():
            return self.cohorts[0]
        else:
            return self.cohorts[1]

    def toss(self, monkey: "Monkey") -> None:
        """Tosses the top item to the specified monkey."""
        monkey.items.append(self.items.popleft())


class MonkeySim:
    """A simulation of monkey behaviour and worry levels."""

    def __init__(self, monkeys: List[Monkey]):
        self.monkeys = monkeys

    def run(self, rounds: int) -> None:
        """Run the simulation for the specified number of rounds."""
        for i in range(rounds):
            logging.debug("Running simulation, round %s", i)
            for monkey in self.monkeys:
                while monkey.items:
                    recipient = monkey.inspect_item()
                    monkey.toss(self.monkeys[recipient])


def sort_by_activity(monkeys: Iterable[Monkey]) -> List[Monkey]:
    """Returns the the most active monkeys."""
    return sorted(monkeys, key=lambda m: m.inspections)


def solve_part_1(puzzle_input: str) -> int:
    """Solve part 1 of today's puzzle."""
    monkeys = [Monkey.from_str(s) for s in puzzle_input.split("\n\n")]
    sim = MonkeySim(monkeys)
    sim.run(rounds=20)
    monkeys_by_activity = sort_by_activity(monkeys)
    return monkeys_by_activity[-1].inspections * monkeys_by_activity[-2].inspections


def solve_part_2(puzzle_input: str) -> int:
    """Solve part 2 of today's puzzle."""
    monkeys = [Monkey.from_str(s) for s in puzzle_input.split("\n\n")]
    lcm = math.lcm(*[m.divisor for m in monkeys])
    for m in monkeys:
        m.mitigation = lambda x: x % lcm
    sim = MonkeySim(monkeys)
    sim.run(rounds=10000)
    monkeys_by_activity = sort_by_activity(monkeys)
    return monkeys_by_activity[-1].inspections * monkeys_by_activity[-2].inspections
