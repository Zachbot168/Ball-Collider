import pygame
import sys
import random
import math

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]

class Ball:
    def __init__(self, x, y, vx, vy, mass, radius, color):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.mass = mass
        self.radius = radius
        self.color = color

    def move(self):
        self.x += self.vx
        self.y += self.vy
        #Wall Collision
        if self.x - self.radius < 0 or self.x + self.radius > SCREEN_WIDTH:
            self.vx = -self.vx
        if self.y - self.radius < 0 or self.y + self.radius > SCREEN_HEIGHT:
            self.vy = -self.vy

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def collide(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance < self.radius + other.radius:
            self.ux, other.ux = self.vx, other.vx
            self.uy, other.uy = self.vy, other.vy
            total_mass = self.mass + other.mass
            self.vx = (self.ux * (self.mass - other.mass))/(total_mass) + (2 * other.ux * other.mass)/(total_mass)
            self.vy = (self.uy * (self.mass - other.mass))/(total_mass) + (2 * other.uy * other.mass)/(total_mass)
            other.vx = (2 * self.ux * self.mass / (total_mass)) + other.ux * (other.mass - self.mass) / (total_mass)
            other.vy = (2 * self.uy * self.mass / (total_mass)) + other.uy * (other.mass - self.mass) / (total_mass)

def create_random_ball():
    x = random.randint(20, SCREEN_WIDTH - 20)
    y = random.randint(20, SCREEN_HEIGHT - 20)
    vx = random.uniform(-5, 5)
    vy = random.uniform(-5, 5)
    mass = random.uniform(3, 10)
    radius = mass
    color = random.choice(COLORS)
    return Ball(x, y, vx, vy, mass, radius, color)

def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Ball Collision: Press Space to Create New Ball")
    clock = pygame.time.Clock()

    # Start with one ball
    balls = [create_random_ball()]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    balls.append(create_random_ball())

        screen.fill(BLACK)

        for ball in balls:
            ball.move()
            ball.draw(screen)
            for other_ball in balls:
                if ball != other_ball:
                    ball.collide(other_ball)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


main()
