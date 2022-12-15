import re


# Get data from .txt file
def get_input() -> tuple[list, list]:
    with open('input/Day15.txt', 'r') as file:
        # Split lines and write each line to list
        data = file.read().splitlines()

        # Find coordinates
        # Initialize lists
        sensors = []
        beacons = []
        # Loop through all lines
        for line in data:
            # Match numbers using regex
            re_matches = re.search(r'\D+=(-*\d+)\D+=(-*\d+)\D+=(-*\d+)\D+=(-?\d+)', line)
            a = int(re_matches.group(1))
            b = int(re_matches.group(2))
            c = int(re_matches.group(3))
            d = int(re_matches.group(4))
            # Append numbers to sensor and beacon lists
            sensors.append((a, b))
            beacons.append((c, d))
    return sensors, beacons


# Calculate Manhattan distance
def manhattan(pos1: tuple, pos2: tuple) -> int:
    # Unpack tuples
    x1, y1 = pos1
    x2, y2 = pos2

    # Calculate distance
    return abs(x1 - x2) + abs(y1 - y2)


# Adjusted from: https://leetcode.com/problems/merge-intervals/solutions/127480/merge-intervals/
def resolve_intervals(all_intervals: list[list[list]]) -> tuple[int, int]:
    # Initialize resolved intervals
    resolved_intervals = []
    # For every interval at each location
    for i, intervals in enumerate(all_intervals):
        if i % 100_000 == 0:
            print(f'\rSolving part 2: {50 + i / (len(all_intervals) - 1) * 100/2:.2f}%', end='')
        # Sort the intervals by their first entry
        intervals.sort(key=lambda x: x[0])
        # Initialize merged list
        merged = []
        # For each interval in the list of intervals
        for interval in intervals:
            # If the list of merged intervals is empty or if the current interval does not overlap with the previous,
            # simply append it. Note: Add + 1 so that [., 4], [5, .] do actually overlap.
            if not merged or merged[-1][1] + 1 < interval[0]:
                merged.append(interval)
            # Else, there is overlap, so we merge the current and previous intervals
            else:
                merged[-1][1] = max(merged[-1][1], interval[1])
        # Append the merged intervals to the resolved intervals list and resolve the next one
        resolved_intervals.append(merged)

    # Initialize positions
    x_pos, y_pos = 0, 0
    # Find the intervals that do not fully overlap, meaning there is only one entry
    for i, intervals in enumerate(resolved_intervals):
        # If we find the one, get the x and y positions and break out of the loop
        if len(intervals) > 1:
            x_pos = intervals[0][1] + 1
            y_pos = i
            break
    # Return the coordinates of the distress beacon
    return x_pos, y_pos


# Solves part 1
def part_one(data: tuple, row: int) -> int:
    # Unpack tuple
    sensors, beacons = data

    # Initialize blocked positions
    blocked = set()
    # Loop through each sensor-beacon pair and add blocked positions
    for i in range(len(sensors)):
        # Calculate Manhattan distance between sensor and beacon
        md = manhattan(sensors[i], beacons[i])
        # Check how far away we are from the row
        horizontal = abs(sensors[i][1] - row)
        # Get the distance we have left to move
        steps = md - horizontal
        # Create all blocked positions in that row
        for j in range(steps + 1):
            # Right
            blocked.add((sensors[i][0] + j, row))
            # Left
            blocked.add((sensors[i][0] - j, row))

    # Find length of the blocked spots minus the beacons that may be there
    return len(blocked - set(beacons))


# Solves part 2
def part_two(data: tuple, limit: int) -> int:
    # Unpack tuple
    sensors, beacons = data

    # Initialize blocked positions list
    blocked = [[] for _ in range(limit + 1)]

    # Loop through each sensor-beacon pair and calculate intervals
    for i in range(len(sensors)):
        print(f'\rSolving part 2: {i/(len(sensors)-1)*50:.2f}%', end='')
        # Calculate Manhattan distance between sensor and beacon
        md = manhattan(sensors[i], beacons[i])
        # Draw up all possible intervals, where the beacon could be
        for j in range(md + 1):
            reach = md - j
            y_pos_up = sensors[i][1] + j
            y_pos_dw = sensors[i][1] - j
            x1 = min(sensors[i][0] - reach, sensors[i][0] + reach)
            x2 = max(sensors[i][0] - reach, sensors[i][0] + reach)
            # Check if y_pos_up is within limits, create interval, and add it to the intervals of that y position
            if 0 <= y_pos_up <= limit:
                blocked[y_pos_up].append([max(0, x1), min(x2, limit)])
            # Check if y_pos_dw is within limits, create interval, and add it to the intervals of that y position
            if 0 <= y_pos_dw <= limit:
                blocked[y_pos_dw].append([max(0, x1), min(x2, limit)])

    # Resolve the intervals
    x, y = resolve_intervals(blocked)
    # Return the tuning frequency
    return x * 4_000_000 + y


def main():
    print('This many positions in row y=2,000,000 cannot contain a beacon:', part_one(get_input(), 2_000_000))
    print('\rThe tuning frequency of the distress beacon is:', part_two(get_input(), 4_000_000))


if __name__ == '__main__':
    main()
