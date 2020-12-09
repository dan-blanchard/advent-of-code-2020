import argparse
from itertools import combinations


def find_first_invalid(num_list, preamble):
    """Find first number in list that is not the sum of two preamble numbers"""
    for i, curr_num in enumerate(num_list):
        if i < preamble:
            continue
        valid_sums = {x + y for x, y in combinations(num_list[i - preamble : i], 2)}
        if curr_num not in valid_sums:
            return curr_num
    raise ValueError("No invalid numbers in input list")


def find_contiguous_sum_to(num_list, target_sum):
    """Find range of numbers in list that sums to target_sum"""
    total = 0
    range_start = 0
    for i, curr_num in enumerate(num_list):
        total += curr_num
        while total > target_sum:
            total -= num_list[range_start]
            range_start += 1
        if total == target_sum:
            return num_list[range_start : i + 1]


def main():
    parser = argparse.ArgumentParser(
        description="Find first number that isn't the sum of one of the previous PREAMBLE numbers",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "input_file",
        nargs="?",
        help="File with numbers (one per line)",
    )
    parser.add_argument(
        "--preamble",
        "-p",
        type=int,
        default=25,
        help="Previous numbers to look at when determining if current is valid",
    )
    args = parser.parse_args()
    with open(args.input_file) as f:
        num_list = [int(line.strip()) for line in f]
    print(f"Number of lines in file: {len(num_list)}")
    first_invalid_num = find_first_invalid(num_list, args.preamble)
    print(f"First invalid num: {first_invalid_num}")
    sum_range = find_contiguous_sum_to(num_list, first_invalid_num)
    print(f"Sum to first invalid: {sum_range}")
    print(f"Sum of min and max in range: {min(sum_range) + max(sum_range)}")


if __name__ == "__main__":
    main()
