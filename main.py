# hovedfilen
from constants import *
import pygame as pg

pg.init()
screen = pg.display.set_mode(SIZE)

from images import *
from president import President
from zombie import Zombie



clock = pg.time.Clock()

# Opprett presidenten
president = President(WIDTH//2, HEIGHT//2)

# Liste med zombier
zombies = [Zombie(president)]

# Variabler for zombie-bølger
last_spawn_time = pg.time.get_ticks()
spawn_interval = 10000  # 10 sekunder (10 000 ms)
zombies_per_wave = 1  # Starter med 1 zombie per wave
wave_count = 1  # Hvilken bølge vi er på
zombie_count = 0  # Totalt antall zombier som har spawnet

running = True
game_over = False

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    clock.tick(FPS)
    screen.fill(WHITE)
    screen.blit(map_image, (0, 0))  # Tegner bakgrunnen

    # Sjekk om spillet er over
    if president.health <= 0:
        game_over = True

    if not game_over:
        president.draw(screen)

        # Sjekk om det har gått 10 sekunder siden forrige wave
        current_time = pg.time.get_ticks()
        if current_time - last_spawn_time > spawn_interval:
            for _ in range(zombies_per_wave):
                zombie_count += 1  # Øk telleren for antall zombier totalt
                strong = (zombie_count % 10 == 0)  # Hver 10. zombie er sterk
                zombies.append(Zombie(president, strong))

            zombies_per_wave += 1  # Øker antall zombier i hver bølge
            wave_count += 1  # Øker bølge-telleren
            last_spawn_time = current_time  # Oppdater tid for siste spawn

        # Oppdater og tegn zombiene
        for zombie in zombies:
            zombie.move()
            zombie.draw(screen)
    else:
        # Tegn "GAME OVER" på skjermen
        font = pg.font.Font(None, 80)
        text = font.render("GAME OVER", True, RED)
        screen.blit(text, (WIDTH//2 - 150, HEIGHT//2 - 40))

    pg.display.update()

pg.quit()




