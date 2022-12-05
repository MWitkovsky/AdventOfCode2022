# Path hack
import os
import sys
sys.path.insert(0, os.path.abspath("../../"))  # noqa

import re

from lib import parsing


int_re = re.compile(r'\d+')


class SupplyStack:
    def __init__(self, initial_desc: list[str]):
        self.__stacks = [[], [], [], [], [], [], [], [], []]
        for row_idx in range(len(initial_desc)-1, -1, -1):
            row = initial_desc[row_idx]
            for idx, i in enumerate(range(1, len(row), 4)):
                char = row[i]
                if char != " ":
                    self.__stacks[idx].append(char)

    def move(self, num: int, from_stack_idx: int, to_stack_idx: int) -> None:
        from_stack = self.__stacks[from_stack_idx-1]
        to_stack = self.__stacks[to_stack_idx-1]
        while num > 0:
            to_stack.append(from_stack.pop())
            num -= 1

    def move_batch(self, num: int, from_stack_idx: int, to_stack_idx: int) -> None:
        from_stack = self.__stacks[from_stack_idx-1]
        to_stack = self.__stacks[to_stack_idx-1]

        cutoff_idx = len(from_stack)-num

        self.__stacks[to_stack_idx-1] = to_stack + from_stack[cutoff_idx:]
        self.__stacks[from_stack_idx-1] = from_stack[:cutoff_idx]

    def get_stack_peak_str(self) -> str:
        out = []
        for stack in self.__stacks:
            out.append(stack[-1])
        return "".join(out)


def _supply_stacks(inp: list[str]):
    """
    Part 1:
        After the rearrangement procedure completes, what crate ends up on top
        of each stack?

    Part 2:
        The CrateMover 9001 is notable for many new and exciting features:
        air conditioning, leather seats, an extra cup holder, and the ability
        to pick up and move multiple crates at once.

        After the rearrangement procedure completes, what crate ends up on top
        of each stack?
    """
    legend_idx = inp.index(" 1   2   3   4   5   6   7   8   9 ")
    stack_desc = inp[:legend_idx]
    move_desc = inp[legend_idx+2:]
    supply_stack_9000 = SupplyStack(stack_desc)

    for move_str in move_desc:
        move_args = list(map(int, int_re.findall(move_str)))
        supply_stack_9000.move(*move_args)
    print(f"Part 1: {supply_stack_9000.get_stack_peak_str()}")

    supply_stack_9001 = SupplyStack(stack_desc)
    for move_str in move_desc:
        move_args = list(map(int, int_re.findall(move_str)))
        supply_stack_9001.move_batch(*move_args)
    print(f"Part 2: {supply_stack_9001.get_stack_peak_str()}")


if __name__ == "__main__":
    parser = parsing.InputParser("inp.txt")
    inp = parser.to_array()
    parser.close()

    _supply_stacks(inp)
