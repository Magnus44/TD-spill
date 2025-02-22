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
president = President(WIDTH // 2, HEIGHT // 2)

# Lister for spillobjekter
zombies = []
towers = []

# Økonomi og kjøp
money = 100  # Startpenger
selected_tower = None  # Spillerens valgte tårn

# Zombie-bølgevariabler
last_spawn_time = pg.time.get_ticks()
spawn_interval = 10000  # 10 sekunder
zombies_per_wave = 1
wave_count = 1
zombie_count = 0

running = True
game_over = False

while running:
    screen.fill(WHITE)
    screen.blit(map_image, (0, 0))  # Tegner bakgrunnen

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        # Klikk for valg av tårn eller plassering
        elif event.type == pg.MOUSEBUTTONDOWN:
            x, y = pg.mouse.get_pos()
            
            # Sjekk om klikket var på kjøpsknappene
            if 10 <= x <= 110 and 10 <= y <= 60:
                selected_tower = "basic"
            elif 120 <= x <= 220 and 10 <= y <= 60:
                selected_tower = "sniper"

            # Plasser tårn hvis valgt
            elif selected_tower:
                if selected_tower in Tower.COSTS:
                    cost = Tower.COSTS[selected_tower]
                    if money >= cost:
                        money -= cost
                        towers.append(Tower(x, y, selected_tower))
                        selected_tower = None  # Nullstill valg
                    else:
                        print("Ikke nok penger!")
                else:
                    print(f"Ugyldig tårntype: {selected_tower}")

    # Spillover-sjekk
    if president.health <= 0:
        game_over = True

    if not game_over:
        president.draw(screen)

        # Spawn zombier med tidsintervall
        current_time = pg.time.get_ticks()
        if current_time - last_spawn_time > spawn_interval:
            for _ in range(zombies_per_wave):
                zombie_count += 1
                strong = (zombie_count % 10 == 0)  # Hver 10. zombie er sterk
                zombies.append(Zombie(president, strong))

            zombies_per_wave += 1
            wave_count += 1
            last_spawn_time = current_time

        # Oppdater zombier og angrep nærmeste tårn eller president
        for zombie in zombies[:]:  # Kopi av listen for trygg fjerning
            zombie.find_nearest_target(towers, president)
            zombie.move()
            zombie.attack()
            zombie.draw(screen)

            if zombie.health <= 0:
                zombies.remove(zombie)
                money += 10  # Spilleren får penger per drept zombie

        # Oppdater og tegn tårnene
        # Oppdater tårnene og kulene deres
        for tower in towers:
            tower.attack(zombies)
            tower.update_bullets()  # Oppdater kulenes posisjon
            tower.draw(screen)


            # Fjerner tårn med 0 helse
            if tower.health <= 0:
                towers.remove(tower)

        # Tegn meny for kjøp av tårn
        pg.draw.rect(screen, GREEN, (10, 10, 100, 50))  # Basic Tower
        pg.draw.rect(screen, RED, (120, 10, 100, 50))  # Sniper Tower
        font = pg.font.Font(None, 24)
        screen.blit(font.render("Basic: 50", True, WHITE), (20, 25))
        screen.blit(font.render("Sniper: 100", True, WHITE), (130, 25))
        screen.blit(font.render(f"Penger: {money}", True, BLACK), (WIDTH - 150, 10))

    else:
        # Tegn "GAME OVER"
        font = pg.font.Font(None, 80)
        text = font.render("GAME OVER", True, RED)
        screen.blit(text, (WIDTH // 2 - 150, HEIGHT // 2 - 40))

    pg.display.update()
    clock.tick(FPS)

pg.quit()