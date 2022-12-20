import numpy as np


# Get data from .txt file
def get_input() -> list:
    with open('input/Day20.txt', 'r') as file:
        # Split lines and write each line to list
        data = file.read().splitlines()
        # Map strings in list to integers
        data = list(map(int, data))
    return data


# Note: Numbers are not unique! IDs are needed to identify them
def cycle(sequence: list, num_cycles: int) -> np.ndarray:
    # Get length
    n = len(sequence)
    # Initialize sequence array
    seq_arr = np.zeros((2, n), dtype=np.int_)
    # First row is the sequence
    seq_arr[0, :] = sequence
    # For the second row generate IDs
    seq_arr[1, :] = np.arange(0, n)
    # Initialize sequence_id list to pull the right numbers in the for loop
    sequence_ids = list(zip(sequence, np.arange(0, n)))

    # Cycle num_cycles times
    for _ in range(num_cycles):
        # For each number in the sequence, pull it and its id
        for number, num_id in sequence_ids:
            # Roll the sequence array so that the first sequence number is in the first position
            seq_arr = np.roll(seq_arr, -int(np.argwhere(seq_arr[1, :] == num_id)), axis=1)
            # Get those two elements
            elements = seq_arr[:, 0]
            # Remove those elements from the sequence array
            seq_arr = np.delete(seq_arr, 0, axis=1)
            # Roll the array now number of times (optimized with mod)
            seq_arr = np.roll(seq_arr, -number % (n - 1), axis=1)
            # Insert the elements taken away in the first position again
            seq_arr = np.insert(seq_arr, 0, elements, axis=1)
        # Sort array with 0 in the first position (no need to later find it again, when returning the sequence)
        seq_arr = np.roll(seq_arr, -int(np.argwhere(seq_arr[0, :] == 0)), axis=1)
    # Return sequence only
    return seq_arr[0, :]


# Solves part 1
def part_one(data: list) -> int:
    # Cycle the list
    cycled_array = cycle(data, 1)
    # Calculate and return result
    return cycled_array[1000 % len(data)] + cycled_array[2000 % len(data)] + cycled_array[3000 % len(data)]


# Solves part 2
def part_two(data: list) -> int:
    # Multiply list values
    data = [i * 811589153 for i in data]
    # Cycle the list
    cycled_array = cycle(data, 10)
    # Calculate and return result
    return cycled_array[1000 % len(data)] + cycled_array[2000 % len(data)] + cycled_array[3000 % len(data)]


def main():
    print('The sum of the three numbers that form the grove coordinates is:', part_one(get_input()))
    print('The sum of the three numbers that form the grove coordinates is:', part_two(get_input()))


if __name__ == '__main__':
    main()
