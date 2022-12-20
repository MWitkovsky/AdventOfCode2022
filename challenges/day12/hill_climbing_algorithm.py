# Path hack
import os
import sys
sys.path.insert(0, os.path.abspath("../../"))  # noqa

from lib import parsing

GOAL_HEIGHT = 123
MIN_HEIGHT = ord("a")


def _can_walk_to_node(map: list[list[int, int]], from_pos: tuple[int, int],
                      to_pos: tuple[int, int]) -> bool:
    from_val = map[from_pos[1]][from_pos[0]]
    target_x = to_pos[0]
    target_y = to_pos[1]

    if target_x < 0 or target_y < 0:
        return False

    try:
        to_val = map[target_y][target_x]
    except Exception:
        return False

    from_val += 1  # plus one for travelling rule comparison
    return to_val <= from_val


def bfs(map: list[list[int, int]], start_x: int, start_y: int) -> int:
    start_node = (start_x, start_y, 0)
    visited_nodes = set()  # set[tuple[int, int]]
    queue = [start_node]  # list[tuple[int, int, int]]
    visited_nodes.add((start_node[0], start_node[1]))
    while len(queue) > 0:
        node = queue.pop(0)
        depth = node[2] + 1
        potential_neighbors = [
            (node[0]-1, node[1], depth),  # left
            (node[0]+1, node[1], depth),  # right
            (node[0], node[1]-1, depth),  # up
            (node[0], node[1]+1, depth)  # down
        ]
        for neighbor in potential_neighbors:
            pos = (neighbor[0], neighbor[1])
            if pos not in visited_nodes and _can_walk_to_node(map, node, pos):
                if map[neighbor[1]][neighbor[0]] == GOAL_HEIGHT:
                    return depth
                visited_nodes.add(pos)
                queue.append(neighbor)

    return -1


def _hill_climbing_algorithm(inp: list[str]):
    """
    Part 1:
        What is the fewest steps required to move from your current
        position to the location that should get the best signal?
    Part 2:
        What is the fewest steps required to move starting from any square
        with elevation a to the location that should get the best signal?
    """
    heightmap = []  # list[list[int]]
    for y, row in enumerate(inp):
        new_heightmap_row = []
        for x, char in enumerate(row):
            if char == "S":
                start_pos = (x, y)
                char = "a"
            if char == "E":
                char = "{"
            new_heightmap_row.append(ord(char))
        heightmap.append(new_heightmap_row)

    print(f"Part 1: {bfs(heightmap, start_pos[0], start_pos[1])}")

    min_dist = 9999999
    for y, row in enumerate(inp):
        for x, char in enumerate(row):
            if heightmap[y][x] == MIN_HEIGHT:
                dist = bfs(heightmap, x, y)
                if dist != -1:
                    min_dist = min(dist, min_dist)
    print(f"Part 2: {min_dist}")


if __name__ == "__main__":
    parser = parsing.InputParser("inp.txt")
    inp = parser.to_array()
    parser.close()

    _hill_climbing_algorithm(inp)
