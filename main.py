from pygame import *
from players import *
from blocks import *

WINDOW_SIZE = (1280, 720)
NINJA = Ninja(120,100)
STRIKER = Striker(80,100)
PLAYER = 1

left = right = up = action = False
entities = sprite.Group()
blocks = []
entities.add(NINJA, STRIKER)
level = ["----------------------------------------",
        "-                                      -",
       "-                                      -",
       "-                                      -",
       "-            --                        -",
       "-                                      -",
       "--                                     -",
       "-                                      -",
       "-                   ---                -",
       "-                                      -",
       "-                                      -",
       "-      ---                             -",
       "-                                      -",
       "-   -----------                        -",
       "-                                      -",
       "-                -                 -   -",
       "-                   --             -   -",
       "-                                  -   -",
       "-                                  -   -",
       "-                                  -   -",
       "-                                      -",
       "----------------------------------------"]
x = y = 0
for row in level:
    for col in row:
        if col == "-":
            block = Block(x,y)
            entities.add(block)
            blocks.append(block)
        x += PLATFORM_WIDTH
    y += PLATFORM_HEIGHT
    x = 0

init()
screen = display.set_mode(
    WINDOW_SIZE,
    DOUBLEBUF | HWSURFACE
)

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
        if key_pressed[K_f]:
            if PLAYER == 1:
                if NINJA.flipped:
                    block = Block(NINJA.rect.x-32,NINJA.rect.y)
                else:
                    block = Block(NINJA.rect.x+32,NINJA.rect.y)
                entities.add(block)
                blocks.append(block)
    screen.fill((100, 200, 255))
    print(NINJA.onGround)

    if PLAYER == 1:
        NINJA.update(left, right, up, blocks, entities, delta)
        STRIKER.update(0, 0, 0, blocks, delta)
    if PLAYER == 2:
        STRIKER.update(left, right, 0, blocks, delta)
        NINJA.update(0, 0, 0, blocks, entities, delta)
    entities.draw(screen)
    display.flip()
