# Get data from .txt file
def get_input() -> set:
    with open('input/Day14.txt', 'r') as file:
        # Split lines and write each line to list
        data = file.read().splitlines()

        # Build cave system
        cave = set()
        # Loop through each line
        for line in data:
            # Split at the arrow
            cords = line.split(' -> ')
            # Pop the first instruction, split at the comma, and convert to int
            x2, y2 = list(map(int, cords.pop(0).split(',')))
            # While there are instructions on this line
            while cords:
                # Set the "to" instruction to a "from" instruction
                y1 = y2
                x1 = x2
                # Get the new "to" instruction
                x2, y2 = list(map(int, cords.pop(0).split(',')))
                # Check if we have a horizontal or vertical wall
                if y1 == y2:
                    # Create rocks and add to cave
                    for i in range(min(x1, x2), max(x1, x2) + 1):
                        cave.add((i, y1))
                elif x1 == x2:
                    for j in range(min(y1, y2), max(y1, y2) + 1):
                        cave.add((x1, j))
    return cave


# Solves part 1
def part_one(cave: set) -> int:
    # Count the rocks for later
    rocks = len(cave)
    # Get the maximum value of the lowest rock to know when a piece is in the abyss
    _, y_max = max(cave, key=lambda item: item[1])
    # Initialize coordinates of the pouring location
    x = 500
    y = 0
    # While no sand piece has ended in the abyss (not really necessary, because the exit condition is in the inner loop)
    while y <= y_max:
        # Initialize/reset not blocked status to see if the sand is still moving
        not_blocked = True
        while not_blocked:
            # Check abyss, if yes, return the number of sand blocks
            if y >= y_max:
                return len(cave) - rocks
            # Check D
            elif (x, y + 1) not in cave:
                y += 1
            # Check DL
            elif (x - 1, y + 1) not in cave:
                y += 1
                x -= 1
            # Check DR
            elif (x + 1, y + 1) not in cave:
                y += 1
                x += 1
            # We are blocked, settle sand
            else:
                # Update status to blocked
                not_blocked = False
                # Add the sand block to the cave pieces
                cave.add((x, y))
                # Reset coordinates for new sand block that's coming
                x = 500
                y = 0
    return - 1


# Solves part 2
def part_two(cave: set) -> int:
    # Count the rocks for later
    rocks = len(cave)
    # Get the maximum value of the lowest rock to know where the floor is
    _, y_max = max(cave, key=lambda item: item[1])
    # Floor location
    y_max += 2
    # Initialize coordinates of the pouring location
    x = 500
    y = 0
    # While a sand block is not blocking the entry, sand is still coming in, else return number of sand blocks
    while (500, 0) not in cave:
        # Initialize/reset not blocked status to see if the sand is still moving
        not_blocked = True
        while not_blocked:
            # Check if we are at floor level (no block can move from here)
            if y == y_max - 1:
                not_blocked = False
                cave.add((x, y))
                x = 500
                y = 0
            # Check D
            elif (x, y + 1) not in cave:
                y += 1
            # Check DL
            elif (x - 1, y + 1) not in cave:
                y += 1
                x -= 1
            # Check DR
            elif (x + 1, y + 1) not in cave:
                y += 1
                x += 1
            # We are blocked, settle sand
            else:
                # Update status to blocked
                not_blocked = False
                # Add the sand block to the cave pieces
                cave.add((x, y))
                # Reset coordinates for new sand block that's coming
                x = 500
                y = 0
    return len(cave) - rocks


def main():
    print('This many units of sand come to rest before sand starts flowing into the abyss:', part_one(get_input()))
    print('This many units of sand come to rest when the entry is blocked:', part_two(get_input()))


if __name__ == '__main__':
    main()
