import argparse
import re
from collections import Counter
from pprint import pprint


def parse_rule(line):
    """Parse rule about what child bags a parent bag can contain

    :returns: (parent, {color1: quantity, color2: quantity, ...}
    """
    parent, children_str = line.strip().split(" bags contain ")
    children = {}
    for child in children_str.split(", "):
        match = re.match(r"(?P<quantity>\d+) (?P<color>.+?) bag", child)
        if match:
            children[match.group("color")] = int(match.group("quantity"))
    return parent, children


def find_can_contain_color(rules, target_color):
    valid_parents = set()
    to_check = rules.keys() - {target_color}
    invalid_parents = set()
    while to_check:
        for parent_color in list(to_check):
            children = rules[parent_color]
            is_invalid = True
            for child in children:
                if child == target_color or child in valid_parents:
                    valid_parents.add(parent_color)
                    if parent_color in to_check:
                        to_check.remove(parent_color)
                    is_invalid = False
                elif child not in invalid_parents:
                    to_check.add(child)
                    is_invalid = False
            if is_invalid:
                invalid_parents.add(parent_color)
                if parent_color in to_check:
                    to_check.remove(parent_color)
    return valid_parents


def count_child_bags(rules, target_color):
    to_check = {target_color}
    child_counts = Counter()
    while to_check:
        for parent_color in list(to_check):
            # print(f"Checking: {parent_color}")
            # pprint(child_counts)
            children = rules[parent_color]
            parent_sum = 0
            children_summed = 0
            for child, num_copies in children.items():
                if child in child_counts:
                    parent_sum += num_copies * child_counts[child] + num_copies
                    children_summed += 1
                else:
                    to_check.add(child)
            if children_summed == len(children):
                child_counts[parent_color] = parent_sum
                if parent_color in to_check:
                    to_check.remove(parent_color)
            else:
                to_check.add(parent_color)
    # pprint(child_counts)
    return child_counts[target_color]


def main():
    parser = argparse.ArgumentParser(
        description="Count number of bags that can contain a particular colored bag"
    )
    parser.add_argument(
        "input_file",
        nargs="?",
        help="File to read",
    )
    parser.add_argument(
        "--color",
        "-c",
        default="shiny gold",
        help="Color bag we want to count other bags that contain",
    )
    args = parser.parse_args()
    with open(args.input_file) as f:
        rules = dict(parse_rule(line) for line in f)
    print(f"Total rules: {len(rules)}")
    print(
        f"Number of types that can contain {args.color}: {len(find_can_contain_color(rules, args.color))}"
    )
    print(f"Number of bags inside {args.color}: {count_child_bags(rules, args.color)}")


if __name__ == "__main__":
    main()
