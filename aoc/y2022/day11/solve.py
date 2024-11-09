"""Day 11: Monkey in the Middle
https://adventofcode.com/2022/day/11
"""

import math
import re
from collections import deque
from pathlib import Path
from typing import Literal

input_file = Path(__file__).parent / "input.txt"


class Monkey:
    def __init__(
        self,
        label: int,
        items: list[int],
        op: Literal["+", "*"],
        arg: int | None,
        divisible_by: int,
        if_true: int,
        if_false: int,
    ) -> None:
        self.label = label
        self.items = deque(items)
        self.op = op
        self.arg = arg
        self.modulus = divisible_by
        self.if_true = if_true
        self.if_false = if_false
        self.inspection_count = 0

    def has_items(self) -> bool:
        return len(self.items) > 0

    def operate(self, value: int) -> int:
        second_arg = self.arg if self.arg is not None else value
        if self.op == "+":
            result = value + second_arg
        else:
            result = value * second_arg
        return result

    def compute_worry_level(
        self,
        value: int,
        calm_down: bool = True,
        total_modulus: int | None = None,
    ) -> int:
        new_level = self.operate(value)
        # Calm down, or keep worry manageable by reducing modulo a divisor
        if calm_down:
            new_level = int(new_level / 3)
        elif total_modulus is not None:
            new_level = new_level % total_modulus
        return new_level

    def inspect(
        self, calm_down: bool = True, combined_modulus: int | None = None
    ) -> tuple[int, int]:
        """The monkey inspects an item, alters its worry level, and then performs
        a divisibility check to determine which monkey to toss it to next."""
        self.inspection_count += 1
        old_level = self.items.popleft()
        new_level = self.compute_worry_level(old_level, calm_down, combined_modulus)
        passes_check = new_level % self.modulus == 0
        toss_to = self.if_true if passes_check else self.if_false
        return new_level, toss_to


RE_PATTERN = r"""Monkey ([0-9]):
  Starting items: ([0-9, ]+)
  Operation: new = old (\+|\*) (old|[0-9]+)
  Test: divisible by ([0-9]+)
    If true: throw to monkey ([0-9])
    If false: throw to monkey ([0-9])"""


class Solver:
    def __init__(self, raw_input: str) -> None:
        self.raw_input = raw_input

    def _parse_monkey(self, data):
        label, item_str, op, arg, modulus, if_true, if_false = data
        items = [int(n) for n in item_str.split(", ")]
        return Monkey(
            int(label),
            items,
            op=op,
            arg=None if arg == "old" else int(arg),
            divisible_by=int(modulus),
            if_true=int(if_true),
            if_false=int(if_false),
        )

    def parse_input(self, raw_input: str) -> dict[int, Monkey]:
        matches = re.findall(RE_PATTERN, raw_input)
        monkeys = [self._parse_monkey(m) for m in matches]
        return {monkey.label: monkey for monkey in monkeys}

    def play_monkey_business(self, rounds: int = 20, calm_down: bool = True):
        monkeys = self.parse_input(self.raw_input)
        if not calm_down:
            combined_modulus = math.prod(m.modulus for m in monkeys.values())
        else:
            combined_modulus = None
        for _ in range(rounds):
            for monkey in monkeys.values():
                while monkey.has_items():
                    new_level, toss_to = monkey.inspect(
                        calm_down=calm_down,
                        combined_modulus=combined_modulus,
                    )
                    monkeys[toss_to].items.append(new_level)
        activity_levels = [monkey.inspection_count for monkey in monkeys.values()]
        first, second = sorted(activity_levels)[-2:]
        return first * second

    def solve_part_1(self) -> int | None:
        return self.play_monkey_business(rounds=20)

    def solve_part_2(self) -> int | None:
        return self.play_monkey_business(rounds=10000, calm_down=False)


if __name__ == "__main__":
    input_ = input_file.read_text().strip()
    solver = Solver(input_)

    part_1 = solver.solve_part_1()
    print("Part 1 solution: ", part_1)

    part_2 = solver.solve_part_2()
    print("Part 2 solution: ", part_2)
