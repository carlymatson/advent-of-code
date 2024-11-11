from pathlib import Path

from snailfish import Snailfish


def load_input(use_example: bool):
    filename = "example.txt" if use_example else "input.txt"
    filepath = Path(__file__).parent / filename
    snailfish_list = filepath.read_text().split("\n")
    return snailfish_list


def add_snailfish_list(sf_list):
    total = Snailfish.from_string(sf_list[0])
    for sf in sf_list[1:]:
        total = total + Snailfish.from_string(sf)
        total = total.reduce()
    return total


def find_greatest_pair_sum(snailfish_list):
    greatest_sum = 0
    num_sf = len(snailfish_list)
    for i in range(num_sf):
        for j in range(num_sf):
            snailfish_pair = [snailfish_list[n] for n in (i, j)]
            sum = add_snailfish_list(snailfish_pair)
            magnitude = sum.get_magnitude()
            if magnitude > greatest_sum:
                greatest_sum = magnitude
    return greatest_sum


def main():
    snailfish_list = load_input(False)

    sum = add_snailfish_list(snailfish_list)
    print(f"Sum: {sum}")
    print(f"Magnitude: {sum.get_magnitude()}")

    greatest_pair_sum = find_greatest_pair_sum(snailfish_list)
    print(f"Greatest sum: {greatest_pair_sum}")


if __name__ == "__main__":
    main()
