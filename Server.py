import pygame
import random
import socket
import threading
import time
import json

IP = '127.0.0.1'
port = 5000

# Build socket between server and client
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((IP, port))
server_socket.listen(1)

# Approve connection
client_socket, client_address = server_socket.accept()
print(f"Connection from {client_address} has been established!\n")

# Screen Set
RES = 32
#      (columns, rows)
DIMS = (20, 20)
SCREEN = (DIMS[0] * RES, DIMS[1] * RES)
pygame.init()
display = pygame.display.set_mode(SCREEN)
pygame.display.set_caption("The Maze")

# Class that creates walls and tiles
class Tile:
    def __init__(self, c, r):
        self.c = c
        self.r = r
        self.x = self.c * RES
        self.y = self.r * RES
        self.color = "black"
        #                      ((Position), (Area))
        self.rect = pygame.Rect(self.x, self.y, RES, RES)
        #            [Right, Down, Left, Up]
        self.walls = [1, 1, 1, 1]
        self.visited = False
        self.moved = False

    # Function that draws tiles
    def draw_tile(self):
        pygame.draw.rect(display, self.color, self.rect)

    # Function that draws walls
    def draw_walls(self):
        # Right
        if bool(self.walls[0]):
            pygame.draw.line(display, "white", (self.x + RES, self.y), (self.x + RES, self.y + RES))
        # Down
        if bool(self.walls[1]):
            pygame.draw.line(display, "white", (self.x, self.y + RES), (self.x + RES, self.y + RES))
        # Left
        if bool(self.walls[2]):
            pygame.draw.line(display, "white", (self.x, self.y), (self.x, self.y + RES))
        # Up
        if bool(self.walls[3]):
            pygame.draw.line(display, "white", (self.x, self.y), (self.x + RES, self.y))

# Grid creation
grid = []
for r in range(DIMS[1]):
# Tile row creation in grid
    tile_row = []
    for c in range(DIMS[0]):
        tile = Tile(c, r)
        tile_row.append(tile)
    grid.append(tile_row)

# Current tile (starting point)
ct = grid[0][0]
ct.visited = True

# Stack for back tracking
stack = [ct]

# Draw grid
def draw():
    display.fill("black")
    # Goal tile (end position)
    gt = grid[DIMS[0] - 1][DIMS[1] - 1]
    for row in grid:
        for tile in row:
            tile.color = "blue"
            if tile == ct:
                tile.color = "orange"
            if tile.moved:
                tile.color = "purple"
            if tile == gt:
                continue
            tile.draw_tile()
    for row in grid:
        for tile in row:
            tile.draw_walls()
    pygame.display.flip()

# Get optional tiles to visit
def get_neigh() -> list:
    neigh = []
    # Right
    if ct.c < DIMS[0] - 1 and not grid[ct.r][ct.c + 1].visited:
        neigh.append(grid[ct.r][ct.c + 1])
    # Down
    if ct.r < DIMS[1] - 1 and not grid[ct.r + 1][ct.c].visited:
        neigh.append(grid[ct.r + 1][ct.c])
    # Left
    if ct.c > 0 and not grid[ct.r][ct.c - 1].visited:
        neigh.append(grid[ct.r][ct.c - 1])
    # Up
    if ct.r > 0 and not grid[ct.r - 1][ct.c].visited:
        neigh.append(grid[ct.r - 1][ct.c])
    # Return list of unvisited neighbors
    return neigh

# Remove wall between chosen tile and current tile based on their relative positions
def tear_down_walls(ch):
    # Right
    if ch.c - ct.c > 0:
        ct.walls[0] = 0
        ch.walls[2] = 0
    # Down
    if ch.r - ct.r > 0:
        ct.walls[1] = 0
        ch.walls[3] = 0
    # Left
    if ch.c - ct.c < 0:
        ct.walls[2] = 0
        ch.walls[0] = 0
    # Up
    if ch.r - ct.r < 0:
        ct.walls[3] = 0
        ch.walls[1] = 0

# Draw maze
def generate_maze():
    global ct
    while True:
        valid_n = get_neigh()
        if len(valid_n) > 0:
            chosen = random.choice(valid_n)
            tear_down_walls(chosen)
            chosen.visited = True
            stack.append(ct)
            ct = chosen
        else:
            if len(stack) > 0:
                ct = stack.pop()
            else:
                break

# Player move
def move(command):
    global ct
    # Right
    if command == "R":
        if ct.walls[0] == 0:
            if not grid[ct.r][ct.c + 1].moved:
                ct.moved = True
            else:
                ct.moved = False
                grid[ct.r][ct.c + 1].moved = False
            ct = grid[ct.r][ct.c + 1]
    # Down
    elif command == "D":
        if ct.walls[1] == 0:
            if not grid[ct.r + 1][ct.c].moved:
                ct.moved = True
            else:
                ct.moved = False
                grid[ct.r + 1][ct.c].moved = False
            ct = grid[ct.r + 1][ct.c]
    # Left
    elif command == "L":
        if ct.walls[2] == 0:
            if not grid[ct.r][ct.c - 1].moved:
                ct.moved = True
            else:
                ct.moved = False
                grid[ct.r][ct.c - 1].moved = False
            ct = grid[ct.r][ct.c - 1]
    # Up
    elif command == "U":
        if ct.walls[3] == 0:
            if not grid[ct.r - 1][ct.c].moved:
                ct.moved = True
            else:
                ct.moved = False
                grid[ct.r - 1][ct.c].moved = False
            ct = grid[ct.r - 1][ct.c]

# unexpected event
shutdown_flag = threading.Event()

# Player end game
def player_leave(command):
    # Exit
    if command == "esc":
        shutdown_flag.set()

# Player play another game after solving
def play_again(command):
    global ct
    # New maze
    if ct == grid[DIMS[0] - 1][DIMS[1] - 1]:
        reset_maze()
    # Reset game
    elif ct != grid[DIMS[0] - 1][DIMS[1] - 1] and command == "enter":
        for row in grid:
            for tile in row:
                tile.moved = False
            ct = grid[0][0]

# generate another maze from scratch after solving
def reset_maze():
    global grid, ct, stack
    for row in grid:
        for tile in row:
            tile.visited = False
            tile.moved = False
            tile.walls = [1, 1, 1, 1]
    ct = grid[0][0]
    ct.visited = True
    stack = [ct]
    generate_maze()

# Time stopper
check = False
start_times = []
end_times = []
time_play = []

# Time stopper for each game
def solution_time(command):
    global start_times, end_times, check
    # Start
    if ct != grid[0][0] and not check:
        start = time.time()
        start_times.append(start)
        check = True
    # New maze
    if ct == grid[DIMS[0] - 1][DIMS[1] - 1] and check:
        end = time.time()
        end_times.append(end)
        check = False
        if len(end_times) > len(time_play) and len(end_times) == len(start_times):
            duration = end_times[-1] - start_times[-1]
            time_play.append(duration)
    # Exit
    if command == "esc":
        # Print solution time of maze after exit
        for duration in time_play:
            print(f"Maze number {time_play.index(duration) + 1} solution time: {duration}")
        sum = 0
        count = 0
        for duration in time_play:
            sum += duration
            count += 1
        if count > 1:
            print(f"Average solution time for maze: {sum / count}")

# Allowed commands for client messages
allowed_commands = {"R", "D", "L", "U", "esc", "enter"}

# Listen for client messages
def listen_for_client():
    buffer = ""
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            buffer += data
            # Take necessary text from message
            while "\n" in buffer:
                # Keep only first json message (before split)
                line, buffer = buffer.split("\n", 1)
                try:
                    message = json.loads(line)
                    command = message["command"]
                    if command in allowed_commands:
                        move(command)
                        solution_time(command)
                        player_leave(command)
                        play_again(command)
                    else:
                        print("Invalid command:", command)
                except json.JSONDecodeError:
                    print("Invalid JSON received.")
        except ConnectionResetError:
            shutdown_flag.set()
            break
        except Exception as e:
            print("Unexpected error:", e)
            shutdown_flag.set()
            break


# Run maze generation and start listening thread
generate_maze()
threading.Thread(target=listen_for_client, daemon=True).start()

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    # exception in main thread
    if shutdown_flag.is_set():
        pygame.quit()
        exit()
    # Updating visual display of maze and player current position
    draw()
