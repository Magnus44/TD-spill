import pygame as pg
from constants import *

class President:
    def __init__(self, x, y, width=50, height=50, color=RED):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.health = 10000
        self.rect = pg.Rect(self.x, self.y, self.width, self.height)

    def take_damage(self, amount):
        """Presidenten mister liv når han blir angrepet"""
        self.health -= amount
        print(f"Presidenten tok {amount} skade! Helse: {self.health}")

    def draw(self, screen):
        pg.draw.rect(screen, self.color, self.rect)
