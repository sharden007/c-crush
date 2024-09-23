import pygame
import random

# Initialize Pygame
pygame.init()

# Constants for the game
WIDTH, HEIGHT = 600, 700  # Increased height to accommodate buttons
GRID_SIZE = 8
CELL_SIZE = WIDTH // GRID_SIZE
CANDY_TYPES = 4

# Colors
WHITE = (255, 255, 255)
BUTTON_COLOR = (100, 100, 250)
BUTTON_HOVER_COLOR = (150, 150, 250)

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

def auto_play(grid):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if col < GRID_SIZE - 1 and swap_candies(grid, (row, col), (row, col + 1)):
                return True
            
            if row < GRID_SIZE - 1 and swap_candies(grid, (row, col), (row + 1, col)):
                return True
    
    return False

def draw_button(text, rect_position):
    x_pos, y_pos, width, height = rect_position
    mouse_pos = pygame.mouse.get_pos()
    
    # Change button color on hover
    if x_pos < mouse_pos[0] < x_pos + width and y_pos < mouse_pos[1] < y_pos + height:
        color = BUTTON_HOVER_COLOR
    else:
        color = BUTTON_COLOR
    
    pygame.draw.rect(screen, color, rect_position)
    
    # Render text on button
    font = pygame.font.SysFont(None, 36)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(x_pos + width // 2, y_pos + height // 2))
    screen.blit(text_surface, text_rect)

def main():
    grid = generate_grid()
    score = 0
    auto_playing = False
    
    start_button_rect = (50, HEIGHT - 80, WIDTH // 3 - 60, 50)
    stop_button_rect = (WIDTH // 3 + 10 + WIDTH //3 -60 , HEIGHT -80 , WIDTH //3 -60 ,50 )
    
    running = True
    
    while running:
        screen.fill(WHITE)
        draw_grid(grid)
        
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text,(10 , HEIGHT -120 ))
        
        draw_button("Start", start_button_rect)
        draw_button("Stop", stop_button_rect)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x , mouse_y= event.pos
                
                if start_button_rect[0]<mouse_x<start_button_rect[0]+start_button_rect[2] and start_button_rect[1]<mouse_y<start_button_rect[1]+start_button_rect[3]:
                    auto_playing=True
                
                elif stop_button_rect[0]<mouse_x<stop_button_rect[0]+stop_button_rect[2] and stop_button_rect[1]<mouse_y<stop_button_rect[1]+stop_button_rect[3]:
                    auto_playing=False
        
        if auto_playing and auto_play(grid):
            while True:
                score += remove_matches_and_apply_gravity(grid)
                if not find_matches(grid):
                    break

    pygame.quit()

if __name__ == "__main__":
    main()