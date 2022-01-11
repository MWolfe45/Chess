import pygame
from Chess.constants import *
from Chess.board import *
import inspect

class Game:
    def __init__(self,win):
        self._init()
        self.win = win
        self.turn_no = 0
        # self.move_record = {}

    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = W
        self.valid_moves = []

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
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            self.board.make_board_rep()
            self.valid_moves = {}
            self.change_turn()
            return True
        elif self.selected and piece != 0 and (row, col) in self.valid_moves:
            self.board.remove(piece)
            self.board.move(self.selected, row, col)
            self.board.make_board_rep()
            self.valid_moves = {}
            self.change_turn()
            return True
        else:
            return False




# Looks to see whether the current player is in check
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
                                square.in_check = True
                                return True
                            else:
                                square.in_check = False
                                pass
                    else:
                        pass
                else:
                    pass

#Looks to see if a given square is under attack by the other player
    def check_square_attacked(self, row, col):
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
        for move in moves:
            if (row, col) in move:
                return True
        else:
            pass







#Switches the turn from one player to the other
    def change_turn(self):
        if self.turn == W:
            self.turn = B
            self.turn_no += 1
        elif self.turn == B:
            self.turn = W
            self.turn_no += 1


# Performs the castling moves
    def castle(self, row, col):
        if isinstance(self.selected, King) or isinstance(self.selected, Rook):
            self.selected.has_moved = True
        if isinstance(self.selected, King) and (row,col) in [(7,2)] and self.selected.player == W and not self.check_square_attacked(7,3) and not self._check_self():
            self.board.whitecastle(row, col)
        if isinstance(self.selected, King) and (row,col) in [(7,6)] and self.selected.player == W and not self.check_square_attacked(7,5) and not self._check_self():
            self.board.whitecastle(row, col)
        if isinstance(self.selected, King) and (row, col) in [(0,2)] and self.selected.player == B and not self.check_square_attacked(0,3) and not self._check_self():
            self.board.blackcastle(row, col)
        if isinstance(self.selected, King) and (row, col) in [(0,6)] and self.selected.player == B and not self.check_square_attacked(0,5) and not self._check_self():
            self.board.blackcastle(row, col)
        if isinstance(self.selected, King) or isinstance(self.selected, Rook):
            self.selected.has_moved = True