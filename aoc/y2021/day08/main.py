from pathlib import Path


def solve_for_1478(segments):
    if len(segments) == 2:
        return 1
    if len(segments) == 3:
        return 7
    if len(segments) == 4:
        return 4
    if len(segments) == 7:
        return 8
    return None


def solve_for_039(segments, one, four):
    if not set(one).issubset(set(segments)):
        return None
    if not set(four).issubset(set(segments)):
        return 3
    if len(segments) == 5:
        return 9
    return 0


def solve_for_256(segments):
    return


def assign_digit(segments, digit, dictionary):
    s = "".join(sorted(segments))
    dictionary[s] = digit
    return dictionary


def segment_set_of_length(segment_sets, num):
    for s in segment_sets:
        if len(s) == num:
            return s
    return None


def solve_for_digits(segment_sets):
    one = segment_set_of_length(segment_sets, 2)
    four = segment_set_of_length(segment_sets, 4)
    seven = segment_set_of_length(segment_sets, 3)
    eight = segment_set_of_length(segment_sets, 7)
    known_digits = {one: 1, four: 4, seven: 7, eight: 8}
    for segments in set(segment_sets).difference(known_digits):
        digit = solve_for_039(segments, one, four)
        if digit is not None:
            assign_digit(segments, digit, known_digits)
    for segments in set(segment_sets).difference(known_digits):
        if len(segments) == 6:
            six = segments
            assign_digit(segments, 6, known_digits)
    for segments in set(segment_sets).difference(known_digits):
        if set(segments).issubset(set(six)):
            assign_digit(segments, 5, known_digits)
        else:
            assign_digit(segments, 2, known_digits)
    return known_digits


def count_1478(digit_list):
    count = 0
    num_letters = [2, 3, 4, 7]
    for digit in digit_list:
        if len(digit) in num_letters:
            count += 1
    return count


def convert_output(outputs, dictionary):
    try:
        output_digits = {str(dictionary["".join(sorted(list(x)))]) for x in outputs}
    except Exception as e:
        print(e)
        print(dictionary)
    return int("".join(output_digits))


def main():
    filepath = Path(__file__).parent / "input.txt"
    text = filepath.read_text()
    lines = text.split("\n")
    num_1478_in_output = 0
    for line in lines:
        inputs, outputs = [s.strip().split(" ") for s in line.split("|")]
        known_digits = solve_for_digits(inputs)
        # print(known_digits)
        translated_output = convert_output(outputs, known_digits)
        print(translated_output)
        if len(known_digits) != 10:
            print("OH NO!!!")
            continue
        num_1478_in_output += count_1478(outputs)
    print(f"Count: {num_1478_in_output}")


if __name__ == "__main__":
    main()
