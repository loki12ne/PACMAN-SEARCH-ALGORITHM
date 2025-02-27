import pygame
from utils import find_direction

from characters import Pacman, Red, Pink, Blue, Orange


class Game:
    def __init__(self, labyrinth, pacman, ghosts):
            self.labyrinth = labyrinth
            self.pacman = pacman
            self.ghosts = ghosts
        
    def render(self, screen):
        self.labyrinth.render(screen)
        self.pacman.render(screen)
        for ghost in self.ghosts:
            ghost.render(screen)

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

    def move_ghosts(self):
        for ghost in self.ghosts:
            target = self.pacman.get_position()
            start = ghost.get_position()
            ghost_type = type(ghost)
            if(ghost_type == Blue):
                next_position = self.labyrinth.bfs(start, target, ghost.get_direction())
            if(ghost_type == Pink):
                next_position = self.labyrinth.dfs(start, target, ghost.get_direction())
            if(ghost_type == Orange):
                next_position = self.labyrinth.ucs(start, target, ghost.get_direction())
            if(ghost_type == Red):
                next_position = self.labyrinth.a_star(start, target, ghost.get_direction())
            ghost.set_direction(find_direction(ghost.get_position(), next_position))
            ghost.set_position(next_position)
            ghost.update_image()

    def check_win(self):
        return not self.check_lose() and self.labyrinth.get_tile_id(self.pacman.get_position()) == self.labyrinth.finish_tile

    def check_lose(self):
        return any(self.pacman.get_position() == ghost.get_position() for ghost in self.ghosts)