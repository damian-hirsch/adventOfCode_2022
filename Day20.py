import numpy as np


# Get data from .txt file
def get_input():
    with open('input/Day20.txt', 'r') as file:
        # Split lines and write each line to list
        data = file.read().splitlines()
        # Map strings in list to integers
        data = list(map(int, data))
    return data


# Solves part 1
def part_one() -> np.ndarray:
    test = np.zeros(5)
    return test


# Solves part 2
def part_two() -> int:

    return 2


def main():

    print('This many measurements are larger than the previous measurement: ', part_one())
    print('This sums are larger than the previous sum: ', part_two())


if __name__ == '__main__':
    main()
