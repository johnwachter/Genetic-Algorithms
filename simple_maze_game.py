import random
import numpy as np

# Maze dimensions
"""ROWS, COLS = 5, 5  # Small 5x5 maze for simplicity

# Generate a simple solvable maze with a fixed random seed
def generate_solvable_maze_simple(rows, cols):#, seed=42):
    #random.seed(seed)
    maze = [[1 for _ in range(cols)] for _ in range(rows)]
    
    # Start position at (0, 0)
    start_x, start_y = 0, 0
    maze[start_y][start_x] = 0
    
    # Center position
    center_x, center_y = rows // 2, cols // 2
    maze[center_y][center_x] = 0
    
    # Make a simple path to ensure solvability
    maze[0][1] = 0
    maze[1][1] = 0
    maze[1][2] = 0
    maze[2][2] = 0
    maze[3][2] = 0
    maze[3][3] = 0
    maze[2][3] = 0
    maze[2][4] = 0
    
    return maze
"""

### Create population of maze runners
population = []

for i in range(5):
	population.append(np.random.choice(('a','s','d','w'),100))

### Do Maze Stuff
ROWS,COLS = 15, 15 # Small 15x15 maze for simplicity
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


# Calculate Manhattan distance to the center
def calculate_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

# Print the maze in text form
def print_maze(maze, player_pos):
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if (x, y) == player_pos:
                print("P", end=" ")
            elif (x,y) == (7,7):
                print("O", end=" ")
            elif cell == 1:
                print("#", end=" ")
            else:
                print(".", end=" ")
        print()
    print()

# Main game function
def main():
    maze = generate_solvable_maze(ROWS, COLS)
    player_pos = [0, 0]  # Starting position (top-left corner)
    center_pos = [ROWS // 2, COLS // 2]
    moves = 0

    print("Navigate the maze by entering a sequence of moves (e.g., 'ddsswa').")
    print("Reach the center of the maze to win!\n")
    print_maze(maze, tuple(player_pos))

    # Get user input for a sequence of moves
    #move_sequence = input("Enter your move sequence (w/a/s/d): ").strip().lower()
    move_sequence = population[0]
    
    for move in move_sequence:
        x, y = player_pos
        if move == 'w' and y > 0 and maze[y - 1][x] == 0:  # Move up
            player_pos[1] -= 1
            moves += 1
        elif move == 's' and y < ROWS - 1 and maze[y + 1][x] == 0:  # Move down
            player_pos[1] += 1
            moves += 1
        elif move == 'a' and x > 0 and maze[y][x - 1] == 0:  # Move left
            player_pos[0] -= 1
            moves += 1
        elif move == 'd' and x < COLS - 1 and maze[y][x + 1] == 0:  # Move right
            player_pos[0] += 1
            moves += 1
        else:
            print(f"Move '{move}' hit a wall or is out of bounds!")

    # Final distance to the center after the sequence
    distance_to_center = calculate_distance(player_pos[0], player_pos[1], center_pos[0], center_pos[1])

    # Display final results
    print("\nFinal Position:")
    print_maze(maze, tuple(player_pos))
    print(f"Distance to Center: {distance_to_center}, Total Moves Made: {moves}")
    
    if player_pos == center_pos:
        print("Congratulations! You've reached the center of the maze!")
    else:
        print("You did not reach the center of the maze. Try a different sequence.")

if __name__ == "__main__":
    main()
