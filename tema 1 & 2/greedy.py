from puzzle import init_state, is_final_state, find_empty_cell, can_move, move_cell, move
import numpy as np
import heapq
import time

directions = ['up', 'down', 'right', 'left']


# sums the horizontal and vertical distances of each tile from its goal position
# measures the number of moves needed to place each tile in its correct spot
def manhattan_distance(state):
    goal = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])

    total_distance = 0

    for i in range(3):
        for j in range(3):
            current_tile = state[0][i, j]
            if current_tile != 0:
                goal_row, goal_col = divmod(current_tile - 1, 3)
                horizontal_distance = abs(j - goal_col)
                vertical_distance = abs(i - goal_row)
                total_distance += horizontal_distance + vertical_distance

    return total_distance


# counts the number of tiles that are not in their goal positions 
def hamming_distance(state):
    goal = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
    return sum(current_tile != goal_tile for current_tile, goal_tile in zip(state[0].flatten(), goal.flatten()) if current_tile != 0)


# tile positions become points with coordinates 
# calculates the  straight line distance between current & goal
def euclidean_distance(state):
    goal = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
    return sum(np.sqrt((current_tile % 3 - goal_tile % 3) ** 2 + (current_tile // 3 - goal_tile // 3) ** 2)
               for i in range(3) for j in range(3)
               for current_tile, goal_tile in ((state[0][i,j], goal[i,j]),) if state[0][i,j] != 0)


# finds the maximum of the horizontal and vertical distances of each tile from its goal position
def chebyshev_distance(state):
    goal = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
    return max(abs(current_tile % 3 - goal_tile % 3) + abs(current_tile // 3 - goal_tile // 3)
               for i in range(3) for j in range(3)
               for current_tile, goal_tile in ((state[0][i, j], goal[i, j]),) if state[0][i, j] != 0)


def greedy(init_state, heuristic):
    pq = []
    moves_count = 0
    init_state_hashable = (tuple(map(tuple, init_state[0])), init_state[1], init_state[2])
    heapq.heappush(pq, (heuristic(init_state), init_state_hashable))
    visited = {init_state_hashable}

    while pq:
        _, state_hashable = heapq.heappop(pq)
        state = (np.array(state_hashable[0]), state_hashable[1], state_hashable[2])

        if is_final_state(state[0]):
            return state, moves_count

        for direction in directions:
            neighbor = move(state, direction)
            if neighbor:
                neighbor_hashable = (tuple(map(tuple, neighbor[0])), neighbor[1], neighbor[2])
                if neighbor_hashable not in visited:
                    heapq.heappush(pq, (heuristic(neighbor), neighbor_hashable))
                    visited.add(neighbor_hashable)
                    moves_count += 1

    return None


if __name__ == "__main__":
    initial_board = list(map(int, input("Please enter a list of numbers separated by comma: ").split(',')))
    # 2, 7, 5, 0, 8, 4, 3, 1, 6 - exemplu de input
    # 8, 6, 7, 2, 5, 4, 0, 3, 1
    # 2, 5, 3, 1, 0, 6, 4, 7, 8
    directions = ['up', 'down', 'right', 'left']

    start = time.time()
    initial_state = init_state(initial_board)
    solution = greedy(initial_state, chebyshev_distance)
    end = time.time()

    if solution is not None:
        print("found solution in", end - start, "seconds:")
        for step in solution[0]:
            print(step)
    else:
        print("can't find solution")
