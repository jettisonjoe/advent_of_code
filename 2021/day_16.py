"""Advent of Code 2021

Day 16:
  https://adventofcode.com/2021/day/16
"""

import argparse
import collections
import functools
import operator
from pathlib import Path

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


class Packet():
    """POD class for BITS packets."""
    def __init__(self, version=None, type_id=None, value=None, subpackets=None):
        self.version = version
        self.type_id = type_id
        self.subpackets = subpackets
        self._value = value
    
    def __repr__(self):
        return f'Packet(version={self.version})'
    
    @property
    def is_literal(self):
        return self.type_id == 4
    
    @property
    def is_operator(self):
        return self.type_id != 4
    
    @property
    def value(self):
        # literal
        if self.is_literal:
            return self._value
        
        # sum
        if self.type_id == 0:
            return sum(packet.value for packet in self.subpackets)
        
        # product
        if self.type_id == 1:
            return functools.reduce(
                operator.mul, (packet.value for packet in self.subpackets))
        
        # minimum
        if self.type_id == 2:
            return min(packet.value for packet in self.subpackets)
        
        # maximum
        if self.type_id == 3:
            return max(packet.value for packet in self.subpackets)

        # greater than
        if self.type_id == 5:
            if self.subpackets[0].value > self.subpackets[1].value:
                return 1
            return 0
        
        # less than
        if self.type_id == 6:
            if self.subpackets[0].value < self.subpackets[1].value:
                return 1
            return 0
        
        # equal to
        if self.type_id == 7:
            if self.subpackets[0].value == self.subpackets[1].value:
                return 1
            return 0
    
    @value.setter
    def value(self, value):
        self._value = value


class PacketDecoder():
    """Decodes BITS packets."""
    HEX_TO_BITS = {
        '0': '0000',
        '1': '0001',
        '2': '0010',
        '3': '0011',
        '4': '0100',
        '5': '0101',
        '6': '0110',
        '7': '0111',
        '8': '1000',
        '9': '1001',
        'A': '1010',
        'B': '1011',
        'C': '1100',
        'D': '1101',
        'E': '1110',
        'F': '1111',
    }

    def __init__(self):
        self.packets = []
        self.version_sum = 0
        self.bits = collections.deque()
    
    def feed(self, hex_str):
        """Feed hex characters into the decoder."""
        for char in hex_str:
            self.bits += list(self.HEX_TO_BITS[char])
    
    def consume(self, num_bits):
        """Remove num_bits bits from the queue and return the int value."""
        bits = ''
        for _ in range(num_bits):
            bits += self.bits.popleft()
        return int(''.join(bits), 2)
    
    def consume_raw(self, num_bits):
        """Remove num_bits bits from the queue and return the bit string."""
        bits = ''
        for _ in range(num_bits):
            bits += self.bits.popleft()
        return ''.join(bits)
    
    def decode(self):
        """Decode the entire transmission."""
        while self.bits:
            # Stop if all that's left is 0 bits.
            if all(bit == '0' for bit in self.bits):
                return

            packet = self.decode_packet()
            self.packets.append(packet)
    
    def decode_literal_value(self):
        """Decode a literal value and return the int."""
        value_bits = ''

        prefix = 1
        while prefix == 1:
            prefix = self.consume(1)
            value_bits += self.consume_raw(4)
        
        return int(value_bits, 2)
            
    def decode_subpacket_bits(self, num_bits):
        """Decode packets from the next num_bits bits."""
        starting_bits_len = len(self.bits)
        packets = []
        while len(self.bits) > starting_bits_len - num_bits:
            packets.append(self.decode_packet())
        if starting_bits_len - len(self.bits) != num_bits:
            raise RuntimeError(
                f'Expected {num_bits} bits of packets, got {len(self.bits)}.')
        return packets
    
    def decode_subpackets(self, num_packets):
        """Decode num_packets packets."""
        packets = []
        for _ in range(num_packets):
            packets.append(self.decode_packet())
        return packets
    
    def decode_packet(self):
        """Decode a single packet (including subpackets) from the input bits."""
        packet = Packet(version=self.consume(3), type_id=self.consume(3))

        if packet.is_literal:
            packet.value = self.decode_literal_value()
        
        if packet.is_operator:
            length_type_id = self.consume(1)

            if length_type_id == 0:
                num_subpacket_bits = self.consume(15)
                subpackets = self.decode_subpacket_bits(num_subpacket_bits)
                packet.subpackets = subpackets

            if length_type_id == 1:
                num_subpackets = self.consume(11)
                packet.subpackets = self.decode_subpackets(num_subpackets)
        
        self.version_sum += packet.version
        return packet


def solve_part_1(puzzle_input):
    """Solve part 1 of today's puzzle."""
    decoder = PacketDecoder()
    decoder.feed(puzzle_input)
    decoder.decode()
    return decoder.version_sum


def solve_part_2(puzzle_input):
    """Solve part 2 of today's puzzle."""
    decoder = PacketDecoder()
    decoder.feed(puzzle_input)
    decoder.decode()
    return decoder.packets[0].value


def run_tests():
    """Run regression tests."""
    assert 16 == solve_part_1('8A004A801A8002F478')
    assert 12 == solve_part_1('620080001611562C8802118E34')
    assert 23 == solve_part_1('C0015000016115A2E0802F182340')
    assert 31 == solve_part_1('A0016C880162017C3686B18A3D4780')


def format_input(puzzle_input):
    """Format the puzzle input."""
    return puzzle_input.strip()


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
