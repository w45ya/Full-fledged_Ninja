from pygame import *
import players
ENEMY_WIDTH = 32
ENEMY_HEIGHT = 32
ENEMY_COLOR = "#2110FF"
import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class Enemy(sprite.Sprite):
    def __init__(self, x, y, end):
        self.x = x
        self.y = y
        sprite.Sprite.__init__(self)
        self.image = Surface((ENEMY_WIDTH, ENEMY_HEIGHT))
        self.path = [x, end]
        self.vel = 1.5
        asset_url = resource_path("sprites/enemy.png")
        self.image = image.load(asset_url).convert_alpha()



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
