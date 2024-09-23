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

def generate_grid():
    return [[random.randint(1, CANDY_TYPES) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

def draw_grid(grid):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            color = (grid[row][col] * 85 % 256, grid[row][col] * 170 % 256, grid[row][col] * 255 % 256)
            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def find_matches(grid):
    matches = set()
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE - 2):
            if grid[row][col] == grid[row][col + 1] == grid[row][col + 2] != 0:
                matches.update({(row, col), (row, col + 1), (row, col + 2)})
    for col in range(GRID_SIZE):
        for row in range(GRID_SIZE - 2):
            if grid[row][col] == grid[row + 1][col] == grid[row + 2][col] != 0:
                matches.update({(row, col), (row + 1, col), (row + 2, col)})
    return matches

def remove_matches_and_apply_gravity(grid):
    matches = find_matches(grid)
    score = len(matches)
    
    for (row, col) in matches:
        grid[row][col] = 0
    
    for col in range(GRID_SIZE):
        empty_row = GRID_SIZE - 1
        for row in range(GRID_SIZE - 1, -1, -1):
            if grid[row][col] != 0:
                grid[empty_row][col] = grid[row][col]
                empty_row -= 1
        for row in range(empty_row + 1):
            grid[row][col] = random.randint(1, CANDY_TYPES)
    
    return score

def swap_candies(grid, pos1, pos2):
    r1, c1 = pos1
    r2, c2 = pos2
    
    if abs(r1 - r2) + abs(c1 - c2) == 1:
        grid[r1][c1], grid[r2][c2] = grid[r2][c2], grid[r1][c1]
        
        if not find_matches(grid):
            grid[r1][c1], grid[r2][c2] = grid[r2][c2], grid[r1][c1]
            return False
        
        return True
    
    return False

# Automated player logic to find and execute a move that results in a match
def auto_play(grid):
    # Try all possible swaps and make the first valid move found
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            # Check right swap
            if col < GRID_SIZE - 1 and swap_candies(grid, (row, col), (row, col + 1)):
                return True
            
            # Check down swap
            if row < GRID_SIZE - 1 and swap_candies(grid, (row, col), (row + 1, col)):
                return True
    
    return False

def main():
    grid = generate_grid()
    score = 0
    
    running = True
    
    while running:
        screen.fill(WHITE)
        draw_grid(grid)
        
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, HEIGHT - 40))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Automatically play the game by finding and making moves
        if auto_play(grid):
            while True:
                score += remove_matches_and_apply_gravity(grid)
                if not find_matches(grid):
                    break

    pygame.quit()

if __name__ == "__main__":
    main()