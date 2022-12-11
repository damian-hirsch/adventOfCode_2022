# Get data from .txt file
def get_input():
    with open('input/Day11.txt', 'r') as file:
        # Split lines and write each line to list
        data = file.read().splitlines()
        # Initialize monkey list
        monkeys = []
        # Loop through all lines
        for i, line in enumerate(data):
            # Check what line type we have and act on it
            match i % 7:
                # Monkey
                case 0:
                    pass
                # Items line
                case 1:
                    items = line[18:].split(', ')
                    items = list(map(int, items))
                # Operator
                case 2:
                    operator = line[23]
                    operator_number = line[25:]
                    if operator_number == 'old':
                        operator = '**'
                        operator_number = 2
                    else:
                        operator_number = int(operator_number)
                # Divisor
                case 3:
                    div = int(line[21:])
                # Throw true
                case 4:
                    throw_true = int(line[29:])
                # Throw false
                case 5:
                    throw_false = int(line[30:])
                # Space, create monkey
                case 6:
                    monkey = Monkey(items, operator, operator_number, div, throw_true, throw_false)
                    monkeys.append(monkey)
        # Create last monkey
        monkey = Monkey(items, operator, operator_number, div, throw_true, throw_false)
        monkeys.append(monkey)

    return monkeys


class Monkey:
    # Initialize values
    def __init__(self, items: list, operator: str, operator_number: int, div: int, throw_true: int, throw_false: int):
        # Items the monkey holds
        self.items = items
        # The operator it uses
        self.operator = operator
        # The operator number
        self.operator_number = operator_number
        # Divisor
        self.div = div
        # To which monkey it throws it if true
        self.throw_true = throw_true
        # To which monkey it throws if false
        self.throw_false = throw_false
        # How many items were inspected
        self.inspected = 0

    # Receive an item
    def add_item(self, item):
        self.items.append(item)

    # Inspect the item and throw it
    def throw_item(self, mod=None) -> tuple[int, int]:
        # Increase inspected item number
        self.inspected += 1
        # Get next item from list
        item = self.items.pop(0)
        # Match the operator
        match self.operator:
            case '*':
                item = (item * self.operator_number)
            case '+':
                item = (item + self.operator_number)
            case '**':
                item = (item ** self.operator_number)
        # Check if we have a mod, none is part 1, with one is part 2
        if mod is None:
            # Divide worry level by 3
            item //= 3
        else:
            # Reduce item size based on mod
            item %= mod
        # Check divisor and throw item to new monkey
        if item % self.div == 0:
            return item, self.throw_true
        else:
            return item, self.throw_false


# Solves part 1
def part_one(monkeys: list[Monkey], total_rounds: int) -> int:
    # Loop through all rounds
    for _ in range(total_rounds):
        # Loop through each monkey
        for monkey in monkeys:
            # While a monkey still has items
            while monkey.items:
                # Inspect and throw the item
                item, target_monkey = monkey.throw_item()
                # Add item to next monkey
                monkeys[target_monkey].add_item(item)

    # Initialize inspected items list
    inspected = []
    # Go through each monkey and get how man inspected items they have
    for monkey in monkeys:
        inspected.append(monkey.inspected)
    # Sort the list
    inspected.sort()
    # Calculate score based on two highest values
    monkey_business = inspected[-1] * inspected[-2]
    return monkey_business


# Solves part 2
def part_two(monkeys: list[Monkey], total_rounds: int) -> int:
    # Initialize and calculate mod for number reduction based on all monkey divisors
    mod = 1
    for monkey in monkeys:
        mod *= monkey.div

    # Loop through all rounds
    for _ in range(total_rounds):
        # Loop through each monkey
        for monkey in monkeys:
            # While a monkey still has items
            while monkey.items:
                # Inspect and throw the item
                item, target_monkey = monkey.throw_item(mod)
                # Add item to next monkey
                monkeys[target_monkey].add_item(item)

    # Initialize inspected items list
    inspected = []
    # Go through each monkey and get how man inspected items they have
    for monkey in monkeys:
        inspected.append(monkey.inspected)
    # Sort the list
    inspected.sort()
    # Calculate score based on two highest values
    monkey_business = inspected[-1] * inspected[-2]
    return monkey_business


def main():
    print('The level of monkey business after 20 rounds is:', part_one(get_input(), 20))
    print('The level of monkey business after 10000 rounds is:', part_two(get_input(), 10_000))


if __name__ == '__main__':
    main()
