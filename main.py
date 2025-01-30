#hovedfilen
import pygame as pg
from constants import *
from images import *

pg.init()
clock = pg.time.Clock()
screen = pg.display.set_mode(SIZE)


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
