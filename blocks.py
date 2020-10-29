from pygame import *
import pyganim

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#FF6262"
DEATH_BLOCK_COLOR = "#FF0000"
TELEPORT_COLOR = "#0055FF"
TELEPORT_COLOR2 = "#00FF55"
ANIMATION_DELAY = 200
ANIMATION_TP = [('sprites/tp_1.png'),
                ('sprites/tp_2.png'),
                ('sprites/tp_3.png'),
                ('sprites/tp_4.png')]

class Block(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(Color(PLATFORM_COLOR))
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)

class DeathBlock(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image = image.load("sprites/deathblock.png")
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)

class Teleport_in(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = image.load("sprites/tp_1.png").convert_alpha()
        self.rect = Rect(x+10, y+10, PLATFORM_WIDTH-10, PLATFORM_HEIGHT-10)
        self.startX = -500
        self.startY = -500
        self.isExist = False
        animation = []
        for anim in ANIMATION_TP:
            animation.append((anim, ANIMATION_DELAY))
        self.animation = pyganim.PygAnimation(animation)
        self.animation.play()

    def update(self):
        self.animation.blit(self.image, (0, 0))

class Teleport_out(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image = image.load("sprites/tp_1.png").convert_alpha()
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        self.startX = x
        self.startY = y
        self.isExist = False
        animation = []
        for anim in ANIMATION_TP:
            animation.append((anim, ANIMATION_DELAY))
        self.animation = pyganim.PygAnimation(animation)
        self.animation.play()
    def update(self):
        self.animation.blit(self.image, (0, 0))
