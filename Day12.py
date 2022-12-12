import numpy as np
import heapq


# Get data from .txt file
def get_input() -> tuple[np.ndarray, tuple, tuple]:
    with open('input/Day12.txt', 'r') as file:
        # Split lines and write each line to list
        data = file.read().splitlines()

        # Create maze from input
        start = None
        end = None
        maze = np.zeros((len(data), len(data[0])), dtype=str)
        for j, line in enumerate(data):
            letters = list(line)
            for i, letter in enumerate(letters):
                maze[j, i] = letter
                # If we have the starting letter, save position and convert to 'a'
                if letter == 'S':
                    start = (j, i)
                    maze[j, i] = 'a'
                # If we have the ending letter, save position and convert to 'z'
                elif letter == 'E':
                    end = (j, i)
                    maze[j, i] = 'z'
    return maze, start, end


# Source: https://gist.github.com/ryancollingwood/32446307e976a11a1185a5394d6657bc
# Setup node class
class Node:
    # Initialize
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0

    # Defining what needs to be compared when comparing two Nodes
    def __eq__(self, other):
        return self.position == other.position

    # Defining how the node class is represented
    def __repr__(self):
        return f'{self.position} - g: {self.g} h: {self.h} f: {self.f}'

    # Defining less than for purposes of heap queue
    def __lt__(self, other):
        return self.f < other.f

    # Defining greater than for purposes of heap queue
    def __gt__(self, other):
        return self.f > other.f


# Function to return the path
def return_path(current_node):
    # Initialize
    path = []
    current = current_node
    # Step through parents
    while current is not None:
        # Append to path
        path.append(current.position)
        # Get parent and set it to current
        current = current.parent
    # Return reversed path
    return path[::-1]


def astar(maze: np.ndarray, starts: list, end: tuple):
    # Initialize open and closed list
    open_list = []
    closed_list = []

    # Heapify the open_list
    heapq.heapify(open_list)

    # Create start nodes and add them to the open_list, forcing f = g = h = 0
    for start in starts:
        start_node = Node(None, start)
        start_node.g = start_node.h = start_node.f = 0
        heapq.heappush(open_list, start_node)

    # Create end node
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Which squares do we search (neighbors)
    adjacent_squares = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    # Loop until no more nodes
    while len(open_list) > 0:
        # Get the current node
        current_node = heapq.heappop(open_list)

        # Add it to the closed list
        closed_list.append(current_node)

        # Define exit condition
        if current_node == end_node:
            return return_path(current_node)

        # Check neighbors
        for new_position in adjacent_squares:
            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # If we step outside the maze, continue and investigate the next node
            if node_position[0] > (maze.shape[0] - 1) or node_position[0] < 0 \
                    or node_position[1] > (maze.shape[1] - 1) or node_position[1] < 0:
                continue

            # Check validity of next node (max of 1 height difference), if not, continue and investigate the next node
            if ord(maze[current_node.position[0], current_node.position[1]]) + 1 \
                    < ord(maze[node_position[0], node_position[1]]):
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Check if new node is already on the closed list
            if new_node in closed_list:
                continue

            # Create the f, g, and h values
            new_node.g = current_node.g + 1
            new_node.h = abs(new_node.position[0] - end_node.position[0]) + abs(new_node.position[1] - end_node.position[1])
            new_node.f = new_node.g + new_node.h

            # Check if the new node is already in the open list
            if new_node in open_list:
                idx = open_list.index(new_node)
                if new_node.g < open_list[idx].g:
                    # Update the element
                    open_list[idx].g = new_node.g
                    open_list[idx].h = new_node.g
                    open_list[idx].f = new_node.g
                    open_list[idx].parent = new_node.parent
                    # Update the priority queue
                    heapq.heapify(open_list)
                    continue
                else:
                    continue

            # If neither in closed and open list, add the new node to the open list
            heapq.heappush(open_list, new_node)

    return -1


# Solves part 1
def part_one(maze: np.ndarray, starts: list, end: tuple) -> int:
    # Run A* algorithm
    path = astar(maze, starts, end)

    # Return length of the path = steps
    return len(path) - 1


# Solves part 2
def part_two(maze: np.ndarray, start: tuple, end: tuple) -> int:
    # Initialize starting positions
    starts = [start]
    # Find all starting nodes in maze
    shape = maze.shape
    for j in range(shape[0]):
        for i in range(shape[1]):
            if maze[j, i] == 'a':
                # Append to starting nodes
                starts.append((j, i))

    # Run A* algorithm with all starting nodes
    path = astar(maze, starts, end)

    # Return length of the path = steps
    return len(path) - 1


def main():
    maze, start, end = get_input()
    print('The fewest steps to move from your current position to the location is:', part_one(maze, [start], end))
    print('The fewest steps to move from any square with elevation "a" to the location is:', part_two(maze, start, end))


if __name__ == '__main__':
    main()
