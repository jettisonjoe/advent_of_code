"""Advent of Code 2021

Day ?:
  https://adventofcode.com/2021/day/
"""

import argparse
import itertools
from pathlib import Path

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


class Player():
    """POD class for a Dirac Dice player."""
    def __init__(self, number, position):
        self.number = number
        self.position = position
        self.score = 0


class CounterUpper():
    """Deterministic dice for Dirac Dice."""
    def __init__(self, num_sides=100):
        self.times_rolled = 0
        self.side = 0
        self.num_sides = num_sides
    
    def roll(self):
        self.side = (self.side + 1) % self.num_sides
        if self.side == 0:
            self.side = self.num_sides
        self.times_rolled += 1
        return self.side


class DiracDice():
    """A game of Dirac Dice."""
    def __init__(self, starts, dice=None):
        self.players = [Player(idx, pos) for idx, pos in enumerate(starts)]
        self.dice = dice or CounterUpper()
        self.turn_count = 0
    
    @property
    def winner(self):
        for player in self.players:
            if player.score >= 1000:
                return player
        return None
    
    @property
    def loser(self):
        winner = self.winner
        if winner is None:
            return None
        for player in self.players:
            if player is not winner:
                return player

    def turn(self, debug=False):
        if self.winner:
            return
        self.turn_count += 1
        for player in self.players:
            roll_1 = self.dice.roll()
            roll_2 = self.dice.roll()
            roll_3 = self.dice.roll()
            player.position = (player.position + roll_1 + roll_2 + roll_3) % 10
            if player.position == 0:
                player.position = 10
            player.score += player.position
            if debug:
                print(f'Player {player.number} '
                      f'rolls {roll_1}+{roll_2}+{roll_3} '
                      f'and moves to space {player.position} '
                      f'with score {player.score}.')
            if player.score >= 1000:
                return


def solve_part_1(puzzle_input):
    """Solve part 1 of today's puzzle."""
    game = DiracDice(puzzle_input)
    while not game.winner:
        game.turn()
    return game.loser.score * game.dice.times_rolled


def solve_part_2(puzzle_input):
    """Solve part 2 of today's puzzle."""


def run_tests():
    """Run regression tests."""
    assert 739785 == solve_part_1((4, 8))


def format_input(puzzle_input):
    """Format the puzzle input."""
    return [int(line[-1]) for line in puzzle_input.splitlines()]


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
