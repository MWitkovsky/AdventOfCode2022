# Path hack
import bisect
import os
import sys
sys.path.insert(0, os.path.abspath("../../"))  # noqa

from lib import parsing


class CRTOpDesc:
    NOOP = "noop"
    ADDX = "addx"
    COSTS = {
        NOOP: 1,
        ADDX: 2
    }


class CRT:
    def __noop(self) -> int:
        cost = CRTOpDesc.COSTS[CRTOpDesc.NOOP]
        for i in range(cost):
            self.__x_tracker.append(self.__x)

    def __addx(self, to_add: int) -> int:
        cost = CRTOpDesc.COSTS[CRTOpDesc.ADDX]
        for i in range(cost):
            self.__x_tracker.append(self.__x)
        self.__x += to_add

    def __calc_signal_strengths(self) -> None:
        self.__x = 1
        self.__x_tracker = []  # type: list[int]
        for op_str in self.__op_list:
            op = op_str.split(" ")
            if op[0] == CRTOpDesc.NOOP:
                self.__noop()
            elif op[0] == CRTOpDesc.ADDX:
                self.__addx(int(op[1]))
        self.__x_tracker.append(self.__x)

    def __init__(self, op_list: list[str]):
        self.__op_list = op_list
        self.__calc_signal_strengths()

    def get_signal_strength_at_clock_cycle(self, cycle) -> int:
        return self.__x_tracker[cycle] * cycle

    def draw_crt(self) -> None:
        for cycle, x in enumerate(self.__x_tracker):
            row_pos = cycle % 40
            if row_pos == 0:
                print()
            if abs(x - row_pos) <= 1:
                print("#", end="")
            else:
                print(".", end="")


def _cathode_ray_tube(inp: list[str]):
    """
    Part 1: 
        Find the signal strength during the 20th, 60th, 100th, 140th, 180th,
        and 220th cycles. What is the sum of these six signal strengths?
    Part 2:
        Render the image given by your program. What eight capital letters 
        appear on your CRT?
    """
    crt = CRT(inp)
    signal_sum = 0
    for i in range(20, 221, 40):
        signal_sum += crt.get_signal_strength_at_clock_cycle(i)
    print(f"Part 1: {signal_sum}")
    crt.draw_crt()


if __name__ == "__main__":
    parser = parsing.InputParser("inp.txt")
    inp = parser.to_array()
    parser.close()

    _cathode_ray_tube(inp)
