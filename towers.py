import pygame as pg
import math
from constants import *
from zombie import *

class Bullet:
    def __init__(self, x, y, target, damage):
        self.x = x
        self.y = y
        self.target = target
        self.damage = damage
        self.speed = 5
        self.radius = 5
        self.alive = True

    def move(self):
        if not self.target or self.target.health <= 0:
            self.alive = False
            return

        dx = self.target.x - self.x
        dy = self.target.y - self.y
        distance = math.sqrt(dx**2 + dy**2)

        if distance > 0:
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed

        if distance < self.radius + 10:
            self.target.health -= self.damage
            self.alive = False

    def draw(self, screen):
        pg.draw.circle(screen, BLACK, (int(self.x), int(self.y)), self.radius)


class Tower:
    COSTS = {"basic": 50, "sniper": 100}

    def __init__(self, x, y, tower_type="basic"):
        self.x = x
        self.y = y
        self.color = GREEN if tower_type == "basic" else RED
        self.type = tower_type
        self.health = 100
        self.bullets = []

        if tower_type == "basic":
            self.range = 100
            self.damage = 5
            self.attack_speed = 500
        elif tower_type == "sniper":
            self.range = 200
            self.damage = 8
            self.attack_speed = 500

        self.rect = pg.Rect(self.x - 15, self.y - 15, 30, 30)
        self.last_attack_time = 0

    def attack(self, zombies):
        current_time = pg.time.get_ticks()
        if current_time - self.last_attack_time >= self.attack_speed:
            for zombie in zombies:
                distance = math.sqrt((self.x - zombie.x) ** 2 + (self.y - zombie.y) ** 2)
                if distance <= self.range:
                    self.bullets.append(Bullet(self.x, self.y, zombie, self.damage))
                    self.last_attack_time = current_time
                    break

    def update_bullets(self):
        for bullet in self.bullets[:]:
            bullet.move()
            if not bullet.alive:
                self.bullets.remove(bullet)

    def draw(self, screen):
        pg.draw.rect(screen, self.color, self.rect, border_radius=10)

        bar_width = 30
        bar_height = 5
        fill = max(0, (self.health / 100) * bar_width)
        outline_rect = pg.Rect(self.x - 15, self.y - 25, bar_width, bar_height)
        fill_rect = pg.Rect(self.x - 15, self.y - 25, fill, bar_height)

        pg.draw.rect(screen, RED, outline_rect)
        pg.draw.rect(screen, GREEN, fill_rect)

        for bullet in self.bullets:
            bullet.draw(screen)

    def draw_range(self, screen):
        pg.draw.circle(screen, (0, 255, 0, 100), (self.x, self.y), self.range, 1)
