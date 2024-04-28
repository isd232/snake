import pygame
import random

pygame.init()

# Display settings
width, height = 800, 600
game_display = pygame.display.set_mode((width, height + 50))
pygame.display.set_caption('Snake Game')

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
light_blue = (100, 183, 233)
score_bg_color = (128, 128, 128)

# Snake settings
snake_block = 10
snake_speed = 15

font_style = pygame.font.SysFont(None, 50)
score_font = pygame.font.SysFont(None, 35)

def draw_background():
    for y in range(0, height, 20):
        color = light_blue if (y // 20) % 2 == 0 else blue
        pygame.draw.rect(game_display, color, [0, y, width, 20])

def score(score):
    pygame.draw.rect(game_display, score_bg_color, [0, height, width, 50])
    value = score_font.render("Your Score: " + str(score), True, white)
    game_display.blit(value, [0, height])

def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(game_display, black, [x[0], x[1], snake_block, snake_block])


def message(msg, color):
    line_height = font_style.get_linesize()  # Get the height of each line of text
    lines = msg.split('\n')  # Split the message into separate lines
    start_y = height / 3 - (
                line_height * len(lines) / 2)  # Calculate the starting y position to center the text block vertically

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

    foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0

    clock = pygame.time.Clock()

    while not game_over:
        while game_close:
            draw_background()
            message("You Lost!\n\nQ-Quit\nC-Play Again", red)
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

        # Wrap-around logic
        if x1 >= width:
            x1 = 0
        elif x1 < 0:
            x1 = width - snake_block

        if y1 >= height:
            y1 = 0
        elif y1 < 0:
            y1 = height - snake_block

        draw_background()
        pygame.draw.rect(game_display, green, [foodx, foody, snake_block, snake_block])
        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
            length_of_snake += 1

        our_snake(snake_block, snake_list)
        score(length_of_snake - 1)

        pygame.display.update()
        clock.tick(snake_speed)

    pygame.quit()
    quit()

game_loop()
