import pygame
from  queue import PriorityQueue
pygame.init()
width = 600
rows = 50
win = pygame.display.set_mode((width,width))
pygame.display.set_caption("Shortest Path with obstruction(A* Algorithm)")
class Node:
    def __init__(self, i, j, width, rows):
        self.width = width
        self.x = i
        self.y = j
        self.rows = rows
        self.color = (255,255,255)
        self.gap = self.width // self.rows
    def make_start(self,win):
        self.color = (255, 165 ,0) #orange

    def make_end(self,win):
        self.color = (128,0,128) #green

    def make_block(self,win):
        self.color = (0, 0 ,0) #black

    def draw(self,win):
        pygame.draw.rect(win, self.color, (self.y*self.gap, self.x *self.gap, self.gap,self.gap))
    def make_boundary(self):
        self.color = (255,0,0)
    def make_closed(self):
        self.color = (0,0,255)
    def reset_node(self):
        self.color = (255,255,255)
    def isbarrier(self):
        if self.color == (0,0,0):
            return True
        else:
            return False
    def find_neighbour(self, grid):
        self.neighbour = []
        if self.x>0 and not grid[self.x-1][self.y].isbarrier(): #left
            self.neighbour.append(grid[self.x-1][self.y])
        if self.x<self.rows -1 and not grid[self.x+1][self.y].isbarrier(): #right
            self.neighbour.append(grid[self.x+1][self.y])
        if self.y >0 and not grid[self.x][self.y-1].isbarrier(): #up
            self.neighbour.append(grid[self.x][self.y-1])
        if self.y <self.rows -1 and not grid[self.x][self.y+1].isbarrier():#down
            self.neighbour.append(grid[self.x][self.y+1])

    def position(self):
        position = self.x, self.y
        return position

def draw_endpath(path, end, draw, start):
    current = end
    while current!=start:
        if path[current]==start:
            current = path[current]
        else:
            current = path[current]
            current.color = (0,255,0)
        draw()



def h_score(position1, position2):
    x1,y1 = position1
    x2, y2 = position2
    return abs(x1-x2) + abs(y1-y2)

def make_grid(rows, width):
    grid = []
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i,j,width, rows)
            grid[i].append(node)
    return grid

def draw_grid(rows, width, win):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win,(0,0,0),(0,i*gap),(width,i*gap))
        pygame.draw.line(win,(0,0,0),(i*gap,0),(i*gap,width))

def draw_nodes(rows, width, win, grid):
    win.fill((255, 255, 255))
    for row in grid:
        for node in row:
            node.draw(win)
    draw_grid(rows, width, win)
    pygame.display.update()



def algorithm(draw, start,end, grid):
    tie_breaker = 0
    open_set = PriorityQueue()
    open_set.put((0,tie_breaker, start))
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = h_score(start.position(),end.position())
    from_path = {}
    open_set_hash = {start}
    while not open_set.empty():
        current = open_set.get()[2]
        open_set_hash.remove(current)
        if current == end:
            draw_endpath(from_path, end, draw, start)
            return True
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                pygame.quit()
        for neighbour in current.neighbour:
            temp_g_score = g_score[current] +1
            if temp_g_score < g_score[neighbour]:
                g_score[neighbour] = temp_g_score
                f_score[neighbour] = g_score[neighbour] + h_score(neighbour.position(), end.position())
                if neighbour not in open_set_hash:
                    open_set_hash.add(neighbour)
                    tie_breaker+=1
                    open_set.put((f_score[neighbour],tie_breaker, neighbour))
                    if neighbour!=end:
                        neighbour.make_boundary()
                    from_path[neighbour] = current
        draw()
        if current!= start and current!= end:
            current.make_closed()
    return False

grid = make_grid(rows,width)
draw_grid(rows,width,win)
pygame.display.update()
start = None
end = None
gap = width//rows
run = True

while run:
    draw_nodes(rows, width, win, grid)
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            run = False
            pygame.quit()
        elif pygame.mouse.get_pressed()[0]:
            position = pygame.mouse.get_pos()
            x = position[1] // gap
            y = position[0] // gap
            node = grid[x][y]
            if not start and node != end:
                start = node
                node.make_start(win)
            elif not end and start!=node:
                end = node
                node.make_end(win)
            elif end!=node and start!=node:
                node.make_block(win)
        elif pygame.mouse.get_pressed()[2]:
            position = pygame.mouse.get_pos()
            x = position[1] // gap
            y = position[0] // gap
            node = grid[x][y]
            if node == start:
                start = None
                node.reset_node()
            elif node == end:
                end = None
                node.reset_node()
            else:
                node.reset_node()

        if events.type == pygame.KEYDOWN:
            if events.key == pygame.K_SPACE and start and end:
                for row in grid:
                    for node in row:
                        node.find_neighbour(grid)
                if algorithm(lambda: draw_nodes(rows, width, win, grid), start, end, grid):
                    print("found the shortest path")
                else:
                    print("There is no path")
pygame.quit()


