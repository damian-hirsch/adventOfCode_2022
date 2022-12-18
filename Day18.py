from collections import deque


# Get data from .txt file
def get_input() -> tuple:
    with open('input/Day18.txt', 'r') as file:
        # Split lines and write each line to list
        data = file.read().splitlines()
        # Initialize cubes and maxima
        cubes = set()
        min_coord = float('inf')
        max_coord = -float('inf')
        for line in data:
            x, y, z = tuple(map(int, line.split(',')))
            # Add cube
            cubes.add(Cube((int(x), int(y), int(z))))
            # Get min and max values
            min_coord = min(min_coord, x, y, z)
            max_coord = max(max_coord, x, y, z)
    return cubes, (min_coord - 1, max_coord + 1)


# Setup cube class
class Cube:
    # Initialize
    def __init__(self, position: tuple):
        self.position = position

    # Defining how the node class is represented
    def __repr__(self):
        return f'{self.position}'

    # Defining what needs to be compared when comparing two cubes
    def __eq__(self, other):
        return self.position == other.position

    # Defining hash to make cubes hashable for sets
    def __hash__(self):
        return hash(self.position)

    # Get all neighbors
    def get_neighbors(self) -> set:
        # Unpack position
        x, y, z = self.position
        # Create 6 neighboring cubes
        neighbors = set()
        neighbors.add(Cube((x + 1, y, z)))
        neighbors.add(Cube((x - 1, y, z)))
        neighbors.add(Cube((x, y + 1, z)))
        neighbors.add(Cube((x, y - 1, z)))
        neighbors.add(Cube((x, y, z + 1)))
        neighbors.add(Cube((x, y, z - 1)))
        return neighbors


# Solves part 1
def part_one(cubes: set) -> int:
    # Initialize free faces
    faces = 0
    # For each cube, add the free sides it has
    for cube in cubes:
        neighbors = cube.get_neighbors()
        # Check how man sides are not occupied by other cubes and add to faces
        faces += len(neighbors - cubes)

    return faces


# Solves part 2
def part_two(cubes: set, minmax: tuple) -> int:
    # Initialize free faces
    faces = 0
    # Get range of the droplet space
    min_coord, max_coord = minmax

    # Go through all air cubes from outside (this way air pockets are never visited) and count all faces
    # Initialize starting air cube
    start_air_cube = Cube((min_coord, min_coord, min_coord))
    # Add it to deque
    air_cube_deque = deque([start_air_cube])
    # Initialize visited
    visited_air_cubes = set()

    # While there are pockets to visit
    while len(air_cube_deque) > 0:
        # Pop the next air cube
        air_cube = air_cube_deque.popleft()
        # If we already visited the air cube, get the next one
        if air_cube in visited_air_cubes:
            continue
        # Otherwise, add it to the visited air cubes and continue
        visited_air_cubes.add(air_cube)

        # Create neighboring cubes (could be air or lava)
        neighbors = air_cube.get_neighbors()

        for neighbor in neighbors:
            (x, y, z) = neighbor.position
            # Make sure the neighbor cube is still within our space
            if min_coord <= x <= max_coord and min_coord <= y <= max_coord and min_coord <= z <= max_coord:
                # If the neighbor is a lava cube, then that is another surface face
                if neighbor in cubes:
                    faces += 1
                # Otherwise, it is another air cube that is added to the deque
                else:
                    air_cube_deque.append(neighbor)

    return faces


def main():
    cubes, minmax = get_input()
    print('The surface area of the lava droplet is:', part_one(cubes))
    print('The exterior surface area of the lava droplet is:', part_two(cubes, minmax))


if __name__ == '__main__':
    main()
