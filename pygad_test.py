import pygad
import random
import numpy as np
import pandas as pd
import math
from collections import deque

###
    ###
    ###
       #############################
"""Functions to Set up Maze Game"""#
       #############################
    ###
    ###
###

def create_population(pop_size, seed = 12):
    random.seed(seed)
    return [np.random.choice((4,8,6,2),200) for x in range(0,pop_size)]


### Do Maze Stuff
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

    # Ensure the bottom-right corner is open as the goal
    maze[rows - 1][cols - 1] = 0

    # Ensure there's an entry point to the goal cell if isolated
    if maze[rows - 2][cols - 1] == 1 and maze[rows - 1][cols - 2] == 1:
        # Open the cell above or to the left
        #maze[rows - 2][cols - 1] = 0  # Open the cell above
        maze[rows - 1][cols - 2] = 0  # Open the cell to the left

    return maze


# Calculate Manhattan distance to the goal
def calculate_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


# Calculate the shortest path from a position to the goal
def shortest_path_distance(maze, start, goal):
    rows, cols = len(maze), len(maze[0])
    queue = deque([(start, 0)])  # Queue holds (position, distance)
    visited = set()
    visited.add(start)

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

    while queue:
        (x, y), dist = queue.popleft()

        # If we've reached the goal, return the distance
        if (x, y) == goal:
            return dist

        # Explore neighbors
        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            # Check if the new position is within bounds and is a path (0) and not visited
            if 0 <= nx < cols and 0 <= ny < rows and maze[ny][nx] == 0 and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append(((nx, ny), dist + 1))

    return -1  # Return -1 if there's no path to the goal


# Print the maze in text form
def print_maze(maze, player_pos):
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if (x, y) == player_pos:
                print("P", end=" ")
            elif (x,y) == (19,19):
                print("O", end=" ")
            elif cell == 1:
                print("#", end=" ")
            else:
                print(".", end=" ")
        print()
    print()


def maze_fitness(ga_instance, solution, solution_idx):
    ROWS = 20
    COLS = 20

    # Run first maze-runner through maze
    maze = generate_solvable_maze(ROWS, COLS)
    player_pos = [0, 0]  # Starting position (top-left corner)
    goal = [ROWS -1, COLS -1]
    moves = 0
    smartness = 0 #indicator of not running into walls


    for move in solution:
            x, y = player_pos # x = columns and y = rows
            if player_pos[0] == 19 and player_pos[1] ==19:
                smartness += 100
            elif move == 8 and y > 0 and maze[y - 1][x] == 0:  # Move up
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
    distance_to_goal_manhattan = calculate_distance(player_pos[0], player_pos[1], goal[0], goal[1])

    distance_to_goal = shortest_path_distance(maze,(player_pos[0],player_pos[1]),(goal[0],goal[1]))

    final_player_pos = player_pos[0], player_pos[1]
    #print(final_player_pos)

    #print(moves, distance_to_center, smartness)

    return smartness, distance_to_goal*-1 # multiplying by -1 because we want solutions with higher values, and 0 is the best



###
    ###
    ###
       #############################
"""Functions to Set up Gent Algo"""#
       #############################
    ###
    ###
###

#OMG pygad makes this so simple
def on_gen(ga_instance):
    print("Generation : ", ga_instance.generations_completed)
    print("Fitness of the best solution :", ga_instance.best_solution()[1])

ga_instance = pygad.GA(gene_space = [4,8,6,2],
                       gene_type = int,
                       num_generations = 1000,
                       num_parents_mating = 6,
                       fitness_func = maze_fitness,
                       initial_population = create_population(100),
                       parent_selection_type = "sss",
                       keep_elitism = 0,
                       keep_parents = 2,
                       crossover_type = "scattered",
                       crossover_probability = .4,
                       mutation_type = "random",
                       mutation_percent_genes = 1,
                       #on_generation = on_gen
                       )


###
    ###
    ###
       #############################
"""Run the Gent Algo & Show Maze"""#
       #############################
    ###
    ###
###
maze = generate_solvable_maze(20,20)
print_maze(maze,(0,0))
ga_instance.run()



solution, solution_fitness, solution_idx = ga_instance.best_solution()
print("Parameters of the best solution : {solution}".format(solution=solution))
print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))
best_maze_runner = list(solution)

COLS = 20
ROWS = 20
def show_maze_progression(maze_runner):
    # Run first maze-runner through maze
    maze = generate_solvable_maze(20, 20)
    player_pos = [0, 0]  # Starting position (top-left corner)
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
            print_maze(maze,(x,y))


user_input = input("show progression? y/n")

if user_input == "y":
    show_maze_progression(best_maze_runner)
else: print("bye")


