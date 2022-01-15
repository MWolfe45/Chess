import pygame
from .constants import *
from .pieces import *
import inspect
from minimax import tables

starting_dict = {'1,1':Rook(0,0,B), '1,2':Knight(0,1,B), '1,3':Bishop(0,2,B), '1,4':Queen(0,3,B), '1,5':King(0,4,B), '1,6':Bishop(0,5,B), '1,7':Knight(0,6,B), '1,8':Rook(0,7,B),
                '2,1':Pawn(1,0,B), '2,2':Pawn(1,1,B), '2,3':Pawn(1,2,B), '2,4':Pawn(1,3,B), '2,5':Pawn(1,4,B), '2,6':Pawn(1,5,B), '2,7':Pawn(1,6,B), '2,8':Pawn(1,7,B),
                '3,1':0, '3,2':0, '3,3':0, '3,4':0, '3,5':0, '3,6':0, '3,7':0, '3,8':0,
                '4,1':0, '4,2':0, '4,3':0, '4,4':0, '4,5':0, '4,6':0, '4,7':0, '4,8':0,
                '5,1':0, '5,2':0, '5,3':0, '5,4':0, '5,5':0, '5,6':0, '5,7':0, '5,8':0,
                '6,1':0, '6,2':0, '6,3':0, '6,4':0, '6,5':0, '6,6':0, '6,7':0, '6,8':0,
                '7,1':Pawn(6,0,W), '7,2':Pawn(6,1,W), '7,3':Pawn(6,2,W), '7,4':Pawn(6,3,W), '7,5':Pawn(6,4,W), '7,6':Pawn(6,5,W), '7,7':Pawn(6,6,W), '7,8':Pawn(6,7,W),
                '8,1':Rook(7,0,W), '8,2':Knight(7,1,W), '8,3':Bishop(7,2,W), '8,4':Queen(7,3,W), '8,5':King(7,4,W), '8,6':Bishop(7,5, W), '8,7':Knight(7,6, W), '8,8':Rook(7,7,W)}



class Board:
    def __init__(self):
        self.board = []
        self.board_rep = []
        self.white_pieces = self.black_pieces = {'p':8, 'b':2, 'n':2, 'r':2, 'q':1}
        self.create_board()
        self.make_board_rep()
        self.winner = None

    def get_all_pieces(self, player):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.player == player:
                    pieces.append(piece)
        return pieces

    def trigger_promotion(self, piece):
        if isinstance(piece, Pawn):
            if piece.row == 0 or piece.row == 7:
                return True

    def draw_squares(self, win):
        win.fill(GREEN)
        for row in range(ROWS):
            for col in range(row%2, COLS, 2):
                pygame.draw.rect(win, TAN, (row * SQUAREWIDTH, col * SQUAREWIDTH, SQUAREWIDTH, SQUAREWIDTH))

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)


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

    def make_board_rep(self):
        self.board_rep = []
        for i, row in enumerate(range(ROWS)):
            self.board_rep.append([])
            for j, col in enumerate(range(COLS)):
                if self.board[i][j] == 0:
                    self.board_rep[i].append('0')
                else:
                    self.board_rep[i].append(self.board[i][j].BOARD_ID)



    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece !=0:
                    piece.draw_piece(win)


#TODO Add method for piece accounting after capture
    def remove_piece(self, piece):
        self.board[piece.row][piece.col] = 0


    # def winner(self):
    #     if self.

    def white_piece_points(self):
        piece_sum = 0
        for row in self.board_rep:
            for square in row:
                if square in ['P', 'R', 'K', 'N', 'Q', 'B']:
                    piece_sum += tables.values[square]
        return piece_sum

    def black_piece_points(self):
        piece_sum = 0
        for row in self.board_rep:
            for square in row:
                if square in ['p', 'r', 'k', 'n', 'q', 'b']:
                    piece_sum += tables.values[square]
        return piece_sum

    def white_position_points(self):
        position_sum = 0
        for row, rank in enumerate(self.board_rep):
            for col, square in enumerate(rank):
                if square == 'P':
                    position_sum += tables.w_pawn[row][col]
                elif square == 'K':
                    position_sum += tables.w_king[row][col]
                elif square == 'N':
                    position_sum += tables.w_knight[row][col]
                elif square == 'B':
                    position_sum += tables.w_bishop[row][col]
                elif square == 'R':
                    position_sum += tables.w_rook[row][col]
                elif square == 'Q':
                    position_sum += tables.w_queen[row][col]
        return position_sum

    def black_position_points(self):
        position_sum = 0
        for row, rank in enumerate(self.board_rep):
            for col, square in enumerate(rank):
                if square == 'p':
                    position_sum += tables.b_pawn[row][col]
                elif square == 'k':
                    position_sum += tables.b_king[row][col]
                elif square == 'n':
                    position_sum += tables.b_knight[row][col]
                elif square == 'b':
                    position_sum += tables.b_bishop[row][col]
                elif square == 'r':
                    position_sum += tables.b_rook[row][col]
                elif square == 'q':
                    position_sum += tables.b_queen[row][col]
        return position_sum

# Algorithm evaluating every hypothetical position as though it's the starting position
    def board_eval(self):
        board_state = self.board_rep
        result = self.white_piece_points() + self.white_position_points() + self.black_piece_points() + self.black_position_points()
        return result


    def _check_self(self, player):
        moves = []
        for row in self.board:
            for square in row:
                if square != 0:
                    if square.player != player:
                        if square.ID == 'p':
                            if square.player == W:
                                moves.append(self._pawn_white_moves(square.row, square.col))
                            elif square.player == B:
                                moves.append(self._pawn_black_moves(square.row, square.col))
                        elif square.ID == 'n':
                            if square.player == W:
                                moves.append(self._knight_white_moves(square.row, square.col))
                            elif square.player == B:
                                moves.append(self._knight_black_moves(square.row, square.col))
                        elif square.ID == 'b':
                            if square.player == W:
                                moves.append(self._bishop_white_moves(square.row, square.col))
                            elif square.player == B:
                                moves.append(self._bishop_black_moves(square.row, square.col))
                        elif square.ID == 'r':
                            if square.player == W:
                                moves.append(self._rook_white_moves(square.row, square.col))
                            elif square.player == B:
                                moves.append(self._rook_black_moves(square.row, square.col))
                        elif square.ID == 'q':
                            if square.player == W:
                                moves.append(self._queen_white_moves(square.row, square.col))
                            elif square.player == B:
                                moves.append(self._queen_black_moves(square.row, square.col))
                        elif square.ID == 'k':
                            if square.player == W:
                                moves.append(self._king_white_moves(square.row, square.col))
                            elif square.player == B:
                                moves.append(self._king_black_moves(square.row, square.col))
                    else:
                        pass
                else:
                    pass
        for row in self.board:
            for square in row:
                if isinstance(square, King):
                    if square.player == player:
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


    def check_square_attacked(self, row, col, player):
        moves = []
        for row in self.board:
            for square in row:
                if square != 0:
                    if square.player != player:
                        moves.append(self.get_valid_moves(square))
                    else:
                        pass
                else:
                    pass
        for move in moves:
            if (row, col) in move:
                return True
            else:
                return False



    def examine_moves(self, piece, moves):
        rem_moves = []
        row, col = piece.row, piece.col
        if not self._check_self(piece.player) and piece.ID == 'k' and piece.player == W:
            if self._whitecastle(piece.row, piece.col):
                moves.append(self._whitecastle(piece.row, piece.col))
        elif not self._check_self(piece.player) and piece.ID == 'k' and piece.player == B:
            if self._blackcastle(piece.row, piece.col):
                moves.append(self._blackcastle(piece.row, piece.col))
        elif not self._check_self(piece.player) and piece.ID == 'p' and piece.player == W:
            if self._white_en_passant_move(piece.row, piece.col):
                moves.append(self._white_en_passant_move(piece.row, piece.col))
        elif not self._check_self(piece.player) and piece.ID == 'p' and piece.player == B:
            if self._black_en_passant_move(piece.row, piece.col):
                moves.append(self._black_en_passant_move(piece.row, piece.col))
        for move in moves:
            if move:
                if self.board[move[0]][move[1]] == 0:
                    self.move(piece, move[0], move[1])
                    if self._check_self(piece.player):
                        self.move(piece, row, col)
                        rem_moves.append(move)
                    elif not self._check_self(piece.player):
                        self.move(piece, row, col)
                elif self.board[move[0]][move[1]] != 0:
                    hold_piece = self.board[move[0]][move[1]]
                    self.remove_piece(self.board[move[0]][move[1]])
                    self.move(piece, move[0], move[1])
                    if self._check_self(piece.player):
                        self.move(piece, row, col)
                        self.board[move[0]][move[1]] = hold_piece
                        rem_moves.append(move)
                    else:
                        self.move(piece, row, col)
                        self.board[move[0]][move[1]] = hold_piece
        moveset = list(set(moves) - set(rem_moves))
        return moveset

#TODO Moved valid move generator to board file, copied over check square attacked and self check too. trying to fold move logic only into this file

    def get_valid_moves(self, piece):
        row, col = piece.row, piece.col
        if isinstance(piece, Pawn):
            if piece.player==W:
                moveset = self._pawn_white_moves(row, col)
            elif piece.player ==B:
                moveset = self._pawn_black_moves(row, col)
            # removed_moves = self._examine_moves(piece, moveset)
            # moveset = list(set(moveset) - set(removed_moves))
#################################################################################################
        elif isinstance(piece, King):
            if piece.player == W:
                moveset = self._king_white_moves(row, col)
            elif piece.player == B:
                moveset = self._king_black_moves(row, col)
            # removed_moves = self._examine_moves(piece, moveset)
            # moveset = list(set(moveset) - set(removed_moves))
########################################################################3
        elif isinstance(piece, Queen):
            if piece.player==W:
                moveset = self._queen_white_moves(row, col)
            elif piece.player ==B:
                moveset = self._queen_black_moves(row, col)
            # removed_moves = self._examine_moves(piece, moveset)
            # moveset = list(set(moveset) - set(removed_moves))
##############################################################################33
        elif isinstance(piece, Bishop):
            if piece.player==W:
                moveset = self._bishop_white_moves(row, col)
            elif piece.player ==B:
                moveset = self._bishop_black_moves(row, col)
            # removed_moves = self._examine_moves(piece, moveset)
            # moveset = list(set(moveset) - set(removed_moves))
###########################################################################
        elif isinstance(piece, Knight):
            if piece.player==W:
                moveset = self._knight_white_moves(row, col)
            elif piece.player ==B:
                moveset = self._knight_black_moves(row, col)
            # removed_moves = self._examine_moves(piece, moveset)
            # moveset = list(set(moveset) - set(removed_moves))
#####################################################################
        elif isinstance(piece, Rook):
            if piece.player==W:
                moveset = self._rook_white_moves(row, col)
            elif piece.player ==B:
                moveset = self._rook_black_moves(row, col)
            # removed_moves = self._examine_moves(piece, moveset)
            # moveset = list(set(moveset) - set(removed_moves))
        return moveset












#####################################################################
#TODO Add en passant and promotion to pawns
#TODO Pawn bug where moving a knight in front of white pawn causes crash related to moves.remove

    def _pawn_white_moves(self, current_row, current_col):
        moves = [(current_row-1, current_col)]
        if current_row == 6:
            moves.append((current_row-2, current_col))
        if self.board[current_row-1][current_col] != 0:
            moves.remove((current_row-1, current_col))
        if self.board[current_row-1][current_col] != 0 and current_row == 6:
            moves.remove((current_row - 2, current_col))
        if (current_col + 1) in range(COLS):
            right_attack = self.board[current_row-1][current_col+1]
            if isinstance(right_attack, Piece):
                if right_attack.player == B:
                    moves.append((current_row - 1, current_col + 1))
        if (current_col - 1) in range(COLS):
            left_attack = self.board[current_row - 1][current_col - 1]
            if isinstance(left_attack, Piece):
                if left_attack.player == B:
                    moves.append((current_row-1, current_col-1))
        return moves

    def _white_en_passant_move(self, current_row, current_col):
        if current_row == 3:
            if isinstance(self.board[current_row][current_col - 1], Pawn):
                if self.board[current_row][current_col - 1].passant == True and self.board[current_row][current_col - 1].player == B:
                    return ((current_row-1,current_col-1))
            elif isinstance(self.board[current_row][current_col +1], Pawn):
                if self.board[current_row][current_col + 1].passant == True and self.board[current_row][current_col + 1].player == B:
                    return ((current_row-1,current_col+1))


    def white_en_passant_capture(self):
        for file in self.board:
            for square in file:
                if isinstance(square, Pawn) and square.player == B:
                    if square.passant == True:
                        self.remove(square)

    def _pawn_black_moves(self, current_row, current_col):
        moves = [(current_row + 1, current_col)]
        if current_row == 1:
            moves.append((current_row + 2, current_col))
        if self.board[current_row + 1][current_col] != 0:
            moves.remove((current_row + 1, current_col))
        if self.board[current_row + 2][current_col] != 0 and current_row == 1:
            moves.remove((current_row + 2, current_col))
        if (current_col + 1) in range(COLS):
            right_attack = self.board[current_row + 1][current_col + 1]
            if isinstance(right_attack, Piece):
                if right_attack.player == W:
                    moves.append((current_row + 1, current_col + 1))
        if (current_col - 1) in range(COLS):
            left_attack = self.board[current_row + 1][current_col - 1]
            if isinstance(left_attack, Piece):
                if left_attack.player == W:
                    moves.append((current_row + 1, current_col - 1))
        return moves


    def _black_en_passant_move(self, current_row, current_col):
        if current_row == 4:
            if isinstance(self.board[current_row][current_col - 1], Pawn):
                if self.board[current_row][current_col - 1].passant == True and self.board[current_row][current_col - 1].player == W:
                    return ((current_row+1,current_col-1))
            elif isinstance(self.board[current_row][current_col +1], Pawn):
                if self.board[current_row][current_col + 1].passant == True and self.board[current_row][current_col + 1].player == W:
                    return ((current_row+1,current_col+1))


    def black_en_passant_capture(self):
        for file in self.board:
            for square in file:
                if isinstance(square, Pawn) and square.player == W:
                    if square.passant == True:
                        self.remove(square)


    def _king_white_moves(self, current_row, current_col):
        moves = [(current_row-1, current_col+1),(current_row, current_col+1),(current_row+1, current_col+1),
                 (current_row+1, current_col),(current_row+1, current_col-1),(current_row, current_col-1),
                 (current_row-1, current_col-1),(current_row-1, current_col)]
        rem_moves = []
        for pos in moves:
            if pos[0] in range(ROWS) and pos[1] in range(COLS):
                if self.board[pos[0]][pos[1]] != 0:
                    if self.board[pos[0]][pos[1]].player == W:
                        rem_moves.append(pos)
                else:
                    pass
            else:
                rem_moves.append(pos)
        moves = list(set(moves) - set(rem_moves))
        return moves


    def _whitecastle(self, current_row, current_col):
        if self.board[7][0] != 0:
            if self.board[7][0].ID == 'r':
                if not self.board[current_row][current_col].has_moved and not self.board[7][0].has_moved and self.board[7][1] == 0 and self.board[7][2] == 0:
                    if not self.check_square_attacked(7,2,W) and not self.check_square_attacked(7,3,W):
                        return (7,2)
        elif self.board[7][7] != 0:
            if self.board[7][7].ID == 'r':
                if not self.board[current_row][current_col].has_moved and not self.board[7][7].has_moved and self.board[7][6] == 0 and self.board[7][5] == 0:
                    if not self.check_square_attacked(7, 6, W) and not self.check_square_attacked(7, 5, W):
                        return (7,6)



    def whitecastle(self, row, col):
        if (row, col) == (7,6):
            self.move(self.board[7][7], 7, 5)
        elif (row, col) == (7,2):
            self.move(self.board[7][0], 7, 3)



    def _king_black_moves(self, current_row, current_col):
        moves = [(current_row - 1, current_col + 1), (current_row, current_col + 1), (current_row + 1, current_col + 1),
                 (current_row + 1, current_col), (current_row + 1, current_col - 1), (current_row, current_col - 1),
                 (current_row - 1, current_col - 1), (current_row - 1, current_col)]
        rem_moves = []
        for pos in moves:
            if pos[0] in range(ROWS) and pos[1] in range(COLS):
                if self.board[pos[0]][pos[1]] != 0:
                    if self.board[pos[0]][pos[1]].player == B:
                        rem_moves.append(pos)
                else:
                    pass
            else:
                rem_moves.append(pos)
        moves = list(set(moves) - set(rem_moves))
        return moves

    def _blackcastle(self, current_row, current_col):
        if self.board [0][0] != 0:
            if self.board[0][0].ID == 'r':
                if not self.board[current_row][current_col].has_moved and not self.board[0][0].has_moved and self.board[0][1] == 0 and self.board[0][2] == 0:
                    if not self.check_square_attacked(0, 2, B) and not self.check_square_attacked(0, 3, B):
                        return (0, 2)
        elif self.board[0][7] != 0:
            if self.board[0][7].ID == 'r':
                if not self.board[current_row][current_col].has_moved and not self.board[7][7].has_moved and self.board[7][6] == 0 and self.board[7][5] == 0:
                    if not self.check_square_attacked(0, 4, B) and not self.check_square_attacked(0, 5, B):
                        return (0, 6)

    def blackcastle(self, row, col):
        if (row, col) == (0,2):
            self.move(self.board[0][0], 0, 3)
        if (row, col) == (0,6):
            self.move(self.board[0][7], 0, 5)

    def _queen_white_moves(self, current_row, current_col):
        moves = []
        # Diag up right
        if (current_row > 0) and (current_col < 7):
            i = 1
            B_count = True
            while B_count == True:
                if ((current_row - i) < 0) or ((current_col + i) > 7):
                    break
                if self.board[current_row - i][current_col + i] != 0:
                    if self.board[current_row - i][current_col + i].player == W:
                        break
                moves.append((current_row - i, current_col + i))
                if ((current_row - i) < 0) or ((current_col + i) > 7):
                    break
                if self.board[current_row - i][current_col + i] != 0:
                    if self.board[current_row - i][current_col + i].player == B:
                        moves.append((current_row - i, current_col + i))
                        break
                i += 1

        # Diag down left
        if (current_row < 7) and (current_col > 0):
            i = 1
            B_count = True
            while B_count == True:
                if ((current_row + i) > 7) or ((current_col - i) < 0):
                    break
                if self.board[current_row + i][current_col - i] != 0:
                    if self.board[current_row + i][current_col - i].player == W:
                        break
                moves.append((current_row + i, current_col - i))
                if ((current_row + i) > 7) or ((current_col + i) < 0):
                    break
                if self.board[current_row + i][current_col - i] != 0:
                    if self.board[current_row + i][current_col - i].player == B:
                        moves.append((current_row + i, current_col - i))
                        break
                i += 1

        # Diag up left
        if (current_row > 0) and (current_col > 0):
            i = 1
            B_count = True
            while B_count == True:
                if ((current_row - i) < 0) or ((current_col - i) < 0):
                    break
                if self.board[current_row - i][current_col - i] != 0:
                    if self.board[current_row - i][current_col - i].player == W:
                        break
                moves.append((current_row - i, current_col - i))
                if ((current_row - i) < 0) or ((current_col - i) > 7):
                    break
                if self.board[current_row - i][current_col - i] != 0:
                    if self.board[current_row - i][current_col - i].player == B:
                        moves.append((current_row - i, current_col - i))
                        break
                i += 1

        # Diag down right
        if (current_row < 7) and (current_col < 7):
            i = 1
            B_count = True
            while B_count == True:
                if ((current_row + i) > 7) or ((current_col + i) > 7):
                    break
                if self.board[current_row + i][current_col + i] != 0:
                    if self.board[current_row + i][current_col + i].player == W:
                        break
                moves.append((current_row + i, current_col + i))
                if ((current_row + i) > 7) or ((current_col + i) > 7):
                    break
                if self.board[current_row + i][current_col + i] != 0:
                    if self.board[current_row + i][current_col + i].player == B:
                        moves.append((current_row + i, current_col + i))
                        break
                i += 1

        if current_row > 0:
            i = 1
            B_count = True
            while B_count == True:
                if current_row - i < 0:
                    break
                if self.board[current_row-i][current_col] != 0:
                    if self.board[current_row-i][current_col].player == W:
                        break
                moves.append((current_row-i, current_col))
                if current_row - i < 0:
                    break
                if self.board[current_row-i][current_col] != 0:
                    if self.board[current_row-i][current_col].player == B:
                        moves.append((current_row-i, current_col))
                        break
                i += 1

        if current_row < 7:
            i = 1
            B_count = True
            while B_count == True:
                if current_row + i > 7:
                    break
                if self.board[current_row+i][current_col] != 0:
                    if self.board[current_row+i][current_col].player == W:
                        break
                moves.append((current_row+i, current_col))
                if current_row + i > 7:
                    break
                if self.board[current_row+i][current_col] != 0:
                    if self.board[current_row+i][current_col].player == B:
                        moves.append((current_row+i, current_col))
                        break
                i += 1

        if current_col > 0:
            i = 1
            B_count = True
            while B_count == True:
                if current_col - i < 0:
                    break
                if self.board[current_row][current_col-i] != 0:
                    if self.board[current_row][current_col-i].player == W:
                        break
                moves.append((current_row, current_col-i))
                if current_col - i < 0:
                    break
                if self.board[current_row][current_col-i] != 0:
                    if self.board[current_row][current_col-i].player == B:
                        moves.append((current_row, current_col-i))
                        break
                i += 1

        if current_col < 7:
            i = 1
            B_count = True
            while B_count == True:
                if current_col + i > 7:
                    break
                if self.board[current_row][current_col+i] != 0:
                    if self.board[current_row][current_col+i].player == W:
                        break
                moves.append((current_row, current_col+i))

                if current_col + i > 7:
                    break
                if self.board[current_row][current_col+i] != 0:
                    if self.board[current_row][current_col+i].player == B:
                        moves.append((current_row, current_col+i))
                        break
                i += 1
        return moves

    def _queen_black_moves(self, current_row, current_col):
        moves = []
        # Diag up right
        if (current_row > 0) and (current_col < 7):
            i = 1
            W_count = True
            while W_count == True:
                if ((current_row - i) < 0) or ((current_col + i) > 7):
                    break
                if self.board[current_row - i][current_col + i] != 0:
                    if self.board[current_row - i][current_col + i].player == B:
                        break
                moves.append((current_row - i, current_col + i))
                if ((current_row - i) < 0) or ((current_col + i) > 7):
                    break
                if self.board[current_row - i][current_col + i] != 0:
                    if self.board[current_row - i][current_col + i].player == W:
                        moves.append((current_row - i, current_col + i))
                        break
                i += 1

        # Diag down left
        if (current_row < 7) and (current_col > 0):
            i = 1
            W_count = True
            while W_count == True:
                if ((current_row + i) > 7) or ((current_col - i) < 0):
                    break
                if self.board[current_row + i][current_col - i] != 0:
                    if self.board[current_row + i][current_col - i].player == B:
                        break
                moves.append((current_row + i, current_col - i))
                if ((current_row + i) > 7) or ((current_col + i) < 0):
                    break
                if self.board[current_row + i][current_col - i] != 0:
                    if self.board[current_row + i][current_col - i].player == W:
                        moves.append((current_row + i, current_col - i))
                        break
                i += 1

        # Diag up left
        if (current_row > 0) and (current_col > 0):
            i = 1
            W_count = True
            while W_count == True:
                if ((current_row - i) < 0) or ((current_col - i) < 0):
                    break
                if self.board[current_row - i][current_col - i] != 0:
                    if self.board[current_row - i][current_col - i].player == B:
                        break
                moves.append((current_row - i, current_col - i))
                if ((current_row - i) < 0) or ((current_col - i) > 7):
                    break
                if self.board[current_row - i][current_col - i] != 0:
                    if self.board[current_row - i][current_col - i].player == W:
                        moves.append((current_row - i, current_col - i))
                        break
                i += 1

        # Diag down right
        if (current_row < 7) and (current_col < 7):
            i = 1
            W_count = True
            while W_count == True:
                if ((current_row + i) > 7) or ((current_col + i) > 7):
                    break
                if self.board[current_row + i][current_col + i] != 0:
                    if self.board[current_row + i][current_col + i].player == B:
                        break
                moves.append((current_row + i, current_col + i))
                if ((current_row + i) > 7) or ((current_col + i) > 7):
                    break
                if self.board[current_row + i][current_col + i] != 0:
                    if self.board[current_row + i][current_col + i].player == W:
                        moves.append((current_row + i, current_col + i))
                        break
                i += 1

        if current_row > 0:
            i = 1
            W_count = True
            while W_count == True:
                if current_row - i < 0:
                    break
                if self.board[current_row-i][current_col] != 0:
                    if self.board[current_row-i][current_col].player == B:
                        break
                moves.append((current_row-i, current_col))
                if current_row - i < 0:
                    break
                if self.board[current_row-i][current_col] != 0:
                    if self.board[current_row-i][current_col].player == W:
                        moves.append((current_row-i, current_col))
                        break
                i += 1
#TODO Checck these if statements, some of the conditions might be redundant
        if current_row < 7:
            i = 1
            W_count = True
            while W_count == True:
                if current_row + i > 7:
                    break
                if self.board[current_row+i][current_col] != 0:
                    if self.board[current_row+i][current_col].player == B:
                        break
                moves.append((current_row+i, current_col))
                if current_row + i > 7:
                    break
                if self.board[current_row+i][current_col] != 0:
                    if self.board[current_row+i][current_col].player == W:
                        moves.append((current_row+i, current_col))
                        break
                i += 1

        if current_col > 0:
            i = 1
            W_count = True
            while W_count == True:
                if current_col - i < 0:
                    break
                if self.board[current_row][current_col-i] != 0:
                    if self.board[current_row][current_col-i].player == B:
                        break
                moves.append((current_row, current_col-i))
                if current_col - i < 0:
                    break
                if self.board[current_row][current_col-i] != 0:
                    if self.board[current_row][current_col-i].player == W:
                        moves.append((current_row, current_col-i))
                        break
                i += 1

        if current_col < 7:
            i = 1
            W_count = True
            while W_count == True:
                if current_col + i > 7:
                    break
                if self.board[current_row][current_col+i] != 0:
                    if self.board[current_row][current_col+i].player == B:
                        break
                moves.append((current_row, current_col+i))

                if current_col + i > 7:
                    break
                if self.board[current_row][current_col+i] != 0:
                    if self.board[current_row][current_col+i].player == W:
                        moves.append((current_row, current_col+i))
                        break
                i += 1

            return moves

    def _bishop_white_moves(self, current_row, current_col):
        moves = []
        #Diag up right
        if (current_row > 0) and (current_col < 7):
            i = 1
            B_count = True
            while B_count == True:
                if ((current_row - i) < 0) or ((current_col + i) > 7):
                    break
                if self.board[current_row-i][current_col+i] != 0:
                    if self.board[current_row-i][current_col+i].player == W:
                        break
                moves.append((current_row-i, current_col+i))
                if ((current_row - i) < 0) or ((current_col + i) > 7):
                    break
                if self.board[current_row-i][current_col+i] != 0:
                    if self.board[current_row-i][current_col+i].player == B:
                        moves.append((current_row-i, current_col+i))
                        break
                i += 1

        #Diag down left
        if (current_row < 7) and (current_col > 0):
            i = 1
            B_count = True
            while B_count == True:
                if ((current_row + i) > 7) or ((current_col - i) < 0):
                    break
                if self.board[current_row+i][current_col-i] != 0:
                    if self.board[current_row+i][current_col-i].player == W:
                        break
                moves.append((current_row+i, current_col-i))
                if ((current_row + i) > 7) or ((current_col + i) < 0):
                    break
                if self.board[current_row+i][current_col-i] != 0:
                    if self.board[current_row+i][current_col-i].player == B:
                        moves.append((current_row+i, current_col-i))
                        break
                i += 1

        #Diag up left
        if (current_row > 0) and (current_col > 0):
            i = 1
            B_count = True
            while B_count == True:
                if ((current_row - i) < 0) or ((current_col - i) < 0):
                    break
                if self.board[current_row-i][current_col-i] != 0:
                    if self.board[current_row-i][current_col-i].player == W:
                        break
                moves.append((current_row-i, current_col-i))
                if ((current_row - i) < 0) or ((current_col-i) > 7):
                    break
                if self.board[current_row-i][current_col-i] != 0:
                    if self.board[current_row-i][current_col-i].player == B:
                        moves.append((current_row-i, current_col-i))
                        break
                i += 1

        #Diag down right
        if (current_row < 7) and (current_col < 7):
            i = 1
            B_count = True
            while B_count == True:
                if ((current_row + i) > 7) or ((current_col + i) > 7):
                    break
                if self.board[current_row+i][current_col+i] != 0:
                    if self.board[current_row+i][current_col+i].player == W:
                        break
                moves.append((current_row+i, current_col+i))
                if ((current_row + i) > 7) or ((current_col + i) > 7):
                    break
                if self.board[current_row+i][current_col+i] != 0:
                    if self.board[current_row+i][current_col+i].player == B:
                        moves.append((current_row+i, current_col+i))
                        break
                i += 1

        return moves

    def _bishop_black_moves(self, current_row, current_col):
        moves = []
        #Diag up right
        if (current_row > 0) and (current_col < 7):
            i = 1
            W_count = True
            while W_count == True:
                if ((current_row - i) < 0) or ((current_col + i) > 7):
                    break
                if self.board[current_row-i][current_col+i] != 0:
                    if self.board[current_row-i][current_col+i].player == B:
                        break
                moves.append((current_row-i, current_col+i))
                if ((current_row - i) < 0) or ((current_col + i) > 7):
                    break
                if self.board[current_row-i][current_col+i] != 0:
                    if self.board[current_row-i][current_col+i].player == W:
                        moves.append((current_row-i, current_col+i))
                        break
                i += 1

        #Diag down left
        if (current_row < 7) and (current_col > 0):
            i = 1
            W_count = True
            while W_count == True:
                if ((current_row + i) > 7) or ((current_col - i) < 0):
                    break
                if self.board[current_row+i][current_col-i] != 0:
                    if self.board[current_row+i][current_col-i].player == B:
                        break
                moves.append((current_row+i, current_col-i))
                if ((current_row + i) > 7) or ((current_col + i) < 0):
                    break
                if self.board[current_row+i][current_col-i] != 0:
                    if self.board[current_row+i][current_col-i].player == W:
                        moves.append((current_row+i, current_col-i))
                        break
                i += 1

        #Diag up left
        if (current_row > 0) and (current_col > 0):
            i = 1
            W_count = True
            while W_count == True:
                if ((current_row - i) < 0) or ((current_col - i) < 0):
                    break
                if self.board[current_row-i][current_col-i] != 0:
                    if self.board[current_row-i][current_col-i].player == B:
                        break
                moves.append((current_row-i, current_col-i))
                if ((current_row - i) < 0) or ((current_col-i) > 7):
                    break
                if self.board[current_row-i][current_col-i] != 0:
                    if self.board[current_row-i][current_col-i].player == W:
                        moves.append((current_row-i, current_col-i))
                        break
                i += 1

        #Diag down right
        if (current_row < 7) and (current_col < 7):
            i = 1
            W_count = True
            while W_count == True:
                if ((current_row + i) > 7) or ((current_col + i) > 7):
                    break
                if self.board[current_row+i][current_col+i] != 0:
                    if self.board[current_row+i][current_col+i].player == B:
                        break
                moves.append((current_row+i, current_col+i))
                if ((current_row + i) > 7) or ((current_col + i) > 7):
                    break
                if self.board[current_row+i][current_col+i] != 0:
                    if self.board[current_row+i][current_col+i].player == W:
                        moves.append((current_row+i, current_col+i))
                        break
                i += 1

        return moves

    def _knight_white_moves(self, current_row, current_col):
        moves = [(current_row+2, current_col-1), (current_row+2, current_col+1),(current_row-2, current_col-1),
                 (current_row-2, current_col+1),(current_row-1, current_col-2),(current_row-1, current_col+2),
                 (current_row+1, current_col-2),(current_row+1, current_col+2)]

        # This code block is able to check to see whether a given move is allowed regarding off-board and friendly fire
        rem_moves = []
        for pos in moves:
            if pos[0] in range(ROWS) and pos[1] in range(COLS):
                if self.board[pos[0]][pos[1]] != 0:
                    if self.board[pos[0]][pos[1]].player == W:
                        rem_moves.append(pos)
                else:
                    pass
            else:
                rem_moves.append(pos)
        moves = list(set(moves) - set(rem_moves))
        return moves

    def _knight_black_moves(self, current_row, current_col):
        moves = [(current_row + 2, current_col - 1), (current_row + 2, current_col + 1), (current_row - 2, current_col - 1),
                 (current_row - 2, current_col + 1), (current_row - 1, current_col - 2), (current_row - 1, current_col + 2),
                 (current_row + 1, current_col - 2), (current_row + 1, current_col + 2)]

        # This code block is able to check to see whether a given move is allowed regarding off-board and friendly fire
        rem_moves = []
        for pos in moves:
            if pos[0] in range(ROWS) and pos[1] in range(COLS):
                if self.board[pos[0]][pos[1]] != 0:
                    if self.board[pos[0]][pos[1]].player == B:
                        rem_moves.append(pos)
                else:
                    pass
            else:
                rem_moves.append(pos)
        moves = list(set(moves) - set(rem_moves))
        return moves

    def _rook_white_moves(self, current_row, current_col):
        moves = []
        if current_row > 0:
            i = 1
            B_count = True
            while B_count == True:
                if current_row - i < 0:
                    break
                if self.board[current_row-i][current_col] != 0:
                    if self.board[current_row-i][current_col].player == W:
                        break
                moves.append((current_row-i, current_col))
                if current_row - i < 0:
                    break
                if self.board[current_row-i][current_col] != 0:
                    if self.board[current_row-i][current_col].player == B:
                        moves.append((current_row-i, current_col))
                        break
                i += 1

        if current_row < 7:
            i = 1
            B_count = True
            while B_count == True:
                if current_row + i > 7:
                    break
                if self.board[current_row+i][current_col] != 0:
                    if self.board[current_row+i][current_col].player == W:
                        break
                moves.append((current_row+i, current_col))
                if current_row + i > 7:
                    break
                if self.board[current_row+i][current_col] != 0:
                    if self.board[current_row+i][current_col].player == B:
                        moves.append((current_row+i, current_col))
                        break
                i += 1

        if current_col > 0:
            i = 1
            B_count = True
            while B_count == True:
                if current_col - i < 0:
                    break
                if self.board[current_row][current_col-i] != 0:
                    if self.board[current_row][current_col-i].player == W:
                        break
                moves.append((current_row, current_col-i))
                if current_col - i < 0:
                    break
                if self.board[current_row][current_col-i] != 0:
                    if self.board[current_row][current_col-i].player == B:
                        moves.append((current_row, current_col-i))
                        break
                i += 1

        if current_col < 7:
            i = 1
            B_count = True
            while B_count == True:
                if current_col + i > 7:
                    break
                if self.board[current_row][current_col+i] != 0:
                    if self.board[current_row][current_col+i].player == W:
                        break
                moves.append((current_row, current_col+i))

                if current_col + i > 7:
                    break
                if self.board[current_row][current_col+i] != 0:
                    if self.board[current_row][current_col+i].player == B:
                        moves.append((current_row, current_col+i))
                        break
                i += 1

        return moves

    def _rook_black_moves(self, current_row, current_col):
        moves = []
        if current_row > 0:
            i = 1
            W_count = True
            while W_count == True:
                if current_row - i < 0:
                    break
                if self.board[current_row-i][current_col] != 0:
                    if self.board[current_row-i][current_col].player == B:
                        break
                moves.append((current_row-i, current_col))
                if current_row - i < 0:
                    break
                if self.board[current_row-i][current_col] != 0:
                    if self.board[current_row-i][current_col].player == W:
                        moves.append((current_row-i, current_col))
                        break
                i += 1

        if current_row < 7:
            i = 1
            W_count = True
            while W_count == True:
                if current_row + i > 7:
                    break
                if self.board[current_row+i][current_col] != 0:
                    if self.board[current_row+i][current_col].player == B:
                        break
                moves.append((current_row+i, current_col))
                if current_row + i > 7:
                    break
                if self.board[current_row+i][current_col] != 0:
                    if self.board[current_row+i][current_col].player == W:
                        moves.append((current_row+i, current_col))
                        break
                i += 1

        if current_col > 0:
            i = 1
            W_count = True
            while W_count == True:
                if current_col - i < 0:
                    break
                if self.board[current_row][current_col-i] != 0:
                    if self.board[current_row][current_col-i].player == B:
                        break
                moves.append((current_row, current_col-i))
                if current_col - i < 0:
                    break
                if self.board[current_row][current_col-i] != 0:
                    if self.board[current_row][current_col-i].player == W:
                        moves.append((current_row, current_col-i))
                        break
                i += 1

        if current_col < 7:
            i = 1
            W_count = True
            while W_count == True:
                if current_col + i > 7:
                    break
                if self.board[current_row][current_col+i] != 0:
                    if self.board[current_row][current_col+i].player == B:
                        break
                moves.append((current_row, current_col+i))

                if current_col + i > 7:
                    break
                if self.board[current_row][current_col+i] != 0:
                    if self.board[current_row][current_col+i].player == W:
                        moves.append((current_row, current_col+i))
                        break
                i += 1

        return moves
#####################################################################
