import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Display settings
width, height = 800, 600
game_display = pygame.display.set_mode((width, height))
pygame.display.set_caption('Enhanced Snake Game')

# Colors
white = (255, 255, 255)
red = (213, 50, 80)
green = (0, 255, 0)

# Load and resize images
snake_head_img = pygame.image.load('images/snake_head.png').convert_alpha()
snake_head_img = pygame.transform.scale(snake_head_img, (20, 20))
snake_body_img = pygame.image.load('images/snake_body.png').convert_alpha()
snake_body_img = pygame.transform.scale(snake_body_img, (20, 20))
food_img = pygame.image.load('images/food.png').convert_alpha()
food_img = pygame.transform.scale(food_img, (20, 20))
background_img = pygame.image.load('images/background.png').convert()
background_img = pygame.transform.scale(background_img, (width, height))

# Sounds
eat_sound = pygame.mixer.Sound('assets/eat_sound.ogg')

# Font
font_style = pygame.font.Font('assets/custom_font.ttf', 50)

# Classes
class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [(width // 2, height // 2)]
        self.direction = random.choice([pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT])
        self.score = 0
        self.change_direction = self.direction  # Buffer to hold the next direction

    def draw(self, surface):
        for i, pos in enumerate(self.positions):
            img = snake_head_img if i == 0 else snake_body_img
            surface.blit(img, pos)

    def move(self):
        if self.change_direction != self.direction:
            self.direction = self.change_direction  # Update direction from buffer
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
        self.change_direction = self.direction

    def eat(self):
        self.length += 1
        self.score += 10
        eat_sound.play()

    def update_direction(self, new_direction):
        # Check if the new direction is a valid turn
        if new_direction == pygame.K_UP and self.direction != pygame.K_DOWN:
            self.change_direction = new_direction
        elif new_direction == pygame.K_DOWN and self.direction != pygame.K_UP:
            self.change_direction = new_direction
        elif new_direction == pygame.K_LEFT and self.direction != pygame.K_RIGHT:
            self.change_direction = new_direction
        elif new_direction == pygame.K_RIGHT and self.direction != pygame.K_LEFT:
            self.change_direction = new_direction


    def get_head_position(self):
        return self.positions[0]



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


def pause_menu(surface):
    paused = True
    pause_text = font_style.render("PAUSED", True, white)
    resume_text = font_style.render("Press 'R' to resume or 'Q' to quit", True, white)
    text_rect = pause_text.get_rect(center=(width // 2, height // 2 - 50))
    options_rect = resume_text.get_rect(center=(width // 2, height // 2 + 50))
    while paused:
        surface.blit(pause_text, text_rect)
        surface.blit(resume_text, options_rect)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Resume
                    paused = False
                elif event.key == pygame.K_q:  # Quit
                    pygame.quit()
                    sys.exit()

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
                elif event.key == pygame.K_p:
                    pause_menu(game_display)  # Activate pause menu
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
