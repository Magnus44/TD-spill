#hovedfilen
from constants import *
import pygame as pg
pg.init()
screen = pg.display.set_mode(SIZE)
# MERK: Må gjøre dette før vi begynner med bilder transform osv 

from images import *

clock = pg.time.Clock()


running = True
while running:

   
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    clock.tick(FPS)
    screen.fill(WHITE)

    
    screen.blit(map_image, (0, 0))

    
    pg.display.update()


pg.quit()
