import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Constants
WINDOW_SIZE = 600
CELL_SIZE = 33  # Change the cell size to 33x33 pixels
GRID_SIZE = WINDOW_SIZE // CELL_SIZE
SNAKE_SPEED = 10

# Create the game window (square window)
window = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Snake Game")

# Set the background color to green
background_color = (0, 128, 0)  # Green color

# Initialize clock
clock = pygame.time.Clock()

# Load snake and apple images
snake_image = pygame.image.load("snake.png")
snake_image = pygame.transform.scale(snake_image, (CELL_SIZE, CELL_SIZE))  # Set snake image size to 33x33 pixels
apple_image = pygame.image.load("apple.png")
apple_image = pygame.transform.scale(apple_image, (32, 32))  # Set apple image size to 32x32 pixels

# Initialize snake
snake = [(5, 5)]
snake_dir = (1, 0)  # Initial direction (right)

# Initialize food
food = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))

# Initialize game state
game_over = False
welcome_screen = True  # Add a welcome screen state
game_started = False  # Add a game started state

# Font for messages and score
font = pygame.font.Font(None, 36)
game_over_text = font.render("Game Over! Press Enter or Space to restart.", True, (255, 255, 255))
game_over_text_rect = game_over_text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2))

welcome_text = font.render("Welcome to Snake Game. Press Space to start.", True, (255, 255, 255))
welcome_text_rect = welcome_text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2))

score = 0  # Initialize the score

# Function to reset the game
def reset_game():
    global snake, snake_dir, food, game_over, welcome_screen, game_started, score
    snake = [(5, 5)]
    snake_dir = (1, 0)
    food = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
    game_over = False
    welcome_screen = True
    game_started = False
    score = 0  # Reset the score

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if welcome_screen:
                if event.key == pygame.K_SPACE:
                    welcome_screen = False
                    game_started = True
                continue

            if game_over:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    reset_game()
            else:
                # Check the current direction and ensure the new direction is not opposite
                if event.key == pygame.K_UP and snake_dir != (0, 1):
                    snake_dir = (0, -1)
                elif event.key == pygame.K_DOWN and snake_dir != (0, -1):
                    snake_dir = (0, 1)
                elif event.key == pygame.K_LEFT and snake_dir != (1, 0):
                    snake_dir = (-1, 0)
                elif event.key == pygame.K_RIGHT and snake_dir != (-1, 0):
                    snake_dir = (1, 0)

    if not game_over and game_started:
        # Update snake position
        new_head = (snake[0][0] + snake_dir[0], snake[0][1] + snake_dir[1])
        snake.insert(0, new_head)

        # Check for collisions
        if snake[0] == food:
            food = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
            score += 1  # Increase the score by 1 when eating food

        else:
            snake.pop()

        # Check for game over
        if (
            snake[0][0] < 0
            or snake[0][0] >= GRID_SIZE
            or snake[0][1] < 0
            or snake[0][1] >= GRID_SIZE
            or snake[0] in snake[1:]
        ):
            game_over = True

    # Fill the window with the background color (green)
    window.fill(background_color)

    # Draw the snake and apple using images based on the game state
    if not welcome_screen:
        for segment in snake:
            window.blit(snake_image, (segment[0] * CELL_SIZE, segment[1] * CELL_SIZE))
        window.blit(apple_image, (food[0] * CELL_SIZE, food[1] * CELL_SIZE))

    # Display game over message when the game is over
    if game_over:
        window.blit(game_over_text, game_over_text_rect)
    # Display welcome message at the beginning
    elif welcome_screen:
        window.blit(welcome_text, welcome_text_rect)

    pygame.display.update()

    # Control game speed
    clock.tick(SNAKE_SPEED)
