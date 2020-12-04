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


def parse_record(raw_record):
    """Parse raw record and return it as dict"""
    return dict(rec.split(":") for rec in raw_record.split())


def is_valid_record1(parsed_record):
    """Check if any required fields are missing from parsed_record"""
    present_fields = set(parsed_record.keys())
    missing_fields = set(REQUIRED_FIELDS.keys()) - present_fields
    return not missing_fields


def is_valid_record2(parsed_record):
    """Check if parsed_record is properly formatted"""
    if not (
        "byr" in parsed_record
        and parsed_record["byr"].isdigit()
        and len(parsed_record["byr"]) == 4
        and (1920 <= int(parsed_record["byr"]) <= 2002)
    ):
        return False

    if not (
        "iyr" in parsed_record
        and parsed_record["iyr"].isdigit()
        and len(parsed_record["iyr"]) == 4
        and (2010 <= int(parsed_record["iyr"]) <= 2020)
    ):
        return False

    if not (
        "eyr" in parsed_record
        and parsed_record["eyr"].isdigit()
        and len(parsed_record["eyr"]) == 4
        and (2020 <= int(parsed_record["eyr"]) <= 2030)
    ):
        return False

    if "hgt" in parsed_record:
        match = re.match(r"(?P<value>\d+)(?P<unit>in|cm)$", parsed_record["hgt"])
        if not match:
            return False
        value = int(match.group("value"))
        unit = match.group("unit")
        if not (
            (unit == "cm" and 150 <= value <= 193)
            or (unit == "in" and 59 <= value <= 76)
        ):
            return False
    else:
        return False

    if not (
        "hcl" in parsed_record and re.match(r"#[0-9a-f]{6}$", parsed_record["hcl"])
    ):
        return False

    if not (
        "ecl" in parsed_record
        and re.match(r"amb|blu|brn|gry|grn|hzl|oth$", parsed_record["ecl"])
    ):
        return False

    if not ("pid" in parsed_record and re.match(r"\d{9}$", parsed_record["pid"])):
        return False

    return True


def main():
    parser = argparse.ArgumentParser(description="Count valid records in passport file")
    parser.add_argument(
        "input_file",
        nargs="?",
        help="File to read",
    )
    args = parser.parse_args()
    with open(args.input_file) as f:
        records = [parse_record(raw_record) for raw_record in f.read().split("\n\n")]
    num_valid1 = 0
    num_valid2 = 0
    for record in records:
        if is_valid_record1(record):
            num_valid1 += 1
        if is_valid_record2(record):
            num_valid2 += 1
    print(f"Total records: {len(records)}")
    print(f"Number of valid records (part 1): {num_valid1}")
    print(f"Number of valid records (part 2): {num_valid2}")


if __name__ == "__main__":
    main()
