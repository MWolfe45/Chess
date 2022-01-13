import os
import pygame

# Window dimensions
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 8, 8
SQUAREWIDTH = WIDTH // COLS

#Asset loading
B_BISHOP = pygame.transform.scale(pygame.image.load(r'C:\Users\Matt\PycharmProjects\Chess\Assets\b_bishop_png_128px.png'), (35, 35))
B_KING = pygame.transform.scale(pygame.image.load(r'C:\Users\Matt\PycharmProjects\Chess\Assets\b_king_png_128px.png'), (35, 35))
B_KNIGNT = pygame.transform.scale(pygame.image.load(r'C:\Users\Matt\PycharmProjects\Chess\Assets\b_knight_png_128px.png'), (35, 35))
B_PAWN = pygame.transform.scale(pygame.image.load(r'C:\Users\Matt\PycharmProjects\Chess\Assets\b_pawn_png_128px.png'), (35, 35))
B_QUEEN = pygame.transform.scale(pygame.image.load(r'C:\Users\Matt\PycharmProjects\Chess\Assets\b_queen_png_128px.png'), (35, 35))
B_ROOK = pygame.transform.scale(pygame.image.load(r'C:\Users\Matt\PycharmProjects\Chess\Assets\b_rook_png_128px.png'), (35, 35))
W_BISHOP = pygame.transform.scale(pygame.image.load(r'C:\Users\Matt\PycharmProjects\Chess\Assets\w_bishop_png_128px.png'), (35, 35))
W_KING = pygame.transform.scale(pygame.image.load(r'C:\Users\Matt\PycharmProjects\Chess\Assets\w_king_png_128px.png'), (35, 35))
W_KNIGNT = pygame.transform.scale(pygame.image.load(r'C:\Users\Matt\PycharmProjects\Chess\Assets\w_knight_png_128px.png'), (35, 35))
W_PAWN = pygame.transform.scale(pygame.image.load(r'C:\Users\Matt\PycharmProjects\Chess\Assets\w_pawn_png_128px.png'), (35, 35))
W_QUEEN = pygame.transform.scale(pygame.image.load(r'C:\Users\Matt\PycharmProjects\Chess\Assets\w_queen_png_128px.png'), (35, 35))
W_ROOK = pygame.transform.scale(pygame.image.load(r'C:\Users\Matt\PycharmProjects\Chess\Assets\w_rook_png_128px.png'), (35, 35))

#Player code
B = 'Black'
W = 'White'


#Colors
GREEN = (0,102,0)
TAN = (255,229,204)
BLUE = (0,0,255)
NIKI = (102,242,205)
