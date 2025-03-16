import pygame
from constants import TILE_SIZE, GAME_EVENT_TYPE, WINDOW_SIZE, ORANGE_EVENT_TYPE

class Pacman:
    def __init__(self, position):
        """Initialize Pacman with starting position and default settings."""
        self.next_direction = ''
        self.current_direction = 'left'
        self.x, self.y = position
        self.delay = 150
        self.image = pygame.image.load(f'characters/pacman/{self.current_direction}1.png')
        self.image1 = pygame.transform.scale(self.image, (18, 18))
        self.count = 0
        pygame.time.set_timer(GAME_EVENT_TYPE, self.delay)

    def get_position(self):
        """Return current position as (x, y)."""
        return self.x, self.y

    def set_position(self, position):
        """Set new position from given (x, y)."""
        self.x, self.y = position

    def get_curr_dir(self):
        """Return current direction."""
        return self.current_direction

    def get_next_dir(self):
        """Return next direction."""
        return self.next_direction

    def set_next_dir(self, direction):
        """Set next direction to move."""
        self.next_direction = direction

    def set_curr_dir(self, direction):
        """Set current direction and clear next direction."""
        self.current_direction = direction
        self.next_direction = ''

    def update_image(self):
        """Update Pacman image based on direction and animation frame."""
        self.image = pygame.image.load(f'characters/pacman/{self.current_direction}{self.count % 3}.png')
        self.image1 = pygame.transform.scale(self.image, (18, 18))
        self.count += 1

    def render(self, screen):
        """Render Pacman on the screen."""
        delta = (self.image1.get_width() - TILE_SIZE) // 2
        screen.blit(self.image1, (self.x * TILE_SIZE - delta, self.y * TILE_SIZE - delta))

class Red:
    def __init__(self, position):
        """Initialize Red ghost with starting position and default settings."""
        self.direction = 'up'
        self.x, self.y = position
        self.delay = 200
        self.image = pygame.image.load(f'characters/red/{self.direction}1.png')
        self.image1 = pygame.transform.scale(self.image, (18, 18))
        self.count = 0
        pygame.time.set_timer(GAME_EVENT_TYPE, self.delay)

    def get_position(self):
        """Return current position as (x, y)."""
        return self.x, self.y

    def set_position(self, position):
        """Set new position from given (x, y)."""
        self.x, self.y = position

    def get_direction(self):
        """Return current direction."""
        return self.direction

    def set_direction(self, direction):
        """Set new direction."""
        self.direction = direction

    def update_image(self):
        """Update Red ghost image based on direction and animation frame."""
        if self.direction is None:
            self.direction = 'up'
        self.image = pygame.image.load(f'characters/red/{self.direction}{self.count % 2}.png')
        self.image1 = pygame.transform.scale(self.image, (18, 18))
        self.count += 1

    def render(self, screen):
        """Render Red ghost on the screen."""
        delta = (self.image1.get_width() - TILE_SIZE) // 2
        screen.blit(self.image1, (self.x * TILE_SIZE - delta, self.y * TILE_SIZE - delta))

class Pink:
    def __init__(self, position):
        """Initialize Pink ghost with starting position and default settings."""
        self.direction = 'up'
        self.x, self.y = position
        self.delay = 200
        self.image = pygame.image.load(f'characters/pink/{self.direction}1.png')
        self.image1 = pygame.transform.scale(self.image, (18, 18))
        self.count = 0
        pygame.time.set_timer(GAME_EVENT_TYPE, self.delay)

    def get_position(self):
        """Return current position as (x, y)."""
        return self.x, self.y

    def set_position(self, position):
        """Set new position from given (x, y)."""
        self.x, self.y = position

    def get_direction(self):
        """Return current direction."""
        return self.direction

    def set_direction(self, direction):
        """Set new direction."""
        self.direction = direction

    def update_image(self):
        """Update Pink ghost image based on direction and animation frame."""
        if self.direction is None:
            self.direction = 'up'
        self.image = pygame.image.load(f'characters/pink/{self.direction}{self.count % 2}.png')
        self.image1 = pygame.transform.scale(self.image, (18, 18))
        self.count += 1

    def render(self, screen):
        """Render Pink ghost on the screen."""
        delta = (self.image1.get_width() - TILE_SIZE) // 2
        screen.blit(self.image1, (self.x * TILE_SIZE - delta, self.y * TILE_SIZE - delta))

class Blue:
    def __init__(self, position):
        """Initialize Blue ghost with starting position and default settings."""
        self.direction = 'up'
        self.x, self.y = position
        self.delay = 200
        self.image = pygame.image.load(f'characters/blue/{self.direction}1.png')
        self.image1 = pygame.transform.scale(self.image, (18, 18))
        self.count = 0
        pygame.time.set_timer(GAME_EVENT_TYPE, self.delay)

    def get_position(self):
        """Return current position as (x, y)."""
        return self.x, self.y

    def set_position(self, position):
        """Set new position from given (x, y)."""
        self.x, self.y = position

    def get_direction(self):
        """Return current direction."""
        return self.direction

    def set_direction(self, direction):
        """Set new direction."""
        self.direction = direction

    def update_image(self):
        """Update Blue ghost image based on direction and animation frame."""
        if self.direction is None:
            self.direction = 'up'
        self.image = pygame.image.load(f'characters/blue/{self.direction}{self.count % 2}.png')
        self.image1 = pygame.transform.scale(self.image, (18, 18))
        self.count += 1

    def render(self, screen):
        """Render Blue ghost on the screen."""
        delta = (self.image1.get_width() - TILE_SIZE) // 2
        screen.blit(self.image1, (self.x * TILE_SIZE - delta, self.y * TILE_SIZE - delta))

class Orange:
    def __init__(self, position):
        """Initialize Orange ghost with starting position and default settings."""
        self.direction = 'up'
        self.x, self.y = position
        self.delay = 200
        self.prev_direction = None
        self.image = pygame.image.load(f'characters/orange/{self.direction}1.png')
        self.image1 = pygame.transform.scale(self.image, (18, 18))
        self.count = 0
        pygame.time.set_timer(ORANGE_EVENT_TYPE, self.delay)

    def get_position(self):
        """Return current position as (x, y)."""
        return self.x, self.y

    def set_position(self, position):
        """Set new position from given (x, y)."""
        self.x, self.y = position

    def get_direction(self):
        """Return current direction."""
        return self.direction

    def set_direction(self, direction):
        """Set new direction and adjust delay based on movement pattern."""
        if self.prev_direction is not None:
            if direction == self.prev_direction:
                self.delay = int(self.delay * 0.9)
            else:
                self.delay = 250
            self.delay = max(self.delay, 125)
            pygame.time.set_timer(ORANGE_EVENT_TYPE, self.delay)
        self.prev_direction = self.direction
        self.direction = direction

    def update_image(self):
        """Update Orange ghost image based on direction and animation frame."""
        if self.direction is None:
            self.direction = 'up'
        self.image = pygame.image.load(f'characters/orange/{self.direction}{self.count % 2}.png')
        self.image1 = pygame.transform.scale(self.image, (18, 18))
        self.count += 1

    def render(self, screen):
        """Render Orange ghost on the screen."""
        delta = (self.image1.get_width() - TILE_SIZE) // 2
        screen.blit(self.image1, (self.x * TILE_SIZE - delta, self.y * TILE_SIZE - delta))

class Point:
    def __init__(self, position):
        """Initialize a collectible point at the given position."""
        self.x, self.y = position
        self.eaten = False

    def get_position(self):
        """Return point position as (x, y)."""
        return (self.x, self.y)

    def render(self, screen):
        """Render point on the screen if not eaten."""
        if not self.eaten:
            center = (self.x * 18 + 9, self.y * 18 + 9)
            pygame.draw.circle(screen, (255, 255, 0), center, 4)

class Score:
    def __init__(self, x=10, y=10, font_size=36, color=(255, 255, 255)):
        """Initialize score display with given position, font size, and color."""
        self.score = 0
        self.font = pygame.font.Font(None, font_size)
        self.color = color
        self.x = x
        self.y = y

    def increase(self, points=10):
        """Increase score by specified points."""
        self.score += points

    def render(self, screen):
        """Render score text on the screen."""
        score_text = self.font.render(str(self.score), True, self.color)
        screen.blit(score_text, (WINDOW_SIZE[0] - 230 + 230 * 0.2, 144 + 105 * 0.6))