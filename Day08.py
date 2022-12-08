import numpy as np


# Get data from .txt file
def get_input() -> np.ndarray:
    with open('input/Day08.txt', 'r') as file:
        # Split lines and write each line to list
        data = file.read().splitlines()

        # Create numpy array
        # Get x and y
        y = len(data)
        x = len(data[0])
        # Initialize array
        trees = np.zeros((y, x), dtype=int)
        for i, line in enumerate(data):
            # Convert strings to lines of array
            trees[i, :] = np.fromiter(line, dtype=int)
    return trees


# Solves part 1
def part_one(trees: np.ndarray) -> int:
    # Get array shape
    y, x = trees.shape
    # Initialize count (include the trees around)
    count = 2 * (x - 1 + y - 1)
    # Go through all centered trees
    for j in range(1, y - 1):
        for i in range(1, x - 1):
            # Check trees toward the top, right, bottom, left
            top = trees[j, i] > trees[:j, i]
            right = trees[j, i] > trees[j, i+1:]
            bottom = trees[j, i] > trees[j+1:, i]
            left = trees[j, i] > trees[j, :i]
            # Check if on any side there is a view of the tree
            if np.all(top) or np.all(right) or np.all(bottom) or np.all(left):
                count += 1
    return count


# Solves part 2
def part_two(trees: np.ndarray) -> int:
    # Get array shape
    y, x = trees.shape
    # Initialize scenic score
    scenic_score = 0
    # Go through all centered trees, edge trees have automatically a scenic score of 0
    for j in range(1, y - 1):
        for i in range(1, x - 1):
            # Check top
            # Initialize variables
            top = 0
            # Check which trees are larger and convert to array
            top_trees = np.asarray(trees[j, i] > trees[:j, i])
            # Reverse the order because we look bottom up
            top_trees = top_trees[::-1]
            # Go through the array and check how many tries we can see
            for k in range(len(top_trees)):
                # If tree is smaller, add it
                if top_trees[k]:
                    top += 1
                # Else, add last tree and break
                else:
                    top += 1
                    break

            # Check right
            # Initialize variables
            right = 0
            # Check which trees are larger and convert to array
            right_trees = np.asarray(trees[j, i] > trees[j, i+1:])
            # Go through the array and check how many tries we can see
            for k in range(len(right_trees)):
                # If tree is smaller, add it
                if right_trees[k]:
                    right += 1
                # Else, add last tree and break
                else:
                    right += 1
                    break

            # Check bottom
            # Initialize variables
            bottom = 0
            # Check which trees are larger and convert to array
            bottom_trees = np.asarray(trees[j, i] > trees[j+1:, i])
            # Go through the array and check how many tries we can see
            for k in range(len(bottom_trees)):
                # If tree is smaller, add it
                if bottom_trees[k]:
                    bottom += 1
                # Else, add last tree and break
                else:
                    bottom += 1
                    break

            # Check left
            # Initialize variables
            left = 0
            # Check which trees are larger and convert to array
            left_trees = np.asarray(trees[j, i] > trees[j, :i])
            # Reverse the order because we look from right to left
            left_trees = left_trees[::-1]
            # Go through the array and check how many tries we can see
            for k in range(len(left_trees)):
                # If tree is smaller, add it
                if left_trees[k]:
                    left += 1
                # Else, add last tree and break
                else:
                    left += 1
                    break

            # Check if the new score is bigger than the current score, if yes, replace it
            if top * right * bottom * left > scenic_score:
                scenic_score = top * right * bottom * left

    return scenic_score


def main():

    print('This many trees are visible from outside the grid:', part_one(get_input()))
    print('The highest scenic score possible for any tree is:', part_two(get_input()))


if __name__ == '__main__':
    main()
