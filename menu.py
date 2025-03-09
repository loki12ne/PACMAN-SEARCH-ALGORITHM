import pygame
import pygame_gui

from labyrinth import Labyrinth
from game import Game
from utils import terminate, show_message
from constants import MENU_SIZE, WINDOW_SIZE, SONG_END, GAME_EVENT_TYPE, PACMAN_EVENT
from characters import Pacman, Red, Blue, Pink, Orange

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
                    start_game(level)
                    # Không đặt running = False ở đây để quay lại menu sau khi chơi xong
                except ValueError:
                    print("Lỗi: Không thể chuyển level")
            manager.process_events(event)
        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.flip()
    pygame.quit()

def start_game(mode):
    pygame.init()
    pygame.display.set_caption(f'Pacman Level {mode}')
    screen = pygame.display.set_mode(WINDOW_SIZE)
    manager = pygame_gui.UIManager(WINDOW_SIZE)

    labyrinth = Labyrinth(map, [0, 2], 2)
    pacman = Pacman((9,19))
    red = Red((21,18))
    blue = Blue((21,16))
    orange = Orange((11,12))
    pink = Pink((13,18))

    point = [(2,3),(4,8),(6,9)]
    ghost = []

    if mode == 1 or mode == 5 or mode == 6:
        ghost.append(blue)
    if mode == 2 or mode == 5 or mode == 6:
        ghost.append(pink)
    if mode == 3 or mode == 5 or mode == 6:
        ghost.append(orange)
    if mode == 4 or mode == 5 or mode == 6:
        ghost.append(red)

    game = Game(labyrinth, pacman, ghost, point)  # Khởi tạo

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
                game.move_ghosts()
            elif event.type == PACMAN_EVENT and not game_over and game_start:
                game.update_direct_pacman()
            manager.process_events(event)
        
        game.direct_pacman()
        screen.fill((0, 0, 0))
        game.render(screen)
        manager.update(time_delta)
        manager.draw_ui(screen)
        
        if game.check_win():
            show_message(screen, "You Win!", (0, 255, 0))  # Hiển thị thông báo thắng
            pygame.display.flip()
            pygame.time.wait(2000)  # Chờ 2 giây
            running = False  # Thoát vòng lặp để quay lại menu
        
        if game.check_lose():
            show_message(screen, "Game Over!", (255, 0, 0))  # Hiển thị thông báo thua
            pygame.display.flip()
            pygame.time.wait(2000)  # Chờ 2 giây
            running = False  # Thoát vòng lặp để quay lại menu
            pygame.mixer.music.pause()
        
        pygame.display.flip()
    
    # Sau khi thoát vòng lặp (thắng hoặc thua), quay lại menu
    load_menu()