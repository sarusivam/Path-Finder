import pygame



def find_path(maze, start_pos, end_pos):
    visited = list()
    def isEnd(maze : list, directions : str):
        x,y = start_pos
        for d in directions:
            if d == "l":
                x -= 1
            elif d == "r":
                x += 1
            elif d == "u":
                y -= 1
            elif d == "d":
                y += 1
        return ( x,y) == end_pos

    def valid_move(move : str, map : list):
            x,y = start_pos
            for direction in move:
                if direction.lower() == "l":
                    x -= 1
                elif direction.lower() == "r":
                    x += 1
                elif direction.lower() == "u":
                    y -= 1
                elif direction.lower() == "d":
                    y += 1

            is_valid = all([y >= 0, y <= len(map) - 1, x >= 0, x <= len(map[0]) - 1,not((x,y) in visited)])
            if is_valid:
                visited.append((x,y))
            return is_valid and map[y][x] != 1
    all_dirs = [""]
    current_dir = all_dirs[0]

    while not isEnd(maze, current_dir):
        all_dirs.pop(0)
        for move in ["l", "r", "u", "d"]:

            if valid_move(current_dir + move, maze):
                all_dirs.append(current_dir + move)
        if all_dirs:
            current_dir = all_dirs[0]
        else:
            return False
    x,y = start_pos
    coords = []
    for direction in current_dir:
        if direction.lower() == "l":
            x -= 1
        elif direction.lower() == "r":
            x += 1
        elif direction.lower() == "u":
            y -= 1
        elif direction.lower() == "d":
            y += 1
        if direction in ['l', 'r', 'u', 'd']:
            coords.append((direction, (x,y)))
    return coords










WIDTH = 750
HEIGHT = 750
grid_boxes = []
map_2d = [[0 for _ in range(25)] for _ in range(25)]
map_2d[0][0] = 2
start_pos,end_pos = (0,0),(24,24)

class GridBox:
    BORDER_COLOR = (0,0,0)
    def __init__(self, x, y, size, color, border_width=1) -> None:
        self.rect = pygame.Rect(x,y,size,size)
        self._color = color
        self.border_width = border_width
    @property
    def color(self) -> tuple:
        return self._color
    @color.setter
    def color(self, color) -> None:
        assert type(color) is tuple, "Type color must be tuple !!!"
        self._color = color
    @staticmethod
    def inverse_color(color : tuple) -> tuple:
            r,g,b = color
            return (255-r,255-g,255-b)
    def draw(self, win : pygame.Surface) -> None:
        pygame.draw.rect(win , self._color, self.rect)
        
        #Borders
        pygame.draw.rect(win, self.BORDER_COLOR, pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.border_width))
        pygame.draw.rect(win, self.BORDER_COLOR, pygame.Rect(self.rect.x, self.rect.y, self.border_width, self.rect.height))
        pygame.draw.rect(win, self.BORDER_COLOR, pygame.Rect(self.rect.x, self.rect.y+self.rect.height-self.border_width, self.rect.width, self.border_width))
        pygame.draw.rect(win, self.BORDER_COLOR, pygame.Rect(self.rect.x+self.rect.width-self.border_width, self.rect.y, self.border_width, self.rect.height))


FPS = 60
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DFS Visual")
clock = pygame.time.Clock()
running = True

for x in range(25):
    for y in range(25):
        grid_boxes.append(GridBox(x*30,y*30,30,(255,255,255)))
grid_boxes[0].color, grid_boxes[-1].color = (255,0,0), (0,0,255)

choosing_start = False
choosing_end = False
while running:
    window.fill((255, 255,255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        if event.type == pygame.MOUSEBUTTONUP:
            for grid in grid_boxes:
                if grid.color == (0,255,0):
                    grid.color = (255,255,255)
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for grid in grid_boxes:
                if mouse_x > grid.rect.x and mouse_y > grid.rect.y and mouse_x < grid.rect.x + grid.rect.width and mouse_y < grid.rect.y + grid.rect.height:
                    if choosing_start and grid.color != (0,0,0) and grid.color != (0,0,255):
                        grid.color = (255, 0, 0)
                        start_pos = int(grid.rect.x/30), int(grid.rect.y/30)
                        choosing_start = False
                        break   
                    if choosing_end and grid.color != (0,0,0) and grid.color != (255,0,0):
                        grid.color = (0,0,255)
                        end_pos = int(grid.rect.x/30), int(grid.rect.y/30)
                        choosing_end = False
                        break
                    if grid.color == (255, 0, 0):
                        choosing_start = True
                        grid.color = (255,255,255)
                        break
                    if grid.color == (0,0,255):
                        choosing_end = True
                        grid.color = (255,255,255)
                        break
                    if grid.color == (0,0,0) or grid.color == (255,255,255):
                        grid.color = GridBox.inverse_color(grid.color)
                        x,y = int(grid.rect.x/30), int(grid.rect.y/30)
                    if grid.color == (0,0,0):
                        map_2d[y][x] = 1
                    else:
                        map_2d[y][x] = 0
                    break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                path = find_path(map_2d, start_pos, end_pos)
                if path:

                    for _, (x,y) in path:
                        for grid in grid_boxes:
                            g_x, g_y = int(grid.rect.x/30), int(grid.rect.y/30)
                            if x == g_x and y == g_y and (x,y) != end_pos:
                                grid.color = (0,255,0)



    for grid_box in grid_boxes:
        grid_box.draw(window)
    pygame.display.update()
    