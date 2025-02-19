import pygame as pg
import math
from constants import *

class Tower:
    COSTS = {"basic": 50, "sniper": 100}  # Kostnad per tårn

    def __init__(self, x, y, tower_type="basic"):
        self.x = x
        self.y = y
        self.color = GREEN if tower_type == "basic" else RED
        self.type = tower_type

        if tower_type == "basic":
            self.range = 100
            self.damage = 1
        elif tower_type == "sniper":
            self.range = 200
            self.damage = 3

        self.rect = pg.Rect(self.x - 15, self.y - 15, 30, 30)

    def attack(self, zombies):
        """Skader zombier innenfor rekkevidden."""
        for zombie in zombies:
            distance = math.sqrt((self.x - zombie.x) ** 2 + (self.y - zombie.y) ** 2)
            if distance <= self.range:
                zombie.health -= self.damage
              

    def draw(self, screen):
        """Tegner tårnet på skjermen."""
        pg.draw.rect(screen, self.color, self.rect, border_radius=10)
        pg.draw.circle(screen, (0, 255, 0, 50), (self.x, self.y), self.range, 1)  # Tegner rekkevidden
