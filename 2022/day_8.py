"""https://adventofcode.com/2022/day/8"""

import collections
import textwrap
from typing import Dict, List, Set


def run_tests() -> None:
    """Run simple unit tests using sample input."""
    test_input = textwrap.dedent(
        """\
        30373
        25512
        65332
        33549
        35390
    """
    )
    forest = Forest.from_str(test_input)

    assert forest[1][1].visibility == {"left", "top"}
    assert forest[1][2].visibility == {"top", "right"}
    assert forest[1][3].visibility == set()
    assert forest[2][1].visibility == {"right"}
    assert forest[2][2].visibility == set()
    assert forest[2][3].visibility == {"right"}
    assert not forest[3][1].visible
    assert forest[3][2].visible
    assert not forest[3][3].visible
    assert forest.visible_count == 21
    assert forest[1][2].view_distance["up"] == 1
    assert forest[1][2].view_distance["left"] == 1
    assert forest[1][2].view_distance["right"] == 2
    assert forest[1][2].view_distance["down"] == 2
    assert forest[1][2].scenic_score == 4
    assert forest[3][2].view_distance["up"] == 2
    assert forest[3][2].view_distance["left"] == 2
    assert forest[3][2].view_distance["down"] == 1
    assert forest[3][2].view_distance["right"] == 2
    assert forest[3][2].scenic_score == 8


class Tree:
    def __init__(self, height: int):
        self.height = height
        self.visibility: Set[str] = set()
        self.view_distance: Dict[str, int] = collections.defaultdict(lambda: 0)

    @property
    def visible(self) -> bool:
        return bool(self.visibility)

    @property
    def scenic_score(self) -> int:
        return (
            self.view_distance["left"]
            * self.view_distance["right"]
            * self.view_distance["up"]
            * self.view_distance["down"]
        )


class Forest:
    def __init__(self, trees: List[List[Tree]]):
        self.trees = trees
        self._visible: Set[Tree] = set()
        self._compute_visibility()

    def __getitem__(self, key: int) -> List[Tree]:
        """Return the corresponding row of trees."""
        return self.trees[key]

    @classmethod
    def from_str(cls, tree_str: str) -> "Forest":
        """Parse the str into a forest of trees."""
        trees = []
        for line in tree_str.splitlines():
            row = []
            for height in line:
                row.append(Tree(int(height)))
            trees.append(row)

        return cls(trees)

    def _compute_visibility(self) -> None:
        """Compute each tree's visibility."""
        for row in self.trees:
            viewers: Set[Tree] = set()
            for tree in row:
                to_remove = set()
                for viewer in viewers:
                    viewer.view_distance["right"] += 1
                    if tree.height >= viewer.height:
                        to_remove.add(viewer)
                viewers -= to_remove
                viewers.add(tree)
            for viewer in viewers:
                viewer.visibility.add("right")
                self._visible.add(viewer)

            viewers = set()
            for tree in reversed(row):
                to_remove = set()
                for viewer in viewers:
                    viewer.view_distance["left"] += 1
                    if tree.height >= viewer.height:
                        to_remove.add(viewer)
                viewers -= to_remove
                viewers.add(tree)
            for viewer in viewers:
                viewer.visibility.add("left")
                self._visible.add(viewer)

        for col_idx in range(len(self.trees[0])):
            viewers = set()
            for row_idx in range(len(self.trees)):
                tree = self.trees[row_idx][col_idx]
                to_remove = set()
                for viewer in viewers:
                    viewer.view_distance["down"] += 1
                    if tree.height >= viewer.height:
                        to_remove.add(viewer)
                viewers -= to_remove
                viewers.add(tree)
            for viewer in viewers:
                viewer.visibility.add("bottom")
                self._visible.add(viewer)

            viewers = set()
            for row_idx in reversed(range(len(self.trees))):
                tree = self.trees[row_idx][col_idx]
                to_remove = set()
                for viewer in viewers:
                    viewer.view_distance["up"] += 1
                    if tree.height >= viewer.height:
                        to_remove.add(viewer)
                viewers -= to_remove
                viewers.add(tree)
            for viewer in viewers:
                viewer.visibility.add("top")
                self._visible.add(viewer)

    @property
    def visible_count(self) -> int:
        """How many trees are visible (from any direction)."""
        return len(self._visible)

    def most_scenic_tree(self) -> Tree:
        """Return the most scenic tree in the forest."""
        most_scenic = self.trees[0][0]
        for row in self.trees:
            for tree in row:
                if tree.scenic_score > most_scenic.scenic_score:
                    most_scenic = tree

        return most_scenic


def solve_part_1(puzzle_input: str) -> int:
    """Solve part 1 of today's puzzle."""
    forest = Forest.from_str(puzzle_input)
    return forest.visible_count


def solve_part_2(puzzle_input: str) -> int:
    """Solve part 2 of today's puzzle."""
    forest = Forest.from_str(puzzle_input)
    return forest.most_scenic_tree().scenic_score
