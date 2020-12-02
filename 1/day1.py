import argparse
import fileinput
import itertools
from functools import reduce
from operator import mul


def find_n_sum_to(*, num_set, n, target_sum):
    """Find n numbers that sum to target_sum"""
    for combo in itertools.combinations(num_set, n):
        if sum(combo) == target_sum:
            return combo


def main():
    parser = argparse.ArgumentParser(
        description="Find n numbers from input files that sum to TARGET_SUM"
    )
    parser.add_argument(
        "--target_sum", "-s", type=int, default=2020, help="Number to sum to"
    )
    parser.add_argument(
        "-n", type=int, default=2, help="How many numbers should sum to TARGET_SUM?"
    )
    parser.add_argument(
        "files",
        metavar="FILE",
        nargs="*",
        help="Files to read. If empty, stdin is used.",
    )
    args = parser.parse_args()
    combo = find_n_sum_to(
        num_set={int(line) for line in fileinput.input(args.files)},
        n=args.n,
        target_sum=args.target_sum,
    )
    print(f'{" * ".join(str(x) for x in combo)} = {reduce(mul, combo, 1)}')


if __name__ == "__main__":
    main()
