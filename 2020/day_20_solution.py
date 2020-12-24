import argparse
import math
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
    """A square tile of arbitrary size, with links to neighbors."""
    N = 'north'
    E = 'east'
    S = 'south'
    W = 'west'
    SIDES = (N, E, S, W)
    MONSTER_TOP = re.compile(r'..................#.')
    MONSTER_MID = re.compile(r'#....##....##....###')
    MONSTER_BOT = re.compile(r'.#..#..#..#..#..#...')
    MONSTER_SIZE = 15

    def __init__(self, tile_id, rows):
        self.tile_id = tile_id
        self.rows = tuple(rows)
        self.size = len(rows)

    def __repr__(self):
        lines = [f'Tile {self.tile_id}:']
        lines.extend(self.rows)
        return '\n'.join(lines)

    @property
    def hashes(self):
        return sum(row.count('#') for row in self.rows)

    @property
    def roughness(self):
        return self.hashes - self.count_sea_monsters() * self.MONSTER_SIZE

    def side(self, side_const):
        if side_const == self.N:
            return self.rows[0]
        if side_const == self.E:
            return ''.join((row[-1] for row in self.rows))
        if side_const == self.S:
            return self.rows[-1]
        if side_const == self.W:
            return ''.join((row[0] for row in self.rows))

    def all_possible_sides(self):
        return (self.side(self.N[:]), self.side(self.N)[::-1],
                self.side(self.E[:]), self.side(self.E)[::-1],
                self.side(self.S[:]), self.side(self.S)[::-1],
                self.side(self.W[:]), self.side(self.W)[::-1])

    def flip(self):
        """Flip the tile horizontally."""
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

    def transform_to_match(self, target_side, side_const):
        for _ in range(2):
            for __ in range(4):
                if target_side == self.side(side_const):
                    return True
                self.rotate()
            self.flip()
        return False

    def _count_sea_monsters_impl(self):
        monsters = 0
        for i in range(1, self.size - 1):
            for match in self.MONSTER_MID.finditer(self.rows[i]):
                start, end = match.span()
                if self.MONSTER_TOP.fullmatch(self.rows[i-1], start, end):
                    if self.MONSTER_BOT.fullmatch(self.rows[i+1], start, end):
                        monsters += 1
        return monsters

    def count_sea_monsters(self):
        for _ in range(2):
            for __ in range(5):
                if self._count_sea_monsters_impl():
                    return self._count_sea_monsters_impl()
                self.rotate()
            self.flip()
        return 0


def find_corners(tiles):
    """Return (tile, matched_sides) for just the four corner tiles; O(n^2)."""
    candidates = set(tiles)
    corners = []
    for tile in tiles:
        matched_sides = []
        for side_const in Tile.SIDES:
            side = tile.side(side_const)
            for other in tiles:
                if tile == other:
                    continue
                if side in other.all_possible_sides():
                    matched_sides.append(side)
                    if len(matched_sides) > 2:
                        candidates.remove(tile)
                        break
            if len(matched_sides) > 2:
                break
        if len(matched_sides) == 2:
            corners.append((tile, matched_sides))
            if len(corners) == 4:
                break
    return corners


def arrange_tiles(tiles):
    """Return a list of rows of properly-arranged tiles."""
    rows = []

    # Orient an arbitrary corner tile so that it's the NW-most tile.
    corner_tile, (south, east) = find_corners(tiles)[0]
    corner_tile.transform_to_match(south, Tile.S)
    if corner_tile.side(Tile.E) not in (east, east[::-1]):
        corner_tile.flip()

    remaining = set(tiles)
    grid_size = int(math.sqrt(len(tiles)))
    row = [corner_tile]
    remaining.remove(corner_tile)
    while len(rows) < grid_size:
        while len(row) < grid_size:
            num_remaining = len(remaining)
            for tile in tiles:
                if tile not in remaining:
                    continue
                if tile.transform_to_match(row[-1].side(Tile.E), Tile.W):
                    row.append(tile)
                    remaining.remove(tile)
            if num_remaining == len(remaining):
                raise RuntimeError("Unable to find tile continue row.")
        rows.append(row)
        if len(rows) == grid_size:
            return rows
        num_remaining = len(remaining)
        for tile in tiles:
            if tile not in remaining:
                continue
            if tile.transform_to_match(row[0].side(Tile.S), Tile.N):
                row = [tile]
                remaining.remove(tile)
        if num_remaining == len(remaining):
            raise RuntimeError("Unable to find a tile to start next row.")


def stitch_tiles(arrangement):
    """Stitch a tile arrangement into a mega-tile, removing borders."""
    rows = []
    for tile_row in arrangement:
        for i in range(1, tile_row[0].size - 1):
            rows.append(''.join((tile.rows[i][1:-1] for tile in tile_row)))
    return Tile(0, rows)


def parse_tiles(input_lines):
    """From input lines, generate a list of tiles."""
    tiles = []
    tile_id = None
    tile_lines = []
    for line in input_lines:
        if line == '':
            tiles.append(Tile(tile_id, tile_lines))
            tile_id = None
            tile_lines = []
        elif line.startswith('Tile'):
            tile_id = int(line.split()[1][:-1])
        else:
            tile_lines.append(line)
    tiles.append(Tile(tile_id, tile_lines))
    return tiles


def run_tests():
    with open('day_20_sample.txt', 'r') as sample_file:
        tiles = parse_tiles(sample_file.read().splitlines())
    assert 9 == len(tiles)
    corners = tuple(find_corners(tiles))
    assert 20899048083289 == (corners[0][0].tile_id * corners[1][0].tile_id
                              * corners[2][0].tile_id * corners[3][0].tile_id)
    arranged = arrange_tiles(tiles)
    target_arrangement =[[1951, 2311, 3079],
                         [2729, 1427, 2473],
                         [2971, 1489, 1171]]
    assert target_arrangement == [[t.tile_id for t in row] for row in arranged]
    stitched = stitch_tiles(arranged)
    assert 2 == stitched.count_sea_monsters()
    assert 273 == stitched.roughness


def main(input_lines):
    run_tests()
    tiles = parse_tiles(input_lines)
    corners = tuple(find_corners(tiles))
    answer_one = (corners[0][0].tile_id * corners[1][0].tile_id
                  * corners[2][0].tile_id * corners[3][0].tile_id)
    arranged = arrange_tiles(tiles)
    stitched = stitch_tiles(arranged)
    answer_two = stitched.roughness
    return answer_one, answer_two


if __name__ == '__main__':
    answer_one, answer_two = main(_parse_args())
    print(f'Part One: {answer_one}')
    print(f'Part Two: {answer_two}')
