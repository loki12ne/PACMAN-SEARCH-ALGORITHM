import pygame
import pygame_gui

from labyrinth import Labyrinth
from game import GameLv1
from utils import terminate, show_message
from constants import MENU_SIZE, WINDOW_SIZE, SONG_END, GAME_EVENT_TYPE, PACMAN_EVENT
from characters import Pacman, Red

def load_menu():
    pygame.init()
    pygame.display.set_caption('Pacman Levels')
    manager = pygame_gui.UIManager(MENU_SIZE)
    screen = pygame.display.set_mode(MENU_SIZE)
    screen.fill((0, 0, 0))

    font = pygame.font.Font(None, 50)
    text = font.render("Pacman", True, (254, 254, 34))
    screen.blit(text, (20, 20))
    pygame.draw.rect(screen, (254, 254, 34), (10, 10, text.get_width() + 20, text.get_height() + 20), 1)

    buttons = [
        pygame_gui.elements.UIButton(relative_rect=pygame.Rect((340, 70 + i * 60), (90, 50)),
                                     text=f'LEVEL {i + 1}', manager=manager)
        for i in range(7)
    ]

    running = True
    clock = pygame.time.Clock()
    while running:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                level_text = event.ui_element.text.replace("LEVEL ", "")
                try:
                    level = int(level_text)
                    switch_level(level)
                    running = False
                except ValueError:
                    print("Lỗi: Không thể chuyển level")

            manager.process_events(event)
        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.flip()
    pygame.quit()

def switch_level(level):
    levels = {
        1: level1,
        2: level2,
        3: level3,
        4: level4,
        5: level5,
        6: level6,
        7: level7
    }
    levels.get(level, lambda: print("Level không hợp lệ"))()

def level1():
    pygame.init()
    pygame.display.set_caption('Pacman Level 1')
    screen = pygame.display.set_mode(WINDOW_SIZE)
    manager = pygame_gui.UIManager(WINDOW_SIZE)

    labyrinth = Labyrinth(map, [0, 2], 2)
    pacman = Pacman((9,19))
    red = Red((21,18))
    game = GameLv1(labyrinth, pacman, red)

    clock = pygame.time.Clock()
    running = True
    game_over = False
    game_start = False
    game_start_time = pygame.time.get_ticks() + 500
    while running:
        current_time = pygame.time.get_ticks()
        time_delta = clock.tick(60) / 1000.0
        if current_time > game_start_time:
            game_start = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == SONG_END:
                pygame.mixer.music.load('sounds/siren.wav')
                pygame.mixer.music.play(-1)
            elif event.type == GAME_EVENT_TYPE and not game_over and game_start:
                game.move_red()

            elif event.type == PACMAN_EVENT and not game_over and game_start:
                game.update_direct_pacman()

            manager.process_events(event)
        game.direct_pacman()
        screen.fill((0, 0, 0))
        game.render(screen)
        manager.update(time_delta)
        manager.draw_ui(screen)
        if game.check_win():
            game_over = True
            break
            pygame.mixer.music.pause()
            # if sound_not_played1:
            #   #  victory.play(0)
            #     sound_not_played1 = False
        if game.check_lose():
            game_over = True
            break
            pygame.mixer.music.pause()
            # if sound_not_played2:
            #   #  lose.play(0)
            #     sound_not_played2 = False
        pygame.display.flip()


def level2():
    pygame.init()
    pygame.display.set_caption('Pacman Level 2')
    screen = pygame.display.set_mode(WINDOW_SIZE)
    screen.fill((0, 255, 0))  # Màn hình màu xanh lá
    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


def level3():
    pygame.init()
    pygame.display.set_caption('Pacman Level 3')
    screen = pygame.display.set_mode(WINDOW_SIZE)
    screen.fill((0, 0, 255))  # Màn hình màu xanh dương
    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


def level4():
    pygame.init()
    pygame.display.set_caption('Pacman Level 4')
    screen = pygame.display.set_mode(WINDOW_SIZE)
    screen.fill((255, 255, 0))  # Màn hình màu vàng
    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


def level5():
    pygame.init()
    pygame.display.set_caption('Pacman Level 5')
    screen = pygame.display.set_mode(WINDOW_SIZE)
    screen.fill((255, 0, 255))  # Màn hình màu tím
    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


def level6():
    pygame.init()
    pygame.display.set_caption('Pacman Level 6')
    screen = pygame.display.set_mode(WINDOW_SIZE)
    screen.fill((0, 255, 255))  # Màn hình màu cyan
    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


def level7():
    pygame.init()
    pygame.display.set_caption('Pacman Level 7')
    screen = pygame.display.set_mode(WINDOW_SIZE)
    screen.fill((255, 165, 0))  # Màn hình màu cam
    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

