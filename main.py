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
score = 0
selected_tower = None  # Spillerens valgte tårn
selected_tower_type = None  # Spillerens valgte tårn (fikset feilen)
dragging_tower = None  # Posisjonen til det visuelle tårnet under dragging

# Zombie-bølgevariabler
last_spawn_time = pg.time.get_ticks() 
spawn_interval = 2000  # 10 sekunder
zombies_per_wave = 1
wave_counter = 0
zombie_count = 0
wave_finished = False

running = True
game_over = False

def is_valid_placement(x, y, towers, president):
    """Sjekker om tårnet kan plasseres uten å overlappe andre tårn eller presidenten."""
    for tower in towers:
        distance = ((x - tower.x) ** 2 + (y - tower.y) ** 2) ** 0.5
        if distance < 30:  # Tårnene er 30x30 px, så 30 som minsteavstand
            return False
    
    tower_rect = pg.Rect(x - 15, y - 15, 30, 30)  
    if tower_rect.colliderect(president.rect):
        return False

    return True


wave_active = False

while running:
    screen.fill(WHITE)
    screen.blit(map_image, (0, 0))  # Tegner bakgrunnen

    font = pg.font.Font(None, 30)
    wave_text = font.render(f"Waves: {wave_counter}", True, BLACK)
    screen.blit(wave_text, (WIDTH - 150, 50))

    score_text = font.render(f"Score: {score}", True, BLACK)  # Tegn score
    screen.blit(score_text, (WIDTH - 150, 80))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        # Klikk for valg av tårn eller plassering
        elif event.type == pg.MOUSEBUTTONDOWN:
            x, y = pg.mouse.get_pos()

            if not wave_active and not zombies and button_x <= x <= button_x + button_width and button_y <= y <= button_y + button_height:
                wave_active = True  # Start bølgen
                last_spawn_time = pg.time.get_ticks()
                wave_finished = False


            for tower in towers:
                if tower.rect.collidepoint(event.pos):  # Sjekker om du klikker på et tårn
                    selected_tower = tower if selected_tower != tower else None  # Velg/fjern valg
                    break
            else:
                selected_tower = None  # Hvis du klikker utenfor et tårn, fjern valg


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
                if drop_y > 70 and is_valid_placement(drop_x, drop_y, towers, president):  # Sørger for at tårn ikke kan plasseres i butikken eller oppå hverandre
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

        if wave_active:

        # Spawn zombier med tidsintervall
            current_time = pg.time.get_ticks()
            if current_time - last_spawn_time > spawn_interval:
                for _ in range(zombies_per_wave):
                    zombie_count += 1
                    strong = (zombie_count % 10 == 0)  # Hver 10. zombie er sterk
                    zombies.append(Zombie(president, strong))

                zombies_per_wave += 1
                wave_active = False 
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
                score += 5 if not zombie.strong else 15  # 5 poeng for vanlig zombie, 15 for sterk zombie

        # Oppdater og tegn tårnene
        # Oppdater tårnene og kulene deres
        for tower in towers[:]:
            tower.attack(zombies)
            tower.update_bullets()  # Oppdater kulenes posisjon
            tower.draw(screen)
            if tower == selected_tower:
                tower.draw_range(screen)  # Viser rekkevidden til det valgte tårnet


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

    if not wave_active and not game_over and not zombies:
        if not wave_finished:
            wave_counter += 1
            score += 100  # 100 poeng for hver wave
            wave_finished = True
       
        button_x = WIDTH - 180
        button_y = HEIGHT - 60
        button_width = 160
        button_height = 40

        pg.draw.rect(screen, BLUE, (button_x, button_y, button_width, button_height), border_radius=10)
        font = pg.font.Font(None, 30)
        text = font.render("Start Wave", True, WHITE)
        screen.blit(text, (button_x + 30, button_y + 10))
       

    pg.display.update()
    clock.tick(FPS)

pg.quit()