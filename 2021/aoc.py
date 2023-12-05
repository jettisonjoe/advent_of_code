"""Library of utilities for Advent of Code 2021."""

import collections


def get_neighbor_locs(rows, r, c, diag=False, center=False, fill=False):
    """Returns an iterable of neighbor locations of the given cell."""
    neighbors = []
    
    # Northwest
    if diag and r > 0 and c > 0:
        neighbors.append((r - 1, c - 1))
    elif fill:
        neighbors.append(None)
    
    # North
    if r > 0:
        neighbors.append((r - 1, c))
    elif fill:
        neighbors.append(None)
    
    # Northeast
    if diag and r > 0 and c < len(rows[0]) - 1:
        neighbors.append((r - 1, c + 1))
    elif fill:
        neighbors.append(None)
    
    # West
    if c > 0:
        neighbors.append((r, c - 1))
    elif fill:
        neighbors.append(None)
    
    # Center
    if center:
        neighbors.append((r, c))
    elif fill:
        neighbors.append(None)
    
    # East
    if c < len(rows[0]) - 1:
        neighbors.append((r, c + 1))
    elif fill:
        neighbors.append(None)
    
    # Southwest
    if diag and r < len(rows) - 1 and c > 0:
        neighbors.append((r + 1, c - 1))
    elif fill:
        neighbors.append(None)
    
    # South
    if r < len(rows) - 1:
        neighbors.append((r + 1, c))
    elif fill:
        neighbors.append(None)
    
    # Southeast
    if diag and r < len(rows) - 1  and c < len(rows[0]) - 1:
        neighbors.append((r + 1, c + 1))
    elif fill:
        neighbors.append(None)

    return neighbors


class Frequencies():
    """A frequency count with most and least common properties."""
    def __init__(self, corpus=None):
        self.freqs = collections.defaultdict(lambda: 0)
        if corpus:
            self.feed(*corpus)
    
    def __getitem__(self, key):
        return self.freqs[key]
    
    def feed(self, *entries):
        for entry in entries:
            self.freqs[entry] += 1
    
    @property
    def most_common(self):
        highest_count = 0
        most_common = None
        for value, count in self.freqs.items():
            if count > highest_count:
                highest_count = count
                most_common = value
        
        return most_common
    
    @property
    def least_common(self):
        lowest_count = float('inf')
        least_common = None
        for value, count in self.freqs.items():
            if count < lowest_count:
                lowest_count = count
                least_common = value
        
        return least_common