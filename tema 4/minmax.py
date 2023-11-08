# define the heuristic values
PLAYER_1_WIN_VALUE = 1000
PLAYER_2_WIN_VALUE = -1000
DRAW_VALUE = 0


def heuristic(state):
    if has_winning_combination(state[0]):
        return PLAYER_1_WIN_VALUE
    elif has_winning_combination(state[1]):
        return PLAYER_2_WIN_VALUE
    elif len(state[0]) + len(state[1]) == 9:
        return DRAW_VALUE
    else:
        # picks a blocking move if the opponent can win in the next turn
        for move in range(1, 10):
            if valid_move(state, move):
                new_state = transition(state, move)
                if has_winning_combination(new_state[1]):
                    return PLAYER_2_WIN_VALUE / 2 # return value that says that the opponent could win

        return len(state[0]) - len(state[1])


def final_state(state):
    if has_winning_combination(state[0]):
        return PLAYER_1_WIN_VALUE
    elif has_winning_combination(state[1]):
        return PLAYER_2_WIN_VALUE
    elif len(state[0]) + len(state[1]) == 9:
        return DRAW_VALUE
    else:
        return None


def has_winning_combination(moves):
    # check if there's a combination that sums up to 15
    for i in range(len(moves)):
        for j in range(i + 1, len(moves)):
            for k in range(j + 1, len(moves)):
                if moves[i] + moves[j] + moves[k] == 15:
                    return True
    return False



def valid_move(state, move):
    if move < 1 or move > 9:
        return False
    if move in state[0] or move in state[1]:
        return False
    return True


def transition(state, move):
    if not valid_move(state, move):
        return None
    new_state = (state[0].copy(), state[1].copy(), 3 - state[2])  # new state copy with the updated move
    new_state[state[2] - 1].append(move)  # add the move to the current player's moves
    return new_state


def minimax(state, depth, alpha, beta, is_max_player):
    if depth == 0 or final_state(state) is not None:
        return heuristic(state)

    if is_max_player:
        value = -float('inf') # maximazing player
        for move in range(1, 10):
            if valid_move(state, move):
                new_state = transition(state, move)
                value = max(value, minimax(new_state, depth - 1, alpha, beta, False))
                alpha = max(alpha, value)
                if beta <= alpha:
                    break
        return value
    else:
        value = float('inf') # minimizing player
        for move in range(1, 10):
            if valid_move(state, move):
                new_state = transition(state, move)
                value = min(value, minimax(new_state, depth - 1, alpha, beta, True))
                beta = min(beta, value)
                if beta <= alpha:
                    break
        return value


def choose_move_minimax(state):
    available_moves = [i for i in range(1, 10) if i not in state[0] and i not in state[1]]

    if state[2] == 1:
        best_move = None
        best_value = -float('inf')
        for move in available_moves:
            new_state = transition(state, move)
            value = minimax(new_state, 3, -float('inf'), float('inf'), False)  # set a finite depth
            if value > best_value:
                best_value = value
                best_move = move
        return best_move
    else:
        if len(available_moves) == 0:
            print("It's a draw.")
            return None

        move = int(input("Enter your move: "))
        while not valid_move(state, move):
            move = int(input("Invalid move, enter your move: "))
        return move


def initialise_game():
    player1_moves = []
    player2_moves = []
    turn = 1
    return player1_moves, player2_moves, turn


def main():
    state = initialise_game()
    while final_state(state) is None:
        if state[2] == 1:
            move = choose_move_minimax(state)
        else:
            move = int(input("Enter your move: "))
            while not valid_move(state, move):
                move = int(input("Invalid move, enter your move: "))
        state = transition(state, move)
        print(f"Player {3 - state[2]} chose {move}. Current state: Player 1: {state[0]}, Player 2: {state[1]}")

        result = final_state(state)
        if result == PLAYER_1_WIN_VALUE:
            print("Player 1 wins.")
            break
        elif result == PLAYER_2_WIN_VALUE:
            print("Player 2 wins.")
            break
        elif result == DRAW_VALUE:
            print("It's a draw.")
            break


if __name__ == "__main__":
    main()
