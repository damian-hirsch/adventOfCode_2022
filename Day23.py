# Get data from .txt file
def get_input() -> set:
    with open('input/Day23.txt', 'r') as file:
        # Split lines and write each line to list
        data = file.read().splitlines()
        # Loop through each line
        elves = set()
        for y, line in enumerate(data):
            for x, char in enumerate(line):
                # Add elves
                if char == '#':
                    elves.add((x, y))
    return elves


# Solves part 1
def part_one(elves: set, rounds: int) -> int:
    # N, NE, E, SE, S, SW, W, NW
    check_directions = {(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)}
    # N, NE, NW, S, SE, SW, W, NW, SW, E, NE, SE
    directions = [[(0, -1), (1, -1), (-1, -1)],
                  [(0, 1), (1, 1), (-1, 1)],
                  [(-1, 0), (-1, -1), (-1, 1)],
                  [(1, 0), (1, -1), (1, 1)]]
    # Repeat for every round
    for _ in range(rounds):
        old = list(elves)
        new = []
        seen_twice = set()
        for elf in elves:
            # Check surroundings
            surroundings = [(elf[0] + x[0], elf[1] + x[1]) for x in check_directions]
            if bool(elves & set(surroundings)):
                # If there neighbors, try to move
                for i in range(4):
                    # Check all directions
                    if not bool(set([(elf[0] + x[0], elf[1] + x[1]) for x in directions[i]]) & elves):
                        proposal = (elf[0] + directions[i][0][0], elf[1] + directions[i][0][1])
                        # Check if we have seen this proposal before this round
                        if proposal in new:
                            seen_twice.add(proposal)
                        new.append(proposal)
                        break
                    # Blocked in all directions, stay in position
                    elif i == 3:
                        new.append(elf)
            # Otherwise, stay in position
            else:
                new.append(elf)

        # Check proposed directions and don't move the overlapping ones
        elves = set()
        for j, proposal in enumerate(new):
            # Check if there is a second one in the proposal list
            if proposal not in seen_twice:
                elves.add(proposal)
            # Otherwise, keep the old value
            else:
                elves.add(old[j])

        # Update direction where the elves move first
        popped = directions.pop(0)
        directions.append(popped)

        # Check if we have the same layout
        if old == new:
            break

    # Calculate rectangle
    min_x = min(elves, key=lambda item: item[0])[0]
    max_x = max(elves, key=lambda item: item[0])[0]
    min_y = min(elves, key=lambda item: item[1])[1]
    max_y = max(elves, key=lambda item: item[1])[1]

    return (max_x - min_x + 1) * (max_y - min_y + 1) - len(elves)


# Solves part 2
def part_two(elves: set) -> int:
    # N, NE, E, SE, S, SW, W, NW
    check_directions = {(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)}
    # N, NE, NW, S, SE, SW, W, NW, SW, E, NE, SE
    directions = [[(0, -1), (1, -1), (-1, -1)],
                  [(0, 1), (1, 1), (-1, 1)],
                  [(-1, 0), (-1, -1), (-1, 1)],
                  [(1, 0), (1, -1), (1, 1)]]
    # Repeat as long as we have changes (break condition at bottom)
    rounds = 0
    while True:
        old = list(elves)
        new = []
        seen_twice = set()
        for elf in elves:
            # Check surroundings
            surroundings = [(elf[0] + x[0], elf[1] + x[1]) for x in check_directions]
            if bool(elves & set(surroundings)):
                # If there neighbors, try to move
                for i in range(4):
                    # Check all directions
                    if not bool(set([(elf[0] + x[0], elf[1] + x[1]) for x in directions[i]]) & elves):
                        proposal = (elf[0] + directions[i][0][0], elf[1] + directions[i][0][1])
                        # Check if we have seen this proposal before this round
                        if proposal in new:
                            seen_twice.add(proposal)
                        new.append(proposal)
                        break
                    # Blocked in all directions, stay in position
                    elif i == 3:
                        new.append(elf)
            # Otherwise, stay in position
            else:
                new.append(elf)

        # Check proposed directions and don't move the overlapping ones
        elves = set()
        for j, proposal in enumerate(new):
            # Check if there is a second one in the proposal list
            if proposal not in seen_twice:
                elves.add(proposal)
            # Otherwise, keep the old value
            else:
                elves.add(old[j])

        # Update direction where the elves move first
        popped = directions.pop(0)
        directions.append(popped)

        # Increase round number
        rounds += 1

        # Check if we have the same layout
        if old == new:
            break

        print(f'\rPart 2: Checking round (expect around 1000): {rounds}', end='')
    return rounds


def main():
    print('Part 1: The rectangle contains this many empty ground tiles:', part_one(get_input(), 10))
    print('\rPart 2: The number of the first round where no elf moves is:', part_two(get_input()))


if __name__ == '__main__':
    main()
