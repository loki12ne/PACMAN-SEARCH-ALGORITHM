import pygame
from constants import TILE_SIZE
from collections import deque
import heapq

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
                rect = pygame.Rect(x * self.tile_size , y * self.tile_size,
                                   self.tile_size, self.tile_size)
                screen.fill(colors[self.get_tile_id((x, y))], rect)



    def get_tile_id(self, position):
        return self.map[position[1]][position[0]]

    def is_free(self, position):
        return self.get_tile_id(position) in self.free_tiles

    def bfs(self, start, target):
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
                if (next_pos not in visited and self._is_valid(next_pos)):
                    visited.add(next_pos)
                    queue.append((next_pos, path + [next_pos]))
        return start
    def _is_valid(self, pos):
        x, y = pos
        return (0 <= x < self.width and 0 <= y < self.height and self.is_free(pos))

    def ids(self, start, target, length_path):
        def ids_depth_limited(current, target, depth, path, visited):

            if len(path) > depth:  # Vượt quá độ sâu cho phép
                return None
            if current == target:
                return path  # Tìm thấy mục tiêu
            
            x, y = current
            directions = [(0, -1), (0, 1), (-1, 0), (1, 0) ]  # up, down, left, right

            for dx, dy in directions:
                next_pos = (x + dx, y + dy)
                if (next_pos not in visited and self._is_valid(next_pos)):
                    visited.add(next_pos)
                    result = ids_depth_limited(next_pos, target, depth, path + [next_pos], visited)
                    if result:
                        return result
            return None

        max_depth = self.width * self.height  
        for depth in range(1, max_depth + 1):
            visited = {start}
            path = [start]
            result = ids_depth_limited(start, target, depth, path, visited)
            if result:
                length_path = len(result) - 1  # Số bước thực tế (không tính start)
                if length_path < 5:
                    return [result[1]] if len(result) > 1 else [start]  # Trả về bước đầu tiên
                else:
                    length_path = int( length_path // 2)  
                    next_steps = result[1:length_path] if len(result) > 1 else [start]
                    return next_steps if len(next_steps) > 0 else [start]
        
        return start  # Không tìm thấy đường, đứng yên
     
    def ucs(self, start, target):
            queue = [(0, start, [start])]  # (cost, position, path)
            visited = set()
            costs = {start: 0}  # Chi phí từ start đến mỗi vị trí
            
            while queue:
                cost, current, path = heapq.heappop(queue)  # Lấy node có chi phí thấp nhất
                if current == target:
                    return path[1] if len(path) > 1 else start
                
                if current in visited:
                    continue
                visited.add(current)
                
                x, y = current
                directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
                
                for dx, dy in directions:
                    next_pos = (x + dx, y + dy)
                    if self._is_valid(next_pos) and next_pos not in visited:
                        new_cost = costs[current] + 1  # Chi phí mỗi bước là 1
                        if next_pos not in costs or new_cost < costs[next_pos]:
                            costs[next_pos] = new_cost
                            heapq.heappush(queue, (new_cost, next_pos, path + [next_pos]))
            
            return start
    def _heuristic(self, pos, target):
        return abs(pos[0] - target[0]) + abs(pos[1] - target[1])

    def a_star(self, start, target):
        queue = [(0, 0, start, [start])]  # (f_score, g_score, position, path)
        visited = set()
        g_scores = {start: 0}  # Chi phí thực tế từ start đến vị trí
        
        while queue:
            f_score, g_score, current, path = heapq.heappop(queue)
            if current == target:
                return path[1] if len(path) > 1 else start
            
            if current in visited:
                continue
            visited.add(current)
            
            x, y = current
            directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
            
            for dx, dy in directions:
                next_pos = (x + dx, y + dy)
                if self._is_valid(next_pos) and next_pos not in visited:
                    new_g_score = g_scores[current] + 1  
                    if next_pos not in g_scores or new_g_score < g_scores[next_pos]:
                        g_scores[next_pos] = new_g_score
                        h_score = self._heuristic(next_pos, target)
                        f_score = new_g_score + h_score
                        heapq.heappush(queue, (f_score, new_g_score, next_pos, path + [next_pos]))
        
        return start