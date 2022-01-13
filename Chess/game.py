import pygame
from Chess.constants import *
from Chess.board import *
import inspect
pygame.init()
BASICFONT = pygame.font.SysFont('arial',25, False, False)

class Game:
    def __init__(self,win):
        self._init()
        self.win = win
        self.turn_no = 0
        self.move_record = {}
        self.white_promote = False
        self.black_promote = False

    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = W
        self.valid_moves = []

    def white_popup(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        popupSurf = pygame.Surface((300,100))
        popupSurf.fill(NIKI)

        A = popupSurf.blit(W_ROOK, (15,30))
        B = popupSurf.blit(W_QUEEN, (90, 30))
        C = popupSurf.blit(W_BISHOP, (165, 30))
        D = popupSurf.blit(W_KNIGNT, (240, 30))

        popupRect = popupSurf.get_rect()
        popupRect.centerx = WIDTH/2
        popupRect.centery = WIDTH/2
        self.win.blit(popupSurf, popupRect)
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    ## if mouse is pressed get position of cursor ##
                    pos = pygame.mouse.get_pos()
                    ## check if cursor is on button ##
                    if A.collidepoint(pos):
                        print('FUCK')
                        return
                    elif B.collidepoint(pos):
                        print('FUCK YOU')
                        return
                    elif C.collidepoint(pos):
                        print('I"M SO TIRED')
                        return
                    elif D.collidepoint(pos):
                        print('Please work')
                        return


    def black_popup(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        popupSurf = pygame.Surface((300,100))
        popupSurf.fill(NIKI)
        A = pygame.Rect()
        B = pygame.Rect()
        C = pygame.Rect()
        D = pygame.Rect()
        spaces = [A, B, C, D]
        options = [B_ROOK,
                   B_QUEEN,
                   B_BISHOP,
                   B_KNIGNT]
        result = zip(spaces, options)
        vert = 30
        hori = 15
        for i, j in result:
            popupSurf.blit(i, (hori,vert))
            popupSurf.blit(j, (hori, vert))
            hori += 75
        popupRect = popupSurf.get_rect()
        popupRect.centerx = WIDTH/2
        popupRect.centery = WIDTH/2
        self.win.blit(popupSurf, popupRect)
        pygame.display.update()


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
            self.valid_moves = self.board.examine_moves(piece, self.board.get_valid_moves(piece))
            return True
        return False

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, BLUE, (col*SQUAREWIDTH + SQUAREWIDTH//2, row*SQUAREWIDTH+ SQUAREWIDTH//2), 5)


    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            if isinstance(self.selected, Pawn) and self.selected.player == W:
                if self.selected.row == 6 and row == 4:
                    self.selected.passant = True
            elif isinstance(self.selected, Pawn) and self.selected.player == B:
                if self.selected.row == 1 and row ==3:
                    self.selected.passant = True
            self.board.move(self.selected, row, col)
            self.castle(row, col)
            self.en_pass()
            if self.board.trigger_promotion(self.selected) and self.selected.player == W:
                self.white_promote = True
            elif self.board.trigger_promotion(self.selected) and self.selected.player == B:
                self.black_promote = True
            self.board.make_board_rep()
            for file in self.board.board:
                for square in file:
                    if square != self.selected:
                        if isinstance(square, Pawn):
                            self.revert_en_pass(square)
            self.valid_moves = {}
            self.change_turn()
            return True
        elif self.selected and piece != 0 and (row, col) in self.valid_moves:
            self.board.remove(piece)
            self.board.move(self.selected, row, col)
            if self.board.trigger_promotion(self.selected) and self.selected.player == W:
                self.white_promote = True
            elif self.board.trigger_promotion(self.selected) and self.selected.player == B:
                self.black_promote = True
            self.board.make_board_rep()
            for file in self.board.board:
                for square in file:
                    if square != self.selected:
                        if isinstance(square, Pawn):
                            self.revert_en_pass(square)
            self.valid_moves = {}
            self.change_turn()
            return True
        else:
            return False



#Switches the turn from one player to the other
    def change_turn(self):
        self.move_record[self.turn_no] = self.board.board
        print('-------------------------------------------')
        for row in self.board.board_rep:
            print(row)
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
        if isinstance(self.selected, King) and (row,col) in [(7,2)] and self.selected.player == W:
            self.board.whitecastle(row, col)
        if isinstance(self.selected, King) and (row,col) in [(7,6)] and self.selected.player == W:
            self.board.whitecastle(row, col)
        if isinstance(self.selected, King) and (row, col) in [(0,2)] and self.selected.player == B:
            self.board.blackcastle(row, col)
        if isinstance(self.selected, King) and (row, col) in [(0,6)] and self.selected.player == B:
            self.board.blackcastle(row, col)
        if isinstance(self.selected, King) or isinstance(self.selected, Rook):
            self.selected.has_moved = True

    def en_pass(self):
        if isinstance(self.selected, Pawn):
            if self.selected.player == W:
                if isinstance(self.board.board[self.selected.row+1][self.selected.col], Pawn):
                    if self.board.board[self.selected.row+1][self.selected.col].passant:
                        self.board.white_en_passant_capture()
                elif isinstance(self.board.board[self.selected.row+1][self.selected.col], Pawn):
                    if self.board.board[self.selected.row+1][self.selected.col].passant:
                        self.board.white_en_passant_capture()
            elif self.selected.player == B:
                if isinstance(self.board.board[self.selected.row-1][self.selected.col], Pawn):
                    if self.board.board[self.selected.row-1][self.selected.col].passant:
                        self.board.black_en_passant_capture()
                elif isinstance(self.board.board[self.selected.row-1][self.selected.col], Pawn):
                    if self.board.board[self.selected.row-1][self.selected.col].passant:
                        self.board.black_en_passant_capture()

    def revert_en_pass(self, piece):
        piece.passant = False
