import numpy as np
import matplotlib.pyplot as plt
import random

# Maze dimensions
height = 15
width = 30

# Create an empty maze filled with walls (1s represent walls, 0s represent paths)
maze = np.ones((height, width))

# Directions for maze generation
DIRECTIONS = [(0, 2), (2, 0), (0, -2), (-2, 0)]

def is_valid(x, y):
    return 0 <= x < height and 0 <= y < width

def generate_maze(maze, x, y):
    # Start maze generation at (x, y)
    maze[x, y] = 0  # Make current cell a path
    random.shuffle(DIRECTIONS)  # Shuffle directions for randomized paths
    for dx, dy in DIRECTIONS:
        nx, ny = x + dx, y + dy
        if is_valid(nx, ny) and maze[nx, ny] == 1:
            maze[x + dx // 2, y + dy // 2] = 0  # Break the wall between
            generate_maze(maze, nx, ny)

# Initialize the maze with recursive backtracking
generate_maze(maze, 1, 1)

# Now we will carve the letters "B", "O", "A", "R", "D" by overlaying them into the maze

def carve_path_for_b(maze, start_row, start_col):
    # Carving the letter 'B'
    maze[start_row:start_row+5, start_col] = 0  # Vertical line
    maze[start_row, start_col:start_col+3] = 0  # Top horizontal line
    maze[start_row+2, start_col:start_col+3] = 0  # Middle horizontal line
    maze[start_row+4, start_col:start_col+3] = 0  # Bottom horizontal line
    maze[start_row+1, start_col+2] = 0  # Upper right vertical
    maze[start_row+3, start_col+2] = 0  # Lower right vertical

def carve_path_for_o(maze, start_row, start_col):
    # Carving the letter 'O'
    maze[start_row:start_row+5, start_col] = 0  # Left vertical
    maze[start_row:start_row+5, start_col+3] = 0  # Right vertical
    maze[start_row, start_col:start_col+4] = 0  # Top horizontal
    maze[start_row+4, start_col:start_col+4] = 0  # Bottom horizontal

def carve_path_for_a(maze, start_row, start_col):
    # Carving the letter 'A'
    maze[start_row:start_row+5, start_col] = 0  # Left vertical
    maze[start_row:start_row+5, start_col+3] = 0  # Right vertical
    maze[start_row, start_col:start_col+4] = 0  # Top horizontal
    maze[start_row+2, start_col:start_col+4] = 0  # Middle horizontal

def carve_path_for_r(maze, start_row, start_col):
    # Carving the letter 'R'
    maze[start_row:start_row+5, start_col] = 0  # Left vertical
    maze[start_row, start_col:start_col+3] = 0  # Top horizontal
    maze[start_row+2, start_col:start_col+3] = 0  # Middle horizontal
    maze[start_row+1, start_col+2] = 0  # Upper right vertical
    maze[start_row+3, start_col+2:start_col+4] = 0  # Diagonal for R

def carve_path_for_d(maze, start_row, start_col):
    # Carving the letter 'D'
    maze[start_row:start_row+5, start_col] = 0  # Left vertical
    maze[start_row, start_col:start_col+3] = 0  # Top horizontal
    maze[start_row+4, start_col:start_col+3] = 0  # Bottom horizontal
    maze[start_row+1:start_row+4, start_col+2] = 0  # Right vertical
    
# Carve the letters "B", "O", "A", "R", "D" into the maze
carve_path_for_b(maze, 3, 1)
carve_path_for_o(maze, 3, 6)
carve_path_for_a(maze, 3, 11)
carve_path_for_r(maze, 3, 16)
carve_path_for_d(maze, 3, 21)

# Display the maze
plt.figure(figsize=(10, 5))
plt.imshow(maze, cmap='binary')
plt.xticks([])  # Remove x ticks
plt.yticks([])  # Remove y ticks
plt.title('Maze with solution spelling "Board"')
plt.show()
