from puzzle import init_state, is_final_state, find_empty_cell, can_move, move_cell, move
import numpy as np
import heapq
import time


def manhattan_distance(state):
    goal = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
    return sum(abs(b % 3 - g % 3) + abs(b // 3 - g // 3)
               for i in range(3) for j in range(3)
               for b, g in ((state[0][i, j], goal[i, j]),) if state[0][i, j] != 0)


def hamming_distance(state):
    goal = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
    return sum(el1 != el2 for el1, el2 in zip(state[0].flatten(), goal.flatten()) if el1 != 0 and el1 != 0)


def euclidean_distance(state):
    goal = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
    return sum(np.sqrt((b % 3 - g % 3) ** 2 + (b // 3 - g // 3) ** 2)
               for i in range(3) for j in range(3)
               for b, g in ((state[0][i,j], goal[i,j]),) if state[0][i,j] != 0)


def greedy(init_state, heuristic):
    pq = []
    init_state_hashable = (tuple(map(tuple, init_state[0])), init_state[1], init_state[2])
    heapq.heappush(pq, (heuristic(init_state), init_state_hashable))
    visited = {init_state_hashable}

    while pq:
        _, state_hashable = heapq.heappop(pq)
        state = (np.array(state_hashable[0]), state_hashable[1], state_hashable[2])

        if is_final_state(state[0]):
            return state

        for direction in directions:
            neighbor = move(state, direction)
            if neighbor:
                neighbor_hashable = (tuple(map(tuple, neighbor[0])), neighbor[1], neighbor[2])
                if neighbor_hashable not in visited:
                    heapq.heappush(pq, (heuristic(neighbor), neighbor_hashable))
                    visited.add(neighbor_hashable)

    return None


if __name__ == "__main__":
    initial_board = list(map(int, input("Please enter a list of numbers separated by comma: ").split(',')))
    # 2, 7, 5, 0, 8, 4, 3, 1, 6 - exemplu de input
    # 8, 6, 7, 2, 5, 4, 0, 3, 1
    # 2, 5, 3, 1, 0, 6, 4, 7, 8
    directions = ['up', 'down', 'right', 'left']

    start = time.time()
    initial_state = init_state(initial_board)
    solution = greedy(initial_state,euclidean_distance)
    end = time.time()

    if solution is not None:
        print("found solution in", end - start, "seconds:")
        for step in solution[0]:
            print(step)
    else:
        print("can't find solution")
