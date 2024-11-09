"""Day 13: Distress Signal
https://adventofcode.com/2022/day/13
"""

import json
from functools import total_ordering
from pathlib import Path
from typing import Self, TypeAlias

input_file = Path(__file__).parent / "input.txt"


PacketData: TypeAlias = int | list["PacketData"]


@total_ordering
class Packet:
    def __init__(self, data: PacketData):
        self.data = (
            data if isinstance(data, int) else [type(self)(item) for item in data]
        )

    def __str__(self) -> str:
        return str(self.data)

    def _make_comparable(self, a, b) -> tuple[int, int] | tuple[list[Self], list[Self]]:
        if isinstance(a, int) and isinstance(b, int):
            return (a, b)
        if isinstance(a, int):
            a = [type(self)(a)]
        if isinstance(b, int):
            b = [type(self)(b)]
        return (a, b)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return False
        a, b = self._make_comparable(self.data, other.data)
        return a == b

    def __lt__(self, other: Self) -> bool:
        if not isinstance(other, type(self)):
            raise TypeError
        a, b = self._make_comparable(self.data, other.data)
        return a < b  # type: ignore


class Solver:
    def __init__(self, raw_input: str) -> None:
        self.raw_input = raw_input
        self.packet_pairs = self.parse_input(raw_input)

    def parse_input(self, raw_input: str) -> list[list[Packet]]:
        blocks = raw_input.split("\n\n")
        return [
            [Packet(json.loads(packet)) for packet in block.split("\n")]
            for block in blocks
        ]

    def solve_part_1(self) -> int:
        correctly_ordered = [
            idx + 1 for idx, pair in enumerate(self.packet_pairs) if pair[0] <= pair[1]
        ]
        return sum(correctly_ordered)

    def solve_part_2(self) -> int:
        divider_packets = [Packet([[2]]), Packet([[6]])]
        packets = sorted(
            [*divider_packets, *(p for pair in self.packet_pairs for p in pair)]
        )
        idx_a = packets.index(divider_packets[0]) + 1
        idx_b = packets.index(divider_packets[1]) + 1
        return idx_a * idx_b


if __name__ == "__main__":
    input_ = input_file.read_text().strip()
    solver = Solver(input_)

    part_1 = solver.solve_part_1()
    print("Part 1 solution: ", part_1)

    part_2 = solver.solve_part_2()
    print("Part 2 solution: ", part_2)
