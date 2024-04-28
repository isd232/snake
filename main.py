import pygame
import random

pygame.init()

# Display settings
width, height = 800, 600
game_display = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Game')

# Colors
white = (255, 255, 255)
red = (213, 50, 80)
blue = (50, 153, 213)

# Snake settings
snake_block = 20
snake_speed = 15

# Load images and resize them
snake_head_img = pygame.image.load('snake_head.png').convert_alpha()
snake_head_img = pygame.transform.scale(snake_head_img, (snake_block, snake_block))
snake_body_img = pygame.image.load('snake_body.png').convert_alpha()
snake_body_img = pygame.transform.scale(snake_body_img, (snake_block, snake_block))
food_img = pygame.image.load('food.png').convert_alpha()
food_img = pygame.transform.scale(food_img, (snake_block, snake_block))

# Font
font_style = pygame.font.Font('custom_font.ttf', 50)

# Load and scale background image
background_img = pygame.image.load('background.png').convert()
background_img = pygame.transform.scale(background_img, (width, height))


def draw_background():
    # Blit the background image
    game_display.blit(background_img, (0, 0))


def score(score):
    value = font_style.render(f"Your Score: {score}", True, white)
    game_display.blit(value, [0, 0])


def our_snake(snake_block, snake_list):
    for idx, block in enumerate(snake_list):
        if idx == 0:
            game_display.blit(snake_head_img, (block[0], block[1]))
        else:
            game_display.blit(snake_body_img, (block[0], block[1]))


def message(msg, color):
    lines = msg.split('\n')
    line_height = font_style.get_linesize()
    start_y = height / 3 - (line_height * len(lines) / 2)
    for i, line in enumerate(lines):
        mesg = font_style.render(line, True, color)
        text_rect = mesg.get_rect(center=(width / 2, start_y + i * line_height))
        game_display.blit(mesg, text_rect)


def game_loop():
    game_over = False
    game_close = False

    x1 = width / 2
    y1 = height / 2

    x1_change = 0
    y1_change = 0

    snake_list = []
    length_of_snake = 1

    foodx = round(random.randrange(0, width - snake_block) / snake_block) * snake_block
    foody = round(random.randrange(0, height - snake_block) / snake_block) * snake_block

    clock = pygame.time.Clock()

    while not game_over:
        while game_close:
            draw_background()
            message("You Lost!\nPress Q-Quit\nPress C-Play Again", red)
            score(length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    elif event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = snake_block
                    x1_change = 0

        x1 += x1_change
        y1 += y1_change

        if x1 >= width:
            x1 = 0
        elif x1 < 0:
            x1 = width - snake_block
        if y1 >= height:
            y1 = 0
        elif y1 < 0:
            y1 = height - snake_block

        draw_background()
        game_display.blit(food_img, (foodx, foody))
        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, width - snake_block) / snake_block) * snake_block
            foody = round(random.randrange(0, height - snake_block) / snake_block) * snake_block
            length_of_snake += 1

        our_snake(snake_block, snake_list)
        score(length_of_snake - 1)

        pygame.display.update()
        clock.tick(snake_speed)

    pygame.quit()
    quit()


game_loop()
