# Path hack
import os
import sys
sys.path.insert(0, os.path.abspath("../../"))  # noqa

from lib import parsing


class SignalParser:
    def __init__(self, signal_str: str):
        self.__signal_str = signal_str

    def find_marker_idx(self, marker_size: int) -> int:
        test_set = set()
        for i in range(marker_size, len(self.__signal_str)):
            test_set.update(self.__signal_str[i-marker_size:i])
            if len(test_set) == marker_size:
                return i
            test_set.clear()

        return -1


def _tuning_trouble(inp: list[str]):
    """
    Part 1: 
        How many characters need to be processed before the first
        start-of-packet marker is detected?
    Part 2:
        How many characters need to be processed before the first 
        start-of-message marker is detected?
    """
    signal_parser = SignalParser(inp[0])
    print(f"Part 1: {signal_parser.find_marker_idx(4)}")
    print(f"Part 1: {signal_parser.find_marker_idx(14)}")


if __name__ == "__main__":
    parser = parsing.InputParser("inp.txt")
    inp = parser.to_array()
    parser.close()

    _tuning_trouble(inp)
