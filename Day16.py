import numpy as np
import re
from math import inf


# Get data from .txt file
def get_input() -> (np.ndarray, list, dict):
    with open('input/Day16.txt', 'r') as file:
        # Split lines and write each line to list
        data = file.read().splitlines()

        # Initialize variables
        valve_dict = dict()
        flow_rate = []
        connecting_valves = []
        # Save first valve position (starting valve)
        start_valve = data[0][6:8]
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


# Source: https://github.com/crixodia/python-dijkstra
def adj_to_dist(adj_mat: np.ndarray, start: int, end=-1):
    """
    Dijkstra algorithm to convert an adjacent matrix to a distance matrix
    """
    n = len(adj_mat)
    dist = [inf] * n
    dist[start] = adj_mat[start, start]

    sp_vertex = [False] * n

    for count in range(n - 1):
        minix = inf
        u = 0

        for v in range(len(sp_vertex)):
            if sp_vertex[v] is False and dist[v] <= minix:
                minix = dist[v]
                u = v

        sp_vertex[u] = True
        for v in range(n):
            if not(sp_vertex[v]) and adj_mat[u, v] != 0 and dist[u] + adj_mat[u, v] < dist[v]:
                dist[v] = dist[u] + adj_mat[u, v]

    return dist[end] if end >= 0 else dist


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
    # Generate distance map from adjacent map by using Dijkstra algorithm
    distance_map = np.zeros((adj_map.shape[0], adj_map.shape[1]), dtype=int)
    for i in range(len(adj_map)):
        distance_map[:, i] = np.asarray(adj_to_dist(adj_map, i), dtype=int)

    # All distances that have a flow rate of 0 are irrelevant, expect the AA one (starting position)
    # Find AA
    idx_start = valve_dict['AA']
    # Find all zeros
    no_flow_idx = set(np.where(flow_rate == 0)[0])
    # Remove AA
    no_flow_idx = list(no_flow_idx - {idx_start})
    # Delete those selected
    distance_map = np.delete(distance_map, no_flow_idx, 0)  # Rows
    distance_map = np.delete(distance_map, no_flow_idx, 1)  # Columns
    flow_rate = np.delete(flow_rate, no_flow_idx)
    # Find AA again in the new setup
    idx_start = int(np.where(flow_rate == 0)[0])
    # Initialize set of indices that should be searched
    indices = set(range(0, len(distance_map))) - {idx_start}
    # Calculate max released pressure
    max_released = calc_pressure(idx_start, 30, indices, distance_map, flow_rate)

    return max_released


def main():
    adj_map, flow_rate, valve_dict = get_input()
    print('The most pressure you can release is:', part_one(adj_map, flow_rate, valve_dict))
    # print('The most pressure you can release with an elephant is:', part_two(adj_map, flow_rate, valve_dict))


if __name__ == '__main__':
    main()
