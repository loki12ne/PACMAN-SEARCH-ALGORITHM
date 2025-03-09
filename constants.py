import pygame

pygame.init()

# SIZE
MENU_SIZE = 1200,800
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 800, 1000
TILE_SIZE = 24

# EVENT
GAME_EVENT_TYPE = pygame.USEREVENT + 1
pygame.time.set_timer(GAME_EVENT_TYPE, 100)

PACMAN_EVENT = pygame.USEREVENT + 2
pygame.time.set_timer(PACMAN_EVENT, 135)

SONG_END = pygame.USEREVENT + 3
