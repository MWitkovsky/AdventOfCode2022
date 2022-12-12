# Path hack
import os
import sys
sys.path.insert(0, os.path.abspath("../../"))  # noqa

from lib import parsing


ROPE_MOVEMENTS = {
    "R": (1, 0),
    "U": (0, 1),
    "L": (-1, 0),
    "D": (0, -1)
}


class RopeNode:
    def __init__(self):
        self.__prev = None  # type: RopeNode
        self.__next = None  # type: RopeNode
        self.__x = 0
        self.__y = 0
        self.__visited_positions = {(0, 0)}  # type: set[tuple[int, int]]

    def __move_body(self) -> None:
        dx = self.__prev.x - self.__x
        dy = self.__prev.y - self.__y
        abs_dx = abs(dx)
        abs_dy = abs(dy)
        if 2 not in (abs_dx, abs_dy):
            return

        if dy != 0:
            self.__y += 1 if dy > 0 else -1
        if dx != 0:
            self.__x += 1 if dx > 0 else -1
        self.__visited_positions.add((self.__x, self.__y))
        if self.__next is not None:
            self.__next.__move_body()

    def set_prev(self, node: "RopeNode") -> None:
        self.__prev = node

    def set_next(self, node: "RopeNode") -> None:
        self.__next = node

    def move_head(self, dx: int, dy: int) -> None:
        if self.__prev is not None:
            raise ValueError(
                "Cannot call move_head on RopeNode with previous node"
            )

        self.__x += dx
        self.__y += dy
        self.__visited_positions.add((self.__x, self.__y))
        if self.__next is not None:
            self.__next.__move_body()

    @property
    def prev(self) -> "RopeNode":
        return self.__prev

    @property
    def next(self) -> "RopeNode":
        return self.__next

    @property
    def x(self) -> int:
        return self.__x

    @property
    def y(self) -> int:
        return self.__y

    @property
    def num_visited_positions(self) -> int:
        return len(self.__visited_positions)


class Rope:
    def __init__(self, length: int):
        self.__rope_nodes = []  # type: list[RopeNode]
        for i in range(length):
            new_node = RopeNode()
            self.__rope_nodes.append(new_node)
            if i != 0:
                prev_node = self.__rope_nodes[i-1]
                new_node.set_prev(prev_node)
                prev_node.set_next(new_node)

    def move_rope(self, x: int, y: int) -> None:
        self.__rope_nodes[0].move_head(x, y)

    def render_rope(self, x_dim: int, y_dim: int):
        half_x_dim = x_dim // 2
        half_y_dim = y_dim // 2
        rope_positions = {
            (node.x+half_x_dim, node.y+half_y_dim)
            for node in self.__rope_nodes
        }
        os.system("cls")
        for y in range(y_dim):
            for x in range(x_dim):
                if (x, y) in rope_positions:
                    print("#", end="")
                else:
                    print(".", end="")
            print()

    @property
    def head(self) -> RopeNode:
        return self.__rope_nodes[0]

    @property
    def tail(self) -> RopeNode:
        return self.__rope_nodes[-1]


def _day(inp: list[str]):
    """
    Part 1:
        Simulate your complete hypothetical series of motions. 
        How many positions does the tail of the rope visit at least once?
    Part 2:
        Rather than two knots, you now must simulate a rope consisting of 
        ten knots.
    """
    rope_movements = []  # type: list[tuple[tuple[int, int], int]]
    for rope_movement_desc in inp:
        rope_movement_desc = rope_movement_desc.split(" ")
        movement = ROPE_MOVEMENTS[rope_movement_desc[0]]
        times = int(rope_movement_desc[1])
        rope_movements.append((movement, times))

    part1_rope = Rope(2)
    part2_rope = Rope(10)
    for rope_movement, times in rope_movements:
        for _ in range(times):
            part1_rope.move_rope(*rope_movement)
            part2_rope.move_rope(*rope_movement)
            # part2_rope.render_rope(50, 20)

    print(f"Part 1: {part1_rope.tail.num_visited_positions}")
    print(f"Part 1: {part2_rope.tail.num_visited_positions}")


if __name__ == "__main__":
    parser = parsing.InputParser("inp.txt")
    inp = parser.to_array()
    parser.close()

    _day(inp)
