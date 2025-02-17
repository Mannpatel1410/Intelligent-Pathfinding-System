import pygame
import sys
from constants import *
from grid_utils import initialize_grid, draw_grid, visualize_path
from algorithms import a_star, dijkstra, bfs, bidirectional_a_star

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption("Pathfinding Visualizer")

    global grid
    grid = initialize_grid()
    start = (0, 0)
    end = (GRID_SIZE - 1, GRID_SIZE - 1)
    message = None
    running = True
    algorithm = None
    algo_name = ""

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    algorithm = a_star
                    algo_name = 'A*'
                elif event.key == pygame.K_d:
                    algorithm = dijkstra
                    algo_name = 'Dijkstra'
                elif event.key == pygame.K_b:
                    algorithm = bfs
                    algo_name = 'BFS'
                elif event.key == pygame.K_x:
                    algorithm = bidirectional_a_star
                    algo_name = 'Bidirectional A*'
                
                elif event.key == pygame.K_r:
                    grid = initialize_grid()
                    message = None
                
                elif event.key == pygame.K_SPACE and algorithm:
                    if algo_name == 'Bidirectional A*':
                        path_result = algorithm(start, end)
                    else:
                        path_result = algorithm(start, end, grid)
                    
                    path, msg = path_result
                    if msg:
                        message = msg
                        draw_grid(screen, grid, message)
                    elif path:
                        message = None
                        visualize_path(path, algo_name, grid, screen)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                i, j = y // CELL_SIZE, x // CELL_SIZE
                if (i, j) != start and (i, j) != end:
                    grid[i][j] = 1 if grid[i][j] == 0 else 0

        draw_grid(screen, grid, message)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()