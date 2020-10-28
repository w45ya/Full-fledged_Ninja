from pygame import *
from blocks import *

MOVE_SPEED_NINJA = 10
MOVE_SPEED_STRIKER = 5
WIDTH = 32
HEIGHT = 48
JUMP_POWER_NINJA = 10
JUMP_POWER_STRIKER = 7
GRAVITY = 0.35
COLOR_NINJA =  "#888888"
COLOR_STRIKER = "#FF0000"

class Ninja(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        self.onWall = False
        self.startX = x
        self.startY = y
        self.flipped = False
        self.image = Surface((WIDTH,HEIGHT))
        self.image.fill(Color(COLOR_NINJA))
        self.rect = Rect(x, y, WIDTH, HEIGHT)

    def update(self, left, right, up, blocks, entities, delta):
        if up:
            if self.onGround or self.onWall:
                self.yvel = -JUMP_POWER_NINJA
            self.onWall = False
        if left and not self.onWall:
            self.xvel += -MOVE_SPEED_NINJA * delta
            self.flipped = True
        if right and not self.onWall:
            self.xvel += MOVE_SPEED_NINJA * delta
            self.flipped = False
        if not(left or right):
            self.xvel = 0
        if not self.onGround:
            self.yvel += GRAVITY
        if self.onWall:
            self.yvel = 0
        self.onGround = False
        self.rect.y += self.yvel
        self.collide(0, self.yvel, blocks)
        self.rect.x += self.xvel
        self.collide(self.xvel, 0, blocks)

    def collide(self, xvel, yvel, blocks):
        for b in blocks:
            if sprite.collide_rect(self,b):
                if xvel > 0:
                    self.rect.right = b.rect.left
                    if not self.onGround:
                        self.onWall = True
                if xvel < 0:
                    self.rect.left = b.rect.right
                    if not self.onGround:
                        self.onWall = True
                if yvel > 0:
                    self.rect.bottom = b.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = b.rect.bottom
                    self.yvel = 0

class Striker(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        self.startX = x
        self.startY = y
        self.image = Surface((WIDTH,HEIGHT))
        self.image.fill(Color(COLOR_STRIKER))
        self.rect = Rect(x, y, WIDTH, HEIGHT)

    def update(self, left, right, up, blocks, delta):
        if up:
            if self.onGround:
                self.yvel = -JUMP_POWER_STRIKER
        if left:
            self.xvel += -MOVE_SPEED_STRIKER * delta
        if right:
            self.xvel += MOVE_SPEED_STRIKER * delta
        if not(left or right):
            self.xvel = 0
        if not self.onGround:
            self.yvel += GRAVITY
        self.onGround = False
        self.rect.y += self.yvel
        self.collide(0, self.yvel, blocks)
        self.rect.x += self.xvel
        self.collide(self.xvel, 0, blocks)

    def collide(self, xvel, yvel, blocks):
        for b in blocks:
            if sprite.collide_rect(self,b):
                if xvel > 0:
                    self.rect.right = b.rect.left
                if xvel < 0:
                    self.rect.left = b.rect.right
                if yvel > 0:
                    self.rect.bottom = b.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = b.rect.bottom
                    self.yvel = 0
