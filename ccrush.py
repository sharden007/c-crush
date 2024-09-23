import pygame
import random

# Initialize Pygame
pygame.init()

# Constants for the game
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 8
CELL_SIZE = WIDTH // GRID_SIZE
CANDY_TYPES = 4

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

# Check for matches of three or more candies in a row or column
def find_matches(grid):
    matches = []
    # Check rows for matches
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE - 2):
            if grid[row][col] == grid[row][col + 1] == grid[row][col + 2]:
                matches.append((row, col))
                matches.append((row, col + 1))
                matches.append((row, col + 2))
    # Check columns for matches
    for col in range(GRID_SIZE):
        for row in range(GRID_SIZE - 2):
            if grid[row][col] == grid[row + 1][col] == grid[row + 2][col]:
                matches.append((row, col))
                matches.append((row + 1, col))
                matches.append((row + 2, col))
    return matches

# Remove matched candies and apply gravity to let candies fall down
def remove_matches_and_apply_gravity(grid):
    matches = find_matches(grid)
    score = len(matches)
    
    # Remove matched candies by setting them to zero
    for (row, col) in matches:
        grid[row][col] = 0
    
    # Apply gravity: make candies fall down into empty spaces
    for col in range(GRID_SIZE):
        empty_row = GRID_SIZE - 1
        for row in range(GRID_SIZE - 1, -1, -1):
            if grid[row][col] != 0:
                grid[empty_row][col] = grid[row][col]
                empty_row -= 1
        # Fill remaining empty spaces with new random candies
        for row in range(empty_row + 1):
            grid[row][col] = random.randint(1, CANDY_TYPES)
    
    return score

# Swap two candies if they are adjacent and check if it results in a match
def swap_candies(grid, pos1, pos2):
    r1, c1 = pos1
    r2, c2 = pos2
    
    # Swap candies if they are adjacent
    if abs(r1 - r2) + abs(c1 - c2) == 1:
        grid[r1][c1], grid[r2][c2] = grid[r2][c2], grid[r1][c1]
        
        # Check if swap results in a match; if not swap back
        if not find_matches(grid):
            grid[r1][c1], grid[r2][c2] = grid[r2][c2], grid[r1][c1]

# Main game loop
def main():
    grid = generate_grid()
    selected_candy = None
    score = 0
    
    running = True
    
    while running:
        screen.fill(WHITE)
        draw_grid(grid)
        
        # Display score on the screen
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, HEIGHT - 40))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                row, col = y // CELL_SIZE, x // CELL_SIZE
                
                if selected_candy is None:
                    selected_candy = (row, col)
                else:
                    swap_candies(grid, selected_candy, (row, col))
                    selected_candy = None
                    
                    # Remove matches and apply gravity after a successful swap
                    score += remove_matches_and_apply_gravity(grid)

    pygame.quit()

if __name__ == "__main__":
    main()