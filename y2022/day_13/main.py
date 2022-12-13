import json
from pathlib import Path
from typing import Tuple

### Parse Input ###


def load_input() -> str:
    filepath = Path(__file__).parent / "input.txt"
    text = filepath.read_text().strip()
    blocks = text.split("\n\n")
    line_pairs = [
        [Packet(json.loads(l)) for l in block.split("\n")] for block in blocks
    ]
    return line_pairs


### Solution ###


class Packet:
    def __init__(self, value):
        self.value = value

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return f"Packet({self.value})"

    def __eq__(self, o) -> bool:
        return type(self) == type(o) and self.value == o.value

    def __lt__(self, o):
        a = self.value
        b = o.value
        if isinstance(a, int) and isinstance(b, int):
            return a < b
        if isinstance(a, int):
            a = [a]
        if isinstance(b, int):
            b = [b]
        shared_length = min(len(a), len(b))
        for i in range(shared_length):
            if Packet(a[i]) < Packet(b[i]):
                return True
            elif Packet(b[i]) < Packet(a[i]):
                return False
        return len(a) < len(b)


def solution() -> Tuple[int, int]:
    packet_pairs = load_input()

    ### Part 1 ###
    pair_indices = [idx + 1 for idx, (a, b) in enumerate(packet_pairs) if a < b]
    part_1_solution = sum(pair_indices)

    ### Part 2 ###
    A = Packet([[2]])
    B = Packet([[6]])
    all_pairs = [p for pair in packet_pairs for p in pair] + [A, B]
    sorted_packets = sorted(all_pairs)
    idx_A = sorted_packets.index(A) + 1
    idx_B = sorted_packets.index(B) + 1
    part_2_solution = idx_A * idx_B

    return part_1_solution, part_2_solution
