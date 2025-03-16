import pygame
import math
from utils import find_direction
from characters import Pacman, Red, Pink, Blue, Orange, Point, Score
from labyrinth import total_stats

class Game:
    def __init__(self, labyrinth, pacman, ghosts, research=False):
        """Initialize game with labyrinth, Pacman, ghosts, and optional research mode."""
        self.labyrinth = labyrinth
        self.pacman = pacman
        self.ghosts = ghosts
        self.score = Score()
        points_positions = self.get_points_positions()
        self.points = [Point(pos) for pos in points_positions] if points_positions else []
        self.pink_next_moves = []
        self.research = research
        self.eating_sound = pygame.mixer.Sound("UI/sound/point_eaten.mp3")
        self.eating_sound.set_volume(0.5)
        self.sound_playing = False
        self.sound_timer = 0
        self.sound_duration = 400

    def get_points_positions(self):
        """Load point positions from file."""
        points = []
        with open("maps/point.txt", 'r') as file:
            for line in file:
                x, y = map(int, line.split())
                points.append((x, y))
        return points

    def render(self, screen):
        """Render game elements on the screen."""
        self.labyrinth.render(screen)
        self.pacman.render(screen)
        for ghost in self.ghosts:
            ghost.render(screen)
        for point in self.points:
            point.render(screen)
        self.score.render(screen)

    def direct_pacman(self):
        """Set Pacman's next direction based on key presses."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.pacman.set_next_dir('left')
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.pacman.set_next_dir('right')
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.pacman.set_next_dir('up')
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.pacman.set_next_dir('down')

    def update_direct_pacman(self):
        """Update Pacman's direction and position, handle point collection."""
        next_x, next_y = self.pacman.get_position()
        next_dir = self.pacman.get_next_dir()
        if next_dir == 'up' and self.labyrinth.is_free((next_x, next_y - 1)):
            self.pacman.set_curr_dir('up')
        if next_dir == 'down' and self.labyrinth.is_free((next_x, next_y + 1)):
            self.pacman.set_curr_dir('down')
        if next_dir == 'right' and self.labyrinth.is_free((next_x + 1, next_y)):
            self.pacman.set_curr_dir('right')
        if next_dir == 'left' and self.labyrinth.is_free((next_x - 1, next_y)):
            self.pacman.set_curr_dir('left')

        curr_dir = self.pacman.get_curr_dir()
        if curr_dir == 'up': next_y -= 1
        if curr_dir == 'down': next_y += 1
        if curr_dir == 'right': next_x += 1
        if curr_dir == 'left': next_x -= 1
        
        if self.labyrinth.is_free((next_x, next_y)):
            self.pacman.set_position((next_x, next_y))

        pacman_pos = self.pacman.get_position()
        for point in self.points:
            if not point.eaten and point.get_position() == pacman_pos:
                point.eaten = True
                self.score.increase(10)
                if not self.sound_playing:
                    self.eating_sound.play(0)
                    self.sound_playing = True
                    self.sound_timer = pygame.time.get_ticks()

        if self.sound_playing and pygame.time.get_ticks() - self.sound_timer >= self.sound_duration:
            self.sound_playing = False

    def get_ghost_position(self):
        """Return list of all ghost positions."""
        return [ghost.get_position() for ghost in self.ghosts]

    def move_ghosts(self):
        """Move all ghosts except Orange using respective algorithms."""
        for i, ghost in enumerate(self.ghosts):
            ghost_positions = self.get_ghost_position()
            target = self.pacman.get_position()
            start = ghost.get_position()
            ghost_type = type(ghost)
            
            if ghost_type == Blue:
                next_position = self.labyrinth.bfs(start, target, track_stats=self.research)
            elif ghost_type == Pink:
                if not self.pink_next_moves:
                    self.pink_next_moves = self.labyrinth.ids(start, target, track_stats=self.research)
                next_position = self.pink_next_moves.pop(0)
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
        """Move Orange ghost using UCS with collision avoidance."""
        for i, ghost in enumerate(self.ghosts):
            if type(ghost) == Orange:
                ghost_positions = self.get_ghost_position()
                target = self.pacman.get_position()
                start = ghost.get_position()
                other_ghost_positions = [pos for j, pos in enumerate(ghost_positions) if j != i]
                next_position = self.labyrinth.ucs(start, target, other_ghost_positions, track_stats=self.research)
                if next_position not in other_ghost_positions:
                    ghost.set_direction(find_direction(ghost.get_position(), next_position))
                    ghost.set_position(next_position)
                    ghost.update_image()
                break

    def check_win(self):
        """Check if Pacman has reached the finish tile without losing."""
        return not self.check_lose() and self.labyrinth.get_tile_id(self.pacman.get_position()) == self.labyrinth.finish_tile

    def check_lose(self):
        """Check if Pacman collides with any ghost; reset stats if true."""
        global total_stats
        if any(self.pacman.get_position() == ghost.get_position() for ghost in self.ghosts):
            print("Total stats:", total_stats)
            total_stats.update({'time': 0, 'memory': 0, 'nodes': 0, 'time_peak': 0, 'memory_peak': 0})
            return True
        return False