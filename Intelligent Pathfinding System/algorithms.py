import heapq
from constants import *

def is_blocked(point, grid):
    if not (0 <= point[0] < GRID_SIZE and 0 <= point[1] < GRID_SIZE):
        return True  # Treat out-of-bounds as blocked
    return grid[point[0]][point[1]] == 1

def reconstruct_path(came_from, current):
    path = []
    while current in came_from:
        path.append(current)
        current = came_from[current]
    path.append(current)
    return path[::-1]

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(start, end, grid):
    if is_blocked(start, grid) or is_blocked(end, grid):
        return None, "Start or End point is blocked!"
        
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = { (i, j): float('inf') for i in range(GRID_SIZE) for j in range(GRID_SIZE) }
    g_score[start] = 0
    f_score = { (i, j): float('inf') for i in range(GRID_SIZE) for j in range(GRID_SIZE) }
    f_score[start] = heuristic(start, end)

    while open_set:
        _, current = heapq.heappop(open_set)
        if current == end:
            return reconstruct_path(came_from, current), None

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < GRID_SIZE and 0 <= neighbor[1] < GRID_SIZE and grid[neighbor[0]][neighbor[1]] != 1:
                tentative_g_score = g_score[current] + 1
                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None, "No path found!"