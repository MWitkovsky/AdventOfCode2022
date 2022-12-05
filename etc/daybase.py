# Path hack
import os
import sys
sys.path.insert(0, os.path.abspath("../../"))  # noqa

from lib import parsing


def _day(inp: list[str]):
    """
    Part 1: 

    Part 2:

    """


if __name__ == "__main__":
    parser = parsing.InputParser("inp.txt")
    inp = parser.to_array()
    parser.close()

    _day(inp)
