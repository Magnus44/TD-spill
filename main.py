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
zombies = [Zombie(president)]
towers = []

# Økonomi og kjøp
money = 100  # Startpenger
selected_tower = None  # Spillerens valgte tårn
selected_tower_type = None  # Spillerens valgte tårn (fikset feilen)
dragging_tower = None  # Posisjonen til det visuelle tårnet under dragging

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
            if 10 <= x <= 110 and 10 <= y <= 60 and money >= Tower.COSTS["basic"]:
                selected_tower_type = "basic"
                dragging_tower = (x, y)
            elif 120 <= x <= 220 and 10 <= y <= 60 and money >= Tower.COSTS["sniper"]:
                selected_tower_type = "sniper"
                dragging_tower = (x, y)

        # Når spilleren drar tårnet
        elif event.type == pg.MOUSEMOTION:
            if selected_tower_type:
                dragging_tower = event.pos  # Oppdater posisjon på dra-tårnet

        # Når spilleren slipper tårnet
        elif event.type == pg.MOUSEBUTTONUP:
            if selected_tower_type and dragging_tower:
                drop_x, drop_y = event.pos
                if drop_y > 70:  # Sørger for at tårn ikke kan plasseres i butikken
                    cost = Tower.COSTS[selected_tower_type]
                    money -= cost
                    towers.append(Tower(drop_x, drop_y, selected_tower_type))

                # Nullstill dra-animasjonen
                selected_tower_type = None
                dragging_tower = None

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
        for tower in towers[:]:
            tower.attack(zombies)
            tower.update_bullets()  # Oppdater kulenes posisjon
            tower.draw(screen)

            if tower.health <= 0:  # Fjern døde tårn
                towers.remove(tower)

        # Tegn meny for kjøp av tårn
        pg.draw.rect(screen, GREEN, (10, 10, 100, 50))  # Basic Tower
        pg.draw.rect(screen, RED, (120, 10, 100, 50))  # Sniper Tower
        font = pg.font.Font(None, 24)
        screen.blit(font.render("Basic: 50", True, WHITE), (20, 25))
        screen.blit(font.render("Sniper: 100", True, WHITE), (130, 25))
        screen.blit(font.render(f"Penger: {money}", True, BLACK), (WIDTH - 150, 10))

        # Tegn tårn-ikonet som dras av spilleren
        if dragging_tower:
            pg.draw.rect(screen, GREEN if selected_tower_type == "basic" else RED, 
                         (dragging_tower[0] - 15, dragging_tower[1] - 15, 30, 30), border_radius=10)

    else:
        # Tegn "GAME OVER"
        font = pg.font.Font(None, 80)
        text = font.render("GAME OVER", True, RED)
        screen.blit(text, (WIDTH // 2 - 150, HEIGHT // 2 - 40))

    pg.display.update()
    clock.tick(FPS)

pg.quit()