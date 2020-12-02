import argparse
import fileinput


def check_line1(line):
    """Parse line password policy line and see if it is valid

    example line:

    6-9 z: qzzzzxzzfzzzz
    """
    line = line.strip()
    count_range, target_char, password = line.split(" ")
    target_char = target_char.strip(":")
    min_count, max_count = tuple(int(x) for x in count_range.split("-"))
    return min_count <= password.count(target_char) <= max_count


def check_line2(line):
    """Parse line password policy line and see if it is valid

    example line:

    6-9 z: qzzzzxzzfzzzz
    """
    line = line.strip()
    indices, target_char, password = line.split(" ")
    target_char = target_char.strip(":")
    index1, index2 = tuple(int(x) - 1 for x in indices.split("-"))
    return (
        password[index1] == target_char or password[index2] == target_char
    ) and not (password[index1] == password[index2])


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
    print(
        f"Number of valid part 1 lines: {sum(1 if check_line1(line) else 0 for line in fileinput.input(args.files))}"
    )
    print(
        f"Number of valid part 2 lines: {sum(1 if check_line2(line) else 0 for line in fileinput.input(args.files))}"
    )


if __name__ == "__main__":
    main()
