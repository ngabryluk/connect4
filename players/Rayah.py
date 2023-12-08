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

    print(board) # Current board state
    print(depth)

    # Check if we have reached a terminal node
    is_gameover, winner = utils.is_gameover(board)
    if is_gameover and winner == ai: # If Rayah wins with this move
        print("There is a winning move! Let's Goooooo!")
        return None, 100 # Pick it!
    elif is_gameover and winner > 0 and winner != ai: # If opponent wins with next move
        return None, -100 # Don't pick it!
    
    # If we have reached the max depth, calculate the utility of the board
    if depth == 0:
        return None, 0#calculate_utility(board, ai)

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

            _, utility = minimax(board, 1 - which_player, ai, depth-1,alpha, beta)

            print(utility)

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

            _, utility = minimax(board, 1 - which_player, ai, depth-1, alpha, beta)

            # Bring the board back to original state
            board[row][move] = 0

            if utility < value:
                value = utility
                best_move = move

        return best_move, value

def calculate_utility(board, which_player):
    rows, cols = board.shape
    scores = []
    max_score = 0
    # Check vertically
    for row in range(rows):
        score = 0
        for col in range(cols):
            if board[row][col] == which_player:
                score += 1
                if board[row + 1][col] is not None and board[row + 1][col] == which_player:
                    score += 1
                    if board[row + 2][col] is not None and board[row + 2][col] == which_player and board[row][col] == 0:
                        score += 1
        if score > max_score:
            max_score = score

    scores.append(max_score)

    max_score = 0

    for row in range(rows):
        score = 0
        for col in range(cols):
            if board[row][col] == which_player:
                score += 1
                if board[row][col + 1] is not None and board[row][col + 1] == which_player:
                    score += 1
                    if board[row][col + 2] is not None and board[row][col + 2] == which_player and board[row][col] == 0:
                        score += 1
        if score > max_score:
            max_score = score

    scores.append(max_score)

    max_score = 0

    for row in range(rows):
        score = 0
        for col in range(cols):
            if board[row][col] == which_player:
                score += 1
                if board[row + 1][col + 1] is not None and board[row + 1][col + 1] == which_player:
                    score += 1
                    if board[row + 2][col + 2] is not None and board[row + 2][col + 2] == which_player:
                        score += 1
        if score > max_score:
            max_score = score

    scores.append(max_score)

    max_score = 0

    for row in range(3, rows):
        score = 0
        for col in range(cols):
            if board[row][col] is not None and board[row][col] == which_player:
                score += 1
                if board[row - 1][col + 1] is not None and board[row][col] == which_player:
                    score += 1
                    if board[row - 2][col + 2] is not None and board[row - 2][col + 2] == which_player:
                        score += 1
        if score > max_score:
            max_score = score
            
    scores.append(max_score)

    return max(scores)