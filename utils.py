import pygame
import sys


def find_direction(start, target):
    """Return direction from start to target: 'right', 'left', 'down', 'up', or None."""
    x, y = start
    xn, yn = target
    if xn - x == 1: return 'right'
    if xn - x == -1: return 'left'
    if yn - y == 1: return 'down'
    if yn - y == -1: return 'up'
    return None

def terminate():
    pygame.quit()
    sys.exit()