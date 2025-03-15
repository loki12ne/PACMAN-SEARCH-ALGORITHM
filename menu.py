import pygame
import pygame_gui

from labyrinth import Labyrinth
from game import Game
from utils import terminate, show_message
from constants import MENU_SIZE, WINDOW_SIZE, SONG_END, GAME_EVENT_TYPE, PACMAN_EVENT, ORANGE_EVENT_TYPE
from characters import Pacman, Red, Blue, Pink, Orange

def load_menu():
    pygame.init()
    pygame.mixer.init()
    pygame.display.set_caption('Pacman Levels')
    manager = pygame_gui.UIManager(MENU_SIZE)
    screen = pygame.display.set_mode(MENU_SIZE)
    screen.fill((0, 0, 0))

    # Load nhạc nền
    pygame.mixer.music.load("UI/sound/bg_music.mp3")  # Thay bằng file của bạn
    pygame.mixer.music.set_volume(0.5)  # Điều chỉnh âm lượng (0.0 - 1.0)
    pygame.mixer.music.play(-1)  # Lặp vô hạn
    music_playing = True

    # Load âm thanh khi hover
    hover_sound = pygame.mixer.Sound("UI/sound/button.mp3")
    hover_sound.set_volume(0.7)  # Điều chỉnh âm lượng

    # # Tạo UIButton có hình ảnh
    # music_panel = pygame_gui.elements.UIPanel(
    #     relative_rect=pygame.Rect((20, MENU_SIZE[1] - 60), (60, 40)), 
    #     manager=manager
    # )
    # music_button = pygame_gui.elements.UIImage(
    #     relative_rect=pygame.Rect((20, MENU_SIZE[1] - 60), (60, 40)), 
    #     image_surface=music_on_img, 
    #     manager=manager
    # )

    #Vẽ logo
    logo = pygame.image.load("UI/logo.png")
    logo = pygame.transform.scale(logo, (600, 320))
    relative_rect = pygame.Rect(((WINDOW_SIZE[0] - 600) * 0.5, 0), (600, 320))

    buttons = []
    button_images = []

    for i in range(5):
        normal_image = pygame.image.load(f"UI/level{i + 1}.png")  
        hover_image = pygame.image.load(f"UI/level{i + 1}_hover.png")  

        normal_image = pygame.transform.scale(normal_image, (168, 60))
        hover_image = pygame.transform.scale(hover_image, (168, 60))
        #còn: 0.3, size button, size panel chưa define
        #Tạo Panel
        if (i < 3):
            button_panel = pygame_gui.elements.UIPanel(
                relative_rect=pygame.Rect((WINDOW_SIZE[0] * 0.5 - (160 + 10), WINDOW_SIZE[1] * 0.4 + i * (20 + 50 + 10)), (160, 50)), 
                manager=manager
            )
        else:
            button_panel = pygame_gui.elements.UIPanel(
                relative_rect=pygame.Rect((WINDOW_SIZE[0] * 0.5 + 10, WINDOW_SIZE[1] * 0.4 + (i - 3) * (20 + 50 + 10)), (160, 50)), 
                manager=manager
            )

        #Tạo ảnh
        if (i < 3):
            button_image = pygame_gui.elements.UIImage(
                relative_rect=pygame.Rect((WINDOW_SIZE[0] * 0.5 - (168 + 10), WINDOW_SIZE[1] * 0.4 + i * (20 + 50 + 10)), (168, 60)), 
                image_surface=normal_image, 
                manager=manager
            )
        else:
            button_image = pygame_gui.elements.UIImage(
                relative_rect=pygame.Rect((WINDOW_SIZE[0] * 0.5 + 10, WINDOW_SIZE[1] * 0.4 + (i - 3) * (20 + 50 + 10)), (168, 60)), 
                image_surface=normal_image, 
                manager=manager
            )

        button_images.append((button_panel, button_image, normal_image, hover_image))
        buttons.append(button_panel)

    #them nut exit
    normal_image = pygame.image.load(f"UI/exit.png")  
    hover_image = pygame.image.load(f"UI/exit_hover.png")  

    normal_image = pygame.transform.scale(normal_image, (168, 60))
    hover_image = pygame.transform.scale(hover_image, (168, 60))

    button_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((WINDOW_SIZE[0] * 0.5 + 10, WINDOW_SIZE[1] * 0.4 + 2 * (20 + 50 + 10)), (160, 50)), 
            manager=manager
    )
    button_image = pygame_gui.elements.UIImage(
            relative_rect=pygame.Rect((WINDOW_SIZE[0] * 0.5 + 10, WINDOW_SIZE[1] * 0.4 + 2 * (20 + 50 + 10)), (168, 60)), 
            image_surface=normal_image, 
            manager=manager
    )

    button_images.append((button_panel, button_image, normal_image, hover_image))
    buttons.append(button_panel)

    # Vẽ nút bật/tắt nhạc
    music_on_img = pygame.image.load("UI/sound_on.png")
    music_off_img = pygame.image.load("UI/sound_off.png")

    music_on_img = pygame.transform.scale(music_on_img, (60, 40))
    music_off_img = pygame.transform.scale(music_off_img, (60, 40))

    music_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((19, MENU_SIZE[1] - 50), (20, 20)),
            manager=manager
    )
    music_image = pygame_gui.elements.UIImage(
            relative_rect=pygame.Rect((20, MENU_SIZE[1] - 60), (60, 40)),
            image_surface=music_on_img, 
            manager=manager
    )

    button_images.append((music_panel, music_image, music_on_img, music_off_img))
    buttons.append(music_panel)


    running = True
    clock = pygame.time.Clock()
    while running:
        time_delta = clock.tick(60) / 1000.0
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, button in enumerate(buttons):
                    if button.relative_rect.collidepoint(mouse_pos):
                        hover_sound.play()
                        if i < 5:
                            start_game(i + 1)
                            running = False
                        elif i == 5:
                            terminate()
                        elif i == 6:
                            if music_playing:
                                pygame.mixer.music.pause()  # Dừng nhạc
                            else:
                                pygame.mixer.music.unpause()  # Bật lại nhạc
                            # Xóa ảnh cũ bằng cách vẽ lại nền
                            panel_x, panel_y = music_panel.relative_rect.topleft
                            button_x, button_y = music_image.relative_rect.topleft
                            pygame.draw.rect(screen, (0, 0, 0), (panel_x + button_x, panel_y + button_y, 60, 40))

                            # Đổi hình ảnh
                            music_image.set_image(music_off_img if music_playing else music_on_img)

                            # Đảo trạng thái nhạc
                            music_playing = not music_playing
                        break

            manager.process_events(event)


        for button, image_element, normal, hover in button_images[:6]:
            if button.relative_rect.collidepoint(mouse_pos):
                image_element.set_image(hover)
            else:
                image_element.set_image(normal)

        manager.update(time_delta)
        screen.fill((0, 0, 0))
        screen.blit(logo, relative_rect.topleft)
        manager.draw_ui(screen)
        pygame.display.flip()

    pygame.quit()

def start_game(mode):
    pygame.init()
    pygame.display.set_caption(f'Pacman Level {mode}')
    screen = pygame.display.set_mode(WINDOW_SIZE)
    manager = pygame_gui.UIManager(WINDOW_SIZE)

    pygame.mixer.music.set_volume(0.3)
    starting_sound = pygame.mixer.Sound("UI/sound/starting.mp3")
    starting_sound.set_volume(0.7)  # Điều chỉnh âm lượng
    starting_sound.play(0)

    logo = pygame.image.load("UI/logo.png")
    logo = pygame.transform.scale(logo, (270, 144))
    logo_rect = pygame.Rect((WINDOW_SIZE[0] - 270, 0), (270, 144))

    # Vẽ khung score
    scrore_board = pygame.image.load("UI/score.png")
    scrore_board = pygame.transform.scale(scrore_board, (180, 105))
    scrore_board_rect = pygame.Rect((WINDOW_SIZE[0] - 230, 144), (180, 105))
    # score_rect = pygame.Rect(WINDOW_SIZE[0] - 270, 150, 150, 50)  # Khung điểm số (tọa độ x, y, rộng, cao)
    # pygame.draw.rect(screen, (255, 255, 255), score_rect, border_radius=10)  # Viền trắng
    # pygame.draw.rect(screen, (0, 0, 0), score_rect.inflate(-4, -4))  # Khung đen bên trong
    # Hiển thị điểm số

    
    labyrinth = Labyrinth(map, [0, 2], 2)
    pacman = Pacman((1,30))

    # test case A: 14,15 B: 15,21 C: 1,2 D:26,30 E: 26,2
    test_case = 'E'
    if(test_case == 'A'):
        px = 14
        py = 15
    elif(test_case == 'B'):
        px = 15
        py = 21
    elif(test_case == 'C'):
        px = 1
        py = 2
    elif(test_case == 'D'):
        px = 26
        py = 30
    elif(test_case == 'E'):
        px = 26
        py = 2


    red = Red((px,py))
    blue = Blue((px,py))
    orange = Orange((px,py))
    pink = Pink((px,py))

    ghost = []

    research = True

    if mode == 1:
        ghost.append(blue)
    elif mode == 2:
        ghost.append(pink)
    elif mode == 3:
        ghost.append(orange)
    elif mode == 4:
        ghost.append(red)
    elif mode == 5:
        research = False
        red = Red((14,15))
        blue = Blue((13,15))
        orange = Orange((12,15))
        pink = Pink((15,15))
        ghost.append(blue)
        ghost.append(red)
        ghost.append(orange)
        ghost.append(pink)


    game = Game(labyrinth, pacman, ghost, research)  # Khởi tạo

    clock = pygame.time.Clock()
    running = True
    game_over = False
    game_start = False
    game_start_time = pygame.time.get_ticks() + 4500
    
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
            elif event.type == ORANGE_EVENT_TYPE and not game_over and game_start:
                game.move_orange()  # Di chuyển riêng Orange
            elif event.type == PACMAN_EVENT and not game_over and game_start:
                game.update_direct_pacman()
            manager.process_events(event)
        
        game.direct_pacman()
        screen.fill((0, 0, 0))
        game.render(screen)
        screen.blit(logo, logo_rect.topleft)
        screen.blit(scrore_board, scrore_board_rect.topleft)
        pygame.draw.line(screen, (255, 215, 0), (WINDOW_SIZE[0] - 280, 0), (WINDOW_SIZE[0] - 280, WINDOW_SIZE[1]), 4)
        manager.update(time_delta)
        manager.draw_ui(screen)
        
        if game.check_win():
            #Âm thanh:
            pygame.mixer.music.pause()
            winning_sound = pygame.mixer.Sound("UI/sound/mom_i_did_it.mp3")
            winning_sound.set_volume(0.7)  # Điều chỉnh âm lượng
            winning_sound.play(0)
            # Hiển thị thông báo thắng
            win = pygame.transform.scale(pygame.image.load("UI/win.png"), (470, 300))
            win_rect = pygame.Rect(((WINDOW_SIZE[0] - 470) * 0.5 , (WINDOW_SIZE[1] - 300) * 0.5), (470, 300))
            screen.blit(win, win_rect.topleft)

            pygame.display.flip()
            pygame.time.wait(3000)  # Chờ 2 giây
            running = False  # Thoát vòng lặp để quay lại menu
        
        if game.check_lose():
            #Âm thanh:
            pygame.mixer.music.pause()
            dying_sound = pygame.mixer.Sound("UI/sound/dying.mp3")
            dying_sound.set_volume(0.7)  # Điều chỉnh âm lượng
            dying_sound.play(0)
            # Hiển thị thông báo thua
            lose = pygame.transform.scale(pygame.image.load("UI/lose.png"), (470, 300))
            lose_rect = pygame.Rect(((WINDOW_SIZE[0] - 470) * 0.5 , (WINDOW_SIZE[1] - 300) * 0.5), (470, 300))
            screen.blit(lose, lose_rect.topleft)

            pygame.display.flip()
            pygame.time.wait(2000)  # Chờ 2 giây
            running = False  # Thoát vòng lặp để quay lại menu
            pygame.mixer.music.pause()
        
        pygame.display.flip()
    
    # Sau khi thoát vòng lặp (thắng hoặc thua), quay lại menu
    load_menu()