import re
from collections import Counter
from pathlib import Path
from pprint import pprint

INPUT_FILE = Path(__file__).parent / "input.txt"


def load_poker_hands() -> list[tuple[str, int]]:
    line_parts = (line.split(" ") for line in INPUT_FILE.read_text().splitlines())
    return [(hand, int(wager)) for hand, wager in line_parts]


CARD_RANKS = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 11,
    "T": 10,
}


def get_card_rank(card: str) -> int:
    if card in CARD_RANKS:
        return CARD_RANKS[card]
    return int(card)


def get_joker_rank(card: str) -> int:
    if card == "J":
        return 1
    if card in CARD_RANKS:
        return CARD_RANKS[card]
    return int(card)


def get_hand_score(hand: str) -> int:
    card_counts = Counter(hand)
    sorted_counts = tuple(sorted(card_counts.values()))
    if sorted_counts == (5,):
        return 6
    if sorted_counts == (1, 4):
        return 5
    if sorted_counts == (2, 3):
        return 4
    if sorted_counts == (1, 1, 3):
        return 3
    if sorted_counts == (1, 2, 2):
        return 2
    if sorted_counts == (1, 1, 1, 2):
        return 1
    return 0


def get_best_candidate_for_replacement(hand: str, exclude: str = "J") -> str:
    card_counts = Counter(hand)
    card_counts.pop(exclude, None)
    if not card_counts:
        # If hand is all J, replace with highest card possible
        return "A"
    max_count = max(card_counts.values())
    candidates = [card for card, count in card_counts.items() if count == max_count]
    return max(candidates, key=get_joker_rank)


def get_part_1_score_key(hand: str) -> tuple[int, ...]:
    hand_score = get_hand_score(hand)
    card_scores = [get_card_rank(card) for card in hand]
    return tuple([hand_score] + card_scores)


def get_part_2_score_key(hand: str) -> tuple[int, ...]:
    # Transform any Js into best other card choice
    replace_with = get_best_candidate_for_replacement(hand, exclude="J")
    subbed_hand = hand.replace("J", replace_with)
    hand_score = get_hand_score(subbed_hand)
    card_scores = [get_joker_rank(card) for card in hand]
    return tuple([hand_score] + card_scores)


def solve_part_1():
    hands = load_poker_hands()
    sorted_hands = sorted(hands, key=lambda hand: get_part_1_score_key(hand[0]))
    score = sum((rank + 1) * hand[1] for rank, hand in enumerate(sorted_hands))
    print("Part 1: ", score)


def solve_part_2():
    hands = load_poker_hands()
    sorted_hands = sorted(hands, key=lambda hand: get_part_2_score_key(hand[0]))
    score = sum((rank + 1) * hand[1] for rank, hand in enumerate(sorted_hands))
    print("Part 2: ", score)


if __name__ == "__main__":
    solve_part_1()
    solve_part_2()
