import pygame as pg
import math
import random
from constants import *
from president import President
from towers import Tower

class Zombie:
    def __init__(self, president, strong=False):
        # Zombien starter på en tilfeldig posisjon rundt kantene av skjermen
        edge = random.choice(["top", "bottom", "left", "right"])
        if edge == "top":
            self.x, self.y = random.randint(0, WIDTH), 0
        elif edge == "bottom":
            self.x, self.y = random.randint(0, WIDTH), HEIGHT
        elif edge == "left":
            self.x, self.y = 0, random.randint(0, HEIGHT)
        elif edge == "right":
            self.x, self.y = WIDTH, random.randint(0, HEIGHT)

        self.speed = 1.5 if strong else 1  # Sterkere zombier er raskere
        self.max_health = 30 if strong else 20  # Sterkere zombier har mer liv
        self.health = self.max_health  # Alle starter med fullt liv
        self.color = YELLOW if strong else RED  # Farge basert på styrke
        self.target = president  # Startmål er presidenten

    def find_nearest_target(self, towers, president):
        """Finner nærmeste mål: Enten et tårn eller presidenten."""
        nearest = president
        min_distance = math.sqrt((self.x - president.x) ** 2 + (self.y - president.y) ** 2)

        for tower in towers:
            distance = math.sqrt((self.x - tower.x) ** 2 + (self.y - tower.y) ** 2)
            if distance < min_distance:
                nearest = tower
                min_distance = distance

        self.target = nearest  # Sett nærmeste mål som target

    def move(self):
        """Beveger zombien mot målet sitt."""
        if self.target:
            dx, dy = self.target.x - self.x, self.target.y - self.y
            distance = math.sqrt(dx**2 + dy**2)
            if distance > 0:
                self.x += (dx / distance) * self.speed
                self.y += (dy / distance) * self.speed

    def draw(self, screen):
        """Tegner zombien og livsbaren over den."""
        pg.draw.circle(screen, self.color, (int(self.x), int(self.y)), 15)

        # Helsebar
        health_bar_width = 30
        health_ratio = self.health / self.max_health  # Hvor mye liv er igjen
        pg.draw.rect(screen, BLACK, (self.x - 15, self.y - 20, health_bar_width, 5))  # Bakgrunn
        pg.draw.rect(screen, GREEN, (self.x - 15, self.y - 20, health_bar_width * health_ratio, 5))  # Grønn bar

    def attack(self):
        """Skader målet sitt hvis det er nært nok."""
        if isinstance(self.target, President) or isinstance(self.target, Tower):
            distance = math.sqrt((self.x - self.target.x) ** 2 + (self.y - self.target.y) ** 2)
            if distance < 20:  # Innenfor angrepsradius
                self.target.health -= 1  # Reduser liv
