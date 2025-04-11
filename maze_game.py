import pygame
import random
import math

# Initialize pygame
pygame.init()

# Game settings
WIDTH, HEIGHT = 600, 600  # Screen size
ROWS, COLS = 15, 15       # Maze grid dimensions
CELL_SIZE = WIDTH // COLS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Navigator")

# Maze generation with DFS and a fixed random seed
def generate_solvable_maze(rows, cols, seed=42):
    # Set the random seed for reproducibility
    random.seed(seed)
    
    # Initialize all cells as walls
    maze = [[1 for _ in range(cols)] for _ in range(rows)]
    
    # Starting position
    start_x, start_y = 0, 0
    maze[start_y][start_x] = 0  # Start point is open
    
    # Stack for DFS and visited set
    stack = [(start_x, start_y)]
    visited = set(stack)

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

    # DFS to carve out the maze
    while stack:
        x, y = stack[-1]
        
        # Find all unvisited neighbors
        neighbors = []
        for dx, dy in directions:
            nx, ny = x + dx * 2, y + dy * 2
            if 0 <= nx < cols and 0 <= ny < rows and (nx, ny) not in visited:
                neighbors.append((nx, ny))

        if neighbors:
            # Choose a random neighbor
            nx, ny = random.choice(neighbors)
            
            # Remove wall between current cell and chosen neighbor
            maze[(y + ny) // 2][(x + nx) // 2] = 0
            maze[ny][nx] = 0  # Make the neighbor cell a path
            
            # Mark as visited and push to stack
            visited.add((nx, ny))
            stack.append((nx, ny))
        else:
            # Backtrack if no unvisited neighbors
            stack.pop()

    # Ensure the center of the maze is open
    maze[rows // 2][cols // 2] = 0
    return maze

# Distance calculation (Manhattan distance)
def calculate_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

# Main game function
def main():
    maze = generate_solvable_maze(ROWS, COLS)
    player_pos = [0, 0]  # Starting position (top-left corner)
    center_pos = [ROWS // 2, COLS // 2]

    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(WHITE)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                x, y = player_pos
                if event.key == pygame.K_LEFT and x > 0 and maze[y][x - 1] == 0:
                    player_pos[0] -= 1
                elif event.key == pygame.K_RIGHT and x < COLS - 1 and maze[y][x + 1] == 0:
                    player_pos[0] += 1
                elif event.key == pygame.K_UP and y > 0 and maze[y - 1][x] == 0:
                    player_pos[1] -= 1
                elif event.key == pygame.K_DOWN and y < ROWS - 1 and maze[y + 1][x] == 0:
                    player_pos[1] += 1

        # Calculate distance to center
        distance_to_center = calculate_distance(player_pos[0], player_pos[1], center_pos[0], center_pos[1])

        # Check if player reached the center
        if player_pos == center_pos:
            font = pygame.font.Font(None, 72)
            win_text = font.render("You Win!", True, (0, 255, 0))
            screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - win_text.get_height() // 2))
            pygame.display.flip()
            pygame.time.delay(2000)
            running = False

        # Draw maze
        for row in range(ROWS):
            for col in range(COLS):
                color = BLACK if maze[row][col] == 1 else WHITE
                pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Draw player and center point
        pygame.draw.rect(screen, RED, (player_pos[0] * CELL_SIZE, player_pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, BLUE, (center_pos[0] * CELL_SIZE, center_pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Display distance to center
        font = pygame.font.Font(None, 36)
        distance_text = font.render(f"Distance to Center: {distance_to_center}", True, (0, 0, 0))
        screen.blit(distance_text, (10, 10))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
