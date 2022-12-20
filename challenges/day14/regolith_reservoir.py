# Path hack
import os
import sys
sys.path.insert(0, os.path.abspath("../../"))  # noqa

from collections import defaultdict
from lib import parsing


class TileType:
    AIR = 0
    SAND = 1
    ROCK = 2
    SOURCE = 3


class Reservoir:
    @classmethod
    def __get_vertex_from_str_desc(cls, vertex_desc: str) -> tuple[int, int]:
        return tuple(map(int, vertex_desc.split(",")))

    def __record_tile(self, x: int, y: int, tile_type: int) -> None:
        self.__min_x = min(self.__min_x, x)
        self.__max_x = max(self.__max_x, x)
        self.__min_y = min(self.__min_y, y)
        self.__max_y = max(self.__max_y, y)
        self.__map[y][x] = tile_type

    def __record_rock_path(self, pos1: tuple[int, int], pos2: tuple[int, int]):
        same_idx = 0 if pos1[0] == pos2[0] else 1
        diff_idx = 1 if same_idx == 0 else 0

        # ensure direction always positive
        diff = pos1[diff_idx] - pos2[diff_idx]
        if diff > 0:
            pos1, pos2 = pos2, pos1

        same_val = pos1[same_idx]
        lo_val = pos1[diff_idx]
        for i in range(lo_val, lo_val + abs(diff) + 1):
            if diff_idx == 0:
                self.__record_tile(i, same_val, TileType.ROCK)
            else:
                self.__record_tile(same_val, i, TileType.ROCK)

    def __init__(self, rock_path_descs: list[str],
                 source_pos: tuple[int, int]):
        self.__min_x = float("inf")
        self.__max_x = -1
        self.__min_y = float("inf")
        self.__max_y = -1
        self.__map = defaultdict(
            lambda: defaultdict(
                lambda: TileType.AIR
            )
        )  # type: dict[int, dict[int, int]]
        self.__source_pos = source_pos
        self.__record_tile(source_pos[0], source_pos[1], TileType.SOURCE)
        for rock_path_desc in rock_path_descs:
            rock_path_vertexes = rock_path_desc.split(" -> ")
            for i in range(0, len(rock_path_vertexes)-1):
                v1 = Reservoir.__get_vertex_from_str_desc(
                    rock_path_vertexes[i]
                )
                v2 = Reservoir.__get_vertex_from_str_desc(
                    rock_path_vertexes[i+1]
                )
                self.__record_rock_path(v1, v2)

    def render_map_to_file(self, fn: str = "out.txt") -> None:
        with open(fn, "w") as f:
            for y in range(self.__min_y, self.__max_y+1):
                for x in range(self.__min_x, self.__max_x+1):
                    tile = self.__map[y][x]
                    if tile == TileType.AIR:
                        f.write(" ")
                    elif tile == TileType.SAND:
                        f.write("*")
                    elif tile == TileType.ROCK:
                        f.write("#")
                    elif tile == TileType.SOURCE:
                        f.write("V")
                f.write("\n")


def _regolith_reservoir(inp: list[str]):
    """
    Part 1:
        Using your scan, simulate the falling sand. How many units of sand
        come to rest before sand starts flowing into the abyss below?
    Part 2:

    """
    reservoir = Reservoir(inp, (500, 0))
    reservoir.render_map_to_file()
    pass


if __name__ == "__main__":
    parser = parsing.InputParser("inp.txt")
    inp = parser.to_array()
    parser.close()

    _regolith_reservoir(inp)
