from collections import deque

def find_start_end(maze):
    start = end = None
    for r in range(len(maze)):
        for c in range(len(maze[0])):
            if maze[r][c] == 'S':
                start = (r, c)
            elif maze[r][c] == 'E':
                end = (r, c)
    return start, end

def shortest_path(maze):
    start, end = find_start_end(maze)
    if not start or not end:
        return []
    rows, cols = len(maze), len(maze[0])
    visited = set()
    queue = deque([(start, [start])])  # (current_pos, path_so_far)

    while queue:
        (r, c), path = queue.popleft()
        if (r, c) == end:
            return path

        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r + dr, c + dc
            if (0 <= nr < rows and 0 <= nc < cols and
                (nr, nc) not in visited and maze[nr][nc] != '#'):
                visited.add((nr, nc))
                queue.append(((nr, nc), path + [(nr, nc)]))
    
    return []  # No path found
# 🧪 Test it
maze = [
    ['S', '.', '.', '#', '.', '.'],
    ['#', '#', '.', '#', '.', '#'],
    ['.', '.', '.', '.', '.', '.'],
    ['.', '#', '#', '#', '#', '.'],
    ['.', '.', '.', '#', 'E', '.']
]

print(shortest_path(maze))
