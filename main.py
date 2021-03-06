import pygame
from Chess.constants import *
from Chess.game import *
from Chess.board import *
from minimax.algorithm import minimax

# Framerate
FPS = 60
# Window object
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Chess')


def raw_mouse_coords(pos):
    x, y = pos
    return x, y

def get_mouse_coords(pos):
    x, y = pos
    row = y // SQUAREWIDTH
    col = x // SQUAREWIDTH
    return row, col

class popup:
    def __init__(self):
        self._init()



def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    while run:
        clock.tick(FPS)
        if game.turn == B:
            value, new_board = minimax(game.board, 2, B, game)
            game.ai_move(new_board)
        # if game.winner() != None:
        #     print(game.winner())
        #     run = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_mouse_coords(pos)
                game.select(row, col)
        if game.white_promote == True:
            game.white_popup()
            game.white_promote = False
            # game.update()
        elif game.black_promote == True:
            game.black_popup()
            game.black_promote = False
            # game.update()
        else:
            game.update()

main()




