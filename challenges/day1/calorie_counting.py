# Path hack
import os
import sys
sys.path.insert(0, os.path.abspath("../../"))  # noqa

from collections import deque
from lib import parsing


class ElfCalorieInventory:
    def __init__(self, food_items: list[int]):
        self.food_items = food_items

    @property
    def total_calories(self):
        if not hasattr(self, "__total_calories"):
            self.__total_calories = sum(self.food_items)
        return self.__total_calories


def _build_elf_calorie_inventory_list(raw_inventory: list[int | str]) -> list[ElfCalorieInventory]:
    elf_calorie_inventories = []
    lo_index = 0
    hi_index = 0
    for item in raw_inventory:
        if not isinstance(item, int):
            elf_calorie_inventories.append(
                ElfCalorieInventory(raw_inventory[lo_index:hi_index])
            )
            lo_index = hi_index + 1
        hi_index += 1

    return elf_calorie_inventories


def _calorie_counting(elf_calorie_inventories: list[ElfCalorieInventory]):
    """
    Part 1: 
        Find the Elf carrying the most Calories. 
        How many total Calories is that Elf carrying?

    Part 2:
        Find the top three Elves carrying the most Calories.
        How many Calories are those Elves carrying in total?
    """
    max_inventory = -1
    max_history = deque(maxlen=3)
    for inventory in elf_calorie_inventories:
        if inventory.total_calories > max_inventory:
            max_inventory = inventory.total_calories
            max_history.append(max_inventory)

    print(f"Part 1: {max_inventory}")
    print(f"Part 2: {sum(max_history)}")


if __name__ == "__main__":
    parser = parsing.InputParser("inp.txt")
    inp = parser.to_array(int, suppress_warnings=True)
    parser.close()

    elf_calorie_inventories = _build_elf_calorie_inventory_list(inp)
    _calorie_counting(elf_calorie_inventories)
