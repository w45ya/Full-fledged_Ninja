from pygame import *
import pyganim
import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#FF6262"
GRASS_COLOR = "#00FF42"
DEATH_BLOCK_COLOR = "#FF0000"
TELEPORT_COLOR = "#0055FF"
TELEPORT_COLOR2 = "#00FF55"
ANIMATION_DELAY = 200
asset_url1 = resource_path('sprites/tp_1.png')
asset_url2 = resource_path('sprites/tp_2.png')
asset_url3 = resource_path('sprites/tp_3.png')
asset_url4 = resource_path('sprites/tp_4.png')
ANIMATION_TP = [(asset_url1),
                (asset_url2),
                (asset_url3),
                (asset_url4)]
asset_url1 = resource_path('sprites/tp1_1.png')
asset_url2 = resource_path('sprites/tp1_2.png')
asset_url3 = resource_path('sprites/tp1_3.png')
asset_url4 = resource_path('sprites/tp1_4.png')
ANIMATION_TP1 = [(asset_url1),
                (asset_url2),
                (asset_url3),
                (asset_url4)]

class Block(sprite.Sprite):
    def __init__(self, x, y, type):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        if type == "default":
            asset_url = resource_path("sprites/platforms/block.png")
            self.image = image.load(asset_url).convert_alpha()
        if type == "grass":
            asset_url = resource_path("sprites/platforms/grass.png")
            self.image = image.load(asset_url ).convert_alpha()
        if type == "grass_left":
            asset_url = resource_path("sprites/platforms/grass_left.png")
            self.image = image.load(asset_url ).convert_alpha()
        if type == "grass_right":
            asset_url = resource_path("sprites/platforms/grass_right.png")
            self.image = image.load(asset_url ).convert_alpha()
        if type == "earth":
            asset_url = resource_path("sprites/platforms/earth.png")
            self.image = image.load(asset_url ).convert_alpha()
        if type == "earth_left":
            asset_url = resource_path("sprites/platforms/earth_left.png")
            self.image = image.load(asset_url ).convert_alpha()
        if type == "earth_right":
            asset_url = resource_path("sprites/platforms/earth_right.png")
            self.image = image.load(asset_url ).convert_alpha()
        if type == "earth_down":
            asset_url = resource_path("sprites/platforms/earth_down.png")
            self.image = image.load(asset_url ).convert_alpha()
        if type == "earth_down_left":
            asset_url = resource_path("sprites/platforms/earth_down_left.png")
            self.image = image.load(asset_url ).convert_alpha()
        if type == "earth_down_right":
            asset_url = resource_path("sprites/platforms/earth_down_right.png")
            self.image = image.load(asset_url ).convert_alpha()
        if type == "platform":
            asset_url = resource_path("sprites/platforms/platform.png")
            self.image = image.load(asset_url ).convert_alpha()
        if type == "platform_left":
            asset_url = resource_path("sprites/platforms/platform_left.png")
            self.image = image.load(asset_url ).convert_alpha()
        if type == "platform_right":
            asset_url = resource_path("sprites/platforms/platform_right.png")
            self.image = image.load(asset_url ).convert_alpha()

class DeathBlock(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        asset_url = resource_path("sprites/deathblock.png")
        self.image = image.load(asset_url)
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)

class Teleport_in(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        asset_url = resource_path("sprites/tp_1.png")
        self.image = image.load(asset_url).convert_alpha()
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
        asset_url = resource_path("sprites/tp_1.png")
        self.image = image.load(asset_url).convert_alpha()
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        self.startX = x
        self.startY = y
        self.isExist = False
        animation = []
        for anim in ANIMATION_TP1:
            animation.append((anim, ANIMATION_DELAY))
        self.animation = pyganim.PygAnimation(animation)
        self.animation.play()
    def update(self):
        self.animation.blit(self.image, (0, 0))
