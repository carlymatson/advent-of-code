from pathlib import Path

DAY = 10


def is_opener(symbol):
    openers = ["(", "{", "[", "<"]
    return symbol in openers


def cancels_latest(closer, sym_stack):
    if len(sym_stack) == 0:
        return False
    opener = sym_stack[-1]
    a, b = ord(opener), ord(closer)
    return (b > a) and (b - a < 3)


def check_validity(row):
    sym_stack = []
    for c in row:
        if is_opener(c):
            # print(f"Is opener...{c}")
            sym_stack.append(c)
        elif cancels_latest(c, sym_stack):
            # print(f"Cancels latest... {c}")
            sym_stack.pop(-1)
        else:
            # print("Fail!")
            return False, sym_stack, c  # Also return metadata
    return True, sym_stack, None


def score_autocomplete(completion):
    char_values = {
        "(": 1,
        "[": 2,
        "{": 3,
        "<": 4,
    }
    score = 0
    for c in completion[::-1]:
        score *= 5
        score += char_values[c]
    return score


def main():
    char_values = {
        ")": 3,
        "]": 57,
        "}": 1197,
        ">": 25137,
    }
    input_file = Path(__file__).parent / "input.txt"
    rows = input_file.read_text().split("\n")
    auto_scores = []
    score = 0
    for row in rows:
        is_valid, sym_stack, illegal_char = check_validity(row)
        if illegal_char is not None:
            score += char_values[illegal_char]
        else:
            score = score_autocomplete(sym_stack)
            # print(f"Score: {score}")
            auto_scores.append(score)
        # print(is_valid)
        # print("".join(sym_stack))

    sorted_scores = sorted(auto_scores)
    middle_index = int((len(sorted_scores) - 1) / 2)
    middle_score = sorted_scores[middle_index]
    print(f"Invalid score: {score}")
    print(f"Middle autocomplete score: {middle_score}")


if __name__ == "__main__":
    main()
