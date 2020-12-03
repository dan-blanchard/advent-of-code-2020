import argparse
import fileinput


def traverse_map(*, tree_map, down, right, row=0, col=0, count=0):
    """Traverse tree_map starting in top-right and return how many trees we hit"""
    if row >= len(tree_map):
        return count
    line = tree_map[row]
    if line[col % len(line)] == "#":
        count += 1
    return traverse_map(
        tree_map=tree_map,
        down=down,
        right=right,
        col=col + right,
        row=row + down,
        count=count,
    )


def main():
    parser = argparse.ArgumentParser(description="Count trees we would hit")
    parser.add_argument(
        "--right", "-r", type=int, default=3, help="Right part of slope"
    )
    parser.add_argument("--down", "-d", type=int, default=1, help="Down part of slope")
    parser.add_argument(
        "files",
        metavar="FILE",
        nargs="*",
        help="Files to read. If empty, stdin is used.",
    )
    args = parser.parse_args()
    tree_map = [line.strip() for line in fileinput.input(args.files)]
    print(f"Traveling at a slope of right {args.right}, down {args.down}")
    print(
        f"Trees hit: {traverse_map(tree_map=tree_map, down=args.down, right=args.right)}"
    )


if __name__ == "__main__":
    main()
