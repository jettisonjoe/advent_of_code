"""Advent of Code 2021

Day 12:
  https://adventofcode.com/2021/day/12
"""

import argparse
import collections
from os import pipe
from pathlib import Path


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


class Traversal:
    def __init__(self, *nodes, double_visit=None):
        self.nodes = list(nodes)
        self.visited = set(nodes)
        self.double_visit = double_visit
    
    def __repr__(self):
        return f'Traversal({self.nodes}, {self.double_visit})'
    
    @property
    def current(self):
        return self.nodes[-1]

    def add(self, node):
        if node in self.visited and node.lower() == node:
            if self.double_visit != node:
                return False
            self.double_visit = None
        self.nodes.append(node)
        self.visited.add(node)
        return True


def traverse(edge_map, starting_paths, end_node='end'):
    """Return all paths through the cave system."""
    partial_paths = starting_paths[:]
    completed_paths = set()
    while partial_paths:
        partial_path = partial_paths.pop()
        for nxt in edge_map[partial_path.current]:
            new_partial = Traversal(*partial_path.nodes,
                                    double_visit=partial_path.double_visit)
            if new_partial.add(nxt):
                if nxt == end_node:
                    completed_paths.add(tuple(new_partial.nodes))
                    continue
                partial_paths.append(new_partial)
    
    return completed_paths


def solve_part_1(puzzle_input):
    """Solve part 1 of today's puzzle."""
    return len(traverse(puzzle_input, [Traversal('start')]))


def solve_part_2(puzzle_input):
    """Solve part 2 of today's puzzle."""
    starting_paths = [Traversal('start')]
    for node in puzzle_input:
        if node.lower() == node and node not in ('start', 'end'):
            starting_paths.append(Traversal('start', double_visit=node))
    return len(traverse(puzzle_input, starting_paths))


def run_tests():
    """Run regression tests."""
    sample_input = {
        'start': ('A', 'b'),
        'A': ('c', 'b', 'end'),
        'b': ('A', 'd', 'end'),
        'c': ('A', ),
        'd': ('b', ),
    }
    assert 10 == solve_part_1(sample_input)
    assert 36 == solve_part_2(sample_input)


def format_input(puzzle_input):
    """Format the puzzle input."""
    edge_map = collections.defaultdict(lambda: list())
    for line in puzzle_input.splitlines():
        node_a, node_b = line.split('-')
        edge_map[node_a].append(node_b)
        edge_map[node_b].append(node_a)
    
    return edge_map


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

