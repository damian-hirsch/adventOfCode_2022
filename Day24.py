from collections import deque


# Get data from .txt file
def get_input() -> tuple:
    with open('input/Day24.txt', 'r') as file:
        # Split lines and write each line to list
        data = file.read().splitlines()
        # Find blizzards
        blizzards = set()
        # Check each line in data
        for rows, line in enumerate(data):
            # Check each char in line
            for columns, char in enumerate(line):
                # Add blizzard
                if char in '^>v<':
                    blizzards.add((char, rows - 1, columns - 1))
    return blizzards, rows - 1, columns - 1


def shortest_path(blizzards: set, max_rows: int, max_columns: int, start: tuple, goal: tuple, t: int):
    # Initialize directions N, E, S, W, wait
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1), (0, 0)]
    # Create deque (t, row, column)
    paths = deque([(t, start[0], start[1])])
    visited = set()

    while len(paths) > 0:
        # Get next path
        t, row, column = paths.popleft()

        # Check if we have seen it already
        if (t, row, column) in visited:
            continue

        # Add it to visited paths
        visited.add((t, row, column))

        # Increase t
        t += 1

        # Check all moves
        for direction in directions:
            new_r = row + direction[0]
            new_c = column + direction[1]

            # Check if we reached the target
            if (new_r, new_c) == goal:
                return t

            # Check if we are within the allowed area
            if (new_r < 0 or new_r >= max_rows or new_c < 0 or new_c >= max_columns) and not (new_r, new_c) == start:
                continue

            # Check if we can move due to the blizzard
            if ('^', (new_r + t) % max_rows, new_c) in blizzards \
                    or ('>', new_r, (new_c - t) % max_columns) in blizzards \
                    or ('v', (new_r - t) % max_rows, new_c) in blizzards \
                    or ('<', new_r, (new_c + t) % max_columns) in blizzards:
                continue

            # If it is a valid move, add new position to paths
            paths.append((t, new_r, new_c))

    return -1


# Solves part 1
def part_one(blizzards: set, max_rows: int, max_columns: int) -> int:
    t = shortest_path(blizzards, max_rows, max_columns, (-1, 0), (max_rows, max_columns - 1), 0)

    return t


# Solves part 2
def part_two(blizzards: set, max_rows: int, max_columns: int, t1: int) -> int:
    t2 = shortest_path(blizzards, max_rows, max_columns, (max_rows, max_columns - 1), (-1, 0), t1)
    t3 = shortest_path(blizzards, max_rows, max_columns, (-1, 0), (max_rows, max_columns - 1), t2)

    return t3


def main():
    bz, mr, mc = get_input()
    t1 = part_one(bz, mr, mc)
    print('Fewest minutes to avoid the blizzards and reach the goal is:', t1)
    print('Fewest minutes to reach the goal, go back, reach the goal again is:', part_two(bz, mr, mc, t1))


if __name__ == '__main__':
    main()
