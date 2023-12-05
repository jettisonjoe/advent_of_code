import argparse
import itertools


def _parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument('card_key',
                        type=int,
                        help='Public key of the card.')
    parser.add_argument('door_key',
                        type=int,
                        help='Public key of the door.')
    return parser.parse_args()


def loop_size(key, subj):
    value = 1
    for i in itertools.count(start=1):
        value = value * subj
        value = value % 20201227
        if value == key:
            return i


def transform(subj, loop_size):
    value = 1
    for i in range(loop_size):
        value = value * subj
        value = value % 20201227
    return value


def run_tests():
    card_key = 5764801
    door_key = 17807724
    assert 8 == loop_size(card_key, 7)
    assert 11 == loop_size(door_key, 7)
    assert 14897079 == transform(17807724, 8)
    assert 14897079 == transform(5764801, 11)


def main(card_key, door_key):
    run_tests()
    card_loop = loop_size(card_key, 7)
    answer_one = transform(door_key, card_loop)
    answer_two = None
    return answer_one, answer_two


if __name__ == '__main__':
    answer_one, answer_two = main(**vars(_parse_args()))
    print(f'Part One: {answer_one}')
    print(f'Part Two: {answer_two}')
