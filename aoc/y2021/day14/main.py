import os
import re
import time
from collections import Counter, defaultdict
from pathlib import Path
from pprint import pprint


def grow_polymer(polymer, rules):
    new_polymer = polymer[0]
    for i in range(len(polymer) - 1):
        pair = polymer[i : i + 2]
        middle = rules[pair]
        new_polymer += middle + pair[1]
    return new_polymer


def add_to_count(counts, item, number):
    if item not in counts:
        counts[item] = 0
    counts[item] += number
    return counts


def polymer_to_adjacent_pair_counts(polymer):
    poly_pairs = [polymer[i : i + 2] for i in range(len(polymer) - 1)]
    poly_counts = Counter(poly_pairs)
    return poly_counts


def grow_adjacent_pair_counts(poly_count, rules):
    for pair, count in list(poly_count.items()):
        insert = rules[pair]
        pair1 = pair[0] + insert
        pair2 = insert + pair[1]
        poly_count = add_to_count(poly_count, pair, -count)
        poly_count = add_to_count(poly_count, pair1, count)
        poly_count = add_to_count(poly_count, pair2, count)
    return poly_count


def pair_to_char_counts(poly_counts, first, last):
    """Total the number of times each character appears in a pair and divide by 2."""
    char_counts = {}
    for pair, count in poly_counts.items():
        a, b = pair
        add_to_count(char_counts, a, count)
        add_to_count(char_counts, b, count)
    # The first and last characters are the only ones not double-counted.
    char_counts[first] += 1
    char_counts[last] += 1
    char_counts = {char: int(count / 2) for char, count in char_counts.items()}
    return char_counts


def load_input():
    input_file = Path(__file__).parent / "input.txt"
    text = input_file.read_text()
    lines = text.split("\n")
    polymer = lines[0]
    pattern = "(?P<pair>\w+) -> (?P<res>\w+)"
    rules = (m.groupdict() for m in re.finditer(pattern, text))
    subs = {rule["pair"]: rule["res"] for rule in rules}
    return polymer, subs


def main():
    # Load input - get starting polymer and substitution rules
    polymer, substitutions = load_input()

    pair_count = polymer_to_adjacent_pair_counts(polymer)
    for step in range(40):
        pair_count = grow_adjacent_pair_counts(pair_count, substitutions)
        # polymer = grow_polymer(polymer, subs)
        animate = True
        if animate:
            if step % 3 == 0:
                os.system("clear")
                print(f"Step {step}...")
                pprint(pair_count)
                time.sleep(0.5)
    ### Part 1 ###
    # char_counts = Counter(polymer)
    ### Part 2 ###
    first_char = polymer[0]
    last_char = polymer[-1]
    char_counts = pair_to_char_counts(pair_count, first_char, last_char)

    # Get difference between minimum and maximum character counts.
    counts = char_counts.values()
    diff = max(counts) - min(counts)
    print(f"Difference: {diff}")


if __name__ == "__main__":
    main()
