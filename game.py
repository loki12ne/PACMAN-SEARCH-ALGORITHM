import pygame
import math
from utils import find_direction

from characters import Pacman, Red, Pink, Blue, Orange, Point, Score

class Game:
    def __init__(self, labyrinth, pacman, ghosts, points_positions=None):
            self.labyrinth = labyrinth
            self.pacman = pacman
            self.ghosts = ghosts
            self.score = Score()
            points_positions = self.get_points_positions()
            self.points = [Point(pos) for pos in points_positions] if points_positions else []
            self.pink_next_moves = []  # Khai báo như thuộc tính của lớp
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
                next_position = self.labyrinth.bfs(start, target)
            elif ghost_type == Pink:
                if len(self.pink_next_moves) == 0:
                    self.pink_next_moves = self.labyrinth.ids(start, target, self.distance(self.pacman, ghost))
                next_position = self.pink_next_moves.pop(0)
            elif ghost_type == Orange:
                next_position = self.labyrinth.ucs(start, target)
            elif ghost_type == Red:
                next_position = self.labyrinth.a_star(start, target)

            other_ghost_positions = [pos for j, pos in enumerate(ghost_positions) if j != i]
            if next_position not in other_ghost_positions:
            # Nếu không có đụng độ, cập nhật hướng và vị trí
                ghost.set_direction(find_direction(ghost.get_position(), next_position))
                ghost.set_position(next_position)
                ghost.update_image()
        self.pacman.update_image()

    def check_win(self):
        return not self.check_lose() and self.labyrinth.get_tile_id(self.pacman.get_position()) == self.labyrinth.finish_tile

    def check_lose(self):
        return any(self.pacman.get_position() == ghost.get_position() for ghost in self.ghosts)