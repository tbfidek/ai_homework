import copy

# generates domains for each cell 
def generate_domains(grid):
    domains = []

    for i in range(len(grid)):
        row_domains = []
        for j in range(len(grid[i])):
            if grid[i][j] == 0:
                row_domains.append([1, 2, 3, 4, 5, 6, 7, 8, 9])
            elif grid[i][j] == -1:
                row_domains.append([2, 4, 6, 8])
            else:
                row_domains.append([grid[i][j]])
        domains.append(row_domains)

    return domains


# checks if the board is full
def isComplete(board):
    for row in board:
        if 0 in row or -1 in row:
            return False
    return True


# checks if the move is valid
def possible(board, row, column, number):

    # checks if number exists in the same row or column
    if number in board[row] or number in [board[i][column] for i in range(9)]:
        return False

    # checks if number exists in the same subgrid
    x0 = (column // 3) * 3
    y0 = (row // 3) * 3
    for i in range(3):
        for j in range(3):
            if board[y0 + i][x0 + j] == number:
                return False

    return True


# updates the domains for all peers when a move is made
def update_domains_FC(domains, row, col, value):

    # updates domain for current piece
    domains[row][col] = [value]

    # updates domain for peers in the same column
    for c in range(9):
        if c != col and value in domains[row][c]:
            domains[row][c].remove(value)

    # updates domain for peers in the same row 
    for r in range(9):
        if r != row and value in domains[r][col]:
            domains[r][col].remove(value)

    # updates domain for peers in the same subgrid
    box_row, box_col = 3 * (row // 3), 3 * (col // 3)
    for r in range(box_row, box_row + 3):
        for c in range(box_col, box_col + 3):
            if (r != row or c != col) and value in domains[r][c]:
                domains[r][c].remove(value)

    return domains


# finds the next piece which is a 0 or -1
def find_unassigned_variables(board):
    unassigned_variables = []  # store unassigned variables as (row, col) pairs.
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0 or board[row][col] == -1:
                unassigned_variables.append((row, col))
    return unassigned_variables


# returns row and col index for the next empty cell
def next_unassigned_variable(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0 or board[row][col] == -1:
                return row, col
    return None, None


# forward checking backtracking
def fwd_checking(board, domains):

    if isComplete(board):
        return board

    row, col = next_unassigned_variable(board)
    
    if row is not None and col is not None:
        for value in domains[row][col]:
            if possible(board, row, col, value):
                # keep the empty cell value for backtracking purposes
                old_value = board[row][col]
                # update the empty cell with a value
                board[row][col] = value
                # keep the domain values for backtracking purposes
                domains_copy = copy.deepcopy(domains)
                updated_domains = update_domains_FC(domains_copy, row, col, value)
                # checks if any empty cells no longer have values in their domain => backtracking required
                if not any(len(updated_domains[r][c]) == 0 for r, c in find_unassigned_variables(board)):
                    result = fwd_checking(board, updated_domains)
                    if result:
                        return result
                board[row][col] = old_value  # backtrack if necessary

    return None


if __name__ == "__main__":

    grid = [[8, 4, 0, 0, 5, 0, -1, 0, 0],
            [3, 0, 0, 6, 0, 8, 0, 4, 0],
            [0, 0, -1, 4, 0, 9, 0, 0, -1],
            [0, 2, 3, 0, -1, 0, 9, 8, 0],
            [1, 0, 0, -1, 0, -1, 0, 0, 4],
            [0, 9, 8, 0, -1, 0, 1, 6, 0],
            [-1, 0, 0, 5, 0, 3, -1, 0, 0],
            [0, 3, 0, 1, 0, 6, 0, 0, 7],
            [0, 0, -1, 0, 2, 0, 0, 1, 3]]

    domains = generate_domains(grid)
    result = fwd_checking(grid, domains)

    if result:
        for row in result:
            print(row)
    else:
        print("no solution found")
