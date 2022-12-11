import re
import math
from pathlib import Path
from collections import deque
from typing import Tuple, List, Callable, Optional, Iterable

### Models ###


class Monkey:
    def __init__(
        self,
        items: List[int],
        operation: Callable,
        modulus: int,
        if_true: int,
        if_false: int,
    ):
        self.items = deque(items)
        self.operation = operation
        self.modulus = modulus
        self.if_true = if_true
        self.if_false = if_false
        self.inspection_count = 0

    def has_items(self) -> bool:
        return len(self.items) > 0

    def inspect(
        self, calm_down: bool = True, total_modulus: Optional[int] = None
    ) -> Tuple[int, int]:
        """The monkey inspects an item, alters its worry level, and then performs
        a divisibility check to determine which monkey to toss it to next."""
        self.inspection_count += 1
        # Compute new worry level
        old_worry = self.items.popleft()
        new = self.operation(old_worry)
        # Calm down, or keep worry manageable by reducing modulo a divisor
        if calm_down:
            new = int(new / 3)
        elif total_modulus is not None:
            new = new % total_modulus
        toss_to = self.if_true if (new % self.modulus == 0) else self.if_false
        return new, toss_to


### Parse Input ###


PATTERN = """Monkey ([0-9]):
  Starting items: ([0-9, ]+)
  Operation: new = old ([*+]) ([a-z0-9]+)
  Test: divisible by ([0-9]+)
    If true: throw to monkey ([0-9])
    If false: throw to monkey ([0-9])"""


def parse_match(m: Iterable[str]) -> Monkey:
    _, item_str, op, arg, modulus, if_true, if_false = m
    items = [int(n) for n in item_str.split(", ")]
    combine = (lambda x, y: x + y) if op == "+" else lambda x, y: x * y
    operation = lambda old: combine(old, (old if arg == "old" else int(arg)))
    return Monkey(
        items,
        operation=operation,
        modulus=int(modulus),
        if_true=int(if_true),
        if_false=int(if_false),
    )


def load_input() -> str:
    filepath = Path(__file__).parent / "input.txt"
    text = filepath.read_text().strip()
    mblocks = re.findall(PATTERN, text)
    return [parse_match(m) for m in mblocks]


### Solution ###


def play_game(
    monkeys, rounds: int, calm_down: bool = True, total_modulus: Optional[int] = None
) -> int:
    for round in range(rounds):
        for monkey in monkeys:
            while monkey.has_items():
                worry, toss_to = monkey.inspect(
                    calm_down=calm_down, total_modulus=total_modulus
                )
                monkeys[toss_to].items.append(worry)
    counts = [m.inspection_count for m in monkeys]
    a, b = sorted(counts)[-2:]
    return a * b


def solution() -> Tuple[int, int]:

    ### Part 1 ###
    monkeys = load_input()
    part_1_solution = play_game(monkeys, 20)

    ### Part 2 ###
    monkeys = load_input()
    total_modulus = math.prod((m.modulus for m in monkeys))
    part_2_solution = play_game(
        monkeys, 10000, calm_down=False, total_modulus=total_modulus
    )
    return part_1_solution, part_2_solution
