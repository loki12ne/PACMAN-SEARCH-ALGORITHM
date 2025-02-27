import pygame
from constants import TILE_SIZE
from collections import deque

class Labyrinth:
    def __init__(self, filename, free_tiles, finish_tile):
        self.map = []
        with open(f'maps/map.txt') as input_file:
            for line in input_file:
                self.map.append(list(map(int, line.split())))
        self.height = len(self.map)
        self.width = len(self.map[0])
        self.tile_size = TILE_SIZE
        self.free_tiles = free_tiles
        self.finish_tile = finish_tile

    def render(self, screen):
        colors = {0: (0, 0, 0), 1: (5, 5, 190), 2: (50, 50, 50)}
        for y in range(self.height):
            for x in range(self.width):
                rect = pygame.Rect(x * self.tile_size, y * self.tile_size,
                                   self.tile_size, self.tile_size)
                screen.fill(colors[self.get_tile_id((x, y))], rect)

    def get_tile_id(self, position):
        return self.map[position[1]][position[0]]

    def is_free(self, position):
        return self.get_tile_id(position) in self.free_tiles

    def find_path_step(self, start, target, direction):
        queue = deque([(start, [start])]) 
        visited = {start} 
        
        while queue:
            current, path = queue.popleft()
            if current == target:
                return path[1] if len(path) > 1 else start  
            
            x, y = current
            directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
            
            for dx, dy in directions:
                next_pos = (x + dx, y + dy)
                if (next_pos not in visited and 
                    0 <= next_pos[0] < self.width and 
                    0 <= next_pos[1] < self.height and 
                    self.is_free(next_pos)):
                    visited.add(next_pos)
                    queue.append((next_pos, path + [next_pos]))
        
        return start