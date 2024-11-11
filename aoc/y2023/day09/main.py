from pathlib import Path
from pprint import pprint

INPUT_FILE = Path(__file__).parent / "input.txt"


def load_inputs(text: str) -> list[list[int]]:
    return [[int(value) for value in line.split(" ")] for line in text.splitlines()]


def get_deltas(report: list[int]) -> list[int]:
    return [report[idx + 1] - report[idx] for idx in range(len(report) - 1)]


def get_derivatives(report: list[int]) -> list[list[int]]:
    derivatives = [report]
    deltas = report
    for _ in range(len(report)):
        deltas = get_deltas(deltas)
        derivatives.append(deltas)
        if all(value == 0 for value in deltas):
            break
    return derivatives


def predict_next(report: list[int]) -> int:
    derivatives = get_derivatives(report)
    delta = 0
    for derivative in derivatives[::-1]:
        delta = derivative[-1] + delta
    return delta


def predict_previous(report: list[int]) -> int:
    derivatives = get_derivatives(report)
    delta = 0
    for derivative in derivatives[::-1]:
        delta = derivative[0] - delta
    return delta


EXAMPLE = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""


def main():
    my_input = INPUT_FILE.read_text()
    # my_input = EXAMPLE
    reports = load_inputs(my_input)
    predictions = [predict_next(report) for report in reports]
    print("Part 1: ", sum(predictions))

    prev_predictions = [predict_previous(report) for report in reports]
    print("Part 2: ", sum(prev_predictions))


if __name__ == "__main__":
    main()
