import argparse
from collections import defaultdict


EMPTY = "L"
OCCUPIED = "#"
FLOOR = "."


def count_adjacent_occupied(seat_grid, row_num, col_num, search_limit):
    num_occupied = 0
    encountered_seat = defaultdict(bool)
    for i in (-1, 0, 1):
        for j in (-1, 0, 1):
            for abs_val in range(1, search_limit + 1):
                direction = (i, j)
                if i == j == 0 or encountered_seat[direction]:
                    break
                curr_row = row_num + (i * abs_val)
                curr_col = col_num + (j * abs_val)
                if (0 <= curr_row < len(seat_grid)) and (
                    0 <= curr_col < len(seat_grid[curr_row])
                ):
                    if seat_grid[curr_row][curr_col] != FLOOR:
                        encountered_seat[direction] = True
                    if seat_grid[curr_row][curr_col] == OCCUPIED:
                        num_occupied += 1
    return num_occupied


def apply_seating_rules(seat_grid, occupied_limit, search_limit):
    new_seat_grid = []
    for row_num, row in enumerate(seat_grid):
        new_row = []
        for col_num, seat in enumerate(row):
            if seat == FLOOR:
                new_row.append(seat)
                continue
            num_occupied = count_adjacent_occupied(
                seat_grid, row_num, col_num, search_limit
            )
            if seat == OCCUPIED:
                new_row.append(EMPTY if num_occupied >= occupied_limit else OCCUPIED)
            elif seat == EMPTY:
                new_row.append(EMPTY if num_occupied else OCCUPIED)
            else:
                raise ValueError(f"Invalid seat value: {seat} at {row_num, col_num}")
        new_seat_grid.append(new_row)
    return new_seat_grid


def run_until_stable(seat_grid, occupied_limit, search_limit, verbose):
    if verbose:
        print("\nInitial seat grid: ")
        print_grid(seat_grid)
    new_seat_grid = apply_seating_rules(seat_grid, occupied_limit, search_limit)
    while new_seat_grid != seat_grid:
        if verbose:
            print("\nCurrent seat grid: ")
            print_grid(new_seat_grid)
        seat_grid = new_seat_grid
        new_seat_grid = apply_seating_rules(seat_grid, occupied_limit, search_limit)
    return new_seat_grid


def print_grid(seat_grid):
    for row in seat_grid:
        print("".join(row))
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Figure out how many seats will be occupied once system stabilizes",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "input_file",
        help="File with current seat states",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Print some debugging output"
    )
    args = parser.parse_args()
    with open(args.input_file) as f:
        seat_grid = [list(line.strip()) for line in f]
    print(f"Number of lines in file: {len(seat_grid)}")
    stable_seat_grid = run_until_stable(seat_grid, 4, 1, args.verbose)
    num_occupied = sum(row.count(OCCUPIED) for row in stable_seat_grid)
    print(f"Number of occupied seats #1: {num_occupied}")
    stable_seat_grid = run_until_stable(seat_grid, 5, len(seat_grid), args.verbose)
    num_occupied = sum(row.count(OCCUPIED) for row in stable_seat_grid)
    print(f"Number of occupied seats #2: {num_occupied}")


if __name__ == "__main__":
    main()
