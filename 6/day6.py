import argparse
import re

REQUIRED_FIELDS = {
    "byr": "Birth Year",
    "iyr": "Issue Year",
    "eyr": "Expiration Year",
    "hgt": "Height",
    "hcl": "Hair Color",
    "ecl": "Eye Color",
    "pid": "Passport ID",
}

OPTIONAL_FIELDS = {
    "cid": "Country ID",
}


def parse_record1(raw_record):
    """Parse raw record and return it as a set of unique symbols without \n"""
    return set(raw_record) - {"\n"}


def parse_record2(raw_record):
    """Parse raw record and return it as a set of common symbols"""
    common_symbols = set("abcdefghijklmnopqrstuvwxyz")
    for person in raw_record.split():
        common_symbols.intersection_update(set(person))
    return common_symbols


def main():
    parser = argparse.ArgumentParser(description="Count unique symbols per group")
    parser.add_argument(
        "input_file",
        nargs="?",
        help="File to read",
    )
    args = parser.parse_args()
    with open(args.input_file) as f:
        records1 = [parse_record1(raw_record) for raw_record in f.read().split("\n\n")]
    with open(args.input_file) as f:
        records2 = [parse_record2(raw_record) for raw_record in f.read().split("\n\n")]
    print(f"Total records: {len(records1)}")
    print(f"Sum of unique yeses per group: {sum(len(group) for group in records1)}")
    print(f"Sum of common yeses per group: {sum(len(group) for group in records2)}")


if __name__ == "__main__":
    main()
