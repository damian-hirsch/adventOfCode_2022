from collections import deque
import sympy


# Get data from .txt file
def get_input() -> list:
    with open('input/Day21.txt', 'r') as file:
        # Split lines and write each line to list
        data = file.read().splitlines()
    return data


# Calculates what the monkeys will yell
def calc_monkeys(numb_dict: dict, monkey: deque) -> dict:
    # While we still have unknown monkeys left
    while len(monkey) > 0:
        # Get the operations of that monkey
        name, val1, operation, val2 = monkey.pop()
        # Check if we already know the attributes it needs, if yes, update
        try:
            match operation:
                case '+':
                    numb_dict[name] = numb_dict[val1] + numb_dict[val2]
                case '-':
                    numb_dict[name] = numb_dict[val1] - numb_dict[val2]
                case '*':
                    numb_dict[name] = numb_dict[val1] * numb_dict[val2]
                case '/':
                    numb_dict[name] = numb_dict[val1] / numb_dict[val2]
        # Otherwise, add it back at the bottom of the deck
        except KeyError:
            monkey.appendleft((name, val1, operation, val2))
    return numb_dict


# Solves part 1
def part_one(data: list) -> int:
    # Initialize dictionary with all numbers and a deque of math monkeys
    numb_dict = {}
    monkey = deque([])
    # For each line
    for line in data:
        # Try to update the dictionary with an integer
        try:
            numb_dict[line[:4]] = int(line[6:])
        # If not possible, it's a math monkey and add it to deque
        except ValueError:
            monkey.append((line[:4], line[6:10], line[11], line[13:]))
    # Get the full number dictionary by analyzing the math monkeys in the deque
    numb_dict = calc_monkeys(numb_dict, monkey)
    # Return the result for 'root'
    return int(numb_dict['root'])


# Solves part 2
def part_two(data: list) -> int:
    # Initialize dictionary with all numbers and a deque of math monkeys
    numb_dict = {}
    monkey = deque([])
    # For each line
    for line in data:
        # Check if it is the human line
        if line[:4] == 'humn':
            # Initialize it as variable we want to solve for
            numb_dict[line[:4]] = sympy.Symbol('x')
        elif line[:4] == 'root':
            # If it is root, change the operation -> we want to solve that root1 - root2 = 0 (they are equal)
            monkey.append((line[:4], line[6:10], '-', line[13:]))
        else:
            # Try to update the dictionary with an integer
            try:
                numb_dict[line[:4]] = sympy.Integer(line[6:])
            # If not possible, it's a math monkey and add it to deque
            except ValueError:
                monkey.append((line[:4], line[6:10], line[11], line[13:]))
    # Get the full number dictionary by analyzing the math monkeys in the deque
    numb_dict = calc_monkeys(numb_dict, monkey)
    # Solve for the root monkey number to be equal and return x (the human number) that fulfills this
    return sympy.solve(sympy.Eq(numb_dict['root'], 0))[0]


def main():
    print('The monkey named root yells:', part_one(get_input()))
    print('To pass root''s equality test you need to yell:', part_two(get_input()))


if __name__ == '__main__':
    main()
