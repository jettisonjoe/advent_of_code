import argparse


def _parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument('infile',
                        type=argparse.FileType('r'),
                        help='Input text file for this puzzle')
    args = parser.parse_args()
    return args.infile.read().splitlines()


class InfiniteLoop(Exception):
    """Raised when a machine detects an infinite loop"""


class Machine:
    def __init__(self, prog):
        self._prog = prog
        self._seen = set()
        self._pc = 0
        self._acc = 0

    def acc(self, n):
        self._acc += n
        self._pc += 1

    def jmp(self, n):
        self._pc += n

    def nop(self, n):
        self._pc += 1

    def run(self):
        while self._pc < len(self._prog):
            if self._pc in self._seen:
                raise InfiniteLoop()
            self._seen.add(self._pc)
            op, arg = self._prog[self._pc].split()
            getattr(self, op)(int(arg))

    def state(self):
        return self._acc


def debug(prog):
    machine = Machine(prog)
    try:
        machine.run()
    except InfiniteLoop:
        return machine.state()


def repair(prog):
    for i in range(len(prog)):
        op, arg = prog[i].split()
        if op not in ('nop', 'jmp'):
            continue
        patched = prog[:]
        if op == 'nop':
            patched[i] = f'jmp {arg}'
        elif op == 'jmp':
            patched[i] = f'nop {arg}'
        try:
            machine = Machine(patched)
            machine.run()
            return machine.state()
        except InfiniteLoop:
            continue


def main(input):
    answer_one = debug(input)
    answer_two = repair(input)
    return answer_one, answer_two


if __name__ == '__main__':
    answer_one, answer_two = main(_parse_args())
    print(f'Part One: {answer_one}')
    print(f'Part Two: {answer_two}')
