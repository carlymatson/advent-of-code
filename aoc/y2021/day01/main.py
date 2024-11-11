DAY = 1

verbose = True


def load_input(filename):
    with open(filename, "r") as f:
        numbers = [int(n) for n in f.readlines()]
    return numbers


def count_increases(numbers):
    increase_count = 0
    prev = numbers[0]
    for num in numbers[1:]:
        if num > prev:
            increase_count += 1
        prev = num
    return increase_count


def main():
    use_example = True
    input_file = "example.txt" if use_example else "input.txt"
    numbers = load_input(input_file)

    ### Part 1 ###
    if verbose:
        print(f"Numbers: {numbers}")
    increase_count = count_increases(numbers)
    print(f"Number of increases: {increase_count}")

    ### Part 2 ###
    print("-" * 20)
    sums = [
        numbers[i] + numbers[i + 1] + numbers[i + 2] for i in range(len(numbers) - 2)
    ]
    numbers = sums
    if verbose:
        print(f"Triple Sums: {numbers}")
    increase_count = count_increases(numbers)
    print(f"Number of increases: {increase_count}")


if __name__ == "__main__":
    main()
