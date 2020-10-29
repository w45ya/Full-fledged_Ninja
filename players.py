from pygame import *
import blocks
import enemies

MOVE_SPEED_NINJA = 10
MOVE_SPEED_STRIKER = 5
BULLET_SPEED = 15
WIDTH = 32
HEIGHT = 48
WIDTH_BULLET = 20
SHOOT_LENGTH = 100
JUMP_POWER_NINJA = 10
JUMP_POWER_STRIKER = 7
GRAVITY = 0.35
COLOR_NINJA = "#888888"
COLOR_STRIKER = "#FF0000"
COLOR_BULLET = "#424200"

class Ninja(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        self.onWall = False
        self.onWallOne = False
        self.startX = x
        self.startY = y
        self.flipped = False
        self.image = Surface((WIDTH,HEIGHT))
        self.image.fill(Color(COLOR_NINJA))
        self.rect = Rect(x, y, WIDTH, HEIGHT)

    def update(self, left, right, up, platforms, entities, bullets, delta):
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
            self.onWallOne = True
        if self.onGround:
            self.yvel += GRAVITY
            self.onWallOne = False
        self.onGround = False
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms, entities, bullets)
        self.rect.x += self.xvel
        self.collide(self.xvel, 0, platforms, entities, bullets)

    def collide(self, xvel, yvel, platforms, entities, bullets):
        for b in platforms:
            if sprite.collide_rect(self,b):
                if isinstance(b, blocks.Block):
                    if xvel > 0:
                        self.rect.right = b.rect.left
                        if not self.onWallOne:
                            self.onWall = True
                    if xvel < 0:
                        self.rect.left = b.rect.right
                        if not self.onWallOne:
                            self.onWall = True
                    if yvel > 0:
                        self.rect.bottom = b.rect.top
                        self.onGround = True
                        self.yvel = 0
                    if yvel < 0:
                        self.rect.top = b.rect.bottom
                        self.yvel = 0
                if isinstance(b, blocks.DeathBlock) or isinstance(b, enemies.Enemy):
                    self.death()
                if isinstance(b, Bullet):
                    self.death()
                    platforms.remove(b)
                    entities.remove(b)
                    bullets.remove(b)
                if isinstance(b, blocks.Teleport_in):
                    for i in platforms:
                        if isinstance(i, blocks.Teleport_out):
                            self.teleporting(i.startX,i.startY)
    def death(self):
        time.wait(500)
        self.teleporting(self.startX, self.startY)

    def teleporting(self, goX, goY):
        self.rect.x = goX
        self.rect.y = goY



class Striker(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        self.startX = x
        self.startY = y
        self.flipped = False
        self.image = Surface((WIDTH,HEIGHT))
        self.image.fill(Color(COLOR_STRIKER))
        self.rect = Rect(x, y, WIDTH, HEIGHT)

    def update(self, left, right, up, platforms, delta):
        if up:
            if self.onGround:
                self.yvel = -JUMP_POWER_STRIKER
        if left:
            self.xvel += -MOVE_SPEED_STRIKER * delta
            self.flipped = True
        if right:
            self.xvel += MOVE_SPEED_STRIKER * delta
            self.flipped = False
        if not(left or right):
            self.xvel = 0
        if not self.onGround:
            self.yvel += GRAVITY
        self.onGround = False
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)
        self.rect.x += self.xvel
        self.collide(self.xvel, 0, platforms)

    def collide(self, xvel, yvel, platforms):
        for b in platforms:
            if sprite.collide_rect(self,b):
                if isinstance(b, blocks.Block):
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
                if isinstance(b, blocks.DeathBlock) or isinstance(b, enemies.Enemy):
                    self.death()
                if isinstance(b, blocks.Teleport_in):
                    for i in platforms:
                        if isinstance(i, blocks.Teleport_out):
                            self.teleporting(i.startX,i.startY)
    def death(self):
        time.wait(500)
        self.teleporting(self.startX, self.startY)

    def teleporting(self, goX, goY):
        self.rect.x = goX
        self.rect.y = goY



class Bullet(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.xvel = BULLET_SPEED
        self.onGround = False
        self.startX = x
        self.startY = y
        self.image = Surface((WIDTH_BULLET,WIDTH_BULLET))
        self.image.fill(Color(COLOR_BULLET))
        self.rect = Rect(x, y, WIDTH_BULLET, WIDTH_BULLET)
        self.flipped = False
    def update(self, platforms, entities, monsters):
        if self.flipped:
            self.rect.x -= self.xvel
        else:
            self.rect.x += self.xvel
            self.collide(self.xvel, 0, platforms, entities, monsters)

    def collide(self, xvel, yvel, platforms, entities, monsters):
        for b in platforms:
            if sprite.collide_rect(self,b):
                if isinstance(b, enemies.Enemy):
                    platforms.remove(b)
                    entities.remove(b)
                    monsters.remove(b)
