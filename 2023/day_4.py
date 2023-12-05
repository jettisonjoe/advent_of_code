"""Solver for Advent of Code 2023, day 4."""

import re
import textwrap
from typing import Iterable, List, Set, Tuple

CARD_ID_RE = re.compile(r"Card\s+(?P<id>[0-9]+)")


class Scratchcard:
    """A scratchcard from Island Island."""

    def __init__(self, id: int, numbers: Set[int], winning: Set[int]):
        self.id = id
        self.numbers = numbers
        self.winning = winning

    @staticmethod
    def resolve_game(cards: Iterable["Scratchcard"]) -> Tuple["Scratchcard"]:
        to_resolve: List["Scratchcard"] = list(cards)
        resolved: List["Scratchcard"] = []

        while to_resolve:
            card = to_resolve.pop()
            for i in range(card.num_winners):
                to_resolve.append(cards[i + card.id])
            resolved.append(card)

        return tuple(resolved)

    @classmethod
    def from_str(cls, card_str: str) -> "Scratchcard":
        """Parses a Scratchcard object from a string representation."""
        id_part, all_numbers_part = card_str.split(":")
        id_match = CARD_ID_RE.match(id_part)
        id = int(id_match.group("id"))

        numbers_part, winning_part = all_numbers_part.split("|")
        numbers = set(int(n) for n in numbers_part.split())
        winning = set(int(n) for n in winning_part.split())

        return cls(id, numbers, winning)

    @property
    def num_winners(self) -> int:
        return len(self.numbers & self.winning)

    @property
    def score(self) -> int:
        num_winners = self.num_winners
        if num_winners == 0:
            return 0
        return 2 ** (num_winners - 1)


def run_tests():
    test_input = textwrap.dedent(
        """\
        Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
        Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
        Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
        Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
        Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
        Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
    """
    )

    cards = [Scratchcard.from_str(s) for s in test_input.splitlines()]
    assert 6 == len(cards)

    assert 8 == cards[0].score, cards[0].score
    assert 2 == cards[1].score, cards[1].score
    assert 2 == cards[2].score, cards[2].score
    assert 1 == cards[3].score, cards[3].score
    assert 0 == cards[4].score, cards[4].score
    assert 0 == cards[5].score, cards[5].score

    resolved_pile = Scratchcard.resolve_game(cards)
    assert 30 == len(resolved_pile), len(resolved_pile)


def solve_part_1(puzzle_input: str):
    cards = [Scratchcard.from_str(s) for s in puzzle_input.splitlines()]
    return sum(c.score for c in cards)


def solve_part_2(puzzle_input: str):
    cards = [Scratchcard.from_str(s) for s in puzzle_input.splitlines()]
    return len(Scratchcard.resolve_game(cards))
