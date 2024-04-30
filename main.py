import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Display settings
width, height = 800, 600
info_width = 200  # Width for the score and high scores display
game_display = pygame.display.set_mode((width + info_width, height))
pygame.display.set_caption('Enhanced Snake Game')

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

# Load images
snake_images = {
    'head_up': pygame.image.load('images/head_up.png').convert_alpha(),
    'head_down': pygame.image.load('images/head_down.png').convert_alpha(),
    'head_left': pygame.image.load('images/head_left.png').convert_alpha(),
    'head_right': pygame.image.load('images/head_right.png').convert_alpha(),
    'tail_up': pygame.image.load('images/tail_up.png').convert_alpha(),
    'tail_down': pygame.image.load('images/tail_down.png').convert_alpha(),
    'tail_left': pygame.image.load('images/tail_left.png').convert_alpha(),
    'tail_right': pygame.image.load('images/tail_right.png').convert_alpha(),
    'body_horizontal': pygame.image.load('images/body_horizontal.png').convert_alpha(),
    'body_vertical': pygame.image.load('images/body_vertical.png').convert_alpha(),
    'body_topleft': pygame.image.load('images/body_topleft.png').convert_alpha(),
    'body_topright': pygame.image.load('images/body_topright.png').convert_alpha(),
    'body_bottomleft': pygame.image.load('images/body_bottomleft.png').convert_alpha(),
    'body_bottomright': pygame.image.load('images/body_bottomright.png').convert_alpha(),
    'food': pygame.image.load('images/food.png').convert_alpha()
}
background_img = pygame.image.load('images/background.png').convert()
background_img = pygame.transform.scale(background_img, (width, height))

# Sounds
eat_sound = pygame.mixer.Sound('assets/eat_sound.ogg')

# Font
font_style = pygame.font.Font('assets/custom_font.ttf', 50)

# High Score Functions
def save_high_score(new_score):
    try:
        with open('high_scores.txt', 'r+') as file:
            scores = [int(line.strip()) for line in file.readlines()]
            scores.append(new_score)
            scores = sorted(scores, reverse=True)[:5]
            file.seek(0)
            file.truncate()
            for score in scores:
                file.write(f"{score}\n")
    except FileNotFoundError:
        with open('high_scores.txt', 'w') as file:
            file.write(f"{new_score}\n")

def load_high_scores():
    try:
        with open('high_scores.txt', 'r') as file:
            return [int(line.strip()) for line in file.readlines()]
    except FileNotFoundError:
        return []

# Snake Class
class Snake:
    def __init__(self, game_display):
        self.game_display = game_display
        self.length = 1
        self.positions = [(width // 2, height // 2)]  # Start in the center
        self.direction = random.choice([pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT])
        self.score = 0
        self.change_direction = self.direction

    def draw(self):
        for i, pos in enumerate(self.positions):
            segment_image = None
            if i == 0:  # Head segment
                if len(self.positions) > 1:
                    next_segment = self.positions[i + 1]
                    if next_segment[1] < pos[1]:  # Moving upwards
                        segment_image = snake_images['head_up']
                    elif next_segment[1] > pos[1]:  # Moving downwards
                        segment_image = snake_images['head_down']
                    elif next_segment[0] > pos[0]:  # Moving right
                        segment_image = snake_images['head_right']
                    elif next_segment[0] < pos[0]:  # Moving left
                        segment_image = snake_images['head_left']
                else:
                    # If the snake has only one segment, choose head image based on current direction
                    direction_map = {
                        pygame.K_UP: 'head_up',
                        pygame.K_DOWN: 'head_down',
                        pygame.K_LEFT: 'head_left',
                        pygame.K_RIGHT: 'head_right'
                    }
                    segment_image = snake_images[direction_map[self.direction]]
            elif i == len(self.positions) - 1:  # Tail segment
                prev_segment = self.positions[i - 1]
                if prev_segment[1] < pos[1]:  # Tail follows upward movement
                    segment_image = snake_images['tail_up']
                elif prev_segment[1] > pos[1]:  # Tail follows downward movement
                    segment_image = snake_images['tail_down']
                elif prev_segment[0] > pos[0]:  # Tail follows movement to the right
                    segment_image = snake_images['tail_right']
                elif prev_segment[0] < pos[0]:  # Tail follows movement to the left
                    segment_image = snake_images['tail_left']
            else:  # Body segments
                prev_segment = self.positions[i - 1]
                next_segment = self.positions[i + 1]
                if prev_segment[0] == next_segment[0]:  # Vertical alignment
                    segment_image = snake_images['body_vertical']
                elif prev_segment[1] == next_segment[1]:  # Horizontal alignment
                    segment_image = snake_images['body_horizontal']
                else:  # Corner segments
                    # Determine the direction of the bend
                    if (prev_segment[0] == pos[0] and next_segment[1] == pos[1]) or (
                            next_segment[0] == pos[0] and prev_segment[1] == pos[1]):
                        if (prev_segment[1] < pos[1] and next_segment[0] > pos[0]) or (
                                next_segment[1] < pos[1] and prev_segment[0] > pos[0]):
                            segment_image = snake_images['body_topright']
                        elif (prev_segment[1] > pos[1] and next_segment[0] > pos[0]) or (
                                next_segment[1] > pos[1] and prev_segment[0] > pos[0]):
                            segment_image = snake_images['body_bottomright']
                        elif (prev_segment[1] > pos[1] and next_segment[0] < pos[0]) or (
                                next_segment[1] > pos[1] and prev_segment[0] < pos[0]):
                            segment_image = snake_images['body_bottomleft']
                        elif (prev_segment[1] < pos[1] and next_segment[0] < pos[0]) or (
                                next_segment[1] < pos[1] and prev_segment[0] < pos[0]):
                            segment_image = snake_images['body_topleft']

            # Blit the segment image to the display
            if segment_image:
                self.game_display.blit(segment_image, pos)

    def move(self):
        head_x, head_y = self.positions[0]
        if self.change_direction == pygame.K_UP:
            head_y -= 20
        elif self.change_direction == pygame.K_DOWN:
            head_y += 20
        elif self.change_direction == pygame.K_LEFT:
            head_x -= 20
        elif self.change_direction == pygame.K_RIGHT:
            head_x += 20
        head_x = head_x % width
        head_y = head_y % height
        new_head = (head_x, head_y)
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()

    def eat(self):
        self.length += 1
        self.score += 10
        eat_sound.play()

    def get_head_position(self):
        return self.positions[0]

# Food Class
class Food:
    def __init__(self, game_display, snake_positions):
        self.game_display = game_display
        self.position = self.randomize_position(snake_positions)

    def randomize_position(self, snake_positions):
        while True:
            new_position = (random.randrange(20, width - 20, 20), random.randrange(20, height - 20, 20))
            if new_position not in snake_positions:
                return new_position

    def draw(self):
        self.game_display.blit(snake_images['food'], self.position)

# Game Class
class Game:
    def __init__(self):
        self.width, self.height = 800, 600
        self.game_display = pygame.display.set_mode((self.width, self.height))
        self.background_img = pygame.image.load('images/background.png').convert()
        self.background_img = pygame.transform.scale(self.background_img, (self.width, self.height))
        self.clock = pygame.time.Clock()
        self.running = True

    def draw_background(self):
        # Draws the background image on the game display
        self.game_display.blit(self.background_img, (0, 0))

    def run(self):
        while self.running:
            self.main_menu()

    def main_menu(self):
        menu_running = True
        while menu_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        self.game_loop()
                    elif event.key == pygame.K_v:
                        self.display_high_scores()

            self.game_display.fill(black)  # Clear screen
            self.draw_text("Snake Game", 50, width // 2, height // 4)
            self.draw_text("Press 'S' to Start", 25, width // 2, height // 2)
            self.draw_text("Press 'V' to View High Scores", 25, width // 2, 3 * height // 4)
            pygame.display.update()
            self.clock.tick(15)

    def game_loop(self):
        snake = Snake(self.game_display)
        food = Food(self.game_display)
        game_loop_running = True
        move_every = 3  # move the snake every 3 frames
        frame_count = 0

        while game_loop_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_loop_running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_loop_running = False
                    elif event.key == pygame.K_UP and snake.direction != pygame.K_DOWN:
                        snake.change_direction = pygame.K_UP
                    elif event.key == pygame.K_DOWN and snake.direction != pygame.K_UP:
                        snake.change_direction = pygame.K_DOWN
                    elif event.key == pygame.K_LEFT and snake.direction != pygame.K_RIGHT:
                        snake.change_direction = pygame.K_LEFT
                    elif event.key == pygame.K_RIGHT and snake.direction != pygame.K_LEFT:
                        snake.change_direction = pygame.K_RIGHT

            frame_count += 1
            if frame_count % move_every == 0:
                snake.move()
                if snake.get_head_position() == food.position:
                    snake.eat()
                    food.position = food.randomize_position()

            self.game_display.fill(black)  # Clear screen
            self.draw_background()
            snake.move()
            if snake.get_head_position() == food.position:
                snake.eat()
                food.position = food.randomize_position(snake.positions)
            snake.draw()
            food.draw()
            self.display_scores(snake.score)  # Update and display scores
            pygame.display.update()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

    def display_scores(self, score):
        score_text = font_style.render(f"Score: {score}", True, white)
        high_scores = load_high_scores()
        high_score_text = font_style.render("High Scores:", True, white)
        self.game_display.blit(score_text, (width + 10, 10))
        self.game_display.blit(high_score_text, (width + 10, 40))
        for i, high_score in enumerate(high_scores):
            hs_text = font_style.render(f"{i + 1}. {high_score}", True, white)
            self.game_display.blit(hs_text, (width + 10, 70 + i * 30))

            self.game_display.fill(black)
            self.draw_text("High Scores", 50, width // 2, height // 4)
            start_y = height // 3
            for i, score in enumerate(score_text):
                self.draw_text(f"{i + 1}. {score}", 30, width // 2, start_y + i * 30)
            pygame.display.update()
            self.clock.tick(15)

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font('assets/custom_font.ttf', size)
        text_surface = font.render(text, True, white)
        text_rect = text_surface.get_rect(center=(x, y))
        self.game_display.blit(text_surface, text_rect)

# Main execution
if __name__ == "__main__":
    game = Game()
    game.run()
