import pygame
import math
import random

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Real-Time Tactical Battle")

clock = pygame.time.Clock()

# Colors
RED = (200, 50, 50)
BLUE = (50, 50, 200)
WHITE = (255, 255, 255)
GREEN = (50, 200, 50)
YELLOW = (255, 255, 0)

# Unit class
class Unit:
    def __init__(self, x, y, color, team):
        self.x = x
        self.y = y
        self.radius = 10
        self.color = color
        self.team = team
        self.hp = 100
        self.speed = 1.5
        self.target = None
        self.destination = None
        self.selected = False

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.rect(screen, GREEN, (self.x - 10, self.y - 15, self.hp / 10, 4))
        if self.selected:
            pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), self.radius + 2, 1)

    def move(self):
        if self.destination:
            dx, dy = self.destination[0] - self.x, self.destination[1] - self.y
            dist = math.hypot(dx, dy)
            if dist > 2:
                self.x += dx / dist * self.speed
                self.y += dy / dist * self.speed
            else:
                self.destination = None

    def move_toward(self, target):
        if target:
            dx, dy = target.x - self.x, target.y - self.y
            dist = math.hypot(dx, dy)
            if dist > 20:
                self.x += dx / dist * self.speed * 0.5
                self.y += dy / dist * self.speed * 0.5

    def attack(self, target):
        if target and math.hypot(target.x - self.x, target.y - self.y) < 20:
            target.hp -= 0.3

    def find_enemy(self, enemy_list):
        closest = None
        closest_dist = float('inf')
        for enemy in enemy_list:
            dist = math.hypot(enemy.x - self.x, enemy.y - self.y)
            if dist < closest_dist:
                closest = enemy
                closest_dist = dist
        self.target = closest


# Create teams
red_team = [Unit(100, 100 + i*30, RED, "red") for i in range(5)]
blue_team = [Unit(700, 100 + i*30, BLUE, "blue") for i in range(5)]
all_units = red_team + blue_team

# Game loop
running = True
selected_unit = None

while running:
    screen.fill(WHITE)
    mx, my = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Left-click to select a unit
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            selected_unit = None
            for unit in all_units:
                if math.hypot(mx - unit.x, my - unit.y) <= unit.radius:
                    if unit.team == "red":  # You control red team
                        selected_unit = unit
                        unit.selected = True
                    else:
                        unit.selected = False
                else:
                    unit.selected = False

        # Right-click to move selected unit
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            if selected_unit:
                selected_unit.destination = (mx, my)

    # Draw and update units
    for unit in all_units:
        unit.draw()
        unit.move()
        if unit.team == "red":
            unit.find_enemy(blue_team)
        else:
            unit.find_enemy(red_team)

        unit.move_toward(unit.target)
        unit.attack(unit.target)

    # Remove dead units
    red_team = [u for u in red_team if u.hp > 0]
    blue_team = [u for u in blue_team if u.hp > 0]
    all_units = red_team + blue_team

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
