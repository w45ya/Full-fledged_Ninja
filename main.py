import pygame
import pyganim
import pygame_menu
from pygame_menu import sound as snd_menu
from pygame import *
from players import *
from blocks import *
from enemies import *
import levels as l
import time as t
import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
pygame.init()
WIN_WIDTH = 1280
WIN_HEIGHT = 720
HALF_WIDTH = int(WIN_WIDTH / 2)
HALF_HEIGHT = int(WIN_HEIGHT / 2)
WINDOW_SIZE = (WIN_WIDTH, WIN_HEIGHT)
screen = display.set_mode(
    WINDOW_SIZE,
    DOUBLEBUF | HWSURFACE
)
pygame.display.set_caption("One full-fledged ninja")
PLOT = ['Издревле ниндзя зачищали загадочные земли от странных чёрных облачков.',
         'Однако, двух ниндзя отстранили от исполнения своего долга из-за',
         'имеющихся у них увечий. Один из них - герой войны, изучивший ниндзютсу',
         'телепортации, но лишившийся рук во время битвы с белыми колючками.',
         'Однако прыгучести он не растерял и даже научился цепляться ногами',
         'за стены. Второй - просто балбес лишившийся ног, потому что не слушал',
         'маму и играл на трамвайных путях. Но руки у него на месте,',
         'а значит и кунаи кидать способен.',
         '',
         'Смогут ли два калеки доказать свою небесполезность и, работая в команде,',
         'стать одним полноценным ниндзя?']
CONTROLS = ['A, D - передвижение влево/вправо',
         'Q - переключение между персонажами',
         'F - действие:',
         '      Безрукий - создать портал',
         '      Безногий - метнуть кунай',
         'E или G - убрать порталы',
         'Пробел - прыжок (только безрукий)',
         'ESC - выход в главное меню']
clock = time.Clock()
LEVEL_No = 0
lvl_svd = 0
entities = sprite.Group()
monsters = sprite.Group()
bullets = sprite.Group()
platforms = []

asset_url = resource_path('sound/60013_qubodup_whoosh.ogg')
WHOOSH_SOUND = mixer.Sound(asset_url)
asset_url = resource_path('sound/456373__felixyadomi__hop9.ogg')
JUMP_SOUND = mixer.Sound(asset_url)
asset_url = resource_path('sound/250128__tim-kahn__portal02.ogg')
PORTAL_SOUND = mixer.Sound(asset_url)
asset_url = resource_path('sound/76966__michel88__paind.ogg')
MONSTER_SOUND = mixer.Sound(asset_url)
asset_url = resource_path('sound/416838__alineaudio__grunt2-death-pain.ogg')
DEATH_SOUND = mixer.Sound(asset_url)
asset_url = resource_path('sound/461017__alanmcki__fast-whoosh.ogg')
SWITCH_SOUND = mixer.Sound(asset_url)
asset_url = resource_path('sound/107640__qat__door-open.ogg')
PORTAL_OPEN_SOUND = mixer.Sound(asset_url)
asset_url = resource_path('sound/514938__matrixxx__scifi-door.ogg')
PORTAL_CLOSE_SOUND = mixer.Sound(asset_url)
sounds = [JUMP_SOUND, PORTAL_SOUND, DEATH_SOUND,MONSTER_SOUND]

class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l+WIN_WIDTH / 2, -t+WIN_HEIGHT / 2

    l = min(-32, l)
    l = max(-(camera.width-WIN_WIDTH)+32, l)
    t = max(-(camera.height-WIN_HEIGHT)+32, t)
    t = min(-64, t)

    return Rect(l, t, w, h)


def game():
    global LEVEL_No, platforms, lvl_svd
    level = l.levels[LEVEL_No]
    for i in entities:
        entities.remove(i)
    for i in monsters:
        monsters.remove(i)
    for i in bullets:
        bullets.remove(i)
    platforms = []
    NINJA = Ninja(l.ninjas[LEVEL_No][0], l.ninjas[LEVEL_No][1])
    STRIKER = Striker(l.strikers[LEVEL_No][0], l.strikers[LEVEL_No][1])
    index = 1
    while (index < l.monsters[LEVEL_No][0]*3):
        EnX = l.monsters[LEVEL_No][index]
        EnY = l.monsters[LEVEL_No][index+1]
        EnL = l.monsters[LEVEL_No][index+2]
        ENEMY = Enemy(EnX, EnY, EnL)
        entities.add(ENEMY)
        monsters.add(ENEMY)
        platforms.append(ENEMY)
        index += 3

    TELEPORT_IN = Teleport_in(-500, -500)
    TELEPORT_OUT = Teleport_out(-500, -500)
    PLAYER = 1
    SHOOT_LENGTH = 500

    left = right = up = action = False

    entities.add(NINJA, STRIKER)

    x = y = 0
    for row in level:
        for col in row:
            if col == "-":
                block = Block(x,y,"default")
                entities.add(block)
                platforms.append(block)
            if col == "X":
                block = DeathBlock(x,y)
                entities.add(block)
                platforms.append(block)
            if col == "G":
                block = Block(x,y,"grass")
                entities.add(block)
                platforms.append(block)
            if col == "{":
                block = Block(x,y,"grass_left")
                entities.add(block)
                platforms.append(block)
            if col == "}":
                block = Block(x,y,"grass_right")
                entities.add(block)
                platforms.append(block)
            if col == "E":
                block = Block(x,y,"earth")
                entities.add(block)
                platforms.append(block)
            if col == "(":
                block = Block(x,y,"earth_left")
                entities.add(block)
                platforms.append(block)
            if col == ")":
                block = Block(x,y,"earth_right")
                entities.add(block)
                platforms.append(block)
            if col == "D":
                block = Block(x,y,"earth_down")
                entities.add(block)
                platforms.append(block)
            if col == "<":
                block = Block(x,y,"earth_down_left")
                entities.add(block)
                platforms.append(block)
            if col == ">":
                block = Block(x,y,"earth_down_right")
                entities.add(block)
                platforms.append(block)
            if col == "P":
                block = Block(x,y,"platform")
                entities.add(block)
                platforms.append(block)
            if col == "[":
                block = Block(x,y,"platform_left")
                entities.add(block)
                platforms.append(block)
            if col == "]":
                block = Block(x,y,"platform_right")
                entities.add(block)
                platforms.append(block)
            x += PLATFORM_WIDTH
        y += PLATFORM_HEIGHT
        x = 0
        total_level_width  = len(level[0])*PLATFORM_WIDTH
        total_level_height = len(level)*PLATFORM_HEIGHT

        camera = Camera(camera_configure, total_level_width, total_level_height)

    running = True
    while running:
        clock.tick(120)
        delta = clock.get_time() / 1000

        key_pressed = key.get_pressed()
        for e in event.get():
            if e.type == QUIT:
                pygame.quit()
                sys.exit()
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

            if key_pressed[K_ESCAPE]:
                running = False
                lvl_svd = LEVEL_No
                LEVEL_No = 99
            if key_pressed[K_1]:
                if PLAYER == 2:
                    SWITCH_SOUND.play()
                    PLAYER = 1
            if key_pressed[K_2]:
                if PLAYER == 1:
                    SWITCH_SOUND.play()
                    PLAYER = 2
            if key_pressed[K_q]:
                SWITCH_SOUND.play()
                if PLAYER == 1:
                    PLAYER = 2
                else:
                    PLAYER = 1
            if key_pressed[K_e] or key_pressed[K_g]:
                if TELEPORT_IN.isExist:
                    PORTAL_CLOSE_SOUND.play()
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
                        PORTAL_OPEN_SOUND.play()
                        if NINJA.flipped:
                            TELEPORT_OUT = Teleport_out(NINJA.rect.x-32,NINJA.rect.y)
                        else:
                            TELEPORT_OUT = Teleport_out(NINJA.rect.x+32,NINJA.rect.y)
                        TELEPORT_OUT.isExist = True
                        entities.add(TELEPORT_OUT)
                        platforms.append(TELEPORT_OUT)

                    if not TELEPORT_IN.isExist:
                        PORTAL_OPEN_SOUND.play()
                        if NINJA.flipped:
                            TELEPORT_IN = Teleport_in(NINJA.rect.x-32,NINJA.rect.y)
                        else:
                            TELEPORT_IN = Teleport_in(NINJA.rect.x+32,NINJA.rect.y)
                        TELEPORT_IN.isExist = True
                        entities.add(TELEPORT_IN)
                        platforms.append(TELEPORT_IN)
                if PLAYER == 2:
                    WHOOSH_SOUND.play()
                    if STRIKER.flipped:
                        SURIKEN = Bullet(STRIKER.rect.x - 12, STRIKER.rect.y + 10, True)
                    else:
                        SURIKEN = Bullet(STRIKER.rect.x + 34, STRIKER.rect.y + 10, False)
                    entities.add(SURIKEN)
                    bullets.add(SURIKEN)
                    platforms.append(SURIKEN)

        for i in platforms:
            if isinstance(i, Bullet):
                if abs(i.rect.x - i.startX) > SHOOT_LENGTH:
                    platforms.remove(i)
                    entities.remove(i)
                    bullets.remove(i)
                for j in platforms:
                        if isinstance(j, blocks.DeathBlock) or isinstance(j, blocks.Block):
                            try:
                                if sprite.collide_rect(i,j):
                                    platforms.remove(i)
                                    entities.remove(i)
                                    monsters.remove(i)
                                    i.rect.x = -500
                                    i.rect.y = -500
                            except:
                                print("Almost crashed...")

        screen.fill((100, 200, 255))
        TELEPORT_IN.update()
        TELEPORT_OUT.update()
        bullets.update(platforms, entities, monsters, sounds)
        monsters.update()
        if PLAYER == 1:
            NINJA.update(left, right, up, platforms, entities, bullets, delta, sounds)
            STRIKER.update(0, 0, 0, platforms, delta, sounds)
            camera.update(NINJA)
        if PLAYER == 2:
            STRIKER.update(left, right, 0, platforms, delta, sounds)
            NINJA.update(0, 0, 0, platforms, entities, bullets, delta, sounds)
            camera.update(STRIKER)
        for e in entities:
            screen.blit(e.image, camera.apply(e))
        display.flip()

        gameWin = True
        for i in platforms:
            if isinstance(i, Enemy):
                gameWin = False

        if gameWin:
            time.wait(500)
            running = False


def change_level(value, lvl):
    global LEVEL_No
    selected, index = value
    LEVEL_No = lvl


asset_font = resource_path('font/OpenSans.ttf')

plot_theme = pygame_menu.themes.THEME_DARK.copy()
plot_theme.title_font = asset_font
plot_theme.widget_font = asset_font
plot_theme.widget_margin = (0, 0)
plot_theme.widget_offset = (0, 0.05)

plot_menu = pygame_menu.Menu(
    height=WINDOW_SIZE[1] * 0.7,
    onclose=pygame_menu.events.DISABLE_CLOSE,
    theme=plot_theme,
    title='Сюжет',
    width=WINDOW_SIZE[0] * 0.6
)
for m in PLOT:
    plot_menu.add_label(m, align=pygame_menu.locals.ALIGN_LEFT, font_size=20)
plot_menu.add_label('')
plot_menu.add_button('Назад', pygame_menu.events.BACK)

controls_menu = pygame_menu.Menu(
    height=WINDOW_SIZE[1] * 0.6,
    onclose=pygame_menu.events.DISABLE_CLOSE,
    theme=plot_theme,
    title='Управление',
    width=WINDOW_SIZE[0] * 0.315
)
for m in CONTROLS:
    controls_menu.add_label(m, align=pygame_menu.locals.ALIGN_LEFT, font_size=20)
controls_menu.add_label('')
controls_menu.add_button('Назад', pygame_menu.events.BACK)

def setLevelGame():
    global LEVEL_No
    if LEVEL_No == 100:
        LEVEL_No = lvl_svd
    while (LEVEL_No < len(l.levels)):
        game()
        LEVEL_No += 1

engine = snd_menu.Sound()
asset_url = resource_path('sound/539606__fivebrosstopmosyt__ui-alert-2.ogg')
engine.set_sound(snd_menu.SOUND_TYPE_CLICK_MOUSE, asset_url)


menu = pygame_menu.Menu(600,500,'Полноценный ниндзя',theme=plot_theme)
menu.add_button('Сюжет', plot_menu)
menu.add_button('Управление', controls_menu)
menu.add_button('Играть', setLevelGame)
menu.add_selector('Уровень:', [('1', 0), ('2', 1), ('3', 2)], onchange=change_level)
menu.add_button('Выход', pygame_menu.events.EXIT)
menu.set_sound(engine, recursive=True)
menu.mainloop(screen)
