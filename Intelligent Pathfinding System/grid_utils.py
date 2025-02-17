import pygame
from constants import *

def initialize_grid():
    return [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

def draw_grid(screen, grid, message=None):
    screen.fill(WHITE)

    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if grid[i][j] == 0:
                color = WHITE
            elif grid[i][j] == 1:
                color = BLACK
            elif grid[i][j] == 2:
                color = GREEN  # A* Path
            elif grid[i][j] == 3:
                color = BLUE   # Dijkstra Path
            elif grid[i][j] == 4:
                color = YELLOW # BFS Path
            else:
                color = RED
            pygame.draw.rect(screen, color, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    if message:
        font = pygame.font.Font(None, 36)
        text_surface = font.render(message, True, RED)
        text_rect = text_surface.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE - 40))
        screen.blit(text_surface, text_rect)
    
    pygame.display.flip()

def visualize_path(path, algorithm, grid, screen):
    if algorithm == 'A*':
        path_value = 2  # A* Path (Green)
    elif algorithm == 'Dijkstra':
        path_value = 3  # Dijkstra Path (Blue)
    elif algorithm == 'BFS':
        path_value = 4  # BFS Path (Yellow)
    elif algorithm == 'Bidirectional A*':
        path_value = 7  # Bidirectional A* Path
    
    for node in path:
        grid[node[0]][node[1]] = path_value
        draw_grid(screen, grid)
        pygame.time.wait(50)