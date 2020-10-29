import pygame
import pyganim
from pygame import *
from players import *
from blocks import *
from enemies import *

pygame.init()
WINDOW_SIZE = (1280, 720)
screen = display.set_mode(
    WINDOW_SIZE,
    DOUBLEBUF | HWSURFACE
)
pygame.display.set_caption("Two 1/2 ninjas")

NINJA = Ninja(120, 100)
STRIKER = Striker(80, 100)
TELEPORT_IN = Teleport_in(-500, -500)
TELEPORT_OUT = Teleport_out(-500, -500)
PLAYER = 1
SHOOT_LENGTH = 500


left = right = up = action = False
entities = sprite.Group()
monsters = sprite.Group()
bullets = sprite.Group()
platforms = []
entities.add(NINJA, STRIKER)
ENEMY = Enemy(928, 624, 1088)
entities.add(ENEMY)
monsters.add(ENEMY)
platforms.append(ENEMY)
ENEMY = Enemy(728, 624, 1088)
entities.add(ENEMY)
monsters.add(ENEMY)
platforms.append(ENEMY)
level = ["----------------------------------------",
        "-                                      -",
       "-                                      -",
       "-                                      -",
       "-            --                        -",
       "-                        -----         -",
       "--                           -    ------",
       "-                            -         -",
       "-                   ---      -         -",
       "-                            -         -",
       "-                            -         -",
       "-      ---            X      -         -",
       "-                            -         -",
       "-   -----------              -     -----",
       "-                            -     -   -",
       "-                -                 -   -",
       "-                   --             -   -",
       "-                                  -   -",
       "-                                  -   -",
       "-                                  -   -",
       "-          X                           -",
       "----------------------------------------"]
x = y = 0
for row in level:
    for col in row:
        if col == "-":
            block = Block(x,y)
            entities.add(block)
            platforms.append(block)
        if col == "X":
            block = DeathBlock(x,y)
            entities.add(block)
            platforms.append(block)
        x += PLATFORM_WIDTH
    y += PLATFORM_HEIGHT
    x = 0



clock = time.Clock()

running = True
while running:
    clock.tick(120)
    delta = clock.get_time() / 1000

    key_pressed = key.get_pressed()
    for e in event.get():
        if e.type == QUIT:
            running = False
        if e.type == KEYDOWN and e.key == K_a:
            left = True
        if e.type == KEYDOWN and e.key == K_d:
            right = True
        if e.type == KEYDOWN and e.key == K_SPACE:
            up = True
        if e.type == KEYUP and e.key == K_a:
            left = False
        if e.type == KEYUP and e.key == K_d:
            right = False
        if e.type == KEYUP and e.key == K_SPACE:
            up = False
        if e.type == KEYUP and e.key == K_f:
            action = False
        if key_pressed[K_1]:
            PLAYER = 1
        if key_pressed[K_2]:
            PLAYER = 2
        if key_pressed[K_g]:
            TELEPORT_OUT = Teleport_out(-500,-500)
            TELEPORT_IN = Teleport_in(-500,-500)
            TELEPORT_OUT.isExist = False
            TELEPORT_IN.isExist = False
            for i in platforms:
                if isinstance(i, Teleport_in):
                    platforms.remove(i)
                    entities.remove(i)
            for i in platforms:
                if isinstance(i, Teleport_out):
                    platforms.remove(i)
                    entities.remove(i)

        if key_pressed[K_f]:
            if PLAYER == 1:
                if TELEPORT_IN.isExist and (not TELEPORT_OUT.isExist):
                    if NINJA.flipped:
                        TELEPORT_OUT = Teleport_out(NINJA.rect.x-32,NINJA.rect.y)
                    else:
                        TELEPORT_OUT = Teleport_out(NINJA.rect.x+32,NINJA.rect.y)
                    TELEPORT_OUT.isExist = True
                    entities.add(TELEPORT_OUT)
                    platforms.append(TELEPORT_OUT)

                if not TELEPORT_IN.isExist:
                    if NINJA.flipped:
                        TELEPORT_IN = Teleport_in(NINJA.rect.x-32,NINJA.rect.y)
                    else:
                        TELEPORT_IN = Teleport_in(NINJA.rect.x+32,NINJA.rect.y)
                    TELEPORT_IN.isExist = True
                    entities.add(TELEPORT_IN)
                    platforms.append(TELEPORT_IN)
            if PLAYER == 2:
                if STRIKER.flipped:
                    SURIKEN = Bullet(STRIKER.rect.x - 12, STRIKER.rect.y + 10)
                    SURIKEN.flipped = True
                else:
                    SURIKEN = Bullet(STRIKER.rect.x + 34, STRIKER.rect.y + 10)
                entities.add(SURIKEN)
                bullets.add(SURIKEN)
                platforms.append(SURIKEN)


    for i in platforms:
        if isinstance(i, Bullet):
            if abs(i.rect.x - i.startX) > SHOOT_LENGTH:
                platforms.remove(i)
                entities.remove(i)
                bullets.remove(i)


    screen.fill((100, 200, 255))
    TELEPORT_IN.update()
    TELEPORT_OUT.update()
    bullets.update(platforms, entities, monsters)
    monsters.update()
    if PLAYER == 1:
        NINJA.update(left, right, up, platforms, entities, bullets, delta)
        STRIKER.update(0, 0, 0, platforms, delta)
    if PLAYER == 2:
        STRIKER.update(left, right, 0, platforms, delta)
        NINJA.update(0, 0, 0, platforms, entities, bullets, delta)
    entities.draw(screen)
    display.flip()
