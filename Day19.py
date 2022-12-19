import re
from collections import deque


# Get data from .txt file
def get_input():
    with open('input/Day19.txt', 'r') as file:
        # Initialize variable
        blueprints = []
        # Read each line and apply regex
        for a, b, c, d, e, f, g in re.findall(r'\D+(\d+)\D+(\d+)\D+(\d+)\D+(\d+)\D+(\d+)\D+(\d+)\D+(\d+)', file.read(),
                                              re.MULTILINE):
            blueprints.append((int(a), int(b), int(c), int(d), int(e), int(f), int(g)))
    return blueprints


# Calculate blueprint output
def calc_blueprint(blueprint: tuple, timer: int) -> int:
    # Initialize variables, m are materials, r are robots, rcm are costs, t is time left
    m1 = m2 = m3 = m4 = 0
    r1 = 1
    r2 = r3 = r4 = 0
    a, r1cm1, r2cm1, r3cm1, r3cm2, r4cm1, r4cm3 = blueprint
    t = timer
    # Create deque
    outcomes_deque = deque([(m1, m2, m3, m4, r1, r2, r3, r4, t)])
    visited_outcomes = set()
    max_geode = 0

    # Maximum number of robots that should be built of any kind to produce enough material in one round to any other one
    max_robots = [max(r1cm1, r2cm1, r3cm1, r4cm1), r3cm2, r4cm3]

    # While there are still outcomes, keep checking
    while len(outcomes_deque) > 0:
        # Pop next outcome (use pop() not popleft() to get a first results as quickly as possible to make use of the
        # max_geode comparison later)
        outcome = outcomes_deque.pop()

        # If we already saw this outcome before, continue
        if outcome in visited_outcomes:
            continue
        # Otherwise, add it to the visited outcomes and proceed
        visited_outcomes.add(outcome)

        # Unpack
        m1, m2, m3, m4, r1, r2, r3, r4, t = outcome

        # Check if we reached the time limit
        if t == 0:
            # If yes, add the results to the blueprint if it is higher than the current one and continue
            max_geode = max(max_geode, m4)
            continue
        # Otherwise check potential next outcomes and add those to the deque
        else:
            # Check if there is still a chance to reach the current best: We calculate the best possible outcome, which
            # is a Gauss sum of time left + time left * the r4 robots that already exist + the already existing geodes
            if ((t + 1) * t / 2) + t * r4 + m4 > max_geode:
                # Do nothing (only if it is still worth waiting, which is if we actually are still saving for a
                # robot, otherwise it is better to just produce them and waiting is not an outcome)
                if m1 < max(r1cm1, r2cm1, r3cm1, r4cm1) or m2 < r3cm2 or m3 < r4cm3:
                    outcomes_deque.append((m1 + r1, m2 + r2, m3 + r3, m4 + r4, r1, r2, r3, r4, t - 1))
                # Create ore robot if we have enough material and haven't reached the robot limit
                if m1 >= r1cm1 and r1 < max_robots[0]:
                    outcomes_deque.append((m1 + r1 - r1cm1, m2 + r2, m3 + r3, m4 + r4, r1 + 1, r2, r3, r4, t - 1))
                # Create clay robot if we have enough material and haven't reached the robot limit
                if m1 >= r2cm1 and r2 < max_robots[1]:
                    outcomes_deque.append((m1 + r1 - r2cm1, m2 + r2, m3 + r3, m4 + r4, r1, r2 + 1, r3, r4, t - 1))
                # Create obsidian robot if we have enough material and haven't reached the robot limit
                if m1 >= r3cm1 and m2 >= r3cm2 and r3 < max_robots[2]:
                    outcomes_deque.append((m1 + r1 - r3cm1, m2 + r2 - r3cm2, m3 + r3, m4 + r4, r1, r2, r3 + 1, r4, t - 1))
                # Create geode robot if we have enough material (no robot limit on the geode robot)
                if m1 >= r4cm1 and m3 >= r4cm3:
                    outcomes_deque.append((m1 + r1 - r4cm1, m2 + r2, m3 + r3 - r4cm3, m4 + r4, r1, r2, r3, r4 + 1, t - 1))
            else:
                continue
    return max_geode


# Solves part 1
def part_one(blueprints: list, timer: int) -> int:
    # Initialize variables
    blueprint_results = [0] * len(blueprints)
    print('Calculating part 1, each update will take a few seconds per blueprint...', end='')
    for i, blueprint in enumerate(blueprints):
        # Calculate result calling the function
        blueprint_results[i] = (i + 1) * calc_blueprint(blueprint, timer)
        print(f'\rThe result for blueprint {i + 1} is: {blueprint_results[i] // (i + 1)}', end='')

    # Sum the results and return them
    return sum(blueprint_results)


# Solves part 2
def part_two(blueprints: list, timer: int) -> int:
    # Only the top 3 blueprints
    blueprints = blueprints[:3]
    # Initialize variables
    blueprint_results = [0] * len(blueprints)
    print('Calculating part 2, each update will take a few seconds per blueprint...', end='')
    for i, blueprint in enumerate(blueprints):
        # Calculate result calling the function
        blueprint_results[i] = calc_blueprint(blueprint, timer)
        print(f'\rThe result for blueprint {i + 1} is: {blueprint_results[i]}', end='')

    return blueprint_results[0] * blueprint_results[1] * blueprint_results[2]


def main():
    print('\rIf you add up the quality level of all the blueprints, you get:', part_one(get_input(), 24))
    print('\rIf you multiply the resulting numbers together, you get:', part_two(get_input(), 32))


if __name__ == '__main__':
    main()

