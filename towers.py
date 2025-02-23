import pygame as pg
import math
from constants import *

class Bullet:
    """Kulene som tårnene skyter."""
    def __init__(self, x, y, target, damage):
        self.x = x
        self.y = y
        self.target = target
        self.damage = damage
        self.speed = 5  # Hastighet på kulene
        self.radius = 5  # Størrelse på kulene
        self.alive = True

    def move(self):
        """Beveger kulen mot målet."""
        if self.target and self.target.health > 0:
            dx = self.target.x - self.x
            dy = self.target.y - self.y
            distance = math.sqrt(dx**2 + dy**2)

            if distance > 0:
                self.x += (dx / distance) * self.speed
                self.y += (dy / distance) * self.speed

            # Sjekk om kulen har truffet zombien
            if distance < self.radius + 10:  # 10 er zombiestørrelse
                self.target.health -= self.damage
                self.alive = False  # Fjern kulen etter treff

    def draw(self, screen):
        """Tegner kulen på skjermen."""
        pg.draw.circle(screen, BLACK, (int(self.x), int(self.y)), self.radius)


class Tower:
    COSTS = {"basic": 50, "sniper": 100}  # Kostnad per tårn

    def __init__(self, x, y, tower_type="basic"):
        self.x = x
        self.y = y
        self.color = GREEN if tower_type == "basic" else RED
        self.type = tower_type
        self.health = 100  # Tårnets helse
        self.bullets = []  # Liste med kuler

        if tower_type == "basic":
            self.range = 100
            self.damage = 5
            self.attack_speed = 500  # Basic tårn skyter hvert 500 ms
        elif tower_type == "sniper":
            self.range = 200
            self.damage = 8
            self.attack_speed = 500  # Snipertårn skyter sjeldnere

        self.rect = pg.Rect(self.x - 15, self.y - 15, 30, 30)
        self.last_attack_time = 0  # Tidspunkt for siste angrep

    def attack(self, zombies):
        """Skaper en kule som beveger seg mot nærmeste zombie."""
        current_time = pg.time.get_ticks()
        if current_time - self.last_attack_time >= self.attack_speed:
            for zombie in zombies:
                distance = math.sqrt((self.x - zombie.x) ** 2 + (self.y - zombie.y) ** 2)
                if distance <= self.range:
                    self.bullets.append(Bullet(self.x, self.y, zombie, self.damage))
                    self.last_attack_time = current_time
                    break  # Bare skyt én kule per angrep

    def update_bullets(self):
        """Oppdaterer posisjonen til kulene og fjerner døde kuler."""
        for bullet in self.bullets[:]:
            bullet.move()
            if not bullet.alive:
                self.bullets.remove(bullet)

    def draw(self, screen):
        """Tegner tårnet, kulene og livsbar."""
        pg.draw.rect(screen, self.color, self.rect, border_radius=10)

        # Tegner helsebar over tårnet
        bar_width = 30
        bar_height = 5
        fill = max(0, (self.health / 100) * bar_width)
        outline_rect = pg.Rect(self.x - 15, self.y - 25, bar_width, bar_height)
        fill_rect = pg.Rect(self.x - 15, self.y - 25, fill, bar_height)

        pg.draw.rect(screen, RED, outline_rect)  # Bakgrunn i rød
        pg.draw.rect(screen, GREEN, fill_rect)  # Grønn for gjenværende helse

        # Tegn kulene
        for bullet in self.bullets:
            bullet.draw(screen)
