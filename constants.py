import pygame

pygame.init()

# SIZE
MENU_SIZE = 600, 600
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
TILE_SIZE = 24

# EVENT
GAME_EVENT_TYPE = pygame.USEREVENT + 1
pygame.time.set_timer(GAME_EVENT_TYPE, 150)

PACMAN_EVENT = pygame.USEREVENT + 2
pygame.time.set_timer(PACMAN_EVENT, 170)

SONG_END = pygame.USEREVENT + 3



# Vị trí nhân vật theo map
# POSITIONS = {
#     'first_map.txt': {
#         'pacman': (5, 15), 'red': (9, 9), 'pink': (18, 19), 'blue': (26, 21), 'orange': (2, 30)},
#     'second_map.txt': {
#         'pacman': (2, 19), 'red': (21, 18), 'pink': (9, 27), 'blue': (9, 2), 'orange': (2, 8)},
#     'third_map.txt': {
#         'pacman': (1, 27), 'red': (26, 20), 'pink': (12, 9), 'blue': (4, 8), 'orange': (1, 14)},
#     'fourth_map.txt': {
#         'pacman': (14, 30), 'red': (26, 18), 'pink': (1, 7), 'blue': (6, 28), 'orange': (7, 9)},
#     'fifth_map.txt': {
#         'pacman': (1, 30), 'red': (12, 18), 'pink': (21, 9), 'blue': (15, 30), 'orange': (5, 12)},
# }