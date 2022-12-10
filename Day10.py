import numpy as np
# Set print width for nump arrays higher, so we can actually read the output
np.set_printoptions(linewidth=300)


# Get data from .txt file
def get_input():
    with open('input/Day10.txt', 'r') as file:
        # Split lines and write each line to list
        data = file.read().splitlines()
    return data


# Solves part 1
def part_one(data: list) -> int:
    # Initialize list of X
    x_list = []
    # Current X
    x = 1
    # Append current X
    x_list.append(x)
    # Loop through instructions
    for i, line in enumerate(data):
        try:
            # Try to split the line
            a, b = line.split(' ')
            # Wait two cycles
            x_list.append(x)
            x_list.append(x)
            # Update X
            x += int(b)
        except ValueError:
            # If we couldn't split, it's a 'noop' instruction
            # Wait one cycle
            x_list.append(x)

    # Calculate signal strength
    sig_sum = 0
    # Start from cycle 20 and take every 40th cycle available
    for i in range(20, len(x_list), 40):
        # Calculate sum
        sig_sum += i * x_list[i]

    return sig_sum


# Solves part 2
def part_two(data: list) -> np.ndarray:
    # Initialize CRT screen
    crt = np.zeros((6, 40), dtype=str)
    # Current X
    x = 1
    # Current cycle (always one less of the current cycle until it's finished)
    cycle = 0
    for line in data:
        try:
            # Try to split the line
            a, b = line.split(' ')

            # Draw first cycle
            # Check if sprite is syncing with the cycle, mod the cycle (0 to 39) and get the right CRT lines (0 to 5)
            if x - 1 <= cycle % 40 <= x + 1:
                crt[cycle // 40, cycle % 40] = '#'
            else:
                crt[cycle // 40, cycle % 40] = '.'
            # Increase cycle
            cycle += 1

            # Draw
            if x - 1 <= cycle % 40 <= x + 1:
                crt[cycle // 40, cycle % 40] = '#'
            else:
                crt[cycle // 40, cycle % 40] = '.'
            # Update X and increase cycle
            x += int(b)
            cycle += 1

        except ValueError:
            # Draw
            if x - 1 <= cycle % 40 <= x + 1:
                crt[cycle // 40, cycle % 40] = '#'
            else:
                crt[cycle // 40, cycle % 40] = '.'
            # Increase cycle
            cycle += 1

    return crt


def main():

    print('The sum of these six signal strengths is:', part_one(get_input()))
    print('The eight capital letters that appear on the CRT are:\n', part_two(get_input()))


if __name__ == '__main__':
    main()
