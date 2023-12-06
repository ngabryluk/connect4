# Rayah.py
# Noah Gabryluk and Raymond Riddell's Connect 4 AI player that picks the best move based on the current game state.

import pdb
import utils
import math

def get_computer_move(board, which_player):
    """Search for the best move based on the current game state. 
 
    Parameters 
    ---------- 
    board : np.array of ints 
        2D array for the current state of the board 
        (0=empty, 1=player1, 2=player2). 
    which_player : int 
        The AI player may want to know which player [1, 2] they are! 
 
    Returns 
    ------- 
    choice : int 
        The column (using 1-indexing!) that the player wants to drop a disc into. 
    """

    ai_player_num = which_player
    move, _ = minimax(board, ai_player_num, ai_player_num, 10)
    return move + 1


def minimax(board, which_player, ai, depth, alpha=-math.inf, beta=math.inf):
    """Apply minimax with alpha-beta pruning to a node in the tree for the given player."""

    # Check if we have reached a terminal node
    is_gameover, winner = utils.is_gameover(board)
    if is_gameover and winner == ai:
        return _, 100
    
    # If we have reached the max depth, calculate the utility of the board
    # if depth = 0:
    #     return _, calculate_utility
    # We need to come up with a heuristic to calculate the utility
    # Possible things to look for in the board
    #   - Opponent 3-in-a-rows (high priority)
    #   - Number of 3-in-a-rows
    #   - Number of 2-in-a-rows

    valid_moves = utils.get_valid_moves(board)
    
    # Search for the max player
    if which_player == ai:
        value = -math.inf
        best_move = None
        for move in valid_moves:
            alpha = max(alpha, value)
            if alpha >= beta:
                break
            
            # Simulate the next move to pass to recursive call
            rows = utils.get_next_available_rows(board)
            row = rows[move]
            board[row][move] = which_player + 1

            _, utility = minimax(board, ai - 1, ai, alpha, beta)

            # Bring the board back to original state
            board[row][move] = 0

            if utility > value:
                value = utility
                best_move = move

        return best_move, value

    # Search for the min player
    if which_player != ai:
        value = math.inf
        best_move = None
        for move in valid_moves:
            beta = min(beta, value)
            if alpha >= beta:
                break

            # Simulate the next move to pass to recursive call
            rows = utils.get_next_available_rows(board)
            row = rows[move]
            board[row][move] = which_player + 1

            _, utility = minimax(board, ai + 1, ai, alpha, beta)

            # Bring the board back to original state
            board[row][move] = 0

            if utility < value:
                value = utility
                best_move = move

        return best_move, value

