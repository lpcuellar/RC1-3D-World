import pygame

from math import cos, sin, pi

##  declaración de colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BG = (96, 96, 96)

colors = {
    '1' : (33, 37, 63),
    '2' : (166, 27, 23),
    '3' : (206, 220, 56),
    '4' : (5, 163, 5),
    '5' : (96, 96, 96),
}

class RayCaster(object):
    def __init__(self, screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()

        self.map = []
        self.block_size = 50
        self.wall_height = 50

        self.step_size = 5

        self.setColor(WHITE)

        self.player = {
            'x': 75,
            'y': 175, 
            'angle': 0,
            'fov': 60,
        }

    def setColor(self, color):
        self.block_color = color
    
    def loadMap(self, filename):
        with open(filename) as mapFile:
            for line in mapFile.readlines():
                self.map.append(list(line))

    def drawRect(self, x, y, color = WHITE):
        rect = (x, y, self.block_size, self.block_size)
        self.screen.fill(color, rect)

    def drawPlayerIcon(self, color):
        rect = (self.player['x'] - 2, self.player['y'] - 2, 5, 5)
        self.screen.fill(color, rect)

    def castRay(self, angle):
        rads = angle * pi / 180
        dist = 0

        while True:
            x = int(self.player['x'] + dist * cos(rads))
            y = int(self.player['y'] + dist * sin(rads))

            i = int(x / self.block_size)
            j = int(y / self.block_size)

            if self.map[j][i] != ' ':
                return dist, self.map[j][i]
            
            self.screen.set_at((x, y), WHITE)
            dist += 5

    def render(self):
        half_width = int(self.width / 2)
        half_height = int(self.height / 2)

        for x in range(0, half_width, self.block_size):
            for y in range(0, self.height, self.block_size):
                i = int(x / self.block_size)
                j = int(y / self.block_size)

                if self.map[j][i] != ' ':
                    self.drawRect(x, y, colors[self.map[j][i]])

        self.drawPlayerIcon(BLACK)

        for i in range(half_width):
            angle = self.player['angle'] - self.player['fov'] / 2 + self.player['fov'] * i / half_width
            dist, c = self.castRay(angle)

            x = half_width + i

            h = self.height / (dist * cos((angle - self.player['angle']) * pi / 180)) * self.wall_height

            start = int(half_height - h / 2)
            finish = int(half_height + h / 2)

            for y in range(start, finish):
                self.screen.set_at((x, y), colors[c])

        for i in range(self.height):
            self.screen.set_at((half_width, i), BLACK)
            self.screen.set_at((half_width + 1, i), BLACK)
            self.screen.set_at((half_width - 1, i), BLACK)
            


pygame.init()
screen = pygame.display.set_mode((1800, 900))

ray = RayCaster(screen)

ray.setColor((128, 0, 0))
ray.loadMap('map.txt')

isRunning = True

while isRunning:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            isRunning = False
        
        elif ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_ESCAPE:
                isRunning = False
            
            elif ev.key == pygame.K_w:
                ray.player['x'] += cos(ray.player['angle'] * pi / 180) * ray.step_size
                ray.player['y'] += sin(ray.player['angle'] * pi / 180) * ray.step_size
            
            elif ev.key == pygame.K_s:
                ray.player['x'] -= cos(ray.player['angle'] * pi / 180) * ray.step_size
                ray.player['y'] -= sin(ray.player['angle'] * pi / 180) * ray.step_size
           
            elif ev.key == pygame.K_a:
                ray.player['x'] -= cos((ray.player['angle'] + 90) * pi / 180) * ray.step_size
                ray.player['y'] -= sin((ray.player['angle'] + 90) * pi / 180) * ray.step_size
            
            elif ev.key == pygame.K_d:
                ray.player['x'] += cos((ray.player['angle'] + 90) * pi / 180) * ray.step_size
                ray.player['y'] += sin((ray.player['angle'] + 90) * pi / 180) * ray.step_size
            
            elif ev.key == pygame.K_q:
                ray.player['angle'] -= 5
            
            elif ev.key == pygame.K_e:
                ray.player['angle'] += 5

    screen.fill(BG)
    ray.render()

    pygame.display.flip()

pygame.quit() 