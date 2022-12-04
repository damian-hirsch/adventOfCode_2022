import re


# Get data from .txt file
def get_input():
    with open('input/Day04.txt', 'r') as file:
        # Split lines and write each line to list
        data = file.read().splitlines()
    # Convert string to list of tuples
    number_list = []
    for line in data:
        # Find the numbers using regex
        re_matches = re.search(r'(\d+)-(\d+),(\d+)-(\d+)', line)
        a = int(re_matches.group(1))
        b = int(re_matches.group(2))
        c = int(re_matches.group(3))
        d = int(re_matches.group(4))
        # Append numbers to list
        number_list.append((a, b, c, d))
    return number_list


# Solves part 1
def part_one(data: list[tuple]) -> int:
    # Initialize count
    count = 0
    for line in data:
        # Unpack tuple
        a, b, c, d = line
        # Create ranges and convert to sets
        section_1 = set(range(a, b + 1))
        section_2 = set(range(c, d + 1))
        # Check if either set is a subset of the other set
        if section_1.issubset(section_2) or section_2.issubset(section_1):
            count += 1
    return count


# Solves part 2
def part_two(data: list[tuple]) -> int:
    # Initialize count
    count = 0
    for line in data:
        # Unpack tuple
        a, b, c, d = line
        # Create ranges and convert to sets
        section_1 = set(range(a, b + 1))
        section_2 = set(range(c, d + 1))
        # Check if there is any overlap between the sets
        if bool(section_1 & section_2):
            count += 1
    return count


def main():

    print('In this many assignment pairs does one range fully contain the other:', part_one(get_input()))
    print('In this many assignment pairs do the ranges overlap:', part_two(get_input()))


if __name__ == '__main__':
    main()
