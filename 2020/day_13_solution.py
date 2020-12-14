import argparse
import itertools

NO_BUS = -1


def _parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument('infile',
                        type=argparse.FileType('r'),
                        help='Input text file for this puzzle')
    args = parser.parse_args()
    return args.infile.read().splitlines()


def busses_from_string(bus_string):
    result = []
    for i, bus in enumerate(bus_string.split(',')):
        if bus == 'x':
            result.append((NO_BUS, i))
            continue
        result.append((int(bus), i))
    return result


class NotFoundError(Exception):
    """Raised internally when a candidate timestamp is invalidated."""


def first_sync(busses, step=None, offset=0):
    """Slow for large inputs."""
    b_max, max_idx = max(busses)
    if step is None:
        step = b_max
    for t_max in itertools.count(step=step):
        t = (t_max - offset) - max_idx
        try:
            for bus, i in busses:
                if bus == NO_BUS:
                    continue
                if (t + i) % bus != 0:
                    raise NotFoundError()
        except NotFoundError:
            continue
        return t


def first_sync_fast(busses):
    """But not *that* fast.

    There's probably the inkling of an approach that's *actually* efficient
    here, but this worked good enough for the puzzle input.
    """
    busses_copy = busses[:]
    b_max = max(busses_copy)
    busses_copy.remove(b_max)
    b_large = max(busses_copy)
    sub_sync = first_sync((b_max, b_large))
    prod = b_max[0] * b_large[0]
    diff = prod - (sub_sync + b_max[1])
    return first_sync(busses, step=prod, offset=diff)


def main(data):
    t = int(data[0])
    busses = [int(e) for e in data[1].split(',') if e != 'x']
    wait_times = [b - (t % b) for b in busses]
    idx = wait_times.index(min(wait_times))
    answer_one = busses[idx] * wait_times[idx]
    assert first_sync_fast(busses_from_string('17,x,13,19')) == 3417
    assert first_sync_fast(busses_from_string('67,7,59,61')) == 754018
    assert first_sync_fast(busses_from_string('67,x,7,59,61')) == 779210
    assert first_sync_fast(busses_from_string('67,7,x,59,61')) == 1261476
    assert first_sync_fast(busses_from_string('1789,37,47,1889')) == 1202161486
    answer_two = first_sync_fast(busses_from_string(data[1]))
    return answer_one, answer_two


if __name__ == '__main__':
    answer_one, answer_two = main(_parse_args())
    print(f'Part One: {answer_one}')
    print(f'Part Two: {answer_two}')
