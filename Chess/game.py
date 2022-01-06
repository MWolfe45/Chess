import pygame
from Chess.constants import *
from Chess.board import *

class Game:
    def __init__(self,win):
        self._init()
        self.win = win

    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = W
        self.valid_moves = {}

    def reset(self):
        self._init()
#TODO Fix bug that causes clicking piece and empty space to kick back attribute error
    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)
        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.player == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True
        return False

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, BLUE, (col*SQUAREWIDTH + SQUAREWIDTH//2, row*SQUAREWIDTH+ SQUAREWIDTH//2), 5)


    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
        elif self.selected and piece.player != self.selected.player and (row, col) in self.valid_moves:
            self.board.remove(piece)
            self.board.move(self.selected, row, col)
        else:
            return False
        return True


