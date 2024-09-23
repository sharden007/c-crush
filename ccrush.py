import pygame
import random

# Initialize Pygame
pygame.init()

# Constants for the game
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 8
CELL_SIZE = WIDTH // GRID_SIZE
CANDY_TYPES = 3

# Colors
WHITE = (255, 255, 255)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Candy Crush")

# Generate the grid with random candies
def generate_grid():
    return [[random.randint(1, CANDY_TYPES) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Draw the grid on the screen
def draw_grid(grid):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            color = (grid[row][col] * 85 % 256, grid[row][col] * 170 % 256, grid[row][col] * 255 % 256)
            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Main game loop
def main():
    grid = generate_grid()
    running = True

    while running:
        screen.fill(WHITE)
        draw_grid(grid)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

if __name__ == "__main__":
    main()