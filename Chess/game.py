import pygame
from Chess.constants import *
from Chess.board import *
import inspect

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
        self.board_state = self.board.board_state
        self.turn = W
        self.valid_moves = {}

    def reset(self):
        self._init()

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
        a, b = self.selected.row, self.selected.col
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            self.valid_moves = {}
            if self._check_self():
                self.board.move(self.selected, a, b)
                return False
            self._check_opponent()
            if self.turn == W:
                self.turn = B
            elif self.turn ==B:
                self.turn = W
        if piece != 0:
            if self.selected and piece.player != self.selected.player and (row, col) in self.valid_moves:
                self.board.remove(piece)
                self.board.move(self.selected, row, col)
                if self._check_self():
                    self.board.move(self.selected, a, b)
                    return False
                self._check_opponent()
                self.valid_moves = {}
                if self.turn == W:
                    self.turn = B
                elif self.turn ==B:
                    self.turn = W
        else:
            return False
        return True
    
    def _check_opponent(self):
        moves = []
        for row in self.board.board:
            for square in row:
                if square != 0:
                    if square.player == self.turn:
                        moves.append(self.board.get_valid_moves(square))
                    else:
                        pass
                else:
                    pass
        for row in self.board.board:
            for square in row:
                if isinstance(square, King):
                    if square.player != self.turn:
                        for move in moves:
                            if (square.row, square.col) in move:
                                return True
                            else:
                                pass
                    else:
                        pass
                else:
                    pass

    def _check_self(self):
        moves = []
        for row in self.board.board:
            for square in row:
                if square != 0:
                    if square.player != self.turn:
                        moves.append(self.board.get_valid_moves(square))
                    else:
                        pass
                else:
                    pass
        for row in self.board.board:
            for square in row:
                if isinstance(square, King):
                    if square.player == self.turn:
                        for move in moves:
                            if (square.row, square.col) in move:
                                return True
                            else:
                                pass
                    else:
                        pass
                else:
                    pass