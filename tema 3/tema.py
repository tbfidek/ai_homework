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


def mrv(board, domains):
    if isComplete(board):
        return board

    unassigned_vars = find_unassigned_variables(board)

    if not unassigned_vars:
        return board

    # choose the min from unnassigned_var
    row, col = min(unassigned_vars, key=lambda var: len(domains[var[0]][var[1]]))

    for value in domains[row][col]:
        if possible(board, row, col, value):
            old_value = board[row][col]
            board[row][col] = value
            domains_copy = copy.deepcopy(domains)
            updated_domains = update_domains_FC(domains_copy, row, col, value)
            if not any(len(updated_domains[r][c]) == 0 for r, c in find_unassigned_variables(board)):
                result = fwd_checking(board, updated_domains)
                if result:
                    return result
            board[row][col] = old_value
    return None


def revise(domains, row1, col1, row2, col2):
    revised = False

    values_to_remove = []
    for value in domains[row1][col1]:
        if value not in domains[row2][col2]:
            values_to_remove.append(value)  # add values to be removed

    for value in values_to_remove:
        domains[row1][col1].remove(value)  # remove values that are not in the other domain
        revised = True

    return revised


def ac3(domains):
    queue = []

    for row1 in range(9):
        for col1 in range(9):
            if grid[row1][col1] == 0 or grid[row1][col1] == -1:
                for row2 in range(9):
                    for col2 in range(9):
                        if (row2 != row1 or col2 != col1) and (row2 == row1 or col2 == col1):
                            queue.append((row1, col1, row2, col2))  # add arcs in queue

    while queue:  # check for each arc if consistent
        row1, col1, row2, col2 = queue.pop(0)

        if revise(domains, row1, col1, row2, col2):
            if not domains[row1][col1]:
                return False

                # check the neighbours
            for row2 in range(9):
                for col2 in range(9):
                    if (row2 != row1 or col2 != col1) and (row2 != row2 or col2 != col2):
                        if (row2 == row1 or col2 == col1) or (row2 == row2 or col2 == col2):
                            queue.append((row2, col2, row1, col1))

    return True  # no inconsistency found


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

    if ac3(domains):
        if result:
            for row in result:
                print(row)
    else:
        print("no solution found")
