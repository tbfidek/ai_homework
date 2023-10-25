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

