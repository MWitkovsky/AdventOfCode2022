# Path hack
import os
import sys
sys.path.insert(0, os.path.abspath("../../"))  # noqa

from lib import parsing


class SeatingAssignment:
    def __init__(self, desc_str: str):
        self.__raw_arrangement = desc_str
        seat_indexes = self.__raw_arrangement.split("-")
        self.__lo_seat = int(seat_indexes[0])
        self.__hi_seat = int(seat_indexes[1])
        self.__num_seats = self.__hi_seat - self.__lo_seat

    @property
    def lo_seat(self):
        return self.__lo_seat

    @property
    def hi_seat(self):
        return self.__hi_seat

    @property
    def num_seats(self):
        return self.__num_seats


def _get_lo_and_hi_assignments(a: SeatingAssignment, b: SeatingAssignment) -> tuple[SeatingAssignment, SeatingAssignment]:
    if a.lo_seat == b.lo_seat:
        lo_assignment = a if a.num_seats > b.num_seats else b
    else:
        lo_assignment = a if a.lo_seat < b.lo_seat else b
    hi_assignment = a if lo_assignment is b else b

    return lo_assignment, hi_assignment


def determine_seating_assignment_subset_exists(a: SeatingAssignment,
                                               b: SeatingAssignment) -> bool:
    lo_assignment, hi_assignment = _get_lo_and_hi_assignments(a, b)
    return hi_assignment.hi_seat <= lo_assignment.hi_seat


def determine_seating_assignment_overlap_exists(a: SeatingAssignment,
                                                b: SeatingAssignment) -> bool:
    lo_assignment, hi_assignment = _get_lo_and_hi_assignments(a, b)
    return lo_assignment.lo_seat <= hi_assignment.lo_seat <= lo_assignment.hi_seat


def _camp_cleanup(inp: list[str]):
    """
    Part 1:
        In how many assignment pairs does one range fully contain the other?
    Part 2:
        It seems like there is still quite a bit of duplicate work planned.
        Instead, the Elves would like to know the number of pairs that overlap
        at all.
    """
    assignment_pairs = []
    for pair in inp:
        pair = pair.split(",")
        assignment_pairs.append(
            (SeatingAssignment(pair[0]), SeatingAssignment(pair[1]))
        )

    num_subsets_found = 0
    num_overlaps_found = 0
    for assignment_pair in assignment_pairs:
        num_subsets_found += \
            determine_seating_assignment_subset_exists(*assignment_pair)
        num_overlaps_found += \
            determine_seating_assignment_overlap_exists(*assignment_pair)
    print(f"Part 1: {num_subsets_found} pairs")
    print(f"Part 1: {num_overlaps_found} pairs")


if __name__ == "__main__":
    parser = parsing.InputParser("inp.txt")
    inp = parser.to_array()
    parser.close()

    _camp_cleanup(inp)
