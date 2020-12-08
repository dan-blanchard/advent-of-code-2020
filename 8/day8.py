import argparse


def parse_line(line):
    """Parse instruction and return it as tuple of operator and value"""
    op, val = line.split()
    val = int(val)
    return op, val


def run_program(program):
    """Run a program, halting when an instruction is executed a second time

    :returns: (accumulator, ran_whole_program)
    """
    accumulator = 0
    visited_instructions = set()
    i = 0
    while i not in visited_instructions and i < len(program):
        visited_instructions.add(i)
        op, val = program[i]
        # print(f"{op} {val} | acc: {accumulator} i: {i}")
        if op == "nop":
            i += 1
        elif op == "acc":
            accumulator += val
            i += 1
        elif op == "jmp":
            i += val
        else:
            raise ValueError(f"Invalid instruction {op} on line {i}")
    return accumulator, i >= len(program)


def fix_program(program):
    """Figure out which instruction needs to change from jmp to nop.

    :returns: Value of accumulator at end of program
    """
    for i, (op, val) in enumerate(program):
        if op == "jmp":
            accumulator, ran_whole_program = run_program(
                program[:i] + [("nop", val)] + program[i + 1 :]
            )
            if ran_whole_program:
                break
    if not ran_whole_program:
        print("Failed to fix program :(")
    return accumulator


def main():
    parser = argparse.ArgumentParser(
        description="Run simple program and print value of accumulator before anything runs twice"
    )
    parser.add_argument(
        "input_file",
        nargs="?",
        help="Program to run",
    )
    args = parser.parse_args()
    with open(args.input_file) as f:
        program = [parse_line(line) for line in f]
    print(f"Total lines in program: {len(program)}")
    accumulator, ran_whole_program = run_program(program)
    print(f"Value of accumulator before looping: {accumulator}")
    accumulator = fix_program(program)
    print(f"Value of accumulator with fixed program: {accumulator}")


if __name__ == "__main__":
    main()
