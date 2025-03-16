import pygame

pygame.init()

# Window and tile sizes
MENU_SIZE = (800, 600)
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = (800, 600)
TILE_SIZE = 18

# Custom event types
GAME_EVENT_TYPE = pygame.USEREVENT + 1
pygame.time.set_timer(GAME_EVENT_TYPE, 100)

PACMAN_EVENT = pygame.USEREVENT + 2
pygame.time.set_timer(PACMAN_EVENT, 135)

SONG_END = pygame.USEREVENT + 3

ORANGE_EVENT_TYPE = pygame.USEREVENT + 4  # Special event for Orange ghost