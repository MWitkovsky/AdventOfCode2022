# Path hack
from io import TextIOWrapper
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
    SAND_REST = 4


class SandGrain:
    def __init__(self, x: int, y: int):
        self.__x = x
        self.__y = y
        self.__at_rest = False

    def move(self, map: dict[int, dict[int, int]],
             floor_y: int = None) -> None:
        if floor_y is not None and self.__y+1 == floor_y:
            self.__at_rest = True
            return

        target_row = map[self.__y + 1]
        if target_row[self.__x] == TileType.AIR:
            self.__y += 1
        elif target_row[self.__x-1] == TileType.AIR:
            self.__x -= 1
            self.__y += 1
        elif target_row[self.__x+1] == TileType.AIR:
            self.__x += 1
            self.__y += 1
        else:
            self.__at_rest = True

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def at_rest(self):
        return self.__at_rest


class Reservoir:
    @classmethod
    def __get_vertex_from_str_desc(cls, vertex_desc: str) -> tuple[int, int]:
        return tuple(map(int, vertex_desc.split(",")))

    def __record_tile(self, x: int, y: int, tile_type: int) -> None:
        if tile_type in (TileType.SOURCE, TileType.ROCK):
            self.__min_y = min(self.__min_y, y)
            self.__max_y = max(self.__max_y, y)
        self.__min_x = min(self.__min_x, x)
        self.__max_x = max(self.__max_x, x)
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
        self.__active_sand = []  # type: list[SandGrain]
        self.__spawner_delay = False
        self.__num_particles_spawned = 0
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

    def __try_spawn_sand(self) -> bool:
        if self.__spawner_delay:
            self.__spawner_delay = False
            return

        spawner_tile = self.__map[self.__source_pos[1]][self.__source_pos[0]]
        if spawner_tile == TileType.SOURCE:
            self.__active_sand.append(
                SandGrain(self.__source_pos[0], self.__source_pos[1])
            )
            self.__record_tile(
                self.__source_pos[0], self.__source_pos[1], TileType.SAND
            )
            self.__spawner_delay = True
            self.__num_particles_spawned += 1
            return True
        return False

    def __move_sand(self, floor_exists: bool = False) -> None:
        grains_to_remove = []
        for grain in self.__active_sand:
            if (grain.x, grain.y) == self.__source_pos:
                before_tile_type = TileType.SOURCE
            else:
                before_tile_type = TileType.AIR
            self.__record_tile(grain.x, grain.y, before_tile_type)

            floor_y = None
            if floor_exists:
                floor_y = self.__max_y + 2
            grain.move(self.__map, floor_y=floor_y)

            after_pos = (grain.x, grain.y)
            if grain.at_rest:
                grains_to_remove.append(grain)
                after_tile_type = TileType.SAND_REST
            else:
                after_tile_type = TileType.SAND

            self.__record_tile(after_pos[0], after_pos[1], after_tile_type)

        for grain in grains_to_remove:
            self.__active_sand.remove(grain)

    def simulate_sand_num_particles(self, num_particles: int) -> None:
        while num_particles > 0 or len(self.__active_sand) != 0:
            if num_particles > 0:
                num_particles -= self.__try_spawn_sand()
            self.__move_sand()

    def simulate_sand_until_covered(self) -> None:
        while self.__map[self.__source_pos[1]][self.__source_pos[0]] != \
                TileType.SAND_REST:
            self.__try_spawn_sand()
            self.__move_sand(floor_exists=True)

    def render_map_to_file(self, fn: str = None) -> None:
        if fn:
            out = open(fn, "w")
        else:
            out = sys.stdout

        for y in range(self.__min_y, self.__max_y+1):
            for x in range(self.__min_x, self.__max_x+1):
                tile = self.__map[y][x]
                if tile == TileType.AIR:
                    out.write(" ")
                elif tile == TileType.SAND:
                    out.write("*")
                elif tile == TileType.SAND_REST:
                    out.write("O")
                elif tile == TileType.ROCK:
                    out.write("#")
                elif tile == TileType.SOURCE:
                    out.write("V")
            out.write("\n")

        if fn is not None:
            out.close()

    @property
    def num_particles_spawned(self):
        return self.__num_particles_spawned


def _regolith_reservoir(inp: list[str]):
    """
    Part 1:
        Using your scan, simulate the falling sand. How many units of sand
        come to rest before sand starts flowing into the abyss below?
    Part 2:
        Using your scan, simulate the falling sand until the source of the 
        sand becomes blocked. How many units of sand come to rest?
    """
    reservoir = Reservoir(inp, (500, 0))
    # reservoir.simulate_sand_num_particles(1513)
    # reservoir.render_map_to_file("out.txt")
    reservoir.simulate_sand_until_covered()
    reservoir.render_map_to_file("out.txt")
    print(f"Num particles spawned: {reservoir.num_particles_spawned}")


if __name__ == "__main__":
    parser = parsing.InputParser("inp.txt")
    inp = parser.to_array()
    parser.close()

    _regolith_reservoir(inp)
