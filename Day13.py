import ast
import copy


# Evaluate list
def eval_list(list_left: list, list_right: list) -> int:
    # While both lists still have data, keep evaluating
    while len(list_left) > 0 and len(list_right) > 0:
        # Pop the left most item of each list
        compare_left = list_left.pop(0)
        compare_right = list_right.pop(0)

        # Check if the data types match
        # If integers, compare them
        if type(compare_left) == int and type(compare_right) == int:
            # If they are the same, continue
            if compare_left == compare_right:
                pass
            # Else return the score
            else:
                return int(compare_left < compare_right)
        # If both lists
        elif type(compare_left) == list and type(compare_right) == list:
            # Evaluate
            result = eval_list(compare_left, compare_right)
            # If the score was inconclusive, continue
            if result == -1:
                pass
            # Else return the score
            else:
                return result
        # If integer and list
        elif type(compare_left) == int and type(compare_right) == list:
            # Convert left to list and evaluate
            result = eval_list([compare_left], compare_right)
            # If the score was inconclusive, continue
            if result == -1:
                pass
            # Else return the score
            else:
                return result
        # If list and integer
        elif type(compare_left) == list and type(compare_right) == int:
            # Convert right to list and evaluate
            result = eval_list(compare_left, [compare_right])
            # If the score was inconclusive, continue
            if result == -1:
                pass
            # Else return the score
            else:
                return result

    # If the left list is empty first --> right order
    if len(list_left) == 0 and len(list_right) > 0:
        return 1
    # If the right list is empty first --> wrong order
    elif len(list_left) > 0 and len(list_right) == 0:
        return 0
    # If both lists are empty, return inconclusive result
    elif len(list_left) == 0 and len(list_right) == 0:
        return -1


# Get data from .txt file
def get_input():
    with open('input/Day13.txt', 'r') as file:
        # Split lines and write each line to list
        data = file.read().splitlines()
        # Create list of lists
        data_list = []
        # Loop through each line
        for line in data:
            # If line is not a space append it
            if line != '':
                # Use literal_eval to convert string representation of list to actual list
                data_list.append(ast.literal_eval(line))
    return data_list


# Solves part 1
def part_one(data: list) -> int:
    # Initialize sum
    sum_indices = 0
    # Take pairs of two and loop through list
    for i in range(len(data) // 2):
        # Evaluate score
        lr = eval_list(data[2 * i], data[2 * i + 1])
        # Add score to the same multiplied by the index position (if score is 0, wrong order, it won't have an effect)
        sum_indices += (i + 1) * lr
    return sum_indices


# Solves part 2
def part_two(data: list) -> int:
    # Append the two elements required
    data.append([[2]])
    data.append([[6]])

    # Initialize sorted_list
    sorted_list = []

    # Sort all list by comparing them to each other (this is an inefficient O(n**2) operation, but good enough for this)
    # For larger data sets this would need to be updated to a merge sort or alike
    while len(data) > 0:
        # Get top item
        current_highest = data[0]
        # Compare it to all other items
        for list_item in data[1:]:
            # Use our evaluation function, because we have lists in list, we need a deepcopy
            score = eval_list(copy.deepcopy(current_highest), copy.deepcopy(list_item))
            # Evaluate if the order is correct
            if score == 0:
                # Not right order, set new current_highest
                current_highest = list_item
            elif score == 1:
                # Right order, go on
                pass
        # At the end of the for loop, we now have the highest item of the remaining data, append it to the sorted_list
        sorted_list.append(current_highest)
        # Remove that entry from the data list that still needs more sorting
        data.remove(current_highest)

    # Find indices of elements [[2]] and [[6]]
    idx_2 = sorted_list.index([[2]])
    idx_6 = sorted_list.index([[6]])

    # Return the score adjusting for index base
    return (idx_2 + 1) * (idx_6 + 1)


def main():

    print('The sum of the indices of pairs in the right order is:', part_one(get_input()))
    print('The decoder key for the distress signal is:', part_two(get_input()))


if __name__ == '__main__':
    main()
