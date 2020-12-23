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


def parse_players(input_lines):
    players = []
    player_id = None
    deck = []
    for line in input_lines:
        if line.startswith('Player'):
            _, id_part = line.split()
            player_id = int(id_part[:-1])
            continue
        if '' == line:
            players.append(Player(player_id, deck))
            player_id = None
            deck = []
            continue
        deck.append(int(line))
    players.append(Player(player_id, deck))
    return players


Player = collections.namedtuple('Player', ('id', 'deck'))


class CombatGame:
    def __init__(self, *players):
        self.players = list(players)
        self.eliminated = []
        self.winner = None
        self.round = 0

    @staticmethod
    def score(player):
        return(sum((i + 1) * x for i, x in enumerate(player.deck[::-1])))

    def play_round(self, increment=True):
        if increment:
            self.round += 1
        winning_card = max(p.deck[0] for p in self.players)
        winner = [p for p in self.players if p.deck[0] == winning_card][0]
        winner.deck.pop(0)
        winner.deck.append(winning_card)
        winner.deck.extend(
            [p.deck.pop(0) for p in self.players if p != winner])
        for player in self.players:
            if len(player.deck) == 0:
                self.players.remove(player)
                self.eliminated.append(player)

    def resolve(self):
        while len(self.players) > 1:
            self.play_round()
        self.winner = self.players.pop()


class RecursiveCombatGame(CombatGame):
    def __init__(self, *players):
        self._seen = set()
        super().__init__(*players)

    @staticmethod
    def can_recurse(player):
        return player.deck[0] < len(player.deck)

    def state_redux(self):
        return tuple([tuple(p.deck) for p in self.players])

    def play_round(self):
        if self.state_redux() in self._seen:
            while len(self.players) > 1:
                self.eliminated.append(self.players.pop())
            return
        self._seen.add(self.state_redux())
        self.round += 1
        if all([self.can_recurse(p) for p in self.players]):
            sub_players = []
            for p in self.players:
                deck_size = p.deck[0]
                sub_players.append(Player(p.id, p.deck[1:1+deck_size]))
            sub_game = RecursiveCombatGame(*sub_players)
            sub_game.resolve()
            winner = [p for p in self.players if p.id == sub_game.winner.id][0]
            winning_card = winner.deck.pop(0)
            winner.deck.append(winning_card)
            winner.deck.extend(
                [p.deck.pop(0) for p in self.players if p != winner])
            return
        super().play_round(increment=False)


def run_tests():
    player_one = Player(1, [9, 2, 6, 3, 1])
    player_two = Player(2, [5, 8, 4, 7, 10])
    game = CombatGame(player_one, player_two)
    game.resolve()
    assert player_two == game.winner
    assert [3, 2, 10, 6, 8, 5, 9, 4, 7, 1] == game.winner.deck
    assert 306 == CombatGame.score(game.winner)
    player_one = Player(1, [9, 2, 6, 3, 1])
    player_two = Player(2, [5, 8, 4, 7, 10])
    game = RecursiveCombatGame(player_one, player_two)
    game.resolve()
    assert 291 == RecursiveCombatGame.score(game.winner)


def main(input_lines):
    run_tests()
    players = parse_players(input_lines)
    game = CombatGame(*players)
    game.resolve()
    answer_one = CombatGame.score(game.winner)
    players = parse_players(input_lines)
    game = RecursiveCombatGame(*players)
    game.resolve()
    answer_two = RecursiveCombatGame.score(game.winner)
    return answer_one, answer_two


if __name__ == '__main__':
    answer_one, answer_two = main(_parse_args())
    print(f'Part One: {answer_one}')
    print(f'Part Two: {answer_two}')
