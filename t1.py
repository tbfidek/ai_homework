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
        return (new_matrix, i, j)
    return None



def iddfs(initial_state, max_iterations):
    max_depth = 0
    iterations = 0
    while iterations < max_iterations:
        visited = set() 
        result = dls(initial_state, max_depth, visited)
        if result is not None:
            return result, iterations
        max_depth += 1
        iterations += 1

    return None, iterations


def dls(state, max_depth, visited):
    if is_final_state(state[0]):
            return state
    if max_depth == 0:
        return None
    if tuple(map(tuple, state[0])) in visited:
        return None  
    visited.add(tuple(map(tuple, state[0])))
    for direction in directions:
        new_state = move(state, direction)
        if new_state is not None:
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

    initial_state = init_state(initial_board)
    max_iterations = 100
    solution, iterations = iddfs(initial_state, max_iterations)

    if solution is not None:
        print("found solution in ", iterations, "iterations:")
        for step in solution[0]:
            print(step)
    else:
        print("can't find solution in ", iterations, "iterations.")