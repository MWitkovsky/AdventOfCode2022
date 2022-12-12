# Path hack
import itertools
import os
import sys
sys.path.insert(0, os.path.abspath("../../"))  # noqa

from lib import parsing


MONKEYS = {}  # type: dict[int, Monkey]


SMALLEST_COMMON_MULTIPLE = -1


class Ops:
    ADD = 1
    MUL = 2
    SQ = 3

    OP_STR_TO_OP = {
        "+": ADD,
        "*": MUL
    }


class Item:
    def __init__(self, worry_level: int):
        self.__worry_level = worry_level

    def set_worry_level(self, worry_level: int) -> None:
        self.__worry_level = worry_level

    @property
    def worry_level(self) -> int:
        return self.__worry_level


class Monkey:
    id_iter = itertools.count()

    def __parse_operation(self, raw_op: str) -> None:
        op_desc = (raw_op.split("new = old ")[1]).split(" ")
        self.__op = Ops.OP_STR_TO_OP[op_desc[0]]
        if self.__op == Ops.MUL and op_desc[1] == "old":
            self.__op = Ops.SQ
        else:
            self.__op_val = int(op_desc[1])

    def __parse_test(self, raw_test: str) -> None:
        self.__divisible_test = int(raw_test.split("divisible by ")[1])

    def __parse_conds(self, raw_true: str, raw_false: str) -> None:
        self.__true_target = int(raw_true.split("throw to monkey ")[1])
        self.__false_target = int(raw_false.split("throw to monkey ")[1])

    def __init__(self, monkey_desc: list[str]):
        self.__id = next(Monkey.id_iter)
        raw_starting_items = monkey_desc[0].split(": ")[1]
        raw_operation = monkey_desc[1].split(": ")[1]
        raw_test = monkey_desc[2].split(": ")[1]
        raw_true = monkey_desc[3].split(": ")[1]
        raw_false = monkey_desc[4].split(": ")[1]

        self.__items = [
            Item(worry) for worry in map(int, raw_starting_items.split(", "))
        ]
        self.__parse_operation(raw_operation)
        self.__parse_test(raw_test)
        self.__parse_conds(raw_true, raw_false)
        self.__num_items_inspected = 0
        MONKEYS[self.__id] = self

    def __catch_item(self, item: Item):
        self.__items.append(item)

    def __throw_item(self, item: Item, target: "Monkey") -> None:
        item.set_worry_level(item.worry_level % self.smallest_common_multiple)
        target.__catch_item(item)

    def throw_items(self):
        for item in self.__items:
            self.__num_items_inspected += 1
            if self.__op == Ops.ADD:
                item.set_worry_level(item.worry_level + self.__op_val)
            elif self.__op == Ops.MUL:
                item.set_worry_level(item.worry_level * self.__op_val)
            elif self.__op == Ops.SQ:
                item.set_worry_level(item.worry_level * item.worry_level)

            if item.worry_level % self.__divisible_test == 0:
                target_monkey = MONKEYS[self.__true_target]
            else:
                target_monkey = MONKEYS[self.__false_target]

            self.__throw_item(item, target_monkey)

        self.__items.clear()

    @property
    def num_items_inspected(self):
        return self.__num_items_inspected

    @property
    def divisible_test(self):
        return self.__divisible_test

    @property
    def smallest_common_multiple(self):
        global SMALLEST_COMMON_MULTIPLE
        if SMALLEST_COMMON_MULTIPLE > -1:
            return SMALLEST_COMMON_MULTIPLE

        highest_divisible_test = max(
            [monkey.divisible_test for monkey in MONKEYS.values()]
        )
        SMALLEST_COMMON_MULTIPLE = highest_divisible_test
        while True:
            ok = True
            for monkey in MONKEYS.values():
                if not ok:
                    continue
                remainder = SMALLEST_COMMON_MULTIPLE % monkey.divisible_test
                if remainder != 0:
                    ok = False
                    break
            if ok:
                break
            SMALLEST_COMMON_MULTIPLE += highest_divisible_test

        return SMALLEST_COMMON_MULTIPLE


def _throw_round():
    for i in range(len(MONKEYS)):
        MONKEYS[i].throw_items()


def monkey_in_the_middle(inp: list[str]):
    """
    Part 1: 
        Figure out which monkeys to chase by counting how many items they
        inspect over 20 rounds. What is the level of monkey business after 20
        rounds of stuff-slinging simian shenanigans?
    Part 2:

    """
    for i in range(1, len(inp), 7):
        Monkey(inp[i:i+5])

    # for i in range(20):
    #     _throw_round()
    # monkey_inspections = sorted(
    #     [monkey.num_items_inspected for monkey in MONKEYS.values()],
    #     reverse=True
    # )
    # monkey_business = monkey_inspections[0] * monkey_inspections[1]
    # print(f"Part 1: {monkey_business}")

    for i in range(10000):
        _throw_round()
    monkey_inspections = sorted(
        [monkey.num_items_inspected for monkey in MONKEYS.values()],
        reverse=True
    )
    monkey_business = monkey_inspections[0] * monkey_inspections[1]
    print(f"Part 2: {monkey_business}")
    pass


if __name__ == "__main__":
    parser = parsing.InputParser("inp.txt")
    inp = parser.to_array()
    parser.close()

    monkey_in_the_middle(inp)
