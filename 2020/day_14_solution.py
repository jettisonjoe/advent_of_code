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


MaskCmd = collections.namedtuple('MaskCmd', ('mask_str'))
MemWriteCmd = collections.namedtuple('MemWriteCmd', ('addr', 'value'))


class Machine:
    def __init__(self):
        self.mem = {}
        self.and_mask = 2^36
        self.or_mask = 0
        self.prog = tuple()

    def load(self, prog):
        self.prog = prog

    def run(self):
        for cmd in self.prog:
            self.execute(cmd)

    def execute(self, cmd):
        if isinstance(cmd, MaskCmd):
            self.set_mask(cmd.mask_str)
        elif isinstance(cmd, MemWriteCmd):
            self.write_mem(cmd.addr, cmd.value)

    def set_mask(self, mask_str):
        and_mask_str = ''
        or_mask_str = ''
        for c in mask_str:
            if c == 'X':
                and_mask_str += '1'
                or_mask_str += '0'
            if c == '0':
                and_mask_str += '0'
                or_mask_str += '0'
            if c == '1':
                and_mask_str += '1'
                or_mask_str += '1'
        self.and_mask = int(and_mask_str, 2)
        self.or_mask = int(or_mask_str, 2)

    def write_mem(self, addr, value):
        value = value & self.and_mask
        value = value | self.or_mask
        self.mem[addr] = value


class MachineV2(Machine):
    def __init__(self):
        self.mem = {}
        self.mask = '0' * 36
        self.prog = tuple()

    def gen_addr(addr_str, vals):
        vals = vals[:]
        generated = ''
        for c in addr_str:
            if c == 'X':
                generated += vals.pop(0)
            else:
                generated

    def decode(self, addr_str):
        num_floating = self.mask.count('X')
        max_floating = 2 ** num_floating
        combos = [format(n, f'0{num_floating}b') for n in range(max_floating)]
        addrs = []
        for combo in combos:
            bits = [b for b in combo]
            addr = ''
            for i in range(len(self.mask)):
                if self.mask[i] == 'X':
                    addr += bits.pop(0)
                if self.mask[i] == '1':
                    addr += '1'
                if self.mask[i] == '0':
                    addr += addr_str[i]
            addrs.append(int(addr, 2))
        return addrs

    def set_mask(self, mask_str):
        self.mask = mask_str

    def write_mem(self, addr, value):
        addrs = self.decode(format(addr, '036b'))
        for a in addrs:
            self.mem[a] = value


def prog_from_data(data):
    result = []
    for line in data:
        op, arg = line.split(' = ')
        if op == 'mask':
            result.append(MaskCmd(arg))
        else:
            _, addr_part = op.split('[')
            addr = addr_part[:-1]
            result.append(MemWriteCmd(int(addr), int(arg)))
    return result


def main(data):
    prog = prog_from_data(data)
    machine = Machine()
    machine.load(prog)
    machine.run()
    answer_one = sum(val for _, val in machine.mem.items())
    machine_v2 = MachineV2()
    machine_v2.load(prog)
    machine_v2.run()
    answer_two = sum(val for _, val in machine_v2.mem.items())
    return answer_one, answer_two


if __name__ == '__main__':
    answer_one, answer_two = main(_parse_args())
    print(f'Part One: {answer_one}')
    print(f'Part Two: {answer_two}')
