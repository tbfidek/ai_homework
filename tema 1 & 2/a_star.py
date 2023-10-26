import numpy as np
from greedy import manhattan_distance, chebyshev_distance, hamming_distance, euclidean_distance
from puzzle import init_state, is_final_state, find_empty_cell, can_move, move_cell, move
import heapq

directions = ['up', 'down', 'right', 'left']


def is_valid(state):
    i, j = find_empty_cell(state[0])

    if can_move(state, "up"):
        new_i, new_j = i - 1, j
        if state[0][new_i, new_j] == 0:
            return False

    if can_move(state, "down"):
        new_i, new_j = i + 1, j
        if state[0][new_i, new_j] == 0:
            return False

    if can_move(state, "left"):
        new_i, new_j = i, j - 1
        if state[0][new_i, new_j] == 0:
            return False

    if can_move(state, "right"):
        new_i, new_j = i, j + 1
        if state[0][new_i, new_j] == 0:
            return False

    return True


# heuristic that checks the distance between current state and final state with manhattan
def h(state):
    distance = 0
    for i in range(3):
        for j in range(3):
            tile = state[0][i, j]
            if tile != 0:
                goal_row, goal_col = divmod(tile - 1, 3)
                distance += min(
                    abs(i - goal_row) + abs(j - goal_col),
                    abs(i - goal_row) + abs(j - goal_col - 1),
                    abs(i - goal_row) + abs(j - goal_col + 1),
                    abs(i - goal_row - 1) + abs(j - goal_col),
                    abs(i - goal_row + 1) + abs(j - goal_col)
                )
    return distance


# manhattan heuristic to check distance between state and neighbor
def dist(state,neighbor):
    distance = 0
    for i in range(3):
        for j in range(3):
            tile = state[0][i, j]
            if tile != 0:
                goal_row, goal_col = divmod(tile - 1, 3)
                distance += abs(i - goal_row) + abs(j - goal_col)
    return distance


def a_star(initial_state):
    came_from = {}
    d = {}  # distance from initial state to current
    initial_state_hashable = tuple(map(tuple, initial_state[0]))
    d[initial_state_hashable] = 0
    f = {initial_state_hashable: h(initial_state)}
    pq = []

    heapq.heappush(pq, (f[initial_state_hashable], initial_state_hashable))

    while pq:
        _, state_hashable = heapq.heappop(pq)
        state = (np.array(state_hashable), state_hashable[1], state_hashable[2])

        if is_final_state(state[0]):
            return reconstruct_path(state_hashable, came_from)

        for direction in directions:
            neighbor = move(state, direction)
            if neighbor:
                neighbor_hashable = tuple(map(tuple, neighbor[0]))
                if neighbor_hashable not in d or d[neighbor_hashable] > d[state_hashable] + dist(state,neighbor):
                    d[neighbor_hashable] = d[state_hashable] + dist(state, neighbor)
                    f[neighbor_hashable] = d[neighbor_hashable] + h(neighbor)
                    came_from[neighbor_hashable] = state_hashable
                    heapq.heappush(pq, (f[neighbor_hashable], neighbor_hashable))

    return None


def reconstruct_path(state_hashable, came_from):
    path = [state_hashable]
    while state_hashable in came_from:
        state_hashable = came_from[state_hashable]
        path.append(state_hashable)
    return list(reversed(path))


if __name__ == "__main__":
    initial_board = list(map(int, input("Please enter a list of numbers separated by comma: ").split(',')))
    # 2, 7, 5, 0, 8, 4, 3, 1, 6 - exemplu de input
    # 8, 6, 7, 2, 5, 4, 0, 3, 1
    # 2, 5, 3, 1, 0, 6, 4, 7, 8
    directions = ['up', 'down', 'right', 'left']

    initial_state = init_state(initial_board)
    solution = a_star(initial_state)

    if solution is not None:
        print("Found solution:")
        for step in solution[-1]:
            print(step)
    else:
        print("Can't find a solution.")
