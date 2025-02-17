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

def dijkstra(start, end, grid):
    if is_blocked(start, grid) or is_blocked(end, grid):
        return None, "Start or End point is blocked!"
        
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = { (i, j): float('inf') for i in range(GRID_SIZE) for j in range(GRID_SIZE) }
    g_score[start] = 0

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
                    heapq.heappush(open_set, (g_score[neighbor], neighbor))

    return None, "No path found!"

def bfs(start, end, grid):
    if is_blocked(start, grid) or is_blocked(end, grid):
        return None, "Start or End point is blocked!"
        
    queue = [start]
    came_from = {}
    visited = set()
    visited.add(start)

    while queue:
        current = queue.pop(0)
        if current == end:
            return reconstruct_path(came_from, current), None

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < GRID_SIZE and 0 <= neighbor[1] < GRID_SIZE and grid[neighbor[0]][neighbor[1]] != 1 and neighbor not in visited:
                came_from[neighbor] = current
                visited.add(neighbor)
                queue.append(neighbor)

    return None, "No path found!"

def bidirectional_a_star(start, end, grid):
    if is_blocked(start, grid) or is_blocked(end, grid):
        return None, "Start or End point is blocked!"
        
    open_set_fwd = []
    open_set_bwd = []
    heapq.heappush(open_set_fwd, (heuristic(start, end), start))
    heapq.heappush(open_set_bwd, (heuristic(end, start), end))

    came_from_fwd = {}
    came_from_bwd = {}

    g_score_fwd = { (i, j): float('inf') for i in range(GRID_SIZE) for j in range(GRID_SIZE) }
    g_score_bwd = { (i, j): float('inf') for i in range(GRID_SIZE) for j in range(GRID_SIZE) }
    g_score_fwd[start] = 0
    g_score_bwd[end] = 0

    f_score_fwd = { (i, j): float('inf') for i in range(GRID_SIZE) for j in range(GRID_SIZE) }
    f_score_bwd = { (i, j): float('inf') for i in range(GRID_SIZE) for j in range(GRID_SIZE) }
    f_score_fwd[start] = heuristic(start, end)
    f_score_bwd[end] = heuristic(end, start)

    visited_fwd = set()  # Nodes visited by forward search
    visited_bwd = set()  # Nodes visited by backward search

    meeting_point = None  # Where the two searches meet

    while open_set_fwd and open_set_bwd:
        if len(open_set_fwd) <= len(open_set_bwd):
            _, current_fwd = heapq.heappop(open_set_fwd)

            if current_fwd in visited_bwd:
                meeting_point = current_fwd
                break

            visited_fwd.add(current_fwd)

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor_fwd = (current_fwd[0] + dx, current_fwd[1] + dy)
                if 0 <= neighbor_fwd[0] < GRID_SIZE and 0 <= neighbor_fwd[1] < GRID_SIZE and grid[neighbor_fwd[0]][neighbor_fwd[1]] != 1:
                    tentative_g_score = g_score_fwd[current_fwd] + 1
                    if tentative_g_score < g_score_fwd[neighbor_fwd]:
                        came_from_fwd[neighbor_fwd] = current_fwd
                        g_score_fwd[neighbor_fwd] = tentative_g_score
                        f_score_fwd[neighbor_fwd] = tentative_g_score + heuristic(neighbor_fwd, end)
                        heapq.heappush(open_set_fwd, (f_score_fwd[neighbor_fwd], neighbor_fwd))

        else:
            _, current_bwd = heapq.heappop(open_set_bwd)

            if current_bwd in visited_fwd:
                meeting_point = current_bwd
                break

            visited_bwd.add(current_bwd)

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor_bwd = (current_bwd[0] + dx, current_bwd[1] + dy)
                if 0 <= neighbor_bwd[0] < GRID_SIZE and 0 <= neighbor_bwd[1] < GRID_SIZE and grid[neighbor_bwd[0]][neighbor_bwd[1]] != 1:
                    tentative_g_score = g_score_bwd[current_bwd] + 1
                    if tentative_g_score < g_score_bwd[neighbor_bwd]:
                        came_from_bwd[neighbor_bwd] = current_bwd
                        g_score_bwd[neighbor_bwd] = tentative_g_score
                        f_score_bwd[neighbor_bwd] = tentative_g_score + heuristic(neighbor_bwd, start)
                        heapq.heappush(open_set_bwd, (f_score_bwd[neighbor_bwd], neighbor_bwd))

    if meeting_point:
        path_fwd = reconstruct_path(came_from_fwd, meeting_point)
        path_bwd = reconstruct_path(came_from_bwd, meeting_point)
        final_path = path_fwd[:-1] + path_bwd[::-1]  # Exclude the meeting point from one of the paths

        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if grid[i][j] == 5 or grid[i][j] == 6:
                    grid[i][j] = 0

        return final_path, None

    return None, "No path found!"