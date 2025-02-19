# hovedfilen
from constants import *
import pygame as pg

pg.init()
screen = pg.display.set_mode(SIZE)

from images import *
from president import President
from zombie import Zombie
from towers import Tower


clock = pg.time.Clock()

# Opprett presidenten
president = President(WIDTH//2, HEIGHT//2)

# Liste med zombier
zombies = [Zombie(president)]

towers = []

# Variabler for økonomi og tårnkjøp
money = 100  # Startpenger
selected_tower = None  # Spillerens valgte tårn


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

        # Klikk for valg av tårn
        elif event.type == pg.MOUSEBUTTONDOWN:
            x, y = pg.mouse.get_pos()
            
            # Sjekk om klikket var i menyområdet (øverst til venstre)
            if 10 <= x <= 110 and 10 <= y <= 60:
                selected_tower = "basic"
            elif 120 <= x <= 220 and 10 <= y <= 60:
                selected_tower = "sniper"
            
            # Hvis spilleren har valgt et tårn, prøv å plassere det
            elif selected_tower:
                cost = Tower.COSTS[selected_tower]
                if money >= cost:
                    money -= cost
                    towers.append(Tower(x, y, selected_tower))
                    selected_tower = None  # Nullstill valg


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
            if zombie.health <= 0:
                zombies.remove(zombie)
                money += 10  # Spilleren får 10 penger per drept zombie


        # TÅRNENE ANGRIPER ZOMBIER
        for tower in towers:
            tower.attack(zombies)
            tower.draw(screen)

        # TEGNER MENY FOR KJØP AV TÅRN
        pg.draw.rect(screen, GREEN, (10, 10, 100, 50))  # Basic Tower
        pg.draw.rect(screen, RED, (120, 10, 100, 50))  # Sniper Tower
        font = pg.font.Font(None, 24)
        screen.blit(font.render("Basic: 50", True, WHITE), (20, 25))
        screen.blit(font.render("Sniper: 100", True, WHITE), (130, 25))
        screen.blit(font.render(f"Penger: {money}", True, BLACK), (WIDTH - 150, 10))

    else:
        # Tegn "GAME OVER" på skjermen
        font = pg.font.Font(None, 80)
        text = font.render("GAME OVER", True, RED)
        screen.blit(text, (WIDTH//2 - 150, HEIGHT//2 - 40))

    pg.display.update()

pg.quit()




