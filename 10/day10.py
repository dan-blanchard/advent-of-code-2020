import argparse
from collections import Counter


def get_adjacent_diff_counts(num_list, max_diff=3):
    """Returns counts of differences between adjacent numbers in sorted num_list"""
    prev_num = 0
    diff_counts = Counter()
    for num in num_list:
        diff = num - prev_num
        diff_counts[diff] += 1
        if diff > max_diff:
            raise ValueError(
                f"List has gap that is too big: {diff} = {num} - {prev_num}"
            )
        prev_num = num
    return diff_counts


def count_possible_combos(num_list, max_diff=3, verbose=False):
    """Returns counts of all possible valid combinations of adapters in list"""
    ways_to_reach_pos = Counter()
    ways_to_reach_pos[0] = 1
    # Figure out how many ways to get to current num
    for num in num_list[1:]:
        ways_to_reach_pos[num] = sum(
            ways_to_reach_pos[num - i] for i in range(1, max_diff + 1)
        )
        if verbose:
            print(sorted(ways_to_reach_pos.items()))
    return ways_to_reach_pos[num_list[-1]]


def main():
    parser = argparse.ArgumentParser(
        description="Find product of differences between list of 'joltages'",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "input_file",
        help="File with numbers (one per line)",
    )
    parser.add_argument(
        "-m",
        "--max_diff",
        type=int,
        help="Maximum difference between adapter joltages",
        default=3,
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Print some debugging output"
    )
    args = parser.parse_args()
    with open(args.input_file) as f:
        num_list = [int(line.strip()) for line in f]
    num_list = [0] + sorted(num_list)
    num_list.append(num_list[-1] + args.max_diff)
    print(f"Number of lines in file: {len(num_list)}")
    diff_counts = get_adjacent_diff_counts(num_list, max_diff=args.max_diff)
    print(
        f"Product of adjacent 1-jolt diffs * 3-jolt diffs: {diff_counts[1] * diff_counts[3]}"
    )
    num_combos = count_possible_combos(
        num_list, max_diff=args.max_diff, verbose=args.verbose
    )
    print(f"Total possible combinations: {num_combos}")


if __name__ == "__main__":
    main()
