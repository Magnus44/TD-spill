import pygame as pg
from constants import *

class President:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = 100  # Maks helse
        self.max_health = 100

    def draw(self, screen):
        pg.draw.rect(screen, BLUE, (self.x - 20, self.y - 20, 40, 40), border_radius=10)
        self.draw_health_bar(screen)

    def draw_health_bar(self, screen):
        bar_width = 50
        bar_height = 5
        fill = (self.health / self.max_health) * bar_width
        outline_rect = pg.Rect(self.x - 25, self.y - 30, bar_width, bar_height)
        fill_rect = pg.Rect(self.x - 25, self.y - 30, fill, bar_height)

        pg.draw.rect(screen, RED, outline_rect)  # Bakgrunn i rød
        pg.draw.rect(screen, GREEN, fill_rect)  # Grønn for gjenværende helse
