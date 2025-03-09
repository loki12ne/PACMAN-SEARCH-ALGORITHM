import pygame
from constants import TILE_SIZE, GAME_EVENT_TYPE

class Pacman:
    def __init__(self, position):
        self.next_direction = ''
        self.current_direction = 'left'
        self.x, self.y = position
        self.delay = 100
        self.image = pygame.image.load(f'characters/pacman/{self.current_direction}1.png')
        self.image1 = pygame.transform.scale(self.image, (18, 18))
        self.count = 0
        pygame.time.set_timer(GAME_EVENT_TYPE, self.delay)

    def get_position(self):
        return self.x, self.y

    def set_position(self, position):
        self.x, self.y = position

    def get_curr_dir(self):
        return self.current_direction

    def get_next_dir(self):
        return self.next_direction

    def set_next_dir(self, direction):
        self.next_direction = direction

    def set_curr_dir(self, direction):
        self.current_direction = direction
        self.next_direction = ''

    def update_image(self):

        self.image = pygame.image.load(f'characters/pacman/{self.current_direction}{self.count % 3}.png')
        self.image1 = pygame.transform.scale(self.image, (18, 18))
        self.count += 1

    def render(self, screen):
        delta = (self.image1.get_width() - TILE_SIZE) // 2
        screen.blit(self.image1, (self.x * TILE_SIZE - delta, self.y * TILE_SIZE - delta))

class Red:
    def __init__(self, position):
        self.direction = 'up'
        self.x, self.y = position
        self.delay = 200
        self.image = pygame.image.load(f'characters/red/{self.direction}1.png')
        self.image1 = pygame.transform.scale(self.image, (18, 18))
        self.count = 0
        pygame.time.set_timer(GAME_EVENT_TYPE, self.delay)

    def get_position(self):
        return self.x, self.y

    def set_position(self, position):
        self.x, self.y = position

    def get_direction(self):
        return self.direction

    def set_direction(self, direction):
        self.direction = direction

    def update_image(self):
        if self.direction is None:
            self.direction = 'up'
        self.image = pygame.image.load(f'characters/red/{self.direction}{self.count % 2}.png')
        self.image1 = pygame.transform.scale(self.image, (18, 18))
        self.count += 1

    def render(self, screen):
        delta = (self.image1.get_width() - TILE_SIZE) // 2
        screen.blit(self.image1, (self.x * TILE_SIZE - delta, self.y * TILE_SIZE - delta))
    
class Pink:
    def __init__(self, position):
        self.direction = 'up'
        self.x, self.y = position
        self.delay = 200
        self.image = pygame.image.load(f'characters/pink/{self.direction}1.png')
        self.image1 = pygame.transform.scale(self.image, (18, 18))
        self.count = 0
        pygame.time.set_timer(GAME_EVENT_TYPE, self.delay)

    def get_position(self):
        return self.x, self.y

    def set_position(self, position):
        self.x, self.y = position

    def get_direction(self):
        return self.direction

    def set_direction(self, direction):
        self.direction = direction

    def update_image(self):
        if self.direction is None:
            self.direction = 'up'
        self.image = pygame.image.load(f'characters/pink/{self.direction}{self.count % 2}.png')
        self.image1 = pygame.transform.scale(self.image, (18, 18))
        self.count += 1

    def render(self, screen):
        delta = (self.image1.get_width() - TILE_SIZE) // 2
        screen.blit(self.image1, (self.x * TILE_SIZE - delta, self.y * TILE_SIZE - delta))

class Blue:
    def __init__(self, position):
        self.direction = 'up'
        self.x, self.y = position
        self.delay = 100
        self.image = pygame.image.load(f'characters/blue/{self.direction}1.png')
        self.image1 = pygame.transform.scale(self.image, (18, 18))
        self.count = 0
        pygame.time.set_timer(GAME_EVENT_TYPE, self.delay)

    def get_position(self):
        return self.x, self.y

    def set_position(self, position):
        self.x, self.y = position

    def get_direction(self):
        return self.direction

    def set_direction(self, direction):
        self.direction = direction

    def update_image(self):
        if self.direction is None:
            self.direction = 'up'
        self.image = pygame.image.load(f'characters/blue/{self.direction}{self.count % 2}.png')
        self.image1 = pygame.transform.scale(self.image, (18, 18))
        self.count += 1

    def render(self, screen):
        delta = (self.image1.get_width() - TILE_SIZE) // 2
        screen.blit(self.image1, (self.x * TILE_SIZE - delta, self.y * TILE_SIZE - delta))

class Orange:
    def __init__(self, position):
        self.direction = 'up'
        self.x, self.y = position
        self.delay = 200
        self.image = pygame.image.load(f'characters/orange/{self.direction}1.png')
        self.image1 = pygame.transform.scale(self.image, (18, 18))
        self.count = 0
        pygame.time.set_timer(GAME_EVENT_TYPE, self.delay)

    def get_position(self):
        return self.x, self.y

    def set_position(self, position):
        self.x, self.y = position

    def get_direction(self):
        return self.direction

    def set_direction(self, direction):
        self.direction = direction

    def update_image(self):
        if self.direction is None:
            self.direction = 'up'
        self.image = pygame.image.load(f'characters/orange/{self.direction}{self.count % 2}.png')
        self.image1 = pygame.transform.scale(self.image, (18, 18))
        self.count += 1

    def render(self, screen):
        delta = (self.image1.get_width() - TILE_SIZE) // 2
        screen.blit(self.image1, (self.x * TILE_SIZE - delta, self.y * TILE_SIZE - delta))

class Point:
    def __init__(self, position):
        self.x, self.y = position
        self.eaten = False 

    def get_position(self):
        return (self.x, self.y)

    def render(self, screen):
        if not self.eaten:
            center = (self.x * 18 + 9, self.y * 18 + 9) 
            pygame.draw.circle(screen, (255, 255, 0), center, 4)


class Score:
    def __init__(self, x= 10, y=10, font_size=30, color=(255, 255, 255)):
        self.score = 0
        self.font = pygame.font.Font(None, font_size)
        self.color = color
        self.x = x
        self.y = y

    def increase(self, points=10):
        """Tăng điểm số khi Pacman ăn điểm."""
        self.score += points

    def render(self, screen):
        """Hiển thị điểm số trên màn hình."""
        text = self.font.render(f"Score: {self.score}", True, self.color)
        screen.blit(text, (self.x, self.y))
