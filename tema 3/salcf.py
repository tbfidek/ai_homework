# deci basically maj functiilor sunt ok, e  o problema la update_domains_FC ptc gen cand face backtracking tre sa si dea revert la domeniile de dinainte cred 
# dar am incercat sa fac copie si tot nu merge so at this point good luck and good night girlie finna go kms

def isComplete(board):
    # Check if the Sudoku board is completely filled.
    for row in board:
        if 0 in row or -1 in row:
            return False
    return True

def possible(board, row, column, number):
    # nr appears on given row
    if number in board[row]:
        return False

    # nr appears on given column
    if number in [board[i][column] for i in range(9)]:
        return False

    # nr appears on given subgrid
    x0 = (column // 3) * 3
    y0 = (row // 3) * 3
    for i in range(3):
        for j in range(3):
            if board[y0 + i][x0 + j] == number:
                return False

    return True

def update_domains_FC(domains, row, col, value):
   
    # update the domain of the assigned variable (cell) to be only the assigned value.
    domains[row][col] = [value]

    # Update the domains of peers in the same row.
    for c in range(9):
        if c != col and value in domains[row][c]:
            domains[row][c].remove(value)

    # Update the domains of peers in the same column.
    for r in range(9):
        if r != row and value in domains[r][col]:
            domains[r][col].remove(value)

    # Update the domains of peers in the same 3x3 box.
    box_row, box_col = 3 * (row // 3), 3 * (col // 3)
    for r in range(box_row, box_row + 3):
        for c in range(box_col, box_col + 3):
            if (r != row or c != col) and value in domains[r][c]:
                domains[r][c].remove(value)

    return domains

def find_unassigned_variables(board):
    unassigned_variables = []  # List to store unassigned variables as (row, col) pairs.
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0 or board[row][col] == -1:
                unassigned_variables.append((row, col))
    return unassigned_variables

def BKT_with_FC(board, domains):
    print()
    print("i", board)
    print()
    print(domains)

    if isComplete(board):
        return board

    row, col = next_unassigned_variable(board)
    
    if row is not None and col is not None:
        for value in domains[row][col]:
            if possible(board, row, col, value):
                old_domain = domains[row][col]  #aici nu e bun (trb dat revert la toti peers cu domeniul vechi nu doar un element, am incercat asta si mi a luat foc calculatoru deci succes)
                old_value = board[row][col]
                board[row][col] = value
                updated_domains = update_domains_FC(domains, row, col, value)
                if not any(len(updated_domains[r][c]) == 0 for r, c in find_unassigned_variables(board)):
                    result = BKT_with_FC(board, updated_domains.copy())
                    if result:
                        return result
                board[row][col] = old_value  # Backtrack
                domains[row][col] = old_domain


    return None

def next_unassigned_variable(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0 or board[row][col] == -1:
                return row, col
    return None, None

# Initialize the Sudoku board and domains.
grid = [[8, 4, 0, 0, 5, 0, -1, 0, 0],
        [3, 0, 0, 6, 0, 8, 0, 4, 0],
        [0, 0, -1, 4, 0, 9, 0, 0, -1],
        [0, 2, 3, 0, -1, 0, 9, 8, 0],
        [1, 0, 0, -1, 0, -1, 0, 0, 4],
        [0, 9, 8, 0, -1, 0, 1, 6, 0],
        [-1, 0, 0, 5, 0, 3, -1, 0, 0],
        [0, 3, 0, 1, 0, 6, 0, 0, 7],
        [0, 0, -1, 0, 2, 0, 0, 1, 3]]

domains = []

for i in range(len(grid)):
    row_domains = []
    for j in range(len(grid[i])):
        if grid[i][j] == 0:
            row_domains.append([1,2,3,4,5,6,7,8,9])
        elif grid[i][j] == -1:
            row_domains.append([2,4,6,8])
        else: 
            row_domains.append([grid[i][j]])
    domains.append(row_domains)

result = BKT_with_FC(grid, domains)
if result:
    for row in result:
        print(row)
else:
    print("No solution found.")