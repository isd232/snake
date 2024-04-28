import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Display settings
width, height = 800, 600
game_display = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Game')

# Colors
white = (255, 255, 255)
red = (213, 50, 80)
green = (0, 255, 0)

# Load and resize images
snake_head_img = pygame.image.load('snake_head.png').convert_alpha()
snake_head_img = pygame.transform.scale(snake_head_img, (20, 20))
snake_body_img = pygame.image.load('snake_body.png').convert_alpha()
snake_body_img = pygame.transform.scale(snake_body_img, (20, 20))
food_img = pygame.image.load('food.png').convert_alpha()
food_img = pygame.transform.scale(food_img, (20, 20))
background_img = pygame.image.load('background.png').convert()
background_img = pygame.transform.scale(background_img, (width, height))

# Sounds
eat_sound = pygame.mixer.Sound('eat_sound.ogg')

# Font
font_style = pygame.font.Font('custom_font.ttf', 50)


# Classes
class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [(width // 2, height // 2)]
        self.direction = random.choice([pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT])
        self.score = 0

    def draw(self, surface):
        for i, pos in enumerate(self.positions):
            img = snake_head_img if i == 0 else snake_body_img
            surface.blit(img, pos)

    def move(self):
        cur = self.positions[0]
        x, y = cur
        if self.direction == pygame.K_UP:
            y -= 20
        elif self.direction == pygame.K_DOWN:
            y += 20
        elif self.direction == pygame.K_LEFT:
            x -= 20
        elif self.direction == pygame.K_RIGHT:
            x += 20
        new_head = (x % width, y % height)
        if new_head in self.positions[1:]:
            self.reset()
        else:
            self.positions.insert(0, new_head)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        self.length = 1
        self.positions = [(width // 2, height // 2)]
        self.score = 0
        self.direction = random.choice([pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT])

    def eat(self):
        self.length += 1
        self.score += 10
        eat_sound.play()

    def get_head_position(self):
        return self.positions[0]

    def update_direction(self, new_direction):
        # Prevent the snake from reversing
        if new_direction == pygame.K_UP and self.direction != pygame.K_DOWN:
            self.direction = new_direction
        elif new_direction == pygame.K_DOWN and self.direction != pygame.K_UP:
            self.direction = new_direction
        elif new_direction == pygame.K_LEFT and self.direction != pygame.K_RIGHT:
            self.direction = new_direction
        elif new_direction == pygame.K_RIGHT and self.direction != pygame.K_LEFT:
            self.direction = new_direction



class Food:
    def __init__(self):
        self.position = (0, 0)
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, (width - 20) // 20) * 20, random.randint(0, (height - 20) // 20) * 20)

    def draw(self, surface):
        surface.blit(food_img, self.position)


# Game functions
def draw_background(surface):
    surface.blit(background_img, (0, 0))


def draw_score(surface, score):
    score_text = font_style.render(f"Score: {score}", True, white)
    surface.blit(score_text, (10, 10))


def game_loop():
    clock = pygame.time.Clock()
    snake = Snake()
    food = Food()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False  # Quit the game
                elif event.key == pygame.K_r:
                    snake.reset()  # Reset the game
                    food.randomize_position()  # Reset food position
                elif event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                    snake.update_direction(event.key)

        snake.move()
        if snake.get_head_position() == food.position:
            snake.eat()
            food.randomize_position()

        draw_background(game_display)
        snake.draw(game_display)
        food.draw(game_display)
        draw_score(game_display, snake.score)

        pygame.display.update()
        clock.tick(15)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    game_loop()
