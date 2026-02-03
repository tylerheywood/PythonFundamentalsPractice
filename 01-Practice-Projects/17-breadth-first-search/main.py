from collections import deque

# --- CONFIG ---
width = 10
height = 10

start = (0, 0)
goal = (9, 9)

walls = [(3, 0), (1, 1), (3, 1), (2, 3), (8, 9), (8, 8), (8, 7), (9, 5), (2, 3), (0, 3)]

walls_set = set(walls)

directions = [
    (0, -1),  # up
    (0, 1),  # down
    (-1, 0),  # left
    (1, 0),  # right
]

grid = []


# --- HELPERS ---
def in_bounds(x, y, width, height) -> bool:
    return 0 <= x < width and 0 <= y < height


def render_grid(width, height, start, goal, walls):
    walls = set(walls)
    sx, sy = start
    gx, gy = goal

    if not in_bounds(sx, sy, width, height):
        raise ValueError("Start is out of bounds")

    if not in_bounds(gx, gy, width, height):
        raise ValueError("Goal is out of bounds")

    if start in walls:
        raise ValueError("Start cannot be on a wall")

    if goal in walls:
        raise ValueError("Goal cannot be on a wall")

    lines = []
    for y in range(height):
        row = []
        for x in range(width):
            if (x, y) == start:
                row.append("S")
            elif (x, y) == goal:
                row.append("G")
            elif (x, y) in walls:
                row.append("#")
            else:
                row.append(".")
        lines.append(" ".join(row))

    return "\n".join(lines)


def get_neighbours(pos, width, height, walls_set):
    px, py = pos
    neighbours = []

    for dx, dy in directions:
        nx = px + dx
        ny = py + dy

        if not in_bounds(nx, ny, width, height):
            continue

        if (nx, ny) in walls_set:
            continue

        neighbours.append((nx, ny))

    return neighbours


def bfs_reachability(start, goal, width, height, walls_set):
    frontier = deque([start])  # double ended queue
    visited = {start}

    while frontier:
        current = frontier.popleft()

        if current == goal:
            return True

        for nxt in get_neighbours(current, width, height, walls_set):
            if nxt in visited:
                continue

            visited.add(nxt)
            frontier.append(nxt)

    return False


def bfs_path(start, goal, width, height, walls_set):
    frontier = deque([start])
    came_from = {start: None}  # also acts like visited

    while frontier:
        current = frontier.popleft()

        if current == goal:
            break

        for nxt in get_neighbours(current, width, height, walls_set):
            if nxt in came_from:
                continue
            came_from[nxt] = current
            frontier.append(nxt)

    if goal not in came_from:
        return None

    # reconstruct path by walking backwards
    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = came_from[cur]
    path.reverse()
    return path


print(render_grid(width, height, start, goal, walls))
print(get_neighbours(start, width, height, walls_set))
print(bfs_reachability(start, goal, width, height, walls_set))
print(bfs_path(start, goal, width, height, walls_set))
