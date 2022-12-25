# Get data from .txt file
def get_input():
    with open('input/Day25.txt', 'r') as file:
        # Split lines and write each line to list
        data = file.read().splitlines()
    return data


# Solves part 1
def part_one(data: list) -> str:
    # Numbers dict
    numb_dict = {'2': 2, '1': 1, '0': 0, '-': -1, '=': -2}
    # Loop through each line
    total_sum = 0
    for line in data:
        for i, char in enumerate(line[::-1]):
            # Convert char and add to total sum
            total_sum += numb_dict[char] * (5 ** i)

    # Convert back into SNAFU system
    # Invert dictionary
    conv_dict = {v: k for k, v in numb_dict.items()}
    # Initialize variables
    result = ''
    # Go through powers of 5, remainder is always the digit counting from the back
    while total_sum > 0:
        # Divide by 5
        total_sum, remainder = divmod(total_sum, 5)
        # If remainder is 3 or 4, we have a '=' or '-' and need to correct
        if remainder > 2:
            remainder -= 5
            total_sum += 1
        # Add new SNAFU digit in front of current string
        result = conv_dict[remainder] + result
    return result


def main():
    print('The SNAFU number is:', part_one(get_input()))
    print('The last star you get automatically for gathering all others')


if __name__ == '__main__':
    main()
