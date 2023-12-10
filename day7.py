from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional, List


class NodeType(Enum):
    FILE, DIRECTORY = auto(), auto()


@dataclass
class Command:
    name: str
    arg: Optional[str] = None

    def __str__(self):
        return f"{self.name} {self.arg}" if self.arg is not None else self.name


class LineParser:
    @classmethod
    def parse(cls, line, cwd):
        if cls.is_command(line):
            out = cls.chomp(line).split()
            if len(out) == 2:
                cmd, arg = out
            else:
                cmd, arg = out[0], None
            if cmd in {"ls", "cd"}:
                return Command(cmd, arg)
        else:
            first, second = line.strip().split()
            if first == "dir":
                return FSNode(
                    name=second,
                    node_type=NodeType.DIRECTORY,
                    parent=cwd,
                )
            elif first.isdigit():
                return FSNode(
                    name=second,
                    node_type=NodeType.FILE,
                    descendants=None,
                    size=int(first),
                    parent=cwd,
                )

    @classmethod
    def chomp(cls, line):
        return line.lstrip("$").strip()

    @classmethod
    def is_command(cls, line):
        return line.startswith("$")


@dataclass
class FSNode:
    name: str
    node_type: NodeType
    descendants: Optional[List["FSNode"]] = field(default_factory=list)
    size: Optional[int] = None
    parent: Optional["FSNode"] = None

    def display_tree(self, offset=0):
        indent = ' ' * offset
        is_dir = self.node_type == NodeType.DIRECTORY
        maybe_slash = '/' if is_dir and self.parent is not None else ''
        print(f"{indent}{maybe_slash}{self.name}")
        if is_dir:
            for d in self.descendants:
                d.display_tree(offset + 2)

    def show_nodes(self):
        for node in self.traverse():
            print(node)

    def is_dir(self):
        return self.node_type == NodeType.DIRECTORY

    def get_size(self):
        if self.size is not None:
            return self.size
        elif self.is_dir():
            size = sum(
                d.size
                for d
                in self.traverse()
                if not d.is_dir()
            )
            if self.size is None:
                self.size = size
            return size

    def traverse(self):
        yield self
        if self.is_dir():
            for d in self.descendants:
                if d.is_dir():
                    yield from d.traverse()
                else:
                    yield d

    def __str__(self):
        s = [
            "D" if self.is_dir() else "F",
            self.name,
            str(self.size),
            self.parent.name if self.parent else "",
        ]
        return " ".join(s)


def get_lines(skip_first=False):
    with open("day7_input.txt") as f:
        if skip_first:
            next(f)
        for line in f:
            yield line.strip()


def build_fs(root):
    cwd = root
    contents = []
    for line in get_lines(skip_first=True):
        out = LineParser.parse(line, cwd)
        if isinstance(out, FSNode):
            contents.append(out)
        elif isinstance(out, Command):
            if out.name == "cd":
                if len(contents) > 0:
                    cwd.descendants = contents[:]
                    contents = []
                if out.arg == "..":
                    cwd = cwd.parent
                else:
                    for node in cwd.descendants:
                        if node.name == out.arg:
                            cwd = node
                            break
    if contents:
        cwd.descendants = contents[:]

    return root


def main():
    root = build_fs(FSNode(
        name="/",
        descendants=[],
        parent=None,
        node_type=NodeType.DIRECTORY,
        size=None,
    ))

    # part one
    SIZE_LIMIT = 100000
    all_sizes = [node.get_size() for node in root.traverse() if node.is_dir()]
    result = sum(size for size in all_sizes if size <= SIZE_LIMIT)
    print(result)

    root.get_size()

    # part two
    max_disk_space = 70000000
    update_size = 30000000
    taken_space = root.size
    free_space = max_disk_space - taken_space
    need_to_free = update_size - free_space
    print("DISK SPACE      ", max_disk_space)
    print("UPDATE SIZE     ", update_size)
    print("ALLOCATED SPACE ", taken_space)
    print("FREE SPACE      ", free_space)
    print("NEEDED SPACE     ", need_to_free)
    result = min(n.size for n in root.traverse() if n.is_dir() and n.size >= need_to_free)
    print(result)


if __name__ == '__main__':
    main()