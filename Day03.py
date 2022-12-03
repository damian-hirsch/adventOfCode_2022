# Get data from .txt file
import string


def get_input():
    with open('input/Day03.txt', 'r') as file:
        # Split lines and write each line to list
        data = file.read().splitlines()
    return data


# Solves part 1
def part_one(data: list) -> int:
    # Create dictionary
    alphabet_list = list(string.ascii_letters)
    number_list = range(1, 53)
    dict_score = dict(zip(alphabet_list, number_list))

    # Calculate score
    total_sum = 0
    for line in data:
        # Split string
        first_part, second_part = line[:len(line) // 2], line[len(line) // 2:]
        # Compare strings using sets
        common_letter = ''.join(set(first_part).intersection(second_part))
        # Get score with dictionary mapping
        total_sum += dict_score[common_letter]

    return total_sum


# Solves part 2
def part_two(data: list) -> int:
    # Create dictionary
    alphabet_list = list(string.ascii_letters)
    number_list = range(1, 53)
    dict_score = dict(zip(alphabet_list, number_list))

    # Calculate score
    total_sum = 0
    for i in range(0, len(data) // 3):
        # Get strings
        a = data[3 * i]
        b = data[3 * i + 1]
        c = data[3 * i + 2]
        # Compare strings using sets
        common_letter = ''.join(set(a).intersection(b, c))
        # Get score with dictionary mapping
        total_sum += dict_score[common_letter]

    return total_sum


def main():
    print('Sum of the priorities of item types:', part_one(get_input()))
    print('Sum of the priorities of item types:', part_two(get_input()))


if __name__ == '__main__':
    main()
