import pygame
from constants import TILE_SIZE
from collections import deque
import heapq
import time
import sys

# Biến toàn cục để lưu tổng số liệu thống kê
total_stats = {
    'time': 0,
    'memory': 0,
    'nodes': 0,
    'time_peak': 0,
    'memory_peak': 0
}

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
        # Biến để lưu trữ số liệu thống kê cho từng thuật toán
        self.stats = {
            'bfs': {'time': 0, 'memory': 0, 'nodes': 0},
            'ids': {'time': 0, 'memory': 0, 'nodes': 0},
            'ucs': {'time': 0, 'memory': 0, 'nodes': 0},
            'a_star': {'time': 0, 'memory': 0, 'nodes': 0}
        }

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

    def _is_valid(self, pos):
        x, y = pos
        return (0 <= x < self.width and 0 <= y < self.height and self.is_free(pos))

    def _track_performance(self, algorithm_name, start_time, queue, visited, expanded_nodes, costs=None):
        """Hàm hỗ trợ để tính toán và lưu trữ số liệu thống kê"""
        global total_stats  # Sử dụng biến toàn cục
        
        end_time = time.time()
        memory_usage = sys.getsizeof(queue) + sys.getsizeof(visited)
        if costs:
            memory_usage += sys.getsizeof(costs)
        
        # Lưu số liệu cho thuật toán cụ thể
        self.stats[algorithm_name]['time'] = end_time - start_time
        self.stats[algorithm_name]['memory'] = memory_usage
        self.stats[algorithm_name]['nodes'] = expanded_nodes
        
        # Cộng dồn vào total_stats
        total_stats['time_peak'] = max(total_stats['time_peak'], end_time - start_time)
        total_stats['memory_peak'] = max(total_stats['memory_peak'], memory_usage)
        total_stats['time'] += end_time - start_time
        total_stats['memory'] += memory_usage
        total_stats['nodes'] += expanded_nodes
        
        # print(f"{algorithm_name.upper()} - Search time: {end_time - start_time:.4f}s, "
        #       f"Memory usage: {memory_usage} bytes, "
        #       f"Expanded nodes: {expanded_nodes}")

    def bfs(self, start, target, track_stats=False):
        start_time = time.time() if track_stats else None
        queue = deque([(start, [start])])
        visited = {start}
        expanded_nodes = 0
        
        while queue:
            current, path = queue.popleft()
            expanded_nodes += 1
            
            if current == target:
                if track_stats:
                    self._track_performance('bfs', start_time, queue, visited, expanded_nodes)
                return path[1] if len(path) > 1 else start
            
            x, y = current
            directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
            
            for dx, dy in directions:
                next_pos = (x + dx, y + dy)
                if next_pos not in visited and self._is_valid(next_pos):
                    visited.add(next_pos)
                    queue.append((next_pos, path + [next_pos]))
        
        if track_stats:
            self._track_performance('bfs', start_time, queue, visited, expanded_nodes)
        return start

    def ids(self, start, target, track_stats=False):
        start_time = time.time() if track_stats else None
        expanded_nodes = 0
        
        def dls(current, target, depth, path, visited):
            nonlocal expanded_nodes
            if len(path) > depth:
                return None
            if current == target:
                return path  # Trả về trực tiếp danh sách đường đi
            expanded_nodes += 1
            x, y = current
            directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
            
            for dx, dy in directions:
                next_pos = (x + dx, y + dy)
                if (next_pos not in visited and self._is_valid(next_pos)):
                    visited.add(next_pos)
                    result = dls(next_pos, target, depth, path + [next_pos], visited)
                    if result:  # Nếu tìm thấy đường, trả về ngay
                        return result
                    visited.remove(next_pos)
            return None  # Không tìm thấy đường trong depth này

        max_depth = self.width * self.height
        for depth in range(1, max_depth + 1):
            visited = {start}  # Reset visited mỗi lần tìm với độ sâu mới
            path = [start]
            result = dls(start, target, depth, path, visited)
            if result:
                if track_stats:
                    self._track_performance('ids', start_time, [], visited, expanded_nodes)

                length_path = len(result) - 1  # Số bước thực tế (không tính start)
                if length_path < 5:
                    return [result[1]] if len(result) > 1 else [start]  # Trả về toàn bộ bước trừ start
                else:
                    mid_index = int(length_path // 2)
                    next_steps = result[1:] if len(result) > 1 else [start]
                    return next_steps if len(next_steps) > 0 else [start]  # Chọn phần giữa đường đi

        if track_stats:
            self._track_performance('ids', start_time, [], visited, expanded_nodes)
        
        return start  

    def ucs(self, start, target, special_positions=None, track_stats=False):
        if special_positions is None:
            special_positions = []
        
        start_time = time.time() if track_stats else None
        queue = [(0, start, [start], None)]
        visited = set()
        costs = {start: 0}
        expanded_nodes = 0
        
        while queue:
            cost, current, path, prev_direction = heapq.heappop(queue)
            if current == target:
                if track_stats:
                    self._track_performance('ucs', start_time, queue, visited, expanded_nodes, costs)
                return path[1] if len(path) > 1 else start
            
            if current in visited:
                continue
            visited.add(current)
            expanded_nodes += 1
            
            x, y = current
            directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
            
            for dx, dy in directions:
                next_pos = (x + dx, y + dy)
                if self._is_valid(next_pos) and next_pos not in visited:
                    if prev_direction is None:
                        step_cost = 1
                    elif (dx, dy) == prev_direction:
                        step_cost = 1
                    else:
                        step_cost = 10
                    
                    if next_pos in special_positions:
                        step_cost += 10
                    
                    new_cost = costs[current] + step_cost
                    if next_pos not in costs or new_cost < costs[next_pos]:
                        costs[next_pos] = new_cost
                        heapq.heappush(queue, (new_cost, next_pos, path + [next_pos], (dx, dy)))
        
        if track_stats:
            self._track_performance('ucs', start_time, queue, visited, expanded_nodes, costs)
        return start

    def _heuristic(self, pos, target):
        return abs(pos[0] - target[0]) + abs(pos[1] - target[1])

    def a_star(self, start, target, track_stats=False):
        start_time = time.time() if track_stats else None
        queue = [(0, 0, start, [start])]
        visited = set()
        g_scores = {start: 0}
        expanded_nodes = 0
        
        while queue:
            f_score, g_score, current, path = heapq.heappop(queue)
            if current == target:
                if track_stats:
                    self._track_performance('a_star', start_time, queue, visited, expanded_nodes, g_scores)
                return path[1] if len(path) > 1 else start
            
            if current in visited:
                continue
            visited.add(current)
            expanded_nodes += 1
            
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
        
        if track_stats:
            self._track_performance('a_star', start_time, queue, visited, expanded_nodes, g_scores)
        return start

    def get_stats(self):
        """Trả về số liệu thống kê của các thuật toán"""
        return self.stats

    def get_total_stats(self):
        """Trả về tổng số liệu thống kê từ biến toàn cục"""
        global total_stats
        return total_stats