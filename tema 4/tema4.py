import random


def initialise_game():
    player1_moves = []
    player2_moves = []
    turn = 1
    return player1_moves, player2_moves, turn


def final_state(state):
    if has_winning_combination(state[0]):
        return 'player 1 wins'
    elif has_winning_combination(state[1]):
        return 'player 2 wins'
    elif len(state[0]) + len(state[1]) == 9:
        return 'draw'
    else:
        return False


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
    if move in state[0] or move in state[1]: # checks to see if the number is already in the board
        return False  
    return True


def transition(state, move):
    if not valid_move(state, move):
        return False
    new_state = (state[0].copy(), state[1].copy(), 3 - state[2])  # new state copy with the updated move
    new_state[state[2] - 1].append(move)  # add the move to the current player's moves
    return new_state


def choose_move(state):
    available_moves = [i for i in range(1, 10) if i not in state[0] and i not in state[1]]
    if state[2] == 1:
        return random.choice(available_moves) # random move for player 1
    else:
        move = int(input("enter ur move: "))
        while not valid_move(state, move):
            move = int(input("invalid move, enter ur move: "))
        return move


def main():
    state = initialise_game()
    while not final_state(state):
        move = choose_move(state)
        state = transition(state, move)
        print(f"player {state[2]} chose {move}. current state: player 1: {state[0]}, player 2: {state[1]}")

    result = final_state(state)
    print(result)


if __name__ == "__main__":
    main()
