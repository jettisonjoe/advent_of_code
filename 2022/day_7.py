"""https://adventofcode.com/2022/day/7"""

from dataclasses import dataclass
import logging
import textwrap
from typing import Dict, List, Optional, Union


def run_tests() -> None:
    """Run regression tests using sample input."""
    test_input = textwrap.dedent(
        """\
        $ cd /
        $ ls
        dir a
        14848514 b.txt
        8504156 c.dat
        dir d
        $ cd a
        $ ls
        dir e
        29116 f
        2557 g
        62596 h.lst
        $ cd e
        $ ls
        584 i
        $ cd ..
        $ cd ..
        $ cd d
        $ ls
        4060174 j
        8033020 d.log
        5626152 d.ext
        7214296 k
    """
    )
    root = dir_from_history(test_input)

    assert root["/a/e"].size == 584
    assert root["/a"].size == 94853
    assert root["/d"].size == 24933642
    assert root.size == 48381165
    sum_of_lte = sum(node.size for node in find_dirs_lte(100000, root))
    logging.debug("Sum of dirs lte 100000: %s", sum_of_lte)
    assert sum_of_lte == 95437
    to_delete = find_dir_to_delete(root)
    assert to_delete.size == 24933642


@dataclass
class FileNode:
    name: str
    size: int
    parent: "DirNode"

    def __str__(self) -> str:
        return self.render()

    def render(self, prefix=""):
        """Return a str representation of this node."""
        return f"{prefix}- {self.name} (file, size={self.size})"


class DirNode:
    def __init__(self, name: str = "/"):
        self.name = name
        self.nodes: "Dict[str, Union[FileNode, DirNode]]" = {}
        self.parent: "Optional[DirNode]" = None

    def __getitem__(self, path: str) -> Union[FileNode, DirNode]:
        """Return file or directory at the given path."""
        if path == "/":
            return self.root

        if path == "..":
            if self.parent is None:
                return self
            return self.parent

        if path.startswith("/"):
            return self.root[path[1:]]

        if "/" not in path:
            return self.nodes[path]

        subdir, subpath = path.split("/", 1)
        assert isinstance(subdir, DirNode)
        return self.nodes[subdir][subpath]

    def __contains__(self, key):
        return key in ("/", "..") or key in self.nodes

    def __str__(self) -> str:
        return self.render()

    @property
    def size(self) -> int:
        """Compute the total size of this directory tree."""
        total_size = 0
        for node in self.nodes.values():
            total_size += node.size

        return total_size

    @property
    def root(self) -> "DirNode":
        """Return the root of this directory tree."""
        if self.parent is None:
            return self
        return self.parent.root

    def render(self, prefix: str = "") -> str:
        """Render the current directory as a str."""
        result = [f"{prefix}- {self.name} (dir)"]

        sorted_keys = sorted(self.nodes.keys(), key=lambda x: x.lower())
        for key in sorted_keys:
            result.append(self.nodes[key].render(prefix=f"{prefix}  "))

        return "\n".join(result)

    def add(self, node: Union[FileNode, DirNode]) -> None:
        """Add the node to this directory."""
        if node.name in self.nodes:
            raise ValueError(f"Node exists! {node.name}")
        self.nodes[node.name] = node
        node.parent = self


def dir_from_history(shell_history: str) -> DirNode:
    """Infer directory tree structure from shell command history."""
    root = DirNode()
    cwd = root
    lines = shell_history.splitlines()
    lines.reverse()

    while lines:
        line = lines.pop().split()
        assert line[0] == "$"
        cmd = line[1]

        if cmd == "cd":
            subdir = line[2]
            if subdir not in cwd:
                cwd.add(DirNode(subdir))
            new_cwd: Union[FileNode, DirNode] = cwd[subdir]
            assert isinstance(new_cwd, DirNode)
            cwd = new_cwd
            continue

        if cmd == "ls":
            while lines and not lines[-1].startswith("$"):
                new_node_str = lines.pop()
                if new_node_str.startswith("dir"):
                    _, name = new_node_str.split()
                    if name not in cwd:
                        cwd.add(DirNode(name))
                else:
                    logging.debug(f"Adding file: {new_node_str}")
                    size_str, name = new_node_str.split()
                    cwd.add(FileNode(name, int(size_str), cwd))
            continue

    return root


def dirs_by_size(dir_node: DirNode) -> List[DirNode]:
    """List all directories in order of size from largest to smallest."""
    all_dirs = set()
    search = [dir_node]
    while search:
        cur = search.pop()
        search.extend(x for x in cur.nodes.values() if isinstance(x, DirNode))
        all_dirs.add(cur)

    return sorted(all_dirs, key=lambda x: -x.size)


def find_dirs_lte(target_size: int, dir_node: DirNode) -> List[DirNode]:
    """Find all directories with total size less than or equal to target."""
    result = []
    remainder = dirs_by_size(dir_node)
    while remainder[-1].size <= target_size:
        result.append(remainder.pop())

    return result


def find_dir_to_delete(
    root: DirNode, disk_size: int = 70000000, free_needed: int = 30000000
) -> DirNode:
    """Find the smallest single directory to delete to get needed space."""
    free = disk_size - root.size
    to_free = free_needed - free
    assert to_free > 0
    remainder = dirs_by_size(root)
    while remainder:
        cur = remainder.pop()
        if cur.size >= to_free:
            return cur
    raise ValueError("Unable to find a deletion candidate")


def solve_part_1(puzzle_input: str) -> int:
    """Solve part 1 of today's puzzle."""
    root = dir_from_history(puzzle_input)
    return sum(node.size for node in find_dirs_lte(100000, root))


def solve_part_2(puzzle_input: str) -> int:
    """Solve part 2 of today's puzzle."""
    root = dir_from_history(puzzle_input)
    return find_dir_to_delete(root).size
