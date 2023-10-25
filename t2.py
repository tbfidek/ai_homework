import time
import heapq
import numpy as np


# initial state
def init_state(board_as_array):
    if len(board_as_array) == 9 and set(board_as_array) == set(range(9)):
        matrix = np.array(board_as_array).reshape(3, 3)
        touple = (matrix, -1, -1)  # (matrix, row, column) = initial state, row + col of last moved piece
        return touple
    else:
        print("the array has more than 9 elements or elements which are not distinct digits lesser than 9")
        exit()


# final state
def is_final_state(board):
    board = np.array(board)
    non_zero_elements = [elem for elem in board.flat if elem != 0]
    return non_zero_elements == sorted(non_zero_elements)


# empty cell indexes
def find_empty_cell(board):
    for i in range(3):
        for j in range(3):
            if board[i, j] == 0:
                return i, j
    return None


# moves:
# up    i - 1, j
# down  i + 1, j
# left  i, j - 1
# right i, j + 1


# verify if move is valid and doesn't go outside borders, also prevents a move if neighbour(s) hasn't been moved yet
def can_move(state, direction):
    i, j = find_empty_cell(state[0])
    if direction == "up":
        return i - 1 >= 0 and (i - 1 != state[1])
    elif direction == "down":
        return i + 1 <= 2 and (i + 1 != state[1])
    elif direction == "left":
        return j - 1 >= 0 and (j - 1 != state[2])
    elif direction == "right":
        return j + 1 <= 2 and (j + 1 != state[2])
    return False


# updates the board with the moved pieces
def move_cell(board, i, j, direction):
    if direction == "up":
        board[i, j], board[i - 1, j] = board[i - 1, j], board[i, j]
    elif direction == "down":
        board[i, j], board[i + 1, j] = board[i + 1, j], board[i, j]
    elif direction == "left":
        board[i, j], board[i, j - 1] = board[i, j - 1], board[i, j]
    elif direction == "right":
        board[i, j], board[i, j + 1] = board[i, j + 1], board[i, j]
    return board


# function providing the wanted move and calls the above functions to verify the validity of and to make the move
def move(state, direction):
    i, j = find_empty_cell(state[0])
    if can_move(state, direction):
        new_matrix = move_cell(state[0].copy(), i, j, direction)
        return new_matrix, i, j
    return None



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
