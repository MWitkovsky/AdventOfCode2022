# Path hack
import os
import sys
sys.path.insert(0, os.path.abspath("../../"))  # noqa

from lib import parsing


class Tree:
    def __init__(self, x: int, y: int, height: int, visible: bool = False):
        self.__x = x
        self.__y = y
        self.__height = height
        self.__visible = visible
        self.__scenic_score = 0

    def set_visible(self, visible: bool) -> None:
        self.__visible = visible

    def set_scenic_score(self, scenic_score: int) -> None:
        self.__scenic_score = scenic_score

    @property
    def x(self) -> int:
        return self.__x

    @property
    def y(self) -> int:
        return self.__y

    @property
    def height(self) -> int:
        return self.__height

    @property
    def visible(self) -> bool:
        return self.__visible

    @property
    def scenic_score(self) -> int:
        return self.__scenic_score


class Forest:
    def __determine_visible_trees_in_row(self, forest_row: list[Tree], 
                                         rtl: bool = False) -> None:
        if rtl:
            forest_row = forest_row[::-1]
        
        curr_max_height = forest_row[0].height
        for tree in forest_row:
            if tree.height > curr_max_height:
                tree.set_visible(True)
                if tree.height == 9:
                    return
                curr_max_height = tree.height
    
    def __determine_visible_trees_in_col(self, col_num: int, btt: bool = False) -> None:
        forest_graph = self.__forest_graph
        if btt:
            forest_graph = forest_graph[::-1]
        
        curr_max_height = forest_graph[0][col_num].height
        for row_num in range(1, len(forest_graph)-1):
            tree = forest_graph[row_num][col_num]
            if tree.height > curr_max_height:
                tree.set_visible(True)
                if tree.height == 9:
                    return
                curr_max_height = tree.height

    def __determine_visible_trees(self) -> None:
        for row_num in range(1, len(self.__forest_graph) - 1):
            forest_row = self.__forest_graph[row_num]
            self.__determine_visible_trees_in_row(forest_row)
            self.__determine_visible_trees_in_row(forest_row, rtl=True)

        for col_num in range(1, len(self.__forest_graph[0]) - 1):
            self.__determine_visible_trees_in_col(col_num)
            self.__determine_visible_trees_in_col(col_num, btt=True)

    def __determine_tree_scenic_score(self, tree: Tree) -> None:
        left_score = 0
        right_score = 0
        up_score = 0
        down_score = 0
        
        # Look left
        for x in range(tree.x - 1, -1, -1):
            left_score += 1
            if self.__forest_graph[tree.y][x].height >= tree.height:
                break
        
        # Look right
        for x in range(tree.x + 1, len(self.__forest_graph[0])):
            right_score += 1
            if self.__forest_graph[tree.y][x].height >= tree.height:
                break

        # Look up
        for y in range(tree.y - 1, -1, -1):
            up_score += 1
            if self.__forest_graph[y][tree.x].height >= tree.height:
                break
        
        # Look down
        for y in range(tree.y + 1, len(self.__forest_graph)):
            down_score += 1
            if self.__forest_graph[y][tree.x].height >= tree.height:
                break

        scenic_score = left_score * right_score * up_score * down_score
        tree.set_scenic_score(scenic_score)
        
        if self.__best_tree == None or \
                self.__best_tree.scenic_score < scenic_score:
            self.__best_tree = tree

    def __determine_tree_scenic_scores(self) -> None:
        for forest_row in self.__forest_graph:
            for tree in forest_row:
                self.__determine_tree_scenic_score(tree)

    def __init__(self, forest_desc: list[str]):
        self.__forest_graph = []  # type: list[list[Tree]]
        self.__best_tree = None  # type: Tree

        x_max = len(forest_desc[0]) - 1        
        y_max = len(forest_desc) - 1

        default_vis_x_values = (0, x_max)
        default_vis_y_values = (0, y_max)
        for y, row in enumerate(forest_desc):
            forest_row = []  # type: list[Tree]
            for x, height in enumerate(row):
                visible = \
                    x in default_vis_x_values or y in default_vis_y_values
                forest_row.append(Tree(x, y, height, visible))
            self.__forest_graph.append(forest_row)
        
        self.__determine_visible_trees()
        self.__determine_tree_scenic_scores()

    def print_visible_graph(self):
        for forest_row in self.__forest_graph:
            for tree in forest_row:
                print("V" if tree.visible else "-", end="")
            print()

    def get_tree(self, x: int, y: int) -> Tree:
        return self.__forest_graph[y][x]
    
    @property
    def num_visible_trees(self):
        if hasattr(self, "__num_visible_trees"):
            return self.__num_visible_trees

        total_sum = 0
        for forest_row in self.__forest_graph:
            total_sum += sum(tree.visible for tree in forest_row)
        
        self.__num_visible_trees = total_sum
        return total_sum
    
    @property
    def best_tree(self) -> Tree:
        return self.__best_tree
    
def _treetop_tree_house(inp: list[str]):
    """
    Part 1: 
        how many trees are visible from outside the grid?
    Part 2:
        Consider each tree on your map.
        What is the highest scenic score possible for any tree?
    """
    forest = Forest(inp)
    forest.print_visible_graph()
    print(f"Part 1: {forest.num_visible_trees}")
    print(f"Part 2: {forest.best_tree.scenic_score}")


if __name__ == "__main__":
    parser = parsing.InputParser("inp.txt")
    inp = parser.to_array()
    parser.close()

    _treetop_tree_house(inp)
