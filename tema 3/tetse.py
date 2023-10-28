# Define the 9x9 grid
# cod smecher in care nu avem fwd_backtracking ci doar backtracking ca la saraci si merge!!! [ dar profei nu o sa i pese]
grid = [[8, 4, 0, 0, 5, 0, 0, 0, 0],
        [3, 0, 0, 6, 0, 8, 0, 4, 0],
        [0, 0, 0, 4, 0, 9, 0, 0, 0],
        [0, 2, 3, 0, 0, 0, 9, 8, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 4],
        [0, 9, 8, 0, 0, 0, 1, 6, 0],
        [0, 0, 0, 5, 0, 3, 0, 0, 0],
        [0, 3, 0, 1, 0, 6, 0, 0, 7],
        [0, 0, 0, 0, 2, 0, 0, 1, 3]]

# Define a function to print the grid
def print_grid(grid):
    for row in grid:
        print(row)

# Define a function to solve the Sudoku puzzle
def solve_sudoku(grid):
    def is_valid(x, y, num):
        # Check if the number is not in the same row or column
        for i in range(9):
            if grid[x][i] == num or grid[i][y] == num:
                return False
        
        # Check if the number is not in the same 3x3 sub-grid
        start_x, start_y = 3 * (x // 3), 3 * (y // 3)
        for i in range(3):
            for j in range(3):
                if grid[start_x + i][start_y + j] == num:
                    return False
        
        return True

    def backtrack():
        for x in range(9):
            for y in range(9):
                if grid[x][y] == 0:
                    for num in range(1, 10):
                        if is_valid(x, y, num):
                            grid[x][y] = num
                            if backtrack():
                                return True
                            grid[x][y] = 0
                    return False
        return True

    if backtrack():
        print("Solution found:")
        print_grid(grid)
    else:
        print("No solution exists for the given Sudoku puzzle.")

# Solve the Sudoku puzzle
solve_sudoku(grid)
