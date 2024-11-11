import math
from pathlib import Path
from typing import TypeVar

INPUT_FILE = Path(__file__).parent / "input.txt"


class InputParser:
    @staticmethod
    def _try_parse_int(text: str) -> int | None:
        try:
            return int(text.strip())
        except ValueError:
            return None

    @classmethod
    def _extract_integers(cls, text: str) -> list[int]:
        return [
            extracted
            for part in text.split(" ")
            if (extracted := cls._try_parse_int(part)) is not None
        ]

    @classmethod
    def _extract_one_int(cls, text: str) -> int:
        parts = text.split(" ")[1:]
        return int("".join(part.strip() for part in parts))

    @classmethod
    def load_race_records(cls) -> list[tuple[int, int]]:
        lines = INPUT_FILE.read_text().splitlines()
        times, distances = [cls._extract_integers(line) for line in lines]
        races = list(zip(times, distances, strict=True))
        return races

    @classmethod
    def load_part_2_record(cls) -> tuple[int, int]:
        lines = INPUT_FILE.read_text().splitlines()
        race_time = cls._extract_one_int(lines[0])
        distance = cls._extract_one_int(lines[1])
        return race_time, distance


def compute_distance(time_held: int, race_total: int) -> int:
    speed = time_held
    time_traveling = race_total - time_held
    return speed * time_traveling


def get_ways_to_win(race_duration: int, distance_record: int) -> list[int]:
    winners = [
        time_held
        for time_held in range(race_duration + 1)
        if compute_distance(time_held, race_duration) > distance_record
    ]
    return winners


def quadratic_formula(a: float, b: float, c: float) -> tuple[float, float]:
    center = -b / (2 * a)
    radius = math.sqrt(b**2 - 4 * a * c) / (2 * a)
    return center - radius, center + radius


def count_ways_to_win_smartly(race_duration: int, distance_record: int) -> int:
    """Count win conditions by applying the quadratic formula."""
    # distance = speed * time = x * (race_duration - x) == distance_record
    # x**2 - race_duration * x + distance_record == 0
    lower_bound, upper_bound = quadratic_formula(1, -race_duration, distance_record)
    first_win = math.ceil(lower_bound)
    last_win = math.floor(upper_bound)
    return last_win - first_win + 1


def solve_part_1() -> int:
    races = InputParser.load_race_records()
    win_counts = [
        len(get_ways_to_win(race_duration, distance_record))
        for race_duration, distance_record in races
    ]
    return math.prod(win_counts)


def solve_part_2() -> int:
    race_duration, distance_record = InputParser.load_part_2_record()
    win_count = count_ways_to_win_smartly(race_duration, distance_record)
    return win_count


def solve():
    print("Part 1: ", solve_part_1())
    print("Part 2: ", solve_part_2())


if __name__ == "__main__":
    solve()
