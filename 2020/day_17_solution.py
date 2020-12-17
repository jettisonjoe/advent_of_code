import argparse
import itertools

def _parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument('infile',
                        type=argparse.FileType('r'),
                        help='Input text file for this puzzle')
    args = parser.parse_args()
    return args.infile.read().splitlines()


def _data_from_lines(lines, z=0):
    """Takes lines of text and returns a set of coordinate 3-tuples."""
    data = set()
    for x in range(len(lines)):
        for y in range(len(lines[0])):
            if lines[x][y] == '#':
                data.add((x, y, z))
    return data


class Simulator:
    def __init__(self, data, k=3):
        self.data = self.pad(data, k)

    @staticmethod
    def pad(data, k):
        """Returns a copy of a set of tuples, 0-padded out to k elements."""
        result = set()
        for coords in data:
            padded = list(coords)
            while len(padded) < k:
                padded.append(0)
            result.add(tuple(padded))
        return result

    @staticmethod
    def all_neighbors(coords):
        """Return all neighboring points to the given coordinates."""
        offsets = set(
            itertools.product((-1, 0, 1), repeat=len(coords)))
        offsets.remove(tuple([0 for _ in coords]))
        neighbors = set()
        for offset in offsets:
            neighbor = []
            for i in range(len(coords)):
                neighbor.append(coords[i] + offset[i])
            neighbors.add(tuple(neighbor))
        return neighbors

    @classmethod
    def count_active_neighbors(cls, coords, data):
        """Returns the number of coords's neighbors present in data."""
        all_neighbors = cls.all_neighbors(coords)
        active_neighbors = set(filter(lambda e: e in data, all_neighbors))
        return len(active_neighbors)

    @classmethod
    def compute_step(cls, data):
        """Returns simulation data resulting from one step from data."""
        result = data.copy()
        checked = set()
        for coords in data:
            neighbors = cls.all_neighbors(coords)
            for n in neighbors:
                if n in checked or n in data:
                    continue
                if cls.count_active_neighbors(n, data) == 3:
                    result.add(n)
                checked.add(n)
            if cls.count_active_neighbors(coords, data) not in (2, 3):
                result.remove(coords)
        return result

    @property
    def active(self):
        """Return the number of active cells in the simulation."""
        return len(self.data)

    def run(self, steps=6):
        """Run the simulation."""
        for i in range(steps):
            self.data = self.compute_step(self.data)


def run_tests():
    sample_data = {(0, 1, 0), (1, 2, 0), (2, 0, 0), (2, 1, 0), (2, 2, 0)}
    assert sample_data == _data_from_lines(('.#.', '..#', '###'))
    sim = Simulator(sample_data)
    sim.run()
    assert 112 == sim.active
    hyper_sim = Simulator(sample_data, k=4)
    hyper_sim.run()
    assert 848 == hyper_sim.active


def main(input_lines):
    run_tests()
    sim = Simulator(_data_from_lines(input_lines))
    sim.run()
    answer_one = sim.active
    hyper_sim = Simulator(_data_from_lines(input_lines), k=4)
    hyper_sim.run()
    answer_two = hyper_sim.active
    return answer_one, answer_two


if __name__ == '__main__':
    answer_one, answer_two = main(_parse_args())
    print(f'Part One: {answer_one}')
    print(f'Part Two: {answer_two}')
