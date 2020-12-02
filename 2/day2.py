import argparse
import fileinput
from functools import reduce
from operator import mul


def check_line(line):
    """Parse line password policy line and see if it is valid

    example line:

    6-9 z: qzzzzxzzfzzzz
    """
    line = line.strip()
    count_range, target_char, password = line.split(" ")
    target_char = target_char.strip(":")
    min_count, max_count = tuple(int(x) for x in count_range.split("-"))
    return min_count <= password.count(target_char) <= max_count


def main():
    parser = argparse.ArgumentParser(
        description="Count valid passwords in password policy file"
    )
    parser.add_argument(
        "files",
        metavar="FILE",
        nargs="*",
        help="Files to read. If empty, stdin is used.",
    )
    args = parser.parse_args()
    num_valid = sum(
        1 if check_line(line) else 0 for line in fileinput.input(args.files)
    )
    print(f"Number of valid lines: {num_valid}")


if __name__ == "__main__":
    main()
