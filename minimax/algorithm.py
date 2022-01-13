import pygame
import Chess.board
import Chess.game
from .tables import *
from copy import deepcopy

# state = Board.board_rep
# # print(state)
BLACK = 'Black'
WHITE = 'White'

def minimax(position, depth, min_player, game):
    if depth == 0 or position.winner != None:
        return position.board_eval(), position
    if min_player:
        minEval = float('inf')
        best_move = None
        for move in get_all_moves(position, BLACK, game):
            evaluation = minimax(move, depth-1, False, game)[0]
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = move
        return minEval, best_move
    else:
        maxEval = float('-inf')
        best_move = None
        for move in get_all_moves(position, WHITE, game):
            evaluation = minimax(move, depth-1, True, game)[0]
            maxEval = min(maxEval, evaluation)
            if maxEval == evaluation:
                best_move = move
        return maxEval, best_move

def get_all_moves(board, color, game):
    moves = []
    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        for move in valid_moves:
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, game)
            new_board.make_board_rep()
            moves.append(new_board)
    return moves

def simulate_move(piece, move, board, game):
    board.move(piece, move[0], move[1])
    return board
