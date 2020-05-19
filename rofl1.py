import pygame
from enum import Enum
import random

pygame.init()
random.seed


def message(msg, color, cords, font, screen):
    txt = font.render(msg, True, color)
    screen.blit(txt, cords)


def GameOver(msg, font, screen):
    screen.fill((255, 255, 255))
    message(msg, (0, 0, 0), [400, 300], font, screen)
    message('Press esc to exit', (0, 0, 0), [400, 500], font, screen)
    pygame.display.flip()


class Super:
    def __init__(self):
        self.x, self.y = (random.randint(0, 799), random.randint(0, 599))

    def tank_inter(self, tank):
        if abs(tank.x - self.x) <= 15 and abs(tank.y - self.y) <= 15:
            tank.boost = 1000

    def draw(self, screen):
        pygame.draw.circle(screen, (173, 216, 230), (self.x, self.y), 3)


class Wall:
    def __init__(self):
        self.health = 3
        self.x, self.y = (random.randint(0, 799), random.randint(0, 599))

    def tank_inter(self, tank):
        if abs(tank.x - self.x) <= 15 and abs(tank.y - self.y) <= 15:
            tank.health -= 1

    def bullet_inter(self, Bull):
        if abs(Bull.x - self.x) <= 5 and abs(Bull.y - self.y) <= 5:
            self.health -= 1
            return True
        return False

    def draw(self, screen):
        pygame.draw.rect(screen, (173, 216, 230), (self.x, self.y, 25, 25), 2)


class Bull():
    def __init__(self, x, y, r, color, facing, target, timing):
        self.x = x
        self.y = y
        self.r = r
        self.color = color
        self.facing = facing
        self.vel = 8
        self.target = target
        self.timing = timing

    def life(self, ticks, FPS):
        if ticks - self.timing > 5 * FPS:
            return False
        return True

    def getTarget(self, tank1, tank2):
        if self.target == 1:
            # print(self.x, self.y, tank1.x, tank1.y)
            if abs(self.x - (tank1.x + tank1.width // 2)) <= 20 and abs(self.y - (tank1.y + tank1.width // 2)) <= 20:
                tank1.health -= 1
                return True
            return False
        else:
            # print(self.x, self.y, tank2.x, tank2.y)
            if abs(self.x - (tank2.x + tank1.width // 2)) <= 20 and abs(self.y - (tank1.y + tank2.width // 2)) <= 20:
                tank2.health -= 1
                return True
            return False

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)

    def movement(self, screen):
        if self.facing == Direction.LEFT:
            self.x -= self.vel
        if self.facing == Direction.RIGHT:
            self.x += self.vel
        if self.facing == Direction.UP:
            self.y -= self.vel
        if self.facing == Direction.DOWN:
            self.y += self.vel
        if self.x + self.r <= 0:
            self.x = 800
        elif self.x >= 800:
            self.x = 0
        if self.y + self.r <= 0:
            self.y = 600
        elif self.y >= 600:
            self.y = 0
        self.draw(screen)


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class Tank:

    def __init__(self, x, y, speed, color, health, lastShot, delay=60, d_right=pygame.K_RIGHT, d_left=pygame.K_LEFT,
                 d_up=pygame.K_UP, d_down=pygame.K_DOWN):
        self.boost = 0
        self.x = abs(x % 800)
        self.y = abs(y % 600)
        self.speed = speed
        self.color = color
        self.width = 40
        self.direction = Direction.RIGHT
        self.health = health
        self.lastShot = lastShot
        self.key = {d_right: Direction.RIGHT, d_left: Direction.LEFT, d_up: Direction.UP, d_down: Direction.DOWN}
        self.delay = delay

    def shoot(self, target, boom, ticks, bullets):
        if ticks - self.lastShot < self.delay:
            return
        boom.play()
        bult = Bull(self.x, self.y + self.width // 2, 7, (255, 0, 0), self.direction, target, ticks)
        bullets.append(bult)
        self.lastShot = ticks

    def draw(self, screen):
        tank_c = (self.x + int(self.width / 2), self.y + int(self.width / 2))
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.width), 2)
        pygame.draw.circle(screen, self.color, tank_c, int(self.width / 2))

        if self.direction == Direction.RIGHT:
            pygame.draw.line(screen, self.color, tank_c,
                             (self.x + self.width + int(self.width / 2), self.y + int(self.width / 2)), 4)

        if self.direction == Direction.LEFT:
            pygame.draw.line(screen, self.color, tank_c, (self.x - int(self.width / 2), self.y + int(self.width / 2)),
                             4)

        if self.direction == Direction.UP:
            pygame.draw.line(screen, self.color, tank_c, (self.x + int(self.width / 2), self.y - int(self.width / 2)),
                             4)

        if self.direction == Direction.DOWN:
            pygame.draw.line(screen, self.color, tank_c,
                             (self.x + int(self.width / 2), self.y + self.width + int(self.width / 2)), 4)

    def change_direction(self, direction):

        if self.direction == direction:
            self.speed = 10
        else:
            self.direction = direction
            self.speed = 5

    def move(self, screen):
        if self.direction == Direction.LEFT:
            self.x -= self.speed
        if self.direction == Direction.RIGHT:
            self.x += self.speed
        if self.direction == Direction.UP:
            self.y -= self.speed
        if self.direction == Direction.DOWN:
            self.y += self.speed
        if self.x + self.width <= 0:
            self.health -= 1
            self.x = 800
        elif self.x >= 800:
            self.health -= 1
            self.x = 0
        if self.y + self.width <= 0:
            self.health -= 1
            self.y = 600
        elif self.y >= 600:
            self.health -= 1
            self.y = 0
        if self.boost:
            if self.direction == Direction.LEFT:
                self.x -= self.speed
            if self.direction == Direction.RIGHT:
                self.x += self.speed
            if self.direction == Direction.UP:
                self.y -= self.speed
            if self.direction == Direction.DOWN:
                self.y += self.speed
            if self.x + self.width <= 0:
                self.health -= 1
                self.x = 800
            elif self.x >= 800:
                self.health -= 1
                self.x = 0
            if self.y + self.width <= 0:
                self.health -= 1
                self.y = 600
            elif self.y >= 600:
                self.health -= 1
                self.y = 0
            self.boost -= 1
        self.draw(screen)


class Game():
    def __init__(self, screen):
        self.b = []
        self.walls = []
        self.screen = screen
        self.font = pygame.font.SysFont(None, 25, bold=True)

        pygame.mixer.music.load('music.mp3')
        pygame.mixer.music.set_volume(2)
        pygame.mixer.music.play(-1)

        self.boom = pygame.mixer.Sound('boom.wav')
        self.mainloop = True
        self.tank1 = Tank(300, 300, 5, (255, 123, 100), 3, -500)
        self.tank2 = Tank(300, 300, 5, (100, 230, 40), 3, -500, 60, pygame.K_d, pygame.K_a, pygame.K_w, pygame.K_s)
        self.FPS = 30
        self.bullets = []
        self.clock = pygame.time.Clock()
        self.millis = self.clock.tick(self.FPS)
        self.ticks = 0
        self.over = ''

    def run(self):
        while self.mainloop:
            ran = random.randint(1, 100)
            if ran == 5 and len(self.walls) < 4:
                self.walls.append(Wall())
            if ran == 100 and len(self.b) < 3:
                self.b.append(Super())
            while self.over:
                GameOver(self.over, self.font, self.screen)
                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            exit()
            ind = 0
            l = []
            self.millis = self.clock.tick(self.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.mainloop = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.mainloop = False
                    if event.key == pygame.K_SPACE:
                        self.tank2.shoot(1, self.boom, self.ticks, self.bullets)
                    if event.key == pygame.K_RETURN:
                        self.tank1.shoot(2, self.boom, self.ticks, self.bullets)
                    if event.key in self.tank1.key.keys():
                        self.tank1.change_direction(self.tank1.key[event.key])
                    if event.key in self.tank2.key.keys():
                        self.tank2.change_direction(self.tank2.key[event.key])

            self.screen.fill((0, 0, 0))

            ind1 = 0
            s = []
            ind2 = 0
            sp = []
            for bullet in self.bullets:
                bullet.movement(self.screen)
                if bullet.getTarget(self.tank1, self.tank2) or not bullet.life(self.ticks, self.FPS):
                    # print('Hello')
                    l.append(ind)
                ind += 1
            for current in l:
                self.bullets.pop(current)
            ind = 0
            for wall in self.walls:
                wall.draw(self.screen)
                if (self.ticks % 4) == 0:
                    wall.tank_inter(self.tank1)
                    wall.tank_inter(self.tank2)
                for bullet in self.bullets:
                    if wall.bullet_inter(bullet):
                        l.append(ind)
                    ind += 1
                if wall.health == 0:
                    s.append(ind1)
                ind1 += 1
            for current in s:
                self.walls.pop(current)
            l = set(l)
            for current in l:
                self.bullets.pop(current)
            for current in self.b:
                current.draw(self.screen)
                if current.tank_inter(self.tank1):
                    sp.append(ind2)
                elif current.tank_inter(self.tank2):
                    sp.append(ind2)
                ind2 += 1
            for current in sp:
                self.b.pop(current)
            message(str(self.tank1.health), (255, 255, 255), [20, 20], self.font, self.screen)
            message(str(self.tank2.health), (255, 255, 255), [700, 20], self.font, self.screen)
            self.tank1.move(self.screen)
            self.tank2.move(self.screen)
            pygame.display.flip()
            self.ticks += 1
            if self.tank1.health == 0:
                self.over = 'TANK 2 WIN'
            elif self.tank2.health == 0:
                self.over = 'TANK 1 WIN'


pygame.quit()
