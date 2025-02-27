import pygame
import sys

def find_direction(start, target):
    x, y = start
    xn, yn = target
    if xn - x == 1: return 'right'
    if xn - x == -1: return 'left'
    if yn - y == 1: return 'down'
    if yn - y == -1: return 'up'
    return None

def show_message(screen, message1, message2):
    font = pygame.font.Font(None, 50)
    text1 = font.render(message1, True, (50, 70, 0))
    text2 = font.render(message2, True, (50, 70, 0))
    text_x = screen.get_width() // 2 - text1.get_width() // 2
    text_y = screen.get_height() // 2 - text1.get_height() // 2
    pygame.draw.rect(screen, (200, 150, 50), (text_x - 10, text_y - 10, text1.get_width() + 20, text1.get_height() + 20))
    screen.blit(text1, (text_x, text_y))
    text_x1 = screen.get_width() // 2 - text2.get_width() // 2
    text_y1 = screen.get_height() // 2 - text2.get_height() // 2 + 50
    pygame.draw.rect(screen, (200, 150, 50), (text_x1 - 10, text_y1 - 10, text2.get_width() + 20, text2.get_height() + 20))
    screen.blit(text2, (text_x1, text_y1))

def terminate():
    pygame.quit()
    sys.exit()