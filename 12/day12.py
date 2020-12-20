import argparse

import numpy as np


# x, y, degrees
COMMANDS_TO_TRANSFORMS = {
    "N": (0, 1, 0),
    "S": (0, -1, 0),
    "E": (1, 0, 0),
    "W": (-1, 0, 0),
    "L": (0, 0, 1),
    "R": (0, 0, -1),
}

DEGREES_TO_DIRECTION = {
    0: "E",
    90: "N",
    180: "W",
    270: "S",
}


def apply_command(position, command):
    command, val = command[0], int(command[1:])
    if command == "F":
        command = DEGREES_TO_DIRECTION[position[2]]
    position = np.add(
        position, np.multiply(COMMANDS_TO_TRANSFORMS[command], (val, val, val))
    )
    position[2] = (position[2] + 360) % 360
    return position


def run_program(program, verbose):
    position = (0, 0, 0)
    if verbose:
        print_position(position)
    for command in program:
        position = apply_command(position, command)
        if verbose:
            print(f"After command {command}: ", end="")
            print_position(position)
    return position


def print_position(position):
    x, y, degrees = position
    print(
        f"{abs(x)} {'east' if x >= 0 else 'west'}, {abs(y)} {'north' if y >= 0 else 'south'}, "
        f"facing {DEGREES_TO_DIRECTION[degrees]}"
    )


def main():
    parser = argparse.ArgumentParser(
        description="Move ship following commands",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "input_file",
        help="File with program",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Print some debugging output"
    )
    args = parser.parse_args()
    with open(args.input_file) as f:
        program = [line.strip() for line in f]
    print(f"Number of lines in file: {len(program)}")
    position = run_program(program, args.verbose)
    print(f"Manhattan distance from origin: {abs(position[0]) + abs(position[1])}")


if __name__ == "__main__":
    main()
