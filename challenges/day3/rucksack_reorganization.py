# Path hack
import os
import sys
sys.path.insert(0, os.path.abspath("../../"))  # noqa

from lib import parsing


def get_item_priority(item: str) -> int:
    ord_value = ord(item)

    if item.isupper():
        return ord_value - 38
    else:
        return ord_value - 96


class Rucksack:
    def __init__(self, items: str):
        self.__num_items = len(items)
        self.__pocket_size = self.__num_items // 2
        self.__left_pocket = items[0:self.__pocket_size]
        self.__right_pocket = items[self.__pocket_size:]

    def find_duplicate_item(self) -> str:
        set_intersect = \
            set(self.__left_pocket).intersection(set(self.__right_pocket))
        return set_intersect.pop()

    def get_unique_items_set(self) -> set:
        return set(self.__left_pocket) | set(self.__right_pocket)


class AuthorityGroup:
    def __init__(self, rucksacks: list[Rucksack]):
        self.__group_size = len(rucksacks)
        self.__rucksacks = rucksacks

    def determine_group_authority(self):
        authority_set = self.__rucksacks[0].get_unique_items_set()
        for rucksack in self.__rucksacks[1:]:
            authority_set = \
                rucksack.get_unique_items_set().intersection(authority_set)
        return authority_set.pop()


def _rucksack_reorganization(inp: list[str]):
    """
    Part 1: 
        Find the item type that appears in both compartments of each rucksack. 
        What is the sum of the priorities of those item types?
    Part 2:
        Find the item type that corresponds to the badges of each three-Elf 
        group. What is the sum of the priorities of those item types?
    """
    rucksacks = [Rucksack(contents) for contents in inp]
    duplicate_items = list(map(Rucksack.find_duplicate_item, rucksacks))
    sum_of_duplicates = sum(map(get_item_priority, duplicate_items))
    print(f"Part 1: {sum_of_duplicates}")

    authority_sum = 0
    for i in range(0, len(rucksacks), 3):
        authority_group = AuthorityGroup(rucksacks[i:i+3])
        authority_item = authority_group.determine_group_authority()
        authority_sum += get_item_priority(authority_item)
    print(f"Part 2: {authority_sum}")


if __name__ == "__main__":
    parser = parsing.InputParser("inp.txt")
    inp = parser.to_array()
    parser.close()

    _rucksack_reorganization(inp)
