import argparse
import collections
import functools
import math
import operator
import re


def _parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument('infile',
                        type=argparse.FileType('r'),
                        help='Input text file for this puzzle')
    args = parser.parse_args()
    return args.infile.read().splitlines()


class Tile:
    """A square tile of arbitrary size."""
    SIDES = ('N', 'E', 'S', 'W')
    MONSTER_TOP = re.compile(r'..................#.')
    MONSTER_MID = re.compile(r'#....##....##....###')
    MONSTER_BOT = re.compile(r'.#..#..#..#..#..#...')
    MONSTER_SIZE = 15

    def __init__(self, tile_id, rows):
        self.tile_id = tile_id
        self.rows = tuple(rows)
        self.size = len(rows)

    def __repr__(self):
        lines = [f'\nTile {self.tile_id}:']
        lines.extend(self.rows)
        return '\n'.join(lines)

    @property
    def hashes(self):
        return sum(row.count('#') for row in self.rows)

    @property
    def roughness(self):
        return self.hashes - self.count_sea_monsters() * self.MONSTER_SIZE

    def side(self, side_name):
        if side_name == 'N':
            return self.rows[0]
        if side_name == 'E':
            return ''.join((row[-1] for row in self.rows))
        if side_name == 'S':
            return self.rows[-1]
        if side_name == 'W':
            return ''.join((row[0] for row in self.rows))

    def flip(self):
        """Flip the tile over the vertical axis."""
        new_rows = []
        for row in self.rows:
            new_rows.append(row[::-1])
        self.rows = new_rows

    def rotate(self):
        """Rotate the tile 90 degrees counter-clockwise."""
        new_rows = []
        for i in range(self.size - 1, -1, -1):
            new_rows.append(''.join((row[i] for row in self.rows)))
        self.rows = new_rows

    def transform_to_fit(self, border_to_match, which_side):
        """Try to transform until our side matches the given border."""
        for _ in range(2):
            for __ in range(4):
                if border_to_match == self.side(which_side):
                    return True
                self.rotate()
            self.flip()
        return False

    def count_sea_monsters(self):
        """Count sea monsters present in our current orientation."""
        monsters = 0
        for i in range(1, self.size - 1):
            for match in self.MONSTER_MID.finditer(self.rows[i]):
                start, end = match.span()
                if self.MONSTER_TOP.fullmatch(self.rows[i-1], start, end):
                    if self.MONSTER_BOT.fullmatch(self.rows[i+1], start, end):
                        monsters += 1
        return monsters

    def find_sea_monsters(self):
        """Re-orient until we have sea monsters, then count them."""
        for _ in range(2):
            for __ in range(5):
                monster_count = self.count_sea_monsters()
                if monster_count > 0:
                    return monster_count
                self.rotate()
            self.flip()
        return 0


SideMatch = collections.namedtuple('SideMatch', ('side', 'tile_id'))


def find_matched_sides(tiles):
    matches_by_id = {}
    for tile in tiles.values():
        matches = []
        for side_name in Tile.SIDES:
            side = tile.side(side_name)
            matches_this_side = []
            for other in tiles.values():
                if tile == other:
                    continue
                for other_side_name in Tile.SIDES:
                    if side in (other.side(other_side_name),
                                other.side(other_side_name)[::-1]):
                        matches_this_side.append(
                            SideMatch(side_name, other.tile_id))
            if len(matches_this_side) > 1:
                raise RuntimeError('Side has more than one match!')
            if matches_this_side:
                matches.append(matches_this_side[0])
        matches_by_id[tile.tile_id] = matches
    return matches_by_id


def arrange_tiles(tiles):
    """Return a list of rows of properly-arranged tiles."""
    rows = []
    matches = find_matched_sides(tiles)
    corners = [t for t in matches if len(matches[t]) == 2]

    # Orient an arbitrary corner tile so that it's the NW-most tile.
    corner_tile = tiles[corners[0]]
    south_match, east_match = matches[corners[0]]
    south_side = corner_tile.side(south_match.side)
    east_side = corner_tile.side(east_match.side)
    corner_tile.transform_to_fit(south_side, 'S')
    if corner_tile.side('E') not in (east_side, east_side[::-1]):
        corner_tile.flip()
    assert corner_tile.side('E') in (east_side, east_side[::-1])

    remaining = set(tiles.keys())
    grid_size = int(math.sqrt(len(tiles)))
    row = [corner_tile]
    remaining.remove(corner_tile.tile_id)
    while len(rows) < grid_size:
        while len(row) < grid_size:
            old_num_remaining = len(remaining)
            side_matches = matches[row[-1].tile_id]
            for side_match in side_matches:
                if side_match.tile_id not in remaining:
                    continue
                tile = tiles[side_match.tile_id]
                if tile.transform_to_fit(row[-1].side('E'), 'W'):
                    row.append(tile)
                    remaining.remove(tile.tile_id)
            if old_num_remaining == len(remaining):
                raise RuntimeError("Unable to find tile continue row.")
        rows.append(row)
        if len(rows) == grid_size:
            return rows
        old_num_remaining = len(remaining)
        side_matches = matches[row[0].tile_id]
        for side_match in side_matches:
            if side_match.tile_id not in remaining:
                continue
            tile = tiles[side_match.tile_id]
            if tile.transform_to_fit(row[0].side('S'), 'N'):
                row = [tile]
                remaining.remove(tile.tile_id)
        if old_num_remaining == len(remaining):
            raise RuntimeError("Unable to find a tile to start next row.")


def stitch_tiles(arrangement):
    """Stitch a tile arrangement into a mega-tile, removing borders."""
    rows = []
    for tile_row in arrangement:
        for i in range(1, tile_row[0].size - 1):
            rows.append(''.join((tile.rows[i][1:-1] for tile in tile_row)))
    return Tile(0, rows)


def parse_tiles(input_lines):
    """From input lines, generate a dict of tiles."""
    tiles = {}
    tile_id = None
    tile_lines = []
    for line in input_lines:
        if line == '':
            tiles[tile_id] = Tile(tile_id, tile_lines)
            tile_id = None
            tile_lines = []
        elif line.startswith('Tile'):
            tile_id = int(line.split()[1][:-1])
        else:
            tile_lines.append(line)
    tiles[tile_id] = Tile(tile_id, tile_lines)
    return tiles


def run_tests():
    with open('day_20_sample.txt', 'r') as sample_file:
        tiles = parse_tiles(sample_file.read().splitlines())
    assert 9 == len(tiles)
    matches = find_matched_sides(tiles)
    corners = [t for t in matches if len(matches[t]) == 2]
    assert 20899048083289 == functools.reduce(operator.mul,
                                              [t for t in corners])
    arranged = arrange_tiles(tiles)
    target_arrangement =[[1951, 2311, 3079],
                         [2729, 1427, 2473],
                         [2971, 1489, 1171]]
    assert target_arrangement == [[t.tile_id for t in row] for row in arranged]
    stitched = stitch_tiles(arranged)
    assert 2 == stitched.find_sea_monsters()
    assert 273 == stitched.roughness


def main(input_lines):
    run_tests()
    tiles = parse_tiles(input_lines)
    matches = find_matched_sides(tiles)
    corners = [t for t in matches if len(matches[t]) == 2]
    answer_one = functools.reduce(operator.mul, [t for t in corners])
    arranged = arrange_tiles(tiles)
    stitched = stitch_tiles(arranged)
    stitched.find_sea_monsters()
    answer_two = stitched.roughness
    return answer_one, answer_two


if __name__ == '__main__':
    answer_one, answer_two = main(_parse_args())
    print(f'Part One: {answer_one}')
    print(f'Part Two: {answer_two}')
