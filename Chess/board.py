import pygame
from .constants import *
from .pieces import *
import inspect

starting_dict = {'1,1':Rook(0,0,B), '1,2':Knight(0,1,B), '1,3':Bishop(0,2,B), '1,4':Queen(0,3,B), '1,5':King(0,4,B), '1,6':Bishop(0,5,B), '1,7':Knight(0,6,B), '1,8':Rook(0,7,B),
                '2,1':Pawn(1,0,B), '2,2':Pawn(1,1,B), '2,3':Pawn(1,2,B), '2,4':Pawn(1,3,B), '2,5':Pawn(1,4,B), '2,6':Pawn(1,5,B), '2,7':Pawn(1,6,B), '2,8':Pawn(1,7,B),
                '3,1':0, '3,2':0, '3,3':0, '3,4':0, '3,5':0, '3,6':0, '3,7':0, '3,8':0,
                '4,1':0, '4,2':0, '4,3':0, '4,4':0, '4,5':0, '4,6':0, '4,7':0, '4,8':0,
                '5,1':0, '5,2':0, '5,3':0, '5,4':0, '5,5':0, '5,6':0, '5,7':0, '5,8':0,
                '6,1':0, '6,2':0, '6,3':0, '6,4':0, '6,5':0, '6,6':0, '6,7':0, '6,8':0,
                '7,1':Pawn(6,0,W), '7,2':Pawn(6,1,W), '7,3':Pawn(6,2,W), '7,4':Pawn(6,3,W), '7,5':Pawn(6,4,W), '7,6':Pawn(6,5,W), '7,7':Pawn(6,6,W), '7,8':Pawn(6,7,W),
                '8,1':Rook(7,0,W), '8,2':Knight(7,1,W), '8,3':Bishop(7,2,W), '8,4':Queen(7,3,W), '8,5':King(7,4,W), '8,6':Bishop(7,5,W), '8,7':Knight(7,6,W), '8,8':Rook(7,7,W)}



class Board:
    def __init__(self):
        self.board = []
        self.white_pieces = self.black_pieces = {'p':8, 'b':2, 'n':2, 'r':2, 'q':1}
        self.create_board()

    def evaluate(self):
#TODO implement board evaluation method for AI
        pass

    def get_all_pieces(self, player):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.player == player:
                    pieces.append(piece)
        return pieces


    def draw_squares(self, win):
        win.fill(GREEN)
        for row in range(ROWS):
            for col in range(row%2, COLS, 2):
                pygame.draw.rect(win, TAN, (row * SQUAREWIDTH, col * SQUAREWIDTH, SQUAREWIDTH, SQUAREWIDTH))

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)
        # INCLUDE ABILITY TO CHANGE PAWN STATUS TO QUEEN/ROOK/KNIGHT/BISHOP


    def get_piece(self, row, col):
        return self.board[row][col]


    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range (COLS):
                piece = starting_dict[str(row+1)+','+str(col+1)]
                if piece == 0:
                    self.board[row].append(0)
                else:
                    self.board[row].append(piece)


    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece !=0:
                    piece.draw_piece(win)


#TODO Add method for piece capture
    # def remove(self, piece):
    #     self.board[piece.row][piece.col] = 0
    #     if piece != 0:
    #         if piece.color == WHITE:
    #             # remove specific piece from white dictionary
    #         else:
    #             # remove speciifc piece from black dictionary
    #
    # def winner(self):
    #     # ADD CONDITIONS FOR CHECKMATE

    def get_valid_moves(self, piece):
        row = piece.row
        col = piece.col
        # WILL NEED TO BE ON A PIECE BY PIECE BASIS
        if isinstance(piece, Pawn):
            if piece.player==W:
                moveset = self._pawn_white_moves(row, col)
            elif piece.player ==B:
                moveset = self._pawn_black_moves(row, col)
#TODO rewrite the class methods to match the piece in the isinstance argument
        elif isinstance(piece, King):
            if piece.player==W:
                moveset = self._pawn_white_moves(row, col)
            elif piece.player ==B:
                moveset = self._pawn_black_moves(row, col)

        elif isinstance(piece, Queen):
            if piece.player==W:
                moveset = self._pawn_white_moves(row, col)
            elif piece.player ==B:
                moveset = self._pawn_black_moves(row, col)

        elif isinstance(piece, Bishop):
            if piece.player==W:
                moveset = self._pawn_white_moves(row, col)
            elif piece.player ==B:
                moveset = self._pawn_black_moves(row, col)


        elif isinstance(piece, Knight):
            if piece.player==W:
                moveset = self._pawn_white_moves(row, col)
            elif piece.player ==B:
                moveset = self._pawn_black_moves(row, col)


        elif isinstance(piece, Rook):
            if piece.player==W:
                moveset = self._pawn_white_moves(row, col)
            elif piece.player ==B:
                moveset = self._pawn_black_moves(row, col)

        return moveset



#TODO Add en passant and promotion to pawns, fix the right attack bug for white (check black)
    def _pawn_white_moves(self, current_row, current_col):
        moves = [(current_row-1, current_col)]
        right_attack = self.board[current_row-1][current_col+1]
        left_attack = self.board[current_row-1][current_col-1]
        if current_row == 6:
            moves.append((current_row-2, current_col))
        if isinstance(right_attack, Piece):
            if right_attack.player == B:
                moves.append((current_row-1, current_col+1))
        if isinstance(left_attack, Piece):
            if left_attack.player == B:
                moves.append((current_row-1, current_col-1))
        return moves

    def _pawn_black_moves(self, current_row, current_col):
        moves = [(current_row+1, current_col)]
        right_attack = self.board[current_row+1][current_col+1]
        left_attack = self.board[current_row+1][current_col-1]
        if current_row == 7:
            moves.append((current_row+2, current_col))
        if isinstance(right_attack, Piece):
            if right_attack.player == W:
                moves.append((current_row+1, current_col+1))
        if isinstance(left_attack, Piece):
            if right_attack.player == W:
                moves.append((current_row+1, current_col-1))
        return moves

    def _king_white_moves(self, current_row, current_col):

    def _king_black_moves(self, current_row, current_col):

    def _queen_white_moves(self, current_row, current_col):

    def _queen_black_moves(self, current_row, current_col):

    def _bishop_white_moves(self, current_row, current_col):

    def _bishop_black_moves(self, current_row, current_col):

    def _knight_white_moves(self, current_row, current_col):

    def _knight_black_moves(self, current_row, current_col):

    def _rook_white_moves(self, current_row, current_col):

    def _rook_black_moves(self, current_row, current_col):

#TODO Define the movesets for each of the different pieces here