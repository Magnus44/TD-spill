import pygame as pg
import random
from constants import *
from president import President

class Zombie:
    def __init__(self, president, strong=False):
        """Oppretter en zombie, med bedre egenskaper om strong=True"""
        self.president = president
        self.size = 30
        self.color = BLUE if not strong else YELLOW  # Gul farge for sterke zombier
        
        if strong:
            self.speed = 0.5
            self.damage = 3
            self.health = 500
        else:
            self.speed = 1
            self.damage = 1
            self.health = 300

        # Velg tilfeldig startposisjon
        side = random.choice(["top", "left", "right", "bottom", "corner"])
        if side == "top":
            self.x, self.y = random.randint(0, WIDTH), -self.size
        elif side == "bottom":
            self.x, self.y = random.randint(0, WIDTH), HEIGHT
        elif side == "left":
            self.x, self.y = -self.size, random.randint(0, HEIGHT)
        elif side == "right":
            self.x, self.y = WIDTH, random.randint(0, HEIGHT)
        elif side == "corner":
            self.x, self.y = random.choice([(0, 0), (0, HEIGHT), (WIDTH, 0), (WIDTH, HEIGHT)])
        
        self.rect = pg.Rect(self.x, self.y, self.size, self.size)
        self.last_attack_time = 0  # Når zombien sist skadet presidenten

    def move(self):
        """Beveger zombien mot presidenten og skader ham hvis de kolliderer"""
        if self.rect.colliderect(self.president.rect):  # Treffer presidenten
            current_time = pg.time.get_ticks()
            if current_time - self.last_attack_time >= 1000:  # Hver 1000 ms (1 sekund)
                self.president.take_damage(self.damage)
                self.last_attack_time = current_time  # Oppdaterer tid for siste skade
        else:  # Fortsetter å bevege seg
            dx = self.president.x - self.x
            dy = self.president.y - self.y
            dist = max(1, (dx**2 + dy**2) ** 0.5)
            self.x += self.speed * (dx / dist)
            self.y += self.speed * (dy / dist)
            self.rect.topleft = (self.x, self.y)

    def draw(self, screen):
        pg.draw.rect(screen, self.color, self.rect)
