import pygame
import math
from utils import find_direction

from characters import Pacman, Red, Pink, Blue, Orange, Point, Score
from labyrinth import total_stats

class Game:
    def __init__(self, labyrinth, pacman, ghosts, research = False):
            self.labyrinth = labyrinth
            self.pacman = pacman
            self.ghosts = ghosts
            self.score = Score()
            points_positions = self.get_points_positions()
            self.points = [Point(pos) for pos in points_positions] if points_positions else []
            self.pink_next_moves = []  # Khai báo như thuộc tính của lớp

            self.research = research
            # Khởi tạo quản lý âm thanh ăn điểm
            self.eating_sound = pygame.mixer.Sound("UI/sound/point_eaten.mp3")
            self.eating_sound.set_volume(0.5)
            self.sound_playing = False  # Trạng thái âm thanh đang phát hay không
            self.sound_timer = 0  # Bộ đếm thời gian để kiểm soát thời gian phát
            self.sound_duration = 400  # Thời gian phát âm thanh (miligiây), điều chỉnh theo ý muốn

    def get_points_positions(self):
        points = []  
        with open("maps/point.txt", 'r') as file:
            # Đọc từng dòng trong file
            for line in file:
                # Tách dòng thành hai số, chuyển thành int
                x, y = map(int, line.split())
                points.append((x, y))  # Thêm cặp (x, y) vào danh sách

        return points
    def render(self, screen):
        self.labyrinth.render(screen)
        self.pacman.render(screen)
        for ghost in self.ghosts:
            ghost.render(screen)
        for point in self.points:
            point.render(screen)
        self.score.render(screen)

    def direct_pacman(self):
        if pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_a]:
            self.pacman.set_next_dir('left')
        if pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_d]:
            self.pacman.set_next_dir('right')
        if pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_w]:
            self.pacman.set_next_dir('up')
        if pygame.key.get_pressed()[pygame.K_DOWN] or pygame.key.get_pressed()[pygame.K_s]:
            self.pacman.set_next_dir('down')

    def update_direct_pacman(self):
        next_x, next_y = self.pacman.get_position()
        if self.pacman.get_next_dir() == 'up' and self.labyrinth.is_free((next_x, next_y - 1)):
            self.pacman.set_curr_dir('up')
        if self.pacman.get_next_dir() == 'down' and self.labyrinth.is_free((next_x, next_y + 1)):
            self.pacman.set_curr_dir('down')
        if self.pacman.get_next_dir() == 'right' and self.labyrinth.is_free((next_x + 1, next_y)):
            self.pacman.set_curr_dir('right')
        if self.pacman.get_next_dir() == 'left' and self.labyrinth.is_free((next_x - 1, next_y)):
            self.pacman.set_curr_dir('left')

        if self.pacman.get_curr_dir() == 'up': next_y -= 1
        if self.pacman.get_curr_dir() == 'down': next_y += 1
        if self.pacman.get_curr_dir() == 'right': next_x += 1
        if self.pacman.get_curr_dir() == 'left': next_x -= 1
        
        if self.labyrinth.is_free((next_x, next_y)):
            self.pacman.set_position((next_x, next_y))

        pacman_pos = self.pacman.get_position()
        for point in self.points:
                if not point.eaten and point.get_position() == pacman_pos:
                    point.eaten = True
                    self.score.increase(10)
                    if not self.sound_playing:
                        self.eating_sound.play(0)  # Phát âm thanh
                        self.sound_playing = True
                        self.sound_timer = pygame.time.get_ticks()  # Lấy thời gian hiện tại
                        

        # Cập nhật trạng thái âm thanh
        if self.sound_playing:
            current_time = pygame.time.get_ticks()
            if current_time - self.sound_timer >= self.sound_duration:
                self.sound_playing = False  # Đặt lại trạng thái khi âm thanh kết thúc

    def get_ghost_position(self):
        return [ghost.get_position() for ghost in self.ghosts]
    def distance(self, pacman, ghost):
        x1, y1 = pacman.get_position()
        x2, y2 = ghost.get_position()
        return math.sqrt((x1 - x2)**2) + ((y1 - y2)**2) // 1
    def move_ghosts(self):
        for i, ghost in enumerate(self.ghosts):
            ghost_positions = self.get_ghost_position()
            target = self.pacman.get_position()
            start = ghost.get_position()
            ghost_type = type(ghost)
            
            if ghost_type == Blue:
                next_position = self.labyrinth.bfs(start, target, track_stats=self.research )
            elif ghost_type == Pink:
                if len(self.pink_next_moves) == 0:
                    self.pink_next_moves = self.labyrinth.ids(start, target, track_stats=self.research )
                next_position = self.pink_next_moves.pop(0)
            # elif ghost_type == Orange:
            #     next_position = self.labyrinth.ucs(start, target)
            elif ghost_type == Red:
                next_position = self.labyrinth.a_star(start, target, track_stats=self.research)
            else:
                continue

            other_ghost_positions = [pos for j, pos in enumerate(ghost_positions) if j != i]
            if next_position not in other_ghost_positions:
                ghost.set_direction(find_direction(ghost.get_position(), next_position))
                ghost.set_position(next_position)
                ghost.update_image()
        self.pacman.update_image()

    def move_orange(self):
            for i, ghost in enumerate(self.ghosts):
                if type(ghost) == Orange:
                    ghost_positions = self.get_ghost_position()
                    target = self.pacman.get_position()
                    start = ghost.get_position()
                    other_ghost_positions = [pos for j, pos in enumerate(ghost_positions) if j != i]
                    next_position = self.labyrinth.ucs(start, target, other_ghost_positions, track_stats=self.research )
                    if next_position not in other_ghost_positions:
                        ghost.set_direction(find_direction(ghost.get_position(), next_position))
                        ghost.set_position(next_position)
                        ghost.update_image()
                    break



    def check_win(self):
        return not self.check_lose() and self.labyrinth.get_tile_id(self.pacman.get_position()) == self.labyrinth.finish_tile

    def check_lose(self):
        global total_stats
        if(any(self.pacman.get_position() == ghost.get_position() for ghost in self.ghosts)):
            print("Total stats:", total_stats)
            total_stats['time'] = 0
            total_stats['memory'] = 0
            total_stats['nodes'] = 0
            total_stats['time_peak'] = 0
            total_stats['memory_peak'] = 0
            return True
        return False