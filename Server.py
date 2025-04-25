import pygame
import random
import socket

IP = '127.0.0.1'
port = 66

# Build socket between server and client
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((IP, port))
server_socket.listen(1)

# Approve connection
client_socket, client_address = server_socket.accept()
print(f"Connection from {client_address} has been established!")

# End connection
server_socket.close()

# Screen Set
RES = 32
#      (columns, rows)
DIMS = (20,20)
SCREEN = (DIMS[0] * RES, DIMS[1] * RES)
pygame.init()
display = pygame.display.set_mode(SCREEN)
pygame.display.set_caption("The Maze")

#Class that creates walls and tiles
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

#Function that draws tiles
    def drawTile(self):
        pygame.draw.rect(display, self.color, self.rect)

#Function that draws walls
    def drawWalls(self):
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

#Grid creation
grid = []
for r in range(DIMS[1]):
#Tile row creation in grid
    tileRow = []
    for c in range(DIMS[0]):
        tile = Tile(c, r)
        tileRow.append(tile)
    grid.append(tileRow)

#Current tile (starting point)
ct = grid[0][0]
ct.visited = True

#Stack for back tracking
stack = [ct]

#Draw grid
def draw():
    display.fill("black")
    for tileRow in grid:
        for tile in tileRow:
            tile.drawTile()
    for tileRow in grid:
        for tile in tileRow:
            tile.drawWalls()
    pygame.display.flip()

#Get optional tiles to visit
def getNeigh(ct):
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

    return neigh

#Remove wall between chosen tile and current tile based on their relative positions
def tearDownWalls(ct, ch):
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

def update():
    global ct

#Mark visited tiles
    for tileRow in grid:
        for tile in tileRow:
            if tile.visited:
                tile.color = "blue"
            if tile == ct:
                tile.color = "red"

#Close pygame window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

#Choosing random neighbor, moving to it, tearing down wall between tiles
    validN = getNeigh(ct)
    if len(validN) > 0:
        chosen = random.choice(validN)
        tearDownWalls(ct, chosen)
        chosen.visited = True
        ct = chosen
        stack.append(chosen)

#Returning to previous tile in stack (back tracking) (if no unvisited neighbors)
    else:
        if len(stack) > 0:
            ct = stack.pop()

#Run
while True:
    draw()
    update()
    pygame.time.delay(20)
