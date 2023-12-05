"""https://adventofcode.com/2022/day/12"""


import dataclasses
import logging
import math
import textwrap
from typing import List, Optional, Set, Tuple
import queue


def run_tests() -> None:
    """Runs simple regression tests using sample input."""
    test_input = textwrap.dedent(
        """\
        Sabqponm
        abcryxxl
        accszExk
        acctuvwj
        abdefghi
    """
    )
    test_solution_1 = solve_part_1(test_input)
    logging.debug("Test 1: %s", test_solution_1)
    assert test_solution_1 == 31
    assert solve_part_2(test_input) == 29


def parse_input(
    puzzle_input: str,
) -> Tuple["Terrain", Tuple[int, int], Tuple[int, int]]:
    """Parses puzzle input and returns a terrain map and star position."""
    rows: List[str] = []
    start: Optional[Tuple[int, int]] = None
    finish: Optional[Tuple[int, int]] = None
    for idx, row in enumerate(puzzle_input.splitlines()):
        rows.append(row)
        if "S" in row:
            start = (row.find("S"), idx)
        if "E" in row:
            finish = (row.find("E"), idx)

    if start is None:
        raise ValueError("No start position found in puzzle input.")
    if finish is None:
        raise ValueError("No finish position found in puzzle input.")

    logging.debug("Parsed rows: %s", rows)
    return Terrain(rows), start, finish


class Terrain:
    """A map of terrain."""

    DIRECTIONS = (
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1),
    )

    def __init__(self, rows):
        self.rows = rows
        self.w = len(rows[0])
        self.h = len(rows)

    def __getitem__(self, key: Tuple[int, int]) -> str:
        col, row = key
        return self.rows[row][col]

    def elevation(self, pos: Tuple[int, int]) -> int:
        """Returns the elevation at the give position."""
        val = self[pos]
        if val == "S":
            return ord("a")
        if val == "E":
            return ord("z")
        return ord(val)

    def neighbors(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Returns all valid neighbors of the given position."""
        x, y = pos
        return [
            (x + dx, y + dy)
            for dx, dy in self.DIRECTIONS
            if self.in_bounds((x + dx, y + dy))
        ]

    def in_bounds(self, pos: Tuple[int, int]) -> bool:
        """True if the location is in bounds."""
        x, y = pos
        return 0 <= x < self.w and 0 <= y < self.h


class Route:
    """A route through some terrain."""

    def __init__(self, *prefix: Tuple[int, int]):
        self.visited: Set[Tuple[int, int]] = set(prefix)
        self.path: List[Tuple[int, int]] = list(prefix)

    def __repr__(self):
        return f"Route<{self.path}>"

    def __lt__(self, other):
        return self.length < other.length

    @property
    def length(self):
        """Returns the length of the route."""
        return len(self.path) - 1


def distance(start: Tuple[int, int], finish: Tuple[int, int]) -> float:
    """Returns the distance between two points."""
    dx = abs(finish[0] - start[0])
    dy = abs(finish[1] - start[1])
    return math.sqrt(dx**2 + dy**2)


@dataclasses.dataclass
class SearchNode:
    pos: Tuple[int, int]
    depth: int
    parent: "Optional[SearchNode]"


def shortest_route(
    terrain: Terrain, start: Tuple[int, int], finish: Tuple[int, int]
) -> Optional[SearchNode]:
    """Searches for the shortest route from start to finish via BFS."""
    shortest: Optional[SearchNode] = None
    frontier: queue.Queue = queue.Queue()
    frontier.put(SearchNode(start, 0, None))
    visited: Set[Tuple[int, int]] = set((start,))

    while not frontier.empty():
        node = frontier.get()
        logging.debug("Testing node at depth: %s", node.depth)
        logging.debug("Visited: %s", len(visited))
        logging.debug("Frontier size: %s", frontier.qsize())
        logging.debug("Terrain size: %s", terrain.w * terrain.h)
        for child in terrain.neighbors(node.pos):
            if child in visited:
                continue
            if terrain.elevation(child) > terrain.elevation(node.pos) + 1:
                continue
            if shortest and node.depth >= shortest.depth:
                continue
            child_node = SearchNode(child, node.depth + 1, node)
            visited.add(child)
            if terrain[child] == "E":
                shortest = child_node
            else:
                frontier.put(child_node)
    return shortest


def solve_part_1(puzzle_input: str) -> Optional[int]:
    """Solves part 1 of today's puzzle."""
    terrain, start, finish = parse_input(puzzle_input)
    shortest = shortest_route(terrain, start, finish)
    if shortest is not None:
        return shortest.depth
    return None


def solve_part_2(puzzle_input: str) -> int:
    """Solves part 2 of today's puzzle."""
    terrain, _, finish = parse_input(puzzle_input)
    starts = []
    for x in range(terrain.w):
        for y in range(terrain.h):
            if terrain[(x, y)] in ("a", "S"):
                starts.append((x, y))

    trail_lengths = []
    for start in starts:
        shortest = shortest_route(terrain, start, finish)
        if shortest is not None:
            trail_lengths.append(shortest.depth)

    return min(trail_lengths)
