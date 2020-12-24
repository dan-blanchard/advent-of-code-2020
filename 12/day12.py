import argparse
import math

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


def apply_transform(position, transform, val):
    position = np.add(position, np.multiply(transform, (val, val, val)))
    position[2] = (position[2] + 360) % 360
    return position


def apply_command(position, command, waypoint):
    command, val = command[0], int(command[1:])
    if waypoint is not None:
        if command == "F":
            position = apply_transform(position, waypoint, val)
        else:
            if command in ("L", "R"):
                if command == "R":
                    val *= -1
                radians = math.radians(val)
                waypoint[0], waypoint[1] = (
                    (waypoint[0] * round(math.cos(radians)))
                    - (waypoint[1] * round(math.sin(radians))),
                    (waypoint[1] * round(math.cos(radians)))
                    + (waypoint[0] * round(math.sin(radians))),
                )

            else:
                waypoint = apply_transform(
                    waypoint, COMMANDS_TO_TRANSFORMS[command], val
                )
    else:
        if command == "F":
            command = DEGREES_TO_DIRECTION[position[2]]
        position = apply_transform(position, COMMANDS_TO_TRANSFORMS[command], val)
    return position, waypoint


def run_program(program, verbose, waypoint):
    position = np.array((0, 0, 0))
    if verbose:
        print("Ship at ", end="")
        print_position(position, waypoint is None)
        if waypoint is not None:
            print("Waypoint at ", end="")
            print_position(waypoint, False)

    for command in program:
        position, waypoint = apply_command(position, command, waypoint)
        if verbose:
            print(f"After command {command}: ship at ", end="")
            print_position(position, waypoint is None)
            if waypoint is not None:
                print("\t\tWaypoint at ", end="")
                print_position(waypoint, False)
    return position


def print_position(position, include_facing=True):
    x, y, degrees = position
    print(
        f"{abs(x)} {'east' if x >= 0 else 'west'}, {abs(y)} {'north' if y >= 0 else 'south'}"
        + (f", facing {DEGREES_TO_DIRECTION[degrees]}" if include_facing else "")
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
    position = run_program(program, args.verbose, None)
    print(
        f"Part 1 Manhattan distance from origin: {abs(position[0]) + abs(position[1])}\n"
    )
    position = run_program(program, args.verbose, np.array((10, 1, 0)))
    print(
        f"Part 2 Manhattan distance from origin: {abs(position[0]) + abs(position[1])}"
    )


if __name__ == "__main__":
    main()
