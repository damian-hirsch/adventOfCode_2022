# Get data from .txt file
def get_input():
    with open('input/Day09.txt', 'r') as file:
        # Split lines and write each line to list
        data = file.read().splitlines()
    return data


def move(pos_1: list, pos_2: list) -> list:
    # Calculate distance
    distance = ((pos_1[0] - pos_2[0]) ** 2 + (pos_1[1] - pos_2[1]) ** 2) ** (1/2)
    # Make sure they are not adjacent already
    if distance <= 2 ** (1/2):
        return pos_2
    else:
        # Check y
        if pos_2[0] < pos_1[0]:
            pos_2[0] += 1
        elif pos_2[0] > pos_1[0]:
            pos_2[0] -= 1
        # Check x
        if pos_2[1] < pos_1[1]:
            pos_2[1] += 1
        elif pos_2[1] > pos_1[1]:
            pos_2[1] -= 1
        return pos_2


# Solves part 1
def part_one(data: list) -> int:
    # Initialize rope knots
    pos_h = [0, 0]
    pos_t = [0, 0]
    # Initialize visited position of tail as a set
    visited_positions = {(pos_t[0], pos_t[1])}
    # Go through instructions
    for line in data:
        # Grab direction
        direction = line[0]
        # Grab number of steps (considering multi-digit numbers)
        steps = int(line[2:])
        # Loop through each step
        for i in range(steps):
            # Match the direction and add to head
            match direction:
                case 'U':
                    pos_h[0] += 1
                case 'R':
                    pos_h[1] += 1
                case 'D':
                    pos_h[0] -= 1
                case 'L':
                    pos_h[1] -= 1
            # Calculate new tail position
            pos_t = move(pos_h, pos_t)
            # Add new tail position to set
            visited_positions.add((pos_t[0], pos_t[1]))

    # Return length of the set
    return len(visited_positions)


# Solves part 2
def part_two(data: list) -> int:
    # Initialize rope knots, could also use an array to make it more compact, but also less understandable
    pos_h = [0, 0]
    pos_1 = [0, 0]
    pos_2 = [0, 0]
    pos_3 = [0, 0]
    pos_4 = [0, 0]
    pos_5 = [0, 0]
    pos_6 = [0, 0]
    pos_7 = [0, 0]
    pos_8 = [0, 0]
    pos_9 = [0, 0]
    # Initialize visited position of tail as a set
    visited_positions = [(pos_9[0], pos_9[1])]
    # Go through instructions
    for line in data:
        # Grab direction
        steps = int(line[2:])
        # Grab number of steps (considering multi-digit numbers)
        direction = line[0]
        # Loop through each step
        for i in range(steps):
            # Match the direction and add to head
            match direction:
                case 'U':
                    pos_h[0] += 1
                case 'R':
                    pos_h[1] += 1
                case 'D':
                    pos_h[0] -= 1
                case 'L':
                    pos_h[1] -= 1
            # Update all positions of subsequent knots
            pos_1 = move(pos_h, pos_1)
            pos_2 = move(pos_1, pos_2)
            pos_3 = move(pos_2, pos_3)
            pos_4 = move(pos_3, pos_4)
            pos_5 = move(pos_4, pos_5)
            pos_6 = move(pos_5, pos_6)
            pos_7 = move(pos_6, pos_7)
            pos_8 = move(pos_7, pos_8)
            pos_9 = move(pos_8, pos_9)
            # Add new tail position to set
            visited_positions.append((pos_9[0], pos_9[1]))

    # Return length of the set
    return len(set(visited_positions))


def main():

    print('The tail of the rope visits this many positions at least once:', part_one(get_input()))
    print('The tail of the rope visits this many positions at least once:', part_two(get_input()))


if __name__ == '__main__':
    main()
