"""https://adventofcode.com/2022/day/6"""

from typing import Iterable


def run_tests() -> None:
    """Run regression tests using sample inputs."""
    assert find_packet("mjqjpqmgbljsphdztnvjfqwrcgsmlb") == 7
    assert find_packet("bvwbjplbgvbhsrlpgdmjqwftvncz") == 5
    assert find_packet("nppdvjthqldpwncqszvftbrmjlhg") == 6
    assert find_packet("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg") == 10
    assert find_packet("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw") == 11
    assert find_message("mjqjpqmgbljsphdztnvjfqwrcgsmlb") == 19
    assert find_message("bvwbjplbgvbhsrlpgdmjqwftvncz") == 23
    assert find_message("nppdvjthqldpwncqszvftbrmjlhg") == 23
    assert find_message("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg") == 29
    assert find_message("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw") == 26


class DataFinder:
    def __init__(self, prefix_len: int):
        self.prefix_len = prefix_len
        self.data = False
        self.pos = 0
        self._prefix = ""

    def feed(self, next_char: str) -> None:
        """Feed a character to the packet finder."""
        assert len(next_char) == 1
        self.pos += 1

        if next_char in self._prefix:
            prev_idx = self._prefix.find(next_char)
            self._prefix = self._prefix[prev_idx + 1 :]
        self._prefix += next_char

        if len(self._prefix) == self.prefix_len:
            self.data = True


def find_data(seq: Iterable[str], prefix_len: int) -> int:
    """Find the data start marker in the sequence."""
    data_finder = DataFinder(prefix_len)
    for char in seq:
        data_finder.feed(char)
        if data_finder.data:
            return data_finder.pos

    raise ValueError("No data found in sequence")


def find_packet(seq: Iterable[str]) -> int:
    """Find the start-of-packet marker in the sequence."""
    return find_data(seq, 4)


def find_message(seq: Iterable[str]) -> int:
    """Find the start-of-message marker in the sequence."""
    return find_data(seq, 14)


def solve_part_1(puzzle_input: str) -> int:
    """Solve part 1 of today's puzzle."""
    return find_packet(puzzle_input)


def solve_part_2(puzzle_input: str) -> int:
    return find_message(puzzle_input)
