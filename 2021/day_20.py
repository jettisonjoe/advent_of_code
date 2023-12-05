"""Advent of Code 2021

Day 20:
  https://adventofcode.com/2021/day/20
"""

import argparse
from pathlib import Path
import textwrap

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


class Image():
    """A trench map scanner image."""
    def __init__(self, img_str, fill='.'):
        self.original = img_str
        self.rows = [list(row) for row in img_str.strip().split('\n')]
        self._fill = fill
    
    def __repr__(self):
        return '\n'.join(''.join(row) for row in self.rows)
    
    @property
    def width(self):
        return len(self.rows[0])
    
    @property
    def height(self):
        return len(self.rows)
    
    @property
    def lit_pixels(self):
        return self.__repr__().count('#')
    
    def expand(self):
        """Expand the canvas by 1 cell all around."""
        blank_row = [self._fill for _ in range(len(self.rows[0]) + 2)]
        expanded = [blank_row[:]]
        for row in self.rows:
            expanded_row = [self._fill]
            expanded_row.extend(row)
            expanded_row.append(self._fill)
            expanded.append(expanded_row)
        expanded.append(blank_row[:])

        self.rows = expanded

    def enhance(self, algo):
        """Zoom and enhance."""
        self.expand()
        enhanced = []
        
        for row in range(self.width):
            enhanced_row = []
            for col in range(self.height):
                neighbors = aoc.get_neighbor_locs(
                    self.rows, row, col, True, True, True)
                bit_str = ''
                for cell in neighbors:
                    if cell is None:
                        bit_str += '0' if self._fill == '.' else '1'
                        continue
                    cell_r, cell_c = cell
                    if self.rows[cell_r][cell_c] == '.':
                        bit_str += '0'
                        continue
                    bit_str += '1'
                algo_idx = int(bit_str, 2)
                enhanced_row.append(algo[algo_idx])
            enhanced.append(enhanced_row)
        
        self.rows = enhanced
        self._fill = algo[0] if self._fill == '.' else algo[-1]


def solve_part_1(puzzle_input):
    """Solve part 1 of today's puzzle."""
    algo, image_str = puzzle_input
    image = Image(image_str)
    image.enhance(algo)
    image.enhance(algo)
    return image.lit_pixels


def solve_part_2(puzzle_input):
    """Solve part 2 of today's puzzle."""
    algo, image_str = puzzle_input
    image = Image(image_str)
    for _ in range(50):
        image.enhance(algo)
    return image.lit_pixels


def run_tests():
    """Run regression tests."""
    sample_input = textwrap.dedent("""\
      ..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..##
      #..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###
      .######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#.
      .#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#.....
      .#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#..
      ...####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.....
      ..##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

      #..#.
      #....
      ##..#
      ..#..
      ..###
    """)

    assert 35 == solve_part_1(format_input(sample_input))
    assert 3351 == solve_part_2(format_input(sample_input))


def format_input(puzzle_input):
    """Format the puzzle input."""
    algo_part, image_part = puzzle_input.split('\n\n')
    algo = ''.join(algo_part.split('\n'))
    image = image_part.strip()
    return algo, image


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
