"""
The first 7 characters will either be F or B; these specify exactly one of the 128 rows on the plane (numbered 0 through 127). Each letter tells you which half of a region the given seat is in. Start with the whole list of rows; the first letter indicates whether the seat is in the front (0 through 63) or the back (64 through 127). The next letter indicates which half of that region the seat is in, and so on until you're left with exactly one row.

For example, consider just the first seven characters of FBFBBFFRLR:

Start by considering the whole range, rows 0 through 127.
F means to take the lower half, keeping rows 0 through 63.
B means to take the upper half, keeping rows 32 through 63.
F means to take the lower half, keeping rows 32 through 47.
B means to take the upper half, keeping rows 40 through 47.
B keeps rows 44 through 47.
F keeps rows 44 through 45.
The final F keeps the lower of the two, row 44.
The last three characters will be either L or R; these specify exactly one of the 8 columns of seats on the plane (numbered 0 through 7). The same process as above proceeds again, this time with only three steps. L means to keep the lower half, while R means to keep the upper half.

For example, consider just the last 3 characters of FBFBBFFRLR:

Start by considering the whole range, columns 0 through 7.
R means to take the upper half, keeping columns 4 through 7.
L means to take the lower half, keeping columns 4 through 5.
The final R keeps the upper of the two, column 5.
"""
import argparse
import math

UPPER_VALS = {"F", "L"}
LOWER_VALS = {"B", "R"}


def id_to_num(id, verbose=False):
    """Takes a boarding pass ID section and returns the appropriate"""
    curr_min = 0
    curr_max = 2 ** len(id) - 1
    if verbose:
        print(f"curr_min: {curr_min} curr_max: {curr_max}")
    for char in id:
        if char in UPPER_VALS:
            curr_max = (curr_min + curr_max) // 2
        elif char in LOWER_VALS:
            curr_min = ((curr_min + curr_max) // 2) + 1
        else:
            raise ValueError(f"Invalid ID: {id}")
        if verbose:
            print(f"char: {char} curr_min: {curr_min} curr_max: {curr_max}")
    if curr_min != curr_max:
        raise ValueError(f"Invalid ID: {id} (min = {curr_min}; max = {curr_max})")
    return curr_min


def parse_line(*, line, row_prefix_len, verbose):
    """Return (row, col, seat ID) for boarding pass ID"""
    line = line.strip()
    row = id_to_num(line[:row_prefix_len], verbose=verbose)
    col = id_to_num(line[row_prefix_len:], verbose=verbose)
    seat_id = row * 8 + col
    return (seat_id, row, col)


def find_gap(sorted_records):
    """Find the gap in the sorted record seat IDs"""
    prev_record = sorted_records[0]
    gap_id = None
    for record in sorted_records:
        if record[0] - prev_record[0] == 2:
            gap_id = record[0] - 1
            break
        prev_record = record
    return gap_id


def main():
    parser = argparse.ArgumentParser(description="Count valid records in passport file")
    parser.add_argument(
        "input_file",
        nargs="?",
        help="File to read",
    )
    parser.add_argument("--rows", "-r", type=int, default=128, help="Number of rows")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()
    row_prefix_len = int(math.log2(args.rows))
    with open(args.input_file) as f:
        records = sorted(
            parse_line(line=line, row_prefix_len=row_prefix_len, verbose=args.verbose)
            for line in f
        )

    print(f"Total records: {len(records)}")
    print(f"Highest seat ID: {records[-1]}")
    print(f"Missing site ID: {find_gap(records)}")


if __name__ == "__main__":
    main()
