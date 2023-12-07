"""Solver for Advent of Code 2023, day 7.

Today I took the opportunity to update my personal workstation to WSL2 and Python 3.12,
and fixed some minor VSCode issues that had been bothering me. I don't know if it will
help me work any faster, but it will certainly be more pleasant.

I had to do a bit more setup, as switching to WSL2 broke some of my VSCode Python
integrations. This set me back a bit, but things are working nicely now, I think.

I was annoyed with part 2 because the modifications needed to solve it were a little too
invasive to be entirely elegant, which means the overall structure I chose for part 1
probably wasn't the most extensible.
"""

import enum
import itertools
import operator
import textwrap


class HandType(enum.Enum):
    """Camel Cards hand types in order of strength."""

    UNKNOWN = 0
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    FULL_HOUSE = 5
    FOUR_OF_A_KIND = 6
    FIVE_OF_A_KIND = 7


class CamelCardsHand:
    """A hand of cards in the game of Camel Cards."""

    CARDS = "23456789TJQKA"

    def __init__(self, cards, bid=0, jokers=False):
        self.cards = cards
        self.bid = bid
        self.jokers = jokers
        if self.jokers:
            self.hand_type = self.strongest_hand_type(cards)
        else:
            self.hand_type = self.hand_type_for_cards(cards)

    def __getitem__(self, i):
        """Used in combination with itemgetter as a sorting key to rank hands."""
        if i == "hand":
            return self.hand_type.value
        return self.card_value(self.cards[i])

    def __repr__(self):
        return self.cards

    @staticmethod
    def hand_type_for_cards(cards):
        c = tuple(sorted(cards))
        if len(c) != 5:
            raise ValueError(f"Invalid hand size for '{c}'.")
        groups = tuple(tuple(g) for _, g in itertools.groupby(c))
        group_lens = tuple(sorted(len(g) for g in groups))
        if len(groups) == 1:
            return HandType.FIVE_OF_A_KIND
        if len(groups) == 2 and group_lens == (1, 4):
            return HandType.FOUR_OF_A_KIND
        if len(groups) == 2 and group_lens == (2, 3):
            return HandType.FULL_HOUSE
        if len(groups) == 3 and group_lens == (1, 1, 3):
            return HandType.THREE_OF_A_KIND
        if group_lens.count(2) == 2:
            return HandType.TWO_PAIR
        if group_lens.count(2) == 1:
            return HandType.ONE_PAIR
        return HandType.HIGH_CARD

    @staticmethod
    def rank_by_str(hands):
        """Using built-in sorting niceties always feels a little cheap in AoC."""
        return sorted(hands, key=operator.itemgetter("hand", 0, 1, 2, 3, 4))

    @classmethod
    def strongest_hand_type(cls, cards):
        """Resolve wild cards by trying everything and picking the best combo."""
        options = cls.CARDS[:].replace("J", "")
        num_jacks = cards.count("J")
        non_jacks = cards[:].replace("J", "")
        hands = []
        for p in itertools.combinations_with_replacement(options, num_jacks):
            hands.append(cls(non_jacks + "".join(p)))

        return tuple(cls.rank_by_str(hands))[-1].hand_type

    @classmethod
    def total_winnings(cls, hands):
        ranked_hands = cls.rank_by_str(hands)
        return sum(h.bid * i for i, h in enumerate(ranked_hands, start=1))

    @classmethod
    def parse_hands(cls, s, jokers=False):
        hands = []
        for line in s.splitlines():
            cards, bid_part = line.split()
            hands.append(cls(cards, int(bid_part), jokers))
        return tuple(hands)

    def card_value(self, c):
        """Assign a value to the card.

        This used to be a classmethod, but had to become an instance method in order to
        get access to whether we're using jokers to score the hand or not. This feels
        inelegant and I disklike it. If I were to refactor I'd probably try to keep game
        state and scoring convention in a game object rather than each hand.
        """
        if c not in self.CARDS:
            raise ValueError(f"Card '{c}' not known.")
        if self.jokers and c == "J":
            return 0
        return self.CARDS.find(c) + 1


def run_tests():
    test_input = textwrap.dedent(
        """\
        32T3K 765
        T55J5 684
        KK677 28
        KTJJT 220
        QQQJA 483
    """
    )
    hands = CamelCardsHand.parse_hands(test_input)
    assert 5 == len(hands), len(hands)

    winnings_1 = CamelCardsHand.total_winnings(hands)
    assert 6440 == winnings_1, winnings_1

    winnings_2 = solve_part_2(test_input)
    assert 5905 == winnings_2, winnings_2


def solve_part_1(puzzle_input):
    hands = CamelCardsHand.parse_hands(puzzle_input)
    return CamelCardsHand.total_winnings(hands)


def solve_part_2(puzzle_input):
    hands = CamelCardsHand.parse_hands(puzzle_input, jokers=True)
    return CamelCardsHand.total_winnings(hands)
