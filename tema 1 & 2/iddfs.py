from puzzle import init_state, is_final_state, find_empty_cell, can_move, move_cell, move
import time


def iddfs(initial_state, max_depth=50):
    for depth in range(0, max_depth):
        visited = []
        result = dls(initial_state, max_depth, visited)
        if result is not None:
            return result
    return None


def dls(state, max_depth, visited):
    if is_final_state(state[0]):
        return state
    if max_depth == 0:
        return None
    visited.append(state[0].tolist())
    for direction in directions:
        new_state = move(state, direction)
        if new_state is not None and new_state[0].tolist() not in visited:
            result = dls(new_state, max_depth - 1, visited)
            if result is not None:
                return result
    return None


if __name__ == "__main__":
    initial_board = list(map(int, input("Please enter a list of numbers separated by comma: ").split(',')))
    # 7, 6, 8, 4, 0, 2, 5, 3, 1 - exemplu de input
    # 8, 6, 7, 2, 5, 4, 0, 3, 1
    # 2, 5, 3, 1, 0, 6, 4, 7, 8
    directions = ['up', 'down', 'right', 'left']

    start = time.time()
    initial_state = init_state(initial_board)
    solution= iddfs(initial_state)
    end = time.time()

    if solution is not None:
        print("found solution in", end - start, "seconds:")
        for step in solution[0]:
            print(step)
    else:
        print("can't find solution")