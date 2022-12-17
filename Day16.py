import numpy as np
import re
from functools import lru_cache


# Get data from .txt file
def get_input() -> (np.ndarray, list, dict):
    with open('input/Day16.txt', 'r') as file:
        # Split lines and write each line to list
        data = file.read().splitlines()

        # Initialize variables
        valve_dict = dict()
        flow_rate = []
        connecting_valves = []

        # Loop through all lines and retrieve info
        for i, line in enumerate(data):
            # Get valve name
            valve_dict[line[6:8]] = i
            # Get valve flow rate
            flow_rate.append(int(re.search(r'(\d+)', line).group(1)))
            # Get connecting valves
            connecting_valves.append(re.search(r'to valve.\s*(.+)', line).group(1))

        # Create adjacent map
        adj_map = np.zeros((len(data), len(data)), dtype=int)
        # Loop through all valves and define their connection
        for i, valves in enumerate(connecting_valves):
            valves = valves.split(', ')
            for valve in valves:
                adj_map[i, valve_dict[valve]] = 1
    return adj_map, np.asarray(flow_rate, dtype=int), valve_dict


# Source: https://stackoverflow.com/questions/32164012/how-to-get-distance-matrix-from-adjacency-matrix-matlab
def adj_to_dist(adj_mat: np.ndarray, cost=1) -> np.ndarray:
    """
    This algorithm converts an adjacency matrix to a distance matrix using matrix properties
    Adjacency matrix: Matrix where the cost of only directly connected nodes is shown and the others are 0
    Distance matrix: Matrix where the cost to each node, potentially over multiple other nodes, is shown
    """

    # Initialize distance matrix
    distance_mat = np.empty((adj_mat.shape[0], adj_mat.shape[1]))
    distance_mat[:] = np.nan
    # Initialize helper matrix
    helper_mat = adj_mat

    # Check if there are still non-visited nodes
    while np.isnan(distance_mat[:]).any():
        # Check for new walks and assign distance
        distance_mat[np.where((helper_mat > 0) & (np.isnan(distance_mat)))] = cost

        # Update for next step
        cost += 1
        helper_mat = np.matmul(helper_mat, adj_mat)

    # Reset diagonals
    np.fill_diagonal(distance_mat, 0)
    return distance_mat


def calc_pressure(i: int, t_left: int, indices: set, dist: np.ndarray, fr: np.ndarray) -> int:
    # Initialize released pressure
    released = 0
    # Loop through all available indices
    for j in indices:
        # Calculate projected time left when moving to that index
        projected_t = t_left - 1 - dist[i, j]
        # If that projected time is greater or equal to zero it still has use
        if projected_t >= 0:
            # Check if we already reached a higher value, otherwise sum the flow_rate of the target location
            # multiplied by its flow rate and recurse for future locations
            released = max(released, fr[j] * projected_t + calc_pressure(j, projected_t, indices - {j}, dist, fr))
    return released


# Solves part 1
def part_one(adj_map: np.ndarray, flow_rate: np.ndarray, valve_dict: dict) -> int:
    # Get distance map from adjacency map
    distance_map = adj_to_dist(adj_map).astype(dtype=int)

    # All distances that have a flow rate of 0 are irrelevant, expect the AA one (starting position)
    # Find 'AA'
    idx_start = valve_dict['AA']
    # Find all zeros
    no_flow_idx = set(np.where(flow_rate == 0)[0])
    # Remove 'AA'
    no_flow_idx = list(no_flow_idx - {idx_start})
    # Delete those selected
    distance_map = np.delete(distance_map, no_flow_idx, 0)  # Rows
    distance_map = np.delete(distance_map, no_flow_idx, 1)  # Columns
    flow_rate = np.delete(flow_rate, no_flow_idx)
    # Find 'AA' again in the new setup
    idx_start = int(np.where(flow_rate == 0)[0])
    # Initialize set of indices that should be searched
    indices = set(range(0, len(distance_map))) - {idx_start}
    # Calculate max released pressure
    max_released = calc_pressure(idx_start, 30, indices, distance_map, flow_rate)

    return max_released


# Solves part 2
def part_two(adj_map: np.ndarray, flow_rate: np.ndarray, valve_dict: dict) -> int:
    # Get distance map from adjacency map
    distance_map = adj_to_dist(adj_map).astype(dtype=int)

    # All distances that have a flow rate of 0 are irrelevant, expect the AA one (starting position)
    # Find 'AA'
    idx_start = valve_dict['AA']
    # Find all zero flow rates
    no_flow_idx = set(np.where(flow_rate == 0)[0])
    # Remove 'AA' from the exclusion set
    no_flow_idx = list(no_flow_idx - {idx_start})
    # Delete the no flow entries
    distance_map = np.delete(distance_map, no_flow_idx, 0)  # Rows
    distance_map = np.delete(distance_map, no_flow_idx, 1)  # Columns
    flow_rate = np.delete(flow_rate, no_flow_idx)

    # Find 'AA' again in the new setup for the starting position
    idx_start = int(np.where(flow_rate == 0)[0])
    # Initialize set of indices that should be searched (all left indices minus the starting index)
    indices = set(range(0, len(distance_map))) - {idx_start}

    # Because we cannot hash numpy arrays, we will add the function within the main function. Hence, the numpy
    # arrays, which are "libraries" anyway, are known already and don't need to be hashed
    @lru_cache(maxsize=None)
    def calc_pressure_part2(current_index: int, t_left: int, index_set: frozenset, elephant: bool) -> int:
        # Initialize released pressure
        # If this pass is after the elephant, we start what it already released, otherwise we start at 0 as usual
        if elephant:
            released = calc_pressure_part2(idx_start, 26, index_set, False)
        else:
            released = 0
        # Loop through all available indices
        for j in index_set:
            # Calculate projected time left when moving to that index
            projected_t = t_left - 1 - distance_map[current_index, j]
            # If that projected time is greater or equal to zero it still has use
            if projected_t >= 0:
                # Check if we already reached a higher value, otherwise sum the flow_rate of the target location
                # multiplied by its flow rate and recurse for future locations
                released = max(released,
                               flow_rate[j] * projected_t + calc_pressure_part2(j, projected_t, index_set - {j},
                                                                                elephant))
        return released

    # Let the elephant go
    return calc_pressure_part2(idx_start, 26, frozenset(indices), True)


def main():
    adj_map, flow_rate, valve_dict = get_input()
    print('The most pressure you can release is:', part_one(adj_map, flow_rate, valve_dict))
    print('The most pressure you can release with an elephant is:', part_two(adj_map, flow_rate, valve_dict))


if __name__ == '__main__':
    main()
