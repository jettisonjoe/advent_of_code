"""https://adventofcode.com/2022/day/13"""

import logging
import re
import textwrap
from typing import List, Optional, Tuple, Union

INT_PATTERN = re.compile(r"\d+")


def run_tests() -> None:
    """Runs simple tests using sample input."""
    test_input = textwrap.dedent(
        """\
        [1,1,3,1,1]
        [1,1,5,1,1]

        [[1],[2,3,4]]
        [[1],4]

        [9]
        [[8,7,6]]

        [[4,4],4,4]
        [[4,4],4,4,4]

        [7,7,7,7]
        [7,7,7]

        []
        [3]

        [[[]]]
        [[]]

        [1,[2,[3,[4,[5,6,7]]]],8,9]
        [1,[2,[3,[4,[5,6,0]]]],8,9]
    """
    )

    assert Packet([1, 1, 3, 1, 1]) < Packet([1, 1, 5, 1, 1])
    assert Packet([[1], [2, 3, 4]]) < Packet([[1], 4])
    assert not Packet([9]) < Packet([8, 7, 6])
    assert Packet([[4, 4], 4, 4]) < Packet([[4, 4], 4, 4, 4])
    assert not Packet([7, 7, 7, 7]) < Packet([7, 7, 7])
    assert Packet([]) < Packet([3])
    assert not Packet([[[]]]) < Packet([[]])
    assert not Packet([1, [2, [3, [4, [5, 6, 7]]]], 8, 9]) < Packet(
        [1, [2, [3, [4, [5, 6, 0]]]], 8, 9]
    )

    assert Packet.from_str("[1,1,3,1,1]") == Packet([1, 1, 3, 1, 1])
    assert Packet.from_str("[[1],[2,3,4]]") == Packet([[1], [2, 3, 4]])
    assert Packet.from_str("[[8,7,6]]") == Packet([[8, 7, 6]])
    assert Packet.from_str("[[[]]]") == Packet([[[]]])
    assert Packet.from_str("[1,[2,[3,[4,[5,6,7]]]],8,9]") == Packet(
        [1, [2, [3, [4, [5, 6, 7]]]], 8, 9]
    )
    assert Packet.from_str("[1,[2,[3,[4,[5,6,0]]]],8,9]") == Packet(
        [1, [2, [3, [4, [5, 6, 0]]]], 8, 9]
    )
    assert solve_part_1(test_input) == 13
    assert solve_part_2(test_input) == 140


def parse_input(puzzle_input: str) -> "List[Tuple[Packet, Packet]]":
    """Return a list of packet pairs."""
    result = []
    pair_strs = puzzle_input.split("\n\n")
    for pair_str in pair_strs:
        left, right = pair_str.splitlines()
        result.append((Packet.from_str(left), Packet.from_str(right)))
    return result


class Packet:
    """An elvish data packet."""

    def __init__(self, data: List):
        self.data = data

    def __lt__(self, other: "Packet") -> bool:
        """True if this packet comes before the other in proper ordering."""
        logging.debug("Comparing two packets %s and %s", self.data, other.data)
        result = bool(self._lt_impl(self.data, other.data))
        logging.debug("Reached a result: %s", result)
        return result

    def __eq__(self, other) -> bool:
        if not isinstance(other, Packet):
            return False
        return self.data == other.data

    @classmethod
    def from_str(cls, data_str: str) -> "Packet":
        """Make a packet from a data str."""
        data, suffix = cls.parse_list_prefix(data_str)
        assert not suffix
        logging.debug("Parsed packet data: %s", data)
        return cls(data)

    @classmethod
    def parse_list_prefix(cls, s: str) -> Tuple[List, str]:
        """Return the initial list and the rest of the str after it."""
        if not s.startswith("["):
            raise ValueError("Str does not start w/ a list: %s", s)

        remainder = list(reversed(s[1:]))
        result: List = []
        int_part = ""
        while remainder:
            char = remainder.pop()
            if char in "0123456789":
                int_part += char
            elif char == ",":
                if int_part:
                    result.append(int(int_part))
                    int_part = ""
            elif char == "[":
                remainder.append("[")
                sublist, rest = cls.parse_list_prefix("".join(reversed(remainder)))
                result.append(sublist)
                remainder = list(reversed(rest))
            elif char == "]":
                if int_part:
                    result.append(int(int_part))
                return result, "".join(reversed(remainder))
            else:
                raise ValueError(
                    f"Unknown token: {char}",
                )

        return result, "".join(reversed(remainder))

    @classmethod
    def _lt_impl(cls, left, right) -> Optional[bool]:
        """Compare two packet data values and return True if left < right."""
        if isinstance(left, int) and isinstance(right, int):
            logging.debug("Comparing two integers %s and %s", left, right)
            if left == right:
                return None
            return left < right

        if isinstance(left, int) and isinstance(right, list):
            logging.debug("Converting %s to list to compare to %s", left, right)
            return cls._lt_impl([left], right)

        if isinstance(left, list) and isinstance(right, int):
            logging.debug("Converting %s to list to compare to %s", right, left)
            return cls._lt_impl(left, [right])

        logging.debug("Comparting two lists %s and %s", left, right)
        for idx in range(min(len(left), len(right))):
            subresult = cls._lt_impl(left[idx], right[idx])
            if subresult is None:
                logging.debug("Two values were equal, continuing.")
                continue
            return subresult
        if len(left) == len(right):
            return None
        logging.debug("One of the lists ran out of values to compare.")
        return len(left) < len(right)


def solve_part_1(puzzle_input: str) -> int:
    """Solves part 1 of today's puzzle."""
    packet_pairs = parse_input(puzzle_input)
    in_order_indices: List[int] = []
    for idx, (left, right) in enumerate(packet_pairs):
        if left < right:
            in_order_indices.append(idx + 1)

    return sum(in_order_indices)


def solve_part_2(puzzle_input: str) -> int:
    """Solves part 2 of today's puzzle."""
    packet_pairs = parse_input(puzzle_input)
    packets = []
    for pair in packet_pairs:
        packets.extend(pair)
    divider_2 = Packet([[2]])
    divider_6 = Packet([[6]])
    packets.extend((divider_2, divider_6))
    packets.sort()
    return (packets.index(divider_2) + 1) * (packets.index(divider_6) + 1)
