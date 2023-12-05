"""Advent of Code 2021

Day 15:
  https://adventofcode.com/2021/day/15
"""

import argparse
import collections
from pathlib import Path
from typing import NamedTuple

import aoc


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--infile',
                        type=Path,
                        default=None,
                        help='Optional input text file for this puzzle')
    parser.add_argument('--part',
                        type=int,
                        default=None,
                        help='Solve just one part of the puzzle (1|2)')
    
    return parser.parse_args()


class Waypoint(NamedTuple):
    row: int = 0
    col: int = 0
    weight: int = 0


class Route():
    def __init__(self, rows, path=None):
        self.weight = 0
        self.path = [Waypoint(0, 0, 0)]

        self._rows = rows
        self._visited = {(0, 0)}

        if path is not None:
            for waypoint in path[1:]:
                self.add(waypoint.row, waypoint.col)
    
    def __repr__(self):
        return f'Route({[(wp.row, wp.col) for wp in self.path]})'
    
    @property
    def row(self):
        return self.path[-1].row
    
    @property
    def col(self):
        return self.path[-1].col
    
    @property
    def waypoint(self):
        return self.path[-1]
    
    def add(self, row, col):
        """Add a waypoint to the route."""
        self.weight += self._rows[row][col]
        self.path.append(Waypoint(row, col, self.weight))
        self._visited.add((row, col))
    
    def evaluate(self, row, col):
        if (row, col) in self._visited:
            return float('inf')
        return self.weight + self._rows[row][col]

    @classmethod
    def straight_lines(cls, rows):
        """Returns a straightforward route from top left to bottom right."""
        route = cls(rows)
        for row in range(1, len(rows)):
            route.add(0, row)
        for col in range(1, len(rows[-1])):
            route.add(len(rows) - 1, col)
        
        return route
    
    @classmethod
    def greedy(cls, rows):
        """Returns a greedy route from top left to bottom right."""
        route = cls(rows)
        row, col = 0, 0
        last_row, last_col = len(rows) - 1, len(rows[-1]) - 1
        while row < last_row or col < last_col:
            down = rows[row + 1][col] if row < last_row else float('inf')
            right = rows[row][col + 1] if col < last_col else float('inf')
            if down < right:
                route.add(row + 1, col)
                row += 1
                continue
            route.add(row, col + 1)
            col += 1

        return route
    

def manhattan_dist(start, end):
    """Returns the manhattan distance between two points."""
    start_x, start_y = start
    end_x, end_y = end
    return abs(end_x - start_x) + abs(end_y - start_y)


def find_path(rows, start=None, end=None, debug=False):
    """Find a path from the top left to the bottom right."""
    if start is None:
        start = (0, 0)
    if end is None:
        end = (len(rows) - 1, len(rows[-1]) - 1)
    unfinished_routes = collections.deque([Route(rows)])
    best_routes = { end: Route.greedy(rows) }

    best_to_row = {0: Waypoint(0, 0, float('inf'))}
    best_to_col = {0: Waypoint(0, 0, float('inf'))}
    for waypoint in best_routes[end].path:
        if waypoint.row not in best_to_row:
            best_to_row[waypoint.row] = waypoint
        if waypoint.col not in best_to_col:
            best_to_col[waypoint.col] = waypoint

    while unfinished_routes:
        route = unfinished_routes.popleft()
        if debug:
            print(f'{len(unfinished_routes)} unfinished, '
                  f'searching: ({route.row}, {route.col}), {route.weight}')

        next_steps = aoc.get_neighbor_locs(rows, route.row, route.col)
        for step in next_steps:
            best_to_step = (best_routes[step].weight if step in best_routes
                            else float('inf'))
            max_to_row = (best_to_row[step[0]].weight
                          + 9 * abs(best_to_row[step[0]].col - step[1]))
            max_to_col = (best_to_col[step[1]].weight
                          + 9 * abs(best_to_col[step[1]].row - step[0]))
            max_weight = min(
                best_routes[end].weight - manhattan_dist(step, end),
                best_to_step,
                max_to_col,
                max_to_row,
                9 * manhattan_dist(start, step))

            if route.evaluate(step[0], step[1]) > max_weight:
                continue

            new_route = Route(rows, path=route.path)
            new_route.add(step[0], step[1])
            if new_route.weight < best_to_row[step[0]].weight:
                best_to_row[step[0]] = new_route.waypoint
            if new_route.weight < best_to_col[step[1]].weight:
                best_to_col[step[1]] = new_route.waypoint
            unfinished_routes.append(new_route)
            best_routes[step] = new_route

    return best_routes[end]


def solve_part_1(puzzle_input):
    """Solve part 1 of today's puzzle."""
    return find_path(puzzle_input, debug=True).weight


def solve_part_2(puzzle_input):
    """Solve part 2 of today's puzzle."""


def run_tests():
    """Run regression tests."""
    sample_input = (
        (1, 1, 6, 3, 7, 5, 1, 7, 4, 2),
        (1, 3, 8, 1, 3, 7, 3, 6, 7, 2),
        (2, 1, 3, 6, 5, 1, 1, 3, 2, 8),
        (3, 6, 9, 4, 9, 3, 1, 5, 6, 9),
        (7, 4, 6, 3, 4, 1, 7, 1, 1, 1),
        (1, 3, 1, 9, 1, 2, 8, 1, 3, 7),
        (1, 3, 5, 9, 9, 1, 2, 4, 2, 1),
        (3, 1, 2, 5, 4, 2, 1, 6, 3, 9),
        (1, 2, 9, 3, 1, 3, 8, 5, 2, 1),
        (2, 3, 1, 1, 9, 4, 4, 5, 8, 1),
    )
    assert 40 == solve_part_1(sample_input)


def format_input(puzzle_input):
    """Format the puzzle input."""
    result = []
    for line in puzzle_input.splitlines():
        result.append(tuple(int(x) for x in line))

    return result


def main(infile=None, part=None):
    """Solves for the given input."""
    solution_1 = None
    solution_2 = None

    if infile:
        puzzle_input = format_input(infile.read_text())
        if part in (None, 1):
            solution_1 = solve_part_1(puzzle_input)
        if part in (None, 2):
            solution_2 = solve_part_2(puzzle_input)

    return solution_1, solution_2


if __name__ == '__main__':
    run_tests()
    solution_1, solution_2 = main(**vars(parse_args()))
    print(f'Part One: {solution_1}')
    print(f'Part Two: {solution_2}')
