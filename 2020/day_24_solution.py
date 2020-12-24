import argparse
import collections


def _parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument('infile',
                        type=argparse.FileType('r'),
                        help='Input text file for this puzzle')
    args = parser.parse_args()
    return args.infile.read().splitlines()


LobbyLayout = collections.namedtuple('LobbyLayout', ('touches', 'colors'))


def tile_for_dirs(directions):
    """Return the x, y pair for the tile arrived at by following directions."""
    x, y = 0, 0
    while directions:
        if directions.startswith('e'):
            x += 1
            directions = directions[1:]
        elif directions.startswith('se'):
            x += 1
            y -= 1
            directions = directions[2:]
        elif directions.startswith('sw'):
            y -= 1
            directions = directions[2:]
        elif directions.startswith('w'):
            x -= 1
            directions = directions[1:]
        elif directions.startswith('nw'):
            x -= 1
            y += 1
            directions = directions[2:]
        elif directions.startswith('ne'):
            y += 1
            directions = directions[2:]
        else:
            raise ValueError(f'Unrecognized directions: {directions}')
    return x, y


def layout_lobby(direction_lines):
    touches = []
    colors = collections.defaultdict(lambda: 'white')
    for line in direction_lines:
        tile = tile_for_dirs(line)
        touches.append(tile)
        if colors[tile] == 'black':
            del colors[tile]
        else:
            colors[tile] = 'black'
    return LobbyLayout(touches, colors)


def adjacent_coords(x, y):
    return ((x + 1, y),
            (x + 1, y - 1),
            (x, y - 1),
            (x - 1, y),
            (x - 1, y + 1),
            (x, y + 1))


def elapse_day(lobby_colors):
    to_del = []
    to_check_for_add = []
    for tile in lobby_colors:
        adjacents = adjacent_coords(*tile)
        to_check_for_add.extend(adjacents)
        black_adjacents = [t for t in adjacents if t in lobby_colors]
        if len(black_adjacents) == 0 or len(black_adjacents) > 2:
            to_del.append(tile)

    to_add = []
    for tile in to_check_for_add:
        adjacents = adjacent_coords(*tile)
        black_adjacents = [t for t in adjacents if t in lobby_colors]
        if len(black_adjacents) == 2:
            to_add.append(tile)

    for tile in to_del:
        del lobby_colors[tile]
    for tile in to_add:
        lobby_colors[tile] = 'black'


def run_tests():
    sample_lines = ('sesenwnenenewseeswwswswwnenewsewsw',
                    'neeenesenwnwwswnenewnwwsewnenwseswesw',
                    'seswneswswsenwwnwse',
                    'nwnwneseeswswnenewneswwnewseswneseene',
                    'swweswneswnenwsewnwneneseenw',
                    'eesenwseswswnenwswnwnwsewwnwsene',
                    'sewnenenenesenwsewnenwwwse',
                    'wenwwweseeeweswwwnwwe',
                    'wsweesenenewnwwnwsenewsenwwsesesenwne',
                    'neeswseenwwswnwswswnw',
                    'nenwswwsewswnenenewsenwsenwnesesenew',
                    'enewnwewneswsewnwswenweswnenwsenwsw',
                    'sweneswneswneneenwnewenewwneswswnese',
                    'swwesenesewenwneswnwwneseswwne',
                    'enesenwswwswneneswsenwnewswseenwsese',
                    'wnwnesenesenenwwnenwsewesewsesesew',
                    'nenewswnwewswnenesenwnesewesw',
                    'eneswnwswnwsenenwnwnwwseeswneewsenese',
                    'neswnwewnwnwseenwseesewsenwsweewe',
                    'wseweeenwnesenwwwswnew')
    assert 10 == len(layout_lobby(sample_lines).colors)
    lobby = layout_lobby(sample_lines)
    elapse_day(lobby.colors)
    assert 15 == len(lobby.colors)
    elapse_day(lobby.colors)
    assert 12 == len(lobby.colors)
    elapse_day(lobby.colors)
    assert 25 == len(lobby.colors)
    elapse_day(lobby.colors)
    assert 14 == len(lobby.colors)


def main(input_lines):
    run_tests()
    answer_one = len(layout_lobby(input_lines).colors.keys())
    lobby = layout_lobby(input_lines)
    for _ in range(100):
        elapse_day(lobby.colors)
    answer_two = len(lobby.colors)
    return answer_one, answer_two


if __name__ == '__main__':
    answer_one, answer_two = main(_parse_args())
    print(f'Part One: {answer_one}')
    print(f'Part Two: {answer_two}')
