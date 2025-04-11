import random
import numpy as np
import pandas as pd
import math

"""Genetic Stuff with Populations and Associated Genetic Functions"""

### Create population of maze runners
def create_population(pop_size):
    return [np.random.choice(('a','s','w','d'),130) for x in range(0,pop_size)]

def select_best_individuals(population, scores, top_n):
    top_individuals = sorted(scores)[-math.ceil(len(population)*top_n)::]
    #print(top_individuals)
    top_genomes = [scores.index(i) for i in top_individuals]
    #print(top_genomes)
    selected_individuals = [population[i] for i in top_genomes]
    return selected_individuals

"""Create the Maze, calculate scores for running the maze, etc."""
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

maze_runner = [8, 6, 4, 2, 2, 4, 6, 4, 8, 6, 4, 4, 8, 6, 2, 6, 8, 6, 6, 4, 8, 6, 6, 4, 8, 2, 8, 8, 8, 2, 8, 8, 6, 8, 8, 8, 2, 8, 2, 8, 6, 2, 2, 8, 2, 4, 6, 6, 2, 2, 4, 8, 8, 4, 8, 4, 4, 6, 8, 2, 4, 6, 2, 4, 8, 2, 4, 6, 2, 8, 2, 4, 8, 8, 4, 6, 4, 2, 2, 8, 8, 2, 2, 2, 4, 4, 8, 6, 4, 4, 2, 6, 2, 6, 8, 8, 2, 4, 6, 8, 8, 8, 2, 2, 2, 8, 8, 6, 8, 6, 4, 4, 6, 2, 6, 6, 6, 8, 4, 6, 6, 6, 2, 8, 2, 4, 8, 2, 2, 2]

def score_attempt(maze_runner):
    # Run first maze-runner through maze
    maze = generate_solvable_maze(ROWS, COLS)
    player_pos = [0, 0]  # Starting position (top-left corner)
    center_pos = [ROWS // 2, COLS // 2]
    moves = 0
    smartness = 0 #indicator of not running into walls

    for move in maze_runner:
            x, y = player_pos # x = columns and y = rows
            if move == 8 and y > 0 and maze[y - 1][x] == 0:  # Move up
                player_pos[1] -= 1
                moves += 1
            elif move == 2 and y < ROWS - 1 and maze[y + 1][x] == 0:  # Move down
                player_pos[1] += 1
                moves += 1
            elif move == 4 and x > 0 and maze[y][x - 1] == 0:  # Move left
                player_pos[0] -= 1
                moves += 1
            elif move == 6 and x < COLS - 1 and maze[y][x + 1] == 0:  # Move right
                player_pos[0] += 1
                moves += 1
            else:
                #print(f"Move '{move}' hit a wall or is out of bounds!")
                smartness-=1

        # Final distance to the center after the sequence
    distance_to_center = calculate_distance(player_pos[0], player_pos[1], center_pos[0], center_pos[1])

    #print(moves, distance_to_center, smartness)

    return smartness #moves, distance_to_center, smartness




"""Run the Program"""
# Main game function
def main():
    population = create_population(300)
    #population = [np.array(['a','a','a','w','s']),np.array(['d', 'a', 's', 's', 's']),np.array(['w', 's', 'd', 'd', 'a'])]

    individuals_scores = []
    for i in range(len(population)):
        individuals_scores.append(score_attempt(population[i]))

    print(individuals_scores)

    print(select_best_individuals(population = population, scores = individuals_scores, top_n = .01))
    



if __name__ == "__main__":
    main()












"""
    
    # Scores is a list of lists containing the individual and their smartness score
    individuals_scores = []
    for i in range(len(population)):
        individuals_scores.append([i, score_attempt(population[i])])
        
    # results is the same thing as individuals_scores but in a dataframe
    results = pd.DataFrame({'individual':[],'score':[]})

    for row in individuals_scores:
        results.loc[len(results)] = row
    
    print(results)

    #select_best_individuals(population = population, scores = results, top_n = 1)
"""




"""
# Main game function
def main():
    maze = generate_solvable_maze(ROWS, COLS)
    player_pos = [0, 0]  # Starting position (top-left corner)
    center_pos = [ROWS // 2, COLS // 2]
    moves = 0

    #print("Navigate the maze by entering a sequence of moves (e.g., 'ddsswa').")
    #print("Reach the center of the maze to win!\n")
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
    #print("\nFinal Position:")
    #print_maze(maze, tuple(player_pos))
    #print(f"Distance to Center: {distance_to_center}, Total Moves Made: {moves}")
    
    if player_pos == center_pos:
        print("Congratulations! You've reached the center of the maze!")
    else:
        print("You did not reach the center of the maze. Try a different sequence.")

if __name__ == "__main__":
    main()
"""
