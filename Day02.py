# Get data from .txt file
def get_input() -> list:
    with open('input/Day02.txt', 'r') as file:
        # Remove space, split lines, and write each line to list
        data = file.read().replace(' ', '').splitlines()
    return data


# Solves part 1
def part_one(data: list) -> int:
    # Create mapper based on all possible outcomes and their result
    dict_map = {
        'AX': 4, 'AY': 8, 'AZ': 3,
        'BX': 1, 'BY': 5, 'BZ': 9,
        'CX': 7, 'CY': 2, 'CZ': 6
    }
    # Convert data list to scores with the mapper
    score_list = list(map(dict_map.get, data))
    # Sum all the results
    return sum(score_list)


# Solves part 2
def part_two(data: list) -> int:
    # Create mapper based on all possible outcomes and their result
    dict_map = {
        'AX': 3, 'AY': 4, 'AZ': 8,
        'BX': 1, 'BY': 5, 'BZ': 9,
        'CX': 2, 'CY': 6, 'CZ': 7
    }
    # Convert data list to scores with the mapper
    score_list = list(map(dict_map.get, data))
    # Sum all the results
    return sum(score_list)


def main():

    print('The score would be:', part_one(get_input()))
    print('The score would be:', part_two(get_input()))


if __name__ == '__main__':
    main()
