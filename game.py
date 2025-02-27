import pygame
from utils import find_direction

from characters import Pacman, Red


#from labyrinth import Labyrinth
#from characters import Pacman, Red, Pink, Blue, Orange

class GameLv1:
    def __init__(self, labyrinth, pacman, red):
        self.labyrinth = labyrinth
        self.pacman = pacman
        self.red = red

    def render(self, screen):
        self.labyrinth.render(screen)
        self.pacman.render(screen)
        self.red.render(screen)

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

    def move_red(self):
        target = self.pacman.get_position()
        next_position = self.labyrinth.find_path_step(self.red.get_position(), target, self.red.get_direction())
        self.red.set_direction(find_direction(self.red.get_position(), next_position))
        self.red.set_position(next_position)
        self.red.update_image()

    def check_win(self):
        return not self.check_lose() and self.labyrinth.get_tile_id(self.pacman.get_position()) == self.labyrinth.finish_tile

    def check_lose(self):
        return self.pacman.get_position() == self.red.get_position()
