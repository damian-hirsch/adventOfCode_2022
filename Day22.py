import numpy as np
import re


# Get data from .txt file
def get_input() -> tuple[np.ndarray, list]:
    with open('input/Day22.txt', 'r') as file:
        translator = {' ': 0, '.': 1, '#': 2}
        # Split lines and write each line to list
        data = file.read().splitlines()
        # Get length of the longest line that is not the instructions
        max_len = len(max(data[:-1], key=len))
        # Initialize array
        board_map = np.zeros((len(data) - 2, max_len), dtype=int)
        # Get instructions line
        instructions_line = data.pop()
        # Remove the empty line
        _ = data.pop()
        # Loop through each line of the map
        for i, line in enumerate(data):
            for j, char in enumerate(line):
                board_map[i, j] = translator[char]
        # Convert instructions_line to single instructions
        instructions = []
        # Regex to split the instructions
        for x, y in re.findall(r'(\d+)([RL]?)', instructions_line):
            instructions.append((int(x), y))
    return board_map, instructions


# Calculates the cube wrapping for the example case (a different layout will not work!)
def cube_wrapping_example(curr_pos: tuple, direction: str, cube_size: int) -> tuple:
    # Initialize variables
    new_pos = (-1, -1)
    direction_dict = {'E': 0, 'S': 1, 'W': 2, 'N': 3}
    new_dir = ''

    # Find out in which section of the cube we are
    # Cube 1
    if curr_pos[0] < cube_size:
        # Cube 1
        match direction:
            # Move N: Cube 2
            case 'N':
                new_pos = (cube_size, 3 * cube_size - curr_pos[1] - 1)
                new_dir = 'S'
            # Move E: Cube 6
            case 'E':
                new_pos = (3 * cube_size - curr_pos[0] - 1, curr_pos[1] + 1 * cube_size)
                new_dir = 'W'
            # Move S: Cube 4 --> no wrap case
            case 'S':
                new_pos = (curr_pos[0] - 1, curr_pos[1])
                new_dir = direction
            # Move W: Cube 3
            case 'W':
                new_pos = (cube_size, curr_pos[0] + 1 * cube_size)
                new_dir = 'S'
    # Cube 2, 3 or 4
    elif cube_size <= curr_pos[0] < 2 * cube_size:
        if curr_pos[1] < cube_size:
            # Cube 2
            match direction:
                # Move N: Cube 1
                case 'N':
                    new_pos = (curr_pos[0] - 1 * cube_size, 3 * cube_size - curr_pos[1] - 1)
                    new_dir = 'S'
                # Move E: Cube 3 --> no wrap case
                case 'E':
                    new_pos = (curr_pos[0], curr_pos[1] + 1)
                    new_dir = direction
                # Move S: Cube 5
                case 'S':
                    new_pos = (curr_pos[0] + 1 * cube_size, 3 * cube_size - curr_pos[1] - 1)
                    new_dir = 'N'
                # Move W: Cube 6
                case 'W':
                    new_pos = (3 * cube_size - 1, 5 * cube_size - curr_pos[0] - 1)
                    new_dir = 'N'
        elif cube_size <= curr_pos[1] < 2 * cube_size:
            # Cube 3
            match direction:
                # Move N: Cube 1
                case 'N':
                    new_pos = (curr_pos[1] - 1 * cube_size, 2 * cube_size)
                    new_dir = 'E'
                # Move E: Cube 4 --> no wrap case
                case 'E':
                    new_pos = (curr_pos[0], curr_pos[1] + 1)
                    new_dir = direction
                # Move S: Cube 5
                case 'S':
                    new_pos = (4 * cube_size - curr_pos[1] - 1, 2 * cube_size)
                    new_dir = 'E'
                # Move W: Cube 2 --> no wrap case
                case 'W':
                    new_pos = (curr_pos[0], curr_pos[1] - 1)
                    new_dir = direction
        elif 2 * cube_size <= curr_pos[1] < 3 * cube_size:
            # Cube 4
            match direction:
                # Move N: Cube 1 --> no wrap case
                case 'N':
                    new_pos = (curr_pos[0] - 1, curr_pos[1])
                    new_dir = direction
                # Move E: Cube 6
                case 'E':
                    new_pos = (2 * cube_size, 5 * cube_size - curr_pos[0] - 1)
                    new_dir = 'S'
                # Move S: Cube 5 --> no wrap case
                case 'S':
                    new_pos = (curr_pos[0] + 1, curr_pos[1])
                    new_dir = direction
                # Move W: Cube 3 --> no wrap case
                case 'W':
                    new_pos = (curr_pos[0], curr_pos[1] - 1)
                    new_dir = direction
    # Cube 5 or 6
    elif 2 * cube_size <= curr_pos[0]:
        if 2 * cube_size <= curr_pos[1] < 3 * cube_size:
            # Cube 5
            match direction:
                # Move N: Cube 4 --> no wrap case
                case 'N':
                    new_pos = (curr_pos[0] - 1, curr_pos[1])
                    new_dir = direction
                # Move E: Cube 6 --> no wrap case
                case 'E':
                    new_pos = (curr_pos[0], curr_pos[1] + 1)
                    new_dir = direction
                # Move S: Cube 2
                case 'S':
                    new_pos = (2 * cube_size - 1, 3 * cube_size - curr_pos[1] - 1)
                    new_dir = 'N'
                # Move W: Cube 3
                case 'W':
                    new_pos = (2 * cube_size - 1, 4 * cube_size - curr_pos[0] - 1)
                    new_dir = 'N'
        elif 3 * cube_size <= curr_pos[1] < 4 * cube_size:
            # Cube 6
            match direction:
                # Move N: Cube 4
                case 'N':
                    new_pos = (5 * cube_size - curr_pos[1] - 1, 3 * cube_size - 1)
                    new_dir = 'W'
                # Move E: Cube 1
                case 'E':
                    new_pos = (3 * cube_size - curr_pos[0] - 1, 3 * cube_size - 1)
                    new_dir = 'W'
                # Move S: Cube 2
                case 'S':
                    new_pos = (5 * cube_size - curr_pos[1] - 1, 0)
                    new_dir = 'E'
                # Move W: Cube 5 --> no wrap case
                case 'W':
                    new_pos = (curr_pos[0], curr_pos[1] - 1)
                    new_dir = direction

    return new_pos, direction_dict[new_dir]


# Calculates the cube wrapping for given input (a different layout will not work!)
def cube_wrapping(curr_pos: tuple, direction: str, cube_size: int) -> tuple:
    # Initialize variables
    new_pos = (-1, -1)
    direction_dict = {'E': 0, 'S': 1, 'W': 2, 'N': 3}
    new_dir = ''

    # Find out in which section of the cube we are
    # Cube 1 or 2
    if 0 * cube_size <= curr_pos[0] < 1 * cube_size:
        if 1 * cube_size <= curr_pos[1] < 2 * cube_size:
            # Cube 1
            match direction:
                # Move N: Cube 6
                case 'N':
                    new_pos = (curr_pos[1] + 2 * cube_size, 0)
                    new_dir = 'E'
                # Move E: Cube 2 --> no wrap case
                case 'E':
                    new_pos = (curr_pos[0], curr_pos[1] + 1)
                    new_dir = direction
                # Move S: Cube 3 --> no wrap case
                case 'S':
                    new_pos = (curr_pos[0] + 1, curr_pos[1])
                    new_dir = direction
                # Move W: Cube 4
                case 'W':
                    new_pos = (3 * cube_size - curr_pos[0] - 1, 0)
                    new_dir = 'E'
        elif 2 * cube_size <= curr_pos[1] < 3 * cube_size:
            # Cube 2
            match direction:
                # Move N: Cube 6
                case 'N':
                    new_pos = (4 * cube_size - 1, curr_pos[1] - 2 * cube_size)
                    new_dir = 'N'
                # Move E: Cube
                case 'E':
                    new_pos = (3 * cube_size - curr_pos[0] - 1, 2 * cube_size - 1)
                    new_dir = 'W'
                # Move S: Cube 3
                case 'S':
                    new_pos = (curr_pos[1] - cube_size, 2 * cube_size - 1)
                    new_dir = 'W'
                # Move W: Cube 1 --> no wrap case
                case 'W':
                    new_pos = (curr_pos[0], curr_pos[1] - 1)
                    new_dir = direction
    # Cube 3
    elif 1 * cube_size <= curr_pos[0] < 2 * cube_size:
        # Cube 3
        match direction:
            # Move N: Cube 1 --> no wrap case
            case 'N':
                new_pos = (curr_pos[0] - 1, curr_pos[1])
                new_dir = direction
            # Move E: Cube 2
            case 'E':
                new_pos = (cube_size - 1, curr_pos[0] + cube_size)
                new_dir = 'N'
            # Move S: Cube 5 --> no wrap case
            case 'S':
                new_pos = (curr_pos[0] + 1, curr_pos[1])
                new_dir = direction
            # Move W: Cube 4
            case 'W':
                new_pos = (2 * cube_size, curr_pos[0] - cube_size)
                new_dir = 'S'

    # Cube 4 or 5
    elif 2 * cube_size <= curr_pos[0] < 3 * cube_size:
        if 0 * cube_size <= curr_pos[1] < 1 * cube_size:
            # Cube 4
            match direction:
                # Move N: Cube 3
                case 'N':
                    new_pos = (curr_pos[1] + cube_size, cube_size)
                    new_dir = 'E'
                # Move E: Cube 5 --> no wrap case
                case 'E':
                    new_pos = (curr_pos[0], curr_pos[1] + 1)
                    new_dir = direction
                # Move S: Cube 6 --> no wrap case
                case 'S':
                    new_pos = (curr_pos[0] + 1, curr_pos[1])
                    new_dir = direction
                # Move W: Cube 1
                case 'W':
                    new_pos = (3 * cube_size - curr_pos[0] - 1, cube_size)
                    new_dir = 'E'
        elif 1 * cube_size <= curr_pos[1] < 2 * cube_size:
            # Cube 5
            match direction:
                # Move N: Cube 3 --> no wrap case
                case 'N':
                    new_pos = (curr_pos[0] - 1, curr_pos[1])
                    new_dir = direction
                # Move E: Cube 2
                case 'E':
                    new_pos = (3 * cube_size - curr_pos[0] - 1, 3 * cube_size - 1)
                    new_dir = 'W'
                # Move S: Cube 6
                case 'S':
                    new_pos = (curr_pos[1] + 2 * cube_size, cube_size - 1)
                    new_dir = 'W'
                # Move W: Cube 4 --> no wrap case
                case 'W':
                    new_pos = (curr_pos[0], curr_pos[1] - 1)
                    new_dir = direction
    # Cube 6
    elif 3 * cube_size <= curr_pos[0] < 4 * cube_size:
        # Cube 6
        match direction:
            # Move N: Cube 4 --> no wrap case
            case 'N':
                new_pos = (curr_pos[0] - 1, curr_pos[1])
                new_dir = direction
            # Move E: Cube 5
            case 'E':
                new_pos = (3 * cube_size - 1, curr_pos[0] - 2 * cube_size)
                new_dir = 'N'
            # Move S: Cube 2
            case 'S':
                new_pos = (0, curr_pos[1] + 2 * cube_size)
                new_dir = 'S'
            # Move W: Cube 1
            case 'W':
                new_pos = (0, curr_pos[0] - 2 * cube_size)
                new_dir = 'S'

    return new_pos, direction_dict[new_dir]


# Solves part 1
def part_one(board_map: np.ndarray, instructions: list) -> int:
    # Direction list to cycle through (order same as for calculation needed)
    direction_list = ['E', 'S', 'W', 'N']
    # Get starting position
    curr_pos = (0, np.where(board_map[0, :] == 1)[0][0])
    # Initialize variables
    curr_dir_idx = 0
    y_len, x_len = board_map.shape
    # Loop through all instructions
    for instruction in instructions:
        steps, direction = instruction
        # Take one step at a time
        for _ in range(steps):
            # Initialize wrap (which is how much we need to wrap around accounting for the "empty space")
            wrap = 0
            # Get direction
            match direction_list[curr_dir_idx]:
                case 'N':
                    # Find new positions, loop while we are in "empty space"
                    while board_map[(curr_pos[0] - 1 - wrap) % y_len, curr_pos[1]] == 0:
                        wrap += 1
                    # Check if it is not blocked
                    if board_map[(curr_pos[0] - 1 - wrap) % y_len, curr_pos[1]] == 1:
                        curr_pos = ((curr_pos[0] - 1 - wrap) % y_len, curr_pos[1])
                    # Otherwise, break the loop
                    elif board_map[(curr_pos[0] - 1 - wrap) % y_len, curr_pos[1]] == 2:
                        break
                case 'E':
                    # Find new positions, loop while we are in "empty space"
                    while board_map[curr_pos[0], (curr_pos[1] + 1 + wrap) % x_len] == 0:
                        wrap += 1
                    # Check if it is not blocked
                    if board_map[curr_pos[0], (curr_pos[1] + 1 + wrap) % x_len] == 1:
                        curr_pos = (curr_pos[0], (curr_pos[1] + 1 + wrap) % x_len)
                    # Otherwise, break the loop
                    elif board_map[curr_pos[0], (curr_pos[1] + 1 + wrap) % x_len] == 2:
                        break
                case 'S':
                    # Find new positions, loop while we are in "empty space"
                    while board_map[(curr_pos[0] + 1 + wrap) % y_len, curr_pos[1]] == 0:
                        wrap += 1
                    # Check if it is not blocked
                    if board_map[(curr_pos[0] + 1 + wrap) % y_len, curr_pos[1]] == 1:
                        curr_pos = ((curr_pos[0] + 1 + wrap) % y_len, curr_pos[1])
                    # Otherwise, break the loop
                    elif board_map[(curr_pos[0] + 1 + wrap) % y_len, curr_pos[1]] == 2:
                        break
                case 'W':
                    # Find new positions
                    while board_map[curr_pos[0], (curr_pos[1] - 1 - wrap) % x_len] == 0:
                        wrap += 1
                    # Check if it is not blocked
                    if board_map[curr_pos[0], (curr_pos[1] - 1 - wrap) % x_len] == 1:
                        curr_pos = (curr_pos[0], (curr_pos[1] - 1 - wrap) % x_len)
                    # Otherwise, break the loop
                    elif board_map[curr_pos[0], (curr_pos[1] - 1 - wrap) % x_len] == 2:
                        break
        # Update direction
        if direction == 'R':
            curr_dir_idx = (curr_dir_idx + 1) % 4
        elif direction == 'L':
            curr_dir_idx = (curr_dir_idx - 1) % 4

    # Return result as given by formula, adjust for 0 index
    return 1000 * (curr_pos[0] + 1) + 4 * (curr_pos[1] + 1) + curr_dir_idx


# Solves part 2
def part_two(board_map: np.ndarray, instructions: list, cube_size: int) -> int:
    # Direction list to cycle through (order same as for calculation needed)
    direction_list = ['E', 'S', 'W', 'N']
    # Get starting position
    curr_pos = (0, np.where(board_map[0, :] == 1)[0][0])
    # Initialize variables
    curr_dir_idx = 0
    y_len, x_len = board_map.shape
    new_pos = (-1, -1)
    new_dir_idx = -1
    # Loop through all instructions
    for instruction in instructions:
        steps, direction = instruction
        # Take one step at a time
        for _ in range(steps):
            # Take a step
            match direction_list[curr_dir_idx]:
                case 'N':
                    # Check if we need to wrap around a cube corner
                    if board_map[(curr_pos[0] - 1) % y_len, curr_pos[1]] == 0 or (curr_pos[0] - 1) < 0:
                        new_pos, new_dir_idx = cube_wrapping(curr_pos, 'N', cube_size)
                    # Otherwise take a normal step
                    else:
                        new_pos = ((curr_pos[0] - 1) % y_len, curr_pos[1])
                        new_dir_idx = curr_dir_idx
                case 'E':
                    # Check if we need to wrap around a cube corner
                    if board_map[curr_pos[0], (curr_pos[1] + 1) % x_len] == 0 or (curr_pos[1] + 1) >= x_len:
                        new_pos, new_dir_idx = cube_wrapping(curr_pos, 'E', cube_size)
                    # Otherwise take a normal step
                    else:
                        new_pos = (curr_pos[0], (curr_pos[1] + 1) % x_len)
                        new_dir_idx = curr_dir_idx
                case 'S':
                    # Check if we need to wrap around a cube corner
                    if board_map[(curr_pos[0] + 1) % y_len, curr_pos[1]] == 0 or (curr_pos[0] + 1) >= y_len:
                        new_pos, new_dir_idx = cube_wrapping(curr_pos, 'S', cube_size)
                    # Otherwise take a normal step
                    else:
                        new_pos = ((curr_pos[0] + 1) % y_len, curr_pos[1])
                        new_dir_idx = curr_dir_idx
                case 'W':
                    # Check if we need to wrap around a cube corner
                    if board_map[curr_pos[0], (curr_pos[1] - 1) % x_len] == 0 or (curr_pos[1] - 1) % x_len < 0:
                        new_pos, new_dir_idx = cube_wrapping(curr_pos, 'W', cube_size)
                    # Otherwise take a normal step
                    else:
                        new_pos = (curr_pos[0], (curr_pos[1] - 1) % x_len)
                        new_dir_idx = curr_dir_idx
            # Check if the new position is blocked
            if board_map[new_pos] == 1:
                # Update position
                curr_pos = new_pos
                # Update direction
                curr_dir_idx = new_dir_idx
            # Otherwise, break the loop
            elif board_map[new_pos] == 2:
                break
        # Update direction
        if direction == 'R':
            curr_dir_idx = (curr_dir_idx + 1) % 4
        elif direction == 'L':
            curr_dir_idx = (curr_dir_idx - 1) % 4

    # Return result as given by formula, adjust for 0 index
    return 1000 * (curr_pos[0] + 1) + 4 * (curr_pos[1] + 1) + curr_dir_idx


def main():
    board_map, instructions = get_input()
    print('The final password is:', part_one(board_map, instructions))
    print('The final password is:', part_two(board_map, instructions, 50))
    print('Note: The code does not automatically adjust for other cube layouts. The example case is provided.')


if __name__ == '__main__':
    main()
