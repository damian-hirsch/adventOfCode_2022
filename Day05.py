import re


# Get data from .txt file
def get_input():
    with open('input/Day05.txt', 'r') as file:
        # Split lines and write each line to list
        data = file.read().splitlines()

        # Initialize value to track when we get to the instructions
        instructions = False
        # Initialize empty list of list for the crates (we know we have 9 stacks, could be read out as well)
        crate_list = [[] for _ in range(9)]
        # Initialize instructions list
        instructions_list = []
        for line in data:
            # Check if we are at the crate numbering or empty line, if yes, the instructions will follow
            if line == '' or line[1] == '1':
                instructions = True
                continue
            # Get instructions
            elif instructions:
                # Find the numbers using regex
                re_matches = re.search(r'\D+(\d+)\D+(\d+)\D+(\d+)', line)
                a = int(re_matches.group(1))
                b = int(re_matches.group(2))
                c = int(re_matches.group(3))
                # Append numbers to list
                instructions_list.append((a, b, c))
            else:
                # Crate labels are spaced every 4 letters
                for i in range(0, len(line) // 4 + 1):
                    crate = line[1 + i * 4]
                    # Append crates to list of list to simulate the stack
                    if crate != ' ':
                        crate_list[i].append(crate)

    return crate_list, instructions_list


# Solves part 1
def part_one(crate_list: list, instruction_list: list) -> str:
    # Go through every instruction
    for instruction in instruction_list:
        # Unpack instructions
        amount, crate_from, crate_to = instruction
        # Go through amount of crates one-by-one
        for i in range(amount):
            # Take the top crate from the source stack ...
            crate = crate_list[crate_from - 1].pop(0)
            # ... and move it to the top of the target stack
            crate_list[crate_to - 1].insert(0, crate)

    # Initialize string
    string = ''
    # Go through all stacks
    for i in range(9):
        # Check if stack is not empty
        if crate_list[i]:
            # Write down label of top crate of each stack
            string += crate_list[i][0]
    return string


# Solves part 2
def part_two(crate_list: list, instruction_list: list) -> str:
    # Go through every instruction
    for instruction in instruction_list:
        # Unpack instructions
        amount, crate_from, crate_to = instruction
        # Get the amount number of crates in one go
        crates_stack = crate_list[crate_from - 1][:amount]
        # Delete those crates from the source stack
        del crate_list[crate_from - 1][:amount]
        # Move those crates to the target stack (at the top of the stack)
        crate_list[crate_to - 1][:0] = crates_stack

    # Initialize string
    string = ''
    # Go through all stacks
    for i in range(9):
        # Check if stack is not empty
        if crate_list[i]:
            # Write down label of top crate of each stack
            string += crate_list[i][0]
    return string


def main():
    crates, instructions = get_input()
    print('These crates end up on top of each stack:', part_one(crates, instructions))

    # Because we are dealing with list, we need to refresh the data for the second part
    crates, instructions = get_input()
    print('These crates end up on top of each stack:', part_two(crates, instructions))


if __name__ == '__main__':
    main()
