from .constants import *
import pygame

class Piece:
    PADDING = 20

    def __init__(self, row, col, player):
        self.row = row
        self.col = col
        self.ID = ''
        self.player = player
        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self):
        self.x = SQUAREWIDTH * self.col + SQUAREWIDTH // 2
        self.y = SQUAREWIDTH * self.row + SQUAREWIDTH // 2

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()

    def __repr__(self):
        return str(self.player)



class Pawn(Piece):
    def __init__(self, row, col, player):
        Piece.__init__(self, row, col, player)
        self.ID = 'p'
        self.BOARD_ID = 'p'
        self.promoted = False
        self.passant = False

    def draw_piece(self, win):
        if self.player == B:
            win.blit(B_PAWN, (self.x - B_PAWN.get_width() // 2, self.y - B_PAWN.get_width() // 2))
        elif self.player == W:
            win.blit(W_PAWN, (self.x - W_PAWN.get_width() // 2, self.y - W_PAWN.get_width() // 2))
            self.BOARD_ID = 'P'







class Knight(Piece):
    def __init__(self, row, col, player):
        Piece.__init__(self, row, col, player)
        self.ID = 'n'
        self.BOARD_ID = 'n'

    def draw_piece(self, win):
        if self.player == B:
            win.blit(B_KNIGNT, (self.x - B_KNIGNT.get_width() // 2, self.y - B_KNIGNT.get_width() // 2))
        elif self.player == W:
            win.blit(W_KNIGNT, (self.x - W_KNIGNT.get_width() // 2, self.y - W_KNIGNT.get_width() // 2))
            self.BOARD_ID = 'N'



class Bishop(Piece):
    def __init__(self, row, col, player):
        Piece.__init__(self, row, col, player)
        self.ID = 'b'
        self.BOARD_ID = 'b'

    def draw_piece(self, win):
        if self.player == B:
            win.blit(B_BISHOP, (self.x - B_BISHOP.get_width() // 2, self.y - B_BISHOP.get_width() // 2))
        elif self.player == W:
            win.blit(W_BISHOP, (self.x - W_BISHOP.get_width() // 2, self.y - W_BISHOP.get_width() // 2))
            self.BOARD_ID = 'B'



class Rook(Piece):
    def __init__(self, row, col, player):
        Piece.__init__(self, row, col, player)
        self.has_moved = False
        self.ID = 'r'
        self.BOARD_ID = 'r'

    def draw_piece(self, win):
        if self.player == B:
            win.blit(B_ROOK, (self.x - B_ROOK.get_width() // 2, self.y - B_ROOK.get_width() // 2))
        elif self.player == W:
            win.blit(W_ROOK, (self.x - W_ROOK.get_width() // 2, self.y - W_ROOK.get_width() // 2))
            self.BOARD_ID = 'R'



class Queen(Piece):
    def __init__(self, row, col, player):
        Piece.__init__(self, row, col, player)
        self.ID = 'q'
        self.BOARD_ID = 'q'

    def draw_piece(self, win):
        if self.player == B:
            win.blit(B_QUEEN, (self.x - B_QUEEN.get_width() // 2, self.y - B_QUEEN.get_width() // 2))
        elif self.player == W:
            win.blit(W_QUEEN, (self.x - W_QUEEN.get_width() // 2, self.y - W_QUEEN.get_width() // 2))
            self.BOARD_ID = 'Q'



class King(Piece):
    def __init__(self, row, col, player):
        Piece.__init__(self, row, col, player)
        self.has_moved = False
        self.in_check = False
        self.ID = 'k'
        self.BOARD_ID = 'k'

    def draw_piece(self, win):
        if self.player == B:
            win.blit(B_KING, (self.x - B_KING.get_width() // 2, self.y - B_KING.get_width() // 2))
        elif self.player == W:
            win.blit(W_KING, (self.x - W_KING.get_width() // 2, self.y - W_KING.get_width() // 2))
            self.BOARD_ID = 'K'
