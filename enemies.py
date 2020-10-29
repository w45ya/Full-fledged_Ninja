from pygame import *
import players
ENEMY_WIDTH = 32
ENEMY_HEIGHT = 32
ENEMY_COLOR = "#2110FF"
ANIMATION_DELAY = 500
ANIMATION_ENEMY = [('sprites/enemy1.png'),
                ('sprites/enemy2.png')]
class Enemy(sprite.Sprite):
    def __init__(self, x, y, end):
        self.x = x
        self.y = y
        sprite.Sprite.__init__(self)
        self.image = Surface((ENEMY_WIDTH, ENEMY_HEIGHT))
        self.path = [x, end]
        self.vel = 1.5
        self.image = image.load("sprites/enemy.png").convert_alpha()



    def update(self):
        self.rect = Rect(self.x, self.y, ENEMY_WIDTH, ENEMY_HEIGHT)
        if self.vel > 0:
            if self.x < self.path[1] + self.vel:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.x += self.vel
        else:

            if self.x > self.path[0] - self.vel:
                self.x += self.vel

            else:
                self.vel = self.vel * -1
                self.x += self.vel
        self.image = transform.flip(self.image,1,0)
