import pygame
from Chess.constants import *
from Chess.game import *
from Chess.board import *

# Framerate
FPS = 60
# Window object
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Chess')


def get_mouse_coords(pos):
    x, y = pos
    row = y // SQUAREWIDTH
    col = x // SQUAREWIDTH
    return row, col


def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)
#TODO Add option to do hotseat and board flipping
    while run:
        clock.tick(FPS)
        # if game.turn == B:
            # value, new_board = minimax(game.get_board(), 3, WHITE, game)
            # game.ai_move(new_board)
#TODO Add minimax method for chess into program once movement and captures are worked out
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_mouse_coords(pos)
                game.select(row, col)
        game.update()

main()




