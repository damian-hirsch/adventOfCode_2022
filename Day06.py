# Get data from .txt file
def get_input() -> str:
    with open('input/Day06.txt', 'r') as file:
        # Get the string from file
        data = file.read()
    return data


# Solves part 1
def part_one(string: str) -> int:
    # Initialize marker
    marker_found = False
    # Set counter to 0
    counter = 0
    # While no marker is found, keep going
    while not marker_found:
        # Get a substring of 4 characters
        marker = string[counter:counter + 4]
        # Take the set and check if that set has a length of 4 (= 4 unique characters)
        if len(set(marker)) == 4:
            # If found, set flag to quit while loop
            marker_found = True
        # Else increase counter to check next substring
        else:
            counter += 1
    # Add +4 to account for the number of the last character
    return counter + 4


# Solves part 2
def part_two(string: str) -> int:
    # Initialize marker
    marker_found = False
    # Set counter to 0
    counter = 0
    # While no marker is found, keep going
    while not marker_found:
        # Get a substring of 14 characters
        marker = string[counter:counter + 14]
        # Take the set and check if that set has a length of 14 (= 14 unique characters)
        if len(set(marker)) == 14:
            # If found, set flag to quit while loop
            marker_found = True
        # Else increase counter to check next substring
        else:
            counter += 1
    # Add +14 to account for the number of the last character
    return counter + 14


def main():
    print('This many characters need to be processed for the start-of-packet marker:', part_one(get_input()))
    print('This many characters need to be processed for the start-of-message marker:', part_two(get_input()))


if __name__ == '__main__':
    main()
