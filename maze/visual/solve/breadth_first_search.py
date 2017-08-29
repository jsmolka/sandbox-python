import numpy as np
from collections import deque
from maze import *
from pyprocessing import *

# Configuration
row_count = 35
col_count = 35
scale = 8
start = 0  # Top left corner if zero
end = 0  # Bottom right corner if zero
create_algorithm = Algorithm.Create.BACKTRACKING

# Define variables
m = Maze()
m.create(row_count, col_count, create_algorithm)
row_count_with_walls = 2 * row_count + 1
col_count_with_walls = 2 * col_count + 1

visited_cells = m.maze.copy()  # List of visited cells, value of visited cell is [0, 0, 0]
deque_ = deque()  # List of cells with according stack [(x, y, stack), ...]
stack = np.zeros((1, 2), dtype=np.uint16)  # List of visited cells [[x, y], ...]

# Define start and end
if start == 0:
    start = (0, 0)
if end == 0:
    end = (row_count - 1, col_count - 1)
start = tuple([2 * x + 1 for x in start])
end = tuple([2 * x + 1 for x in end])

x, y = start
stack[0] = (x, y)
deque_.append((x, y, stack))
visited_cells[x, y] = [0, 0, 0]  # Mark as visited

current_cells = []  # List of cells [(x, y), ...]
last_cells = []  # List of cells [(x, y), ...]
current_cells.append((x, y))

found = False
finished = False

dir_two = [
    lambda x, y: (x + 2, y, x + 1, y),
    lambda x, y: (x - 2, y, x - 1, y),
    lambda x, y: (x, y - 2, x, y - 1),
    lambda x, y: (x, y + 2, x, y + 1)
]


def enqueue():
    """Queues next cells"""
    global deque_, visited_cells, dir_two, current_cells
    x, y, stack = deque_.popleft()
    for direction in dir_two:  # Check adjacent cells
        tx, ty, bx, by = direction(x, y)
        if visited_cells[bx, by, 0] == 255:  # Check if unvisited
            visited_cells[bx, by] = visited_cells[tx, ty] = [0, 0, 0]  # Mark as visited
            current_cells.extend([(bx, by), (tx, ty)])
            deque_.append((tx, ty, np.append(stack, [(bx, by), (tx, ty)], axis=0)))


def draw_maze():
    """Draws maze"""
    global m, row_count_with_walls, col_count_with_walls, scale
    fill(255)
    for x in range(0, row_count_with_walls):
        for y in range(0, col_count_with_walls):
            if m.maze[x, y, 0] == 255:
                rect(y * scale, x * scale, scale, scale)


def draw_stack():
    """Draws stack"""
    global x, y, r, g, b, offset, finished, scale
    if stack:
        r -= offset
        b += offset
        fill(r, g, b)
        x, y = tuple(stack.pop())
        rect(y * scale, x * scale, scale, scale)
    else:
        finished = True


def draw_cells():
    """Draws cells"""
    global finished, current_cells, last_cells, scale
    fill(0, 255, 0)
    for x, y in current_cells:
        rect(y * scale, x * scale, scale, scale)
    fill(128)
    for x, y in last_cells:
        rect(y * scale, x * scale, scale, scale)
    if finished:
        fill(128)
        for x, y in current_cells:
            rect(y * scale, x * scale, scale, scale)
    current_cells, last_cells = [], current_cells


def setup():
    global row_count_with_walls, col_count_with_walls, scale
    size(col_count_with_walls * scale, row_count_with_walls * scale, caption=Algorithm.Solve.BREADTH.value)
    background(0)
    noStroke()
    draw_maze()


def draw():
    global deque_, stack, end, r, g, b, offset, found
    if not found:
        enqueue()
        if (deque_[0][0], deque_[0][1]) == end:  # Stop if end has been found
            found = True
            draw_cells()  # Remove old cells
            stack = deque_[0][2].tolist()
            r, b, g, offset = 255, 0, 0, 255 / len(stack)
        draw_cells()
    else:
        draw_stack()


run()
