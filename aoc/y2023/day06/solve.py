"""Day 6: Wait For It
https://adventofcode.com/2023/day/6
"""

import math
import re
from pathlib import Path

input_file = Path(__file__).parent / "input.txt"


def quadratic_formula(a: float, b: float, c: float) -> tuple[float, float]:
    center = -b / 2.0
    radius = math.sqrt(b**2 - 4 * a * c) / 2.0
    return (center - radius, center + radius)


class Solver:
    def __init__(self, raw_input: str) -> None:
        self.raw_input = raw_input
        times, distances = self.parse_input(raw_input)
        self.times = times
        self.distances = distances

    def parse_input(self, raw_input: str) -> tuple[list[int], list[int]]:
        time_str, distance_str = raw_input.split("\n")
        times = [int(x) for x in re.findall(r"\d+", time_str)]
        distances = [int(x) for x in re.findall(r"\d+", distance_str)]
        return times, distances

    def parse_input_part_2(self, raw_input: str) -> tuple[int, int]:
        time_str, distance_str = raw_input.split("\n")
        duration = int("".join(re.findall(r"\d+", time_str)))
        distance = int("".join(re.findall(r"\d+", distance_str)))
        return duration, distance

    def get_boat_distance(self, seconds_held: int, duration: int) -> int:
        speed = seconds_held
        return speed * (duration - seconds_held)  # -X**2 + duration * X = distance

    def count_ways_to_win(self, duration: int, distance_record: int) -> int:
        winners = [
            hold
            for hold in range(duration + 1)
            if self.get_boat_distance(hold, duration) > distance_record
        ]
        return len(winners)

    def count_ways_to_win_efficiently(self, duration: int, distance_record: int) -> int:
        min_hold, max_hold = quadratic_formula(1, -duration, distance_record)
        return math.floor(max_hold) - math.ceil(min_hold) + 1

    def solve_part_1(self) -> int:
        times, distances = self.parse_input(self.raw_input)
        counts = [
            self.count_ways_to_win(times[idx], distances[idx])
            for idx in range(len(self.times))
        ]
        return math.prod(counts)

    def solve_part_2(self) -> int | None:
        duration, distance = self.parse_input_part_2(self.raw_input)
        return self.count_ways_to_win_efficiently(duration, distance)


if __name__ == "__main__":
    input_ = input_file.read_text().strip()
    solver = Solver(input_)

    print("--- Day 6: Wait For It ---")
    print("https://adventofcode.com/2023/day/6")

    print("(1) What do you get if you multiply these numbers together?")
    part_1 = solver.solve_part_1()
    print("Solution: " + str(part_1))
    print("Expected: 1108800")

    print("(2) How many ways can you beat the record in this one much longer race?")
    part_2 = solver.solve_part_2()
    print("Solution: " + str(part_2))
    print("Expected: 36919753")
