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

def show_message(screen, message, color):
    font = pygame.font.Font(None, 50)
    text = font.render(message, True, color)
    text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    
    # Vẽ nền chữ nhật có viền
    pygame.draw.rect(screen, (200, 150, 50), text_rect.inflate(20, 20))  # Hình chữ nhật nền
    pygame.draw.rect(screen, (0, 0, 0), text_rect.inflate(22, 22), 2)  # Viền đen
    
    # Hiển thị text
    screen.blit(text, text_rect)
    pygame.display.flip()  # Cập nhật màn hình

    pygame.time.wait(1000)  # Tạm dừng 2 giây trước khi tiếp tục
def terminate():
    pygame.quit()
    sys.exit()