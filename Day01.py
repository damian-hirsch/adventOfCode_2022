import numpy as np


# Get data from .txt file
def get_input():
    with open('input/Day01.txt', 'r') as file:
        # Split lines and write each line to list
        data = file.read().splitlines()
    return data


# Solves part 1
def part_one(data: list) -> int:
    # Initialize list and calorie sum
    calorie_list = []
    calorie_sum = 0
    # Go through the list
    for line in data:
        # If we find a blank line, append value to the calorie list and set sum to 0
        if line == '':
            calorie_list.append(calorie_sum)
            calorie_sum = 0
        # Add value to current sum
        else:
            calorie_sum += int(line)
    # Add last entry to list (no blank line at end of list)
    calorie_list.append(calorie_sum)
    # Find the maximum value in list
    max_calorie = max(calorie_list)

    return max_calorie


# Solves part 2
def part_two(data: list) -> int:
    # Initialize list and calorie sum
    calorie_list = []
    calorie_sum = 0
    # Go through the list
    for line in data:
        # If we find a blank line, append value to the calorie list and set sum to 0
        if line == '':
            calorie_list.append(calorie_sum)
            calorie_sum = 0
        # Add value to current sum
        else:
            calorie_sum += int(line)
    # Add last entry to list (no blank line at end of list)
    calorie_list.append(calorie_sum)
    # Sort the list
    calorie_list.sort()
    # Get last three values (list is sorted ASC by default) and take the sum
    top3_calorie = sum(calorie_list[-3:])

    return top3_calorie


def main():

    print('The elf is carrying:', part_one(get_input()))
    print('The top three elves are carrying:', part_two(get_input()))


if __name__ == '__main__':
    main()
