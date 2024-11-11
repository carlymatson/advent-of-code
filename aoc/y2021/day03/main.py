from pathlib import Path

DAY = 3


def get_digit(arrays, digit, use_most_common=True):
    halfway = len(arrays) / 2.0
    count = sum([array[digit] for array in arrays])
    if use_most_common:
        return int(count >= halfway)
    else:
        return int(count < halfway)


def most_common_digit(arrays, index, use_least_common=False):
    halfway = len(arrays) / 2.0
    count = sum([array[index] for array in arrays])
    digit = int(count >= halfway)
    if use_least_common:
        return 1 - digit
    return digit


def binary_to_int(array, powers_increasing=False, base=2):
    increment = 1 if powers_increasing else -1
    total = 0
    power = 0
    for digit in array[::increment]:
        total += int(digit) * base**power
        power += 1
    return total


def filter_arrays(arrays, use_least_common=False):
    filtered_arrays = arrays[:]
    num_digits = len(arrays[0])
    for i in range(num_digits):
        digit = most_common_digit(filtered_arrays, i, use_least_common=use_least_common)
        filtered_arrays = [arr for arr in filtered_arrays if int(arr[i]) == digit]
        if len(filtered_arrays) == 1:
            return filtered_arrays[0]
        if len(filtered_arrays) == 0:
            return None
    return []


def to_string(binary_array):
    char_array = [str(digit) for digit in binary_array]
    return "".join(char_array)


def main():
    ## Load input. ##
    input_file = Path(__file__).parent / "input.txt"
    input_strings = input_file.read_text().split("\n")
    binary_strings = [[int(b) for b in bs] for bs in input_strings]

    ## Part 1. ##
    num_digits = len(binary_strings[0])
    gamma = [most_common_digit(binary_strings, i) for i in range(num_digits)]
    epsilon = [most_common_digit(binary_strings, i, True) for i in range(num_digits)]
    print(f"Gamma: {to_string(gamma)}; Epsilon: {to_string(epsilon)}")

    ## Part 2. ##
    oxygen = filter_arrays(binary_strings)
    scrubber = filter_arrays(binary_strings, True)
    print(f"Oxygen rate: {to_string(oxygen)}; Scrubber rate: {to_string(scrubber)}")
    o_int, s_int = binary_to_int(oxygen), binary_to_int(scrubber)
    print(f"Result: {o_int} * {s_int} = {o_int * s_int}")


if __name__ == "__main__":
    main()
