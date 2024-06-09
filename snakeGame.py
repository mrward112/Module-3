import pygame
import random

# Initialize Pygame
pygame.init()

# Define constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Define colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
BLACK = (0, 0, 0)

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

# Define the snake class
class Snake:
    def __init__(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT])
        self.grow = False
        self.buff_active = False
        self.buff_timer = 0
        self.speed_buff_active = False
        self.speed_buff_timer = 0
        self.speed = 10

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if (self.direction == pygame.K_UP and point != pygame.K_DOWN) or \
           (self.direction == pygame.K_DOWN and point != pygame.K_UP) or \
           (self.direction == pygame.K_LEFT and point != pygame.K_RIGHT) or \
           (self.direction == pygame.K_RIGHT and point != pygame.K_LEFT):
            self.direction = point

    def move(self):
        cur = self.get_head_position()
        x, y = cur
        if self.direction == pygame.K_UP:
            y -= 1
        elif self.direction == pygame.K_DOWN:
            y += 1
        elif self.direction == pygame.K_LEFT:
            x -= 1
        elif self.direction == pygame.K_RIGHT:
            x += 1
        new = (x, y)
        
        if new in self.positions:
            if not self.buff_active:
                self.reset()
        else:
            if x < 0:
                x = GRID_WIDTH - 1
            elif x >= GRID_WIDTH:
                x = 0
            elif y < 0:
                y = GRID_HEIGHT - 1
            elif y >= GRID_HEIGHT:
                y = 0
            new = (x, y)
            
            self.positions.insert(0, new)
            if not self.grow:
                self.positions.pop()
            self.grow = False

    def reset(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT])
        self.grow = False
        self.buff_active = False
        self.buff_timer = 0
        self.speed_buff_active = False
        self.speed_buff_timer = 0
        self.speed = 10

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                    self.turn(event.key)

    def draw(self, surface):
        for p in self.positions:
            r = pygame.Rect((p[0] * GRID_SIZE, p[1] * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, GREEN, r)
            pygame.draw.rect(surface, BLACK, r, 1)

    def update_buff(self):
        if self.buff_active:
            self.buff_timer -= 1
            if self.buff_timer <= 0:
                self.buff_active = False
        if self.speed_buff_active:
            self.speed_buff_timer -= 1
            if self.speed_buff_timer <= 0:
                self.speed_buff_active = False
                self.speed = 10

# Define the food class
class Food:
    def __init__(self):
        self.position = (0, 0)
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

    def draw(self, surface):
        r = pygame.Rect((self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, RED, r)
        pygame.draw.rect(surface, BLACK, r, 1)

# Define the buff class
class Buff:
    def __init__(self, color):
        self.position = (0, 0)
        self.color = color
        self.active = False
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), (random.randint(0, GRID_HEIGHT - 1)))

    def draw(self, surface):
        if self.active:
            r = pygame.Rect((self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, BLACK, r, 1)

# Main game loop
def main():
    clock = pygame.time.Clock()
    snake = Snake()
    food = Food()
    blue_buff = Buff(BLUE)
    purple_buff = Buff(PURPLE)
    score = 0

    while True:
        clock.tick(snake.speed)
        snake.handle_keys()
        snake.move()
        if snake.get_head_position() == food.position:
            snake.grow = True
            score += 1
            food.randomize_position()
            if score % 3 == 0 and not blue_buff.active:
                blue_buff.randomize_position()
                blue_buff.active = True
            if score % 7 == 0 and not purple_buff.active:
                purple_buff.randomize_position()
                purple_buff.active = True
        if snake.get_head_position() == blue_buff.position and blue_buff.active:
            snake.buff_active = True
            snake.buff_timer = 50  # Buff duration in ticks
            blue_buff.active = False
        if snake.get_head_position() == purple_buff.position and purple_buff.active:
            snake.speed_buff_active = True
            snake.speed_buff_timer = 50  # Buff duration in ticks
            snake.speed = 5  # Slower speed
            purple_buff.active = False

        snake.update_buff()
        screen.fill(WHITE)
        snake.draw(screen)
        food.draw(screen)
        blue_buff.draw(screen)
        purple_buff.draw(screen)
        pygame.display.update()

if __name__ == "__main__":
    main()
