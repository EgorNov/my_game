import os
import sys

import pygame

pygame.init()

pygame.key.set_repeat(200, 10)
fps = 60

width = 800
height = 600
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

f = pygame.sprite.Group()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    # image = image.convert_alpha()

    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


def startScreen():
    # здесь можно вывести красивую картинку
    # ...

    introText = ["ЗАСТАВКА", "",
                 "Правила игры",
                 "Отстреливайся от врагов",
                 "Не умирай", "Убей босса и перейди на новый этаж"]

    screen.fill(0)
    spr = pygame.sprite.Sprite()
    spr.image = pygame.transform.scale2x(load_image("fone_1.png"))
    spr.rect = spr.image.get_rect()
    spr.rect.x, spr.rect.x = 0, 0
    f.add(spr)

    font = pygame.font.Font(None, 27)
    textCoord = 50
    f.draw(screen)
    for i in range(len(introText)):
        stringRendered = pygame.transform.scale2x(font.render(introText[i], 1, pygame.Color('black')))
        introRect = stringRendered.get_rect()
        textCoord += 10
        introRect.top = textCoord
        introRect.x = 30
        textCoord += introRect.height
        screen.blit(stringRendered, introRect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == 13 or event.key == pygame.K_SPACE:
                    return  # начинаем игру
        pygame.display.flip()
        clock.tick(fps)


def end_screen(sprite):
    # здесь можно вывести красивую картинку
    # ...

    introText = ["Игра Окончена", "",
                 "Вас Убило Это:"]

    screen.fill(0)
    spr = pygame.sprite.Sprite()
    spr.image = pygame.transform.scale2x(load_image("fone_1.png"))
    spr.rect = spr.image.get_rect()
    sprite.image = pygame.transform.scale2x(sprite.image)
    sprite.rect.x = 259 * 2
    sprite.rect.y = 99
    f.add(spr)

    font = pygame.font.Font(None, 27)
    textCoord = 50
    f.draw(screen)
    for i in range(len(introText)):
        stringRendered = pygame.transform.scale2x(font.render(introText[i], 1, pygame.Color('black')))
        introRect = stringRendered.get_rect()
        textCoord += 10
        introRect.top = textCoord
        introRect.x = 30
        textCoord += introRect.height
        screen.blit(stringRendered, introRect)
    e = pygame.sprite.Group()
    e.add(sprite)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == 13 or event.key == pygame.K_SPACE:
                    return  # начинаем игру
        pygame.display.flip()
        e.draw(screen)
        clock.tick(fps)


def terminate():
    pygame.quit()
    sys.exit()


class Room:
    def __init__(self, map):
        self.level = map
        self.tiles = []
        self.other = []
        self.enemies = []
        self.generate_level()

    def generate_level(self):
        global player
        global boss
        level = self.level
        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] == '.':
                    self.tiles.append(Tile('empty', x, y))
                elif level[y][x] == '-':
                    self.tiles.append(Tile('-', x, y, wall=True))
                elif level[y][x] == '_':
                    self.tiles.append(Tile('_', x, y, wall=True))
                elif level[y][x] == 'r':
                    self.tiles.append(Tile('r', x, y, wall=True))
                elif level[y][x] == 'l':
                    self.tiles.append(Tile('l', x, y, wall=True))
                elif level[y][x] == 'L':
                    self.tiles.append(Tile('L', x, y, wall=True))
                elif level[y][x] == '1':
                    self.tiles.append(Tile('1', x, y, wall=True))
                elif level[y][x] == '2':
                    self.tiles.append(Tile('2', x, y, wall=True))
                elif level[y][x] == '3':
                    self.tiles.append(Tile('3', x, y, wall=True))
                elif level[y][x] == '4':
                    self.tiles.append(Tile('4', x, y, wall=True))
                elif level[y][x] == 'o':
                    self.tiles.append(Door(x, y))
                elif level[y][x] == '@':
                    self.tiles.append(Tile('empty', x, y))
                    player = Player(3, 4, x, y, )
                elif level[y][x] == '*':
                    self.tiles.append(Tile('empty', x, y))
                    self.enemies.append(Fly(2, 1, x, y))
                elif level[y][x] == 'B':
                    self.tiles.append(Tile('empty', x, y))
                    boss = Boss(2, 1, x, y)
                    self.enemies.append(boss)

                elif level[y][x] == 't':
                    self.tiles.append(Tile('empty', x, y))
                    self.enemies.append(Turret(x, y))
                elif level[y][x] == '!':
                    self.tiles.append(Tile('empty', x, y))
                    self.other.append(Diamond(x, y))


def load_level(filename):
    filename = "data/" + filename
    mapFile = open(filename, 'r')
    level_map = mapFile.readlines()
    mapFile.close()

    # убираем переводы строк
    # и подсчитываем максимальную длину
    maxWidth = -1
    for i in range(len(level_map)):
        level_map[i] = level_map[i].rstrip('\r\n')
        if len(level_map[i]) > maxWidth:
            maxWidth = len(level_map[i])

    # допролняем каждую строку пустыми клетками ('.')
    # for i in range(len(level_map)):
    #     if len(level_map[i]) < maxWidth:
    #         level_map[i] += '.' * (maxWidth - len(level_map[i]))
    return level_map


close_door = load_image('close_door.png', colorkey=(255, 255, 255))
open_door = load_image('open_door.png', colorkey=(255, 255, 255))
pause_image = load_image('fone_2.png')
tile_images = {'l': load_image('l_wall.png', colorkey=(255, 255, 255)),
               'r': load_image('r_wall.png', colorkey=(255, 255, 255)),
               '_': load_image('_.png', colorkey=(255, 255, 255)),
               '-': load_image('-.png', colorkey=(255, 255, 255)), '1': load_image('1.png', colorkey=(255, 255, 255)),
               '2': load_image('2.png', colorkey=(255, 255, 255)), '3': load_image('3.png', colorkey=(255, 255, 255)),
               '4': load_image('4.png', colorkey=(255, 255, 255)),
               'empty': load_image('floor.png', colorkey=(255, 255, 255))}
player_image = load_image('player.png', colorkey=(255, 255, 255))
fly_image = pygame.transform.scale2x(load_image('fly.png', colorkey=-1))
boss_image = load_image('boss.png', colorkey=-1)
hurt_image = load_image('hurt.png', colorkey=-1)
laser_image = load_image('laser.png', colorkey=-1)
bullet_image = load_image('bullet.png', colorkey=-1)
fireball_image = load_image('fireball.png', colorkey=pygame.Color('white'))
bullet_image_f = load_image('bullet_f.png', colorkey=-1)
bullet_image_l = pygame.transform.scale2x(load_image('bullet.png', colorkey=-1))
bullet_image_l_f = pygame.transform.scale2x(load_image('bullet_f.png', colorkey=-1))
diamond_image = load_image('diamond.png', colorkey=(255, 255, 255))
heart_image = load_image('heart.png', colorkey=(255, 255, 255))
turret_image = load_image('turret.png', colorkey=(255, 255, 255))

player_high = player_image.get_rect()[2]
player_width = player_image.get_rect()[3]

tile_height = tile_images['empty'].get_rect()[2]
tile_width = tile_images['empty'].get_rect()[3]


class Heart(pygame.sprite.Sprite):
    def __init__(self, posx):
        super().__init__(heart_group)
        self.image = heart_image
        self.rect = self.image.get_rect()
        self.rect.x = posx * 50


class Door(pygame.sprite.Sprite):
    def __init__(self, posx, posy):
        super().__init__(door_group, all_sprites)
        self.image = close_door
        self.type = 'wall'
        self.hearts = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = posx * tile_width
        self.rect.y = posy * tile_height

    def update(self):
        if dim:
            self.type = 'empty'
            self.image = open_door
        else:
            self.type = 'wall'
            self.image = close_door


class Bullet(pygame.sprite.Sprite):
    def __init__(self, speed, dir, posx, posy, range, type, scale=False, boss=False):
        if type == 'enemy':
            super().__init__(bullet_group, enemy_group, all_sprites)
        else:
            super().__init__(bullet_group, all_sprites)
        self.type = type
        if scale:
            self.image = bullet_image_l
            self.image_f = bullet_image_l_f
        else:
            if not boss:
                self.image = bullet_image
                self.image_f = bullet_image_f
            else:
                self.image = bullet_image_l
                self.image_f = fireball_image
        self.mask = pygame.mask.from_surface(self.image)
        self.frames = []
        self.cut_sheet(self.image_f, 4, 1)
        self.rect = self.image.get_rect()
        self.rect.x = posx

        self.rect.y = posy

        self.cur_frame = 0
        self.speed = speed
        self.hearts = 0
        self.dir = dir
        self.range = range
        self.cur_range = 0

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):

            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):

        owner = self.type
        if self.cur_range >= self.range - len(self.frames):
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
        if self.cur_range >= self.range:
            all_sprites.remove(self)
            bullet_group.remove(self)
            if self.type == 'enemy':
                enemy_group.remove(self)
        for sprite in all_sprites:
            if pygame.sprite.collide_mask(self, sprite):
                if sprite.type != owner and sprite.type != 'empty' and sprite.type != 'dim':
                    if sprite.type == 'player':
                        pass
                    else:
                        sprite.hearts -= 1
                    bullet_group.remove(self)
                    all_sprites.remove(self)
                    if self.type == 'enemy':
                        enemy_group.remove(self)
        if self.dir == 'up':
            self.rect.y -= self.speed
            self.cur_range += self.speed
        if self.dir == 'down':
            self.rect.y += self.speed
            self.cur_range += self.speed
        if self.dir == 'left':
            self.rect.x -= self.speed
            self.cur_range += self.speed
        if self.dir == 'right':
            self.rect.x += self.speed
            self.cur_range += self.speed


class Tile(pygame.sprite.Sprite):
    def __init__(self, type, posx, posy, wall=False):
        super().__init__(tiles_group, all_sprites)
        self.hearts = 0
        self.image = tile_images[type]
        if wall:
            type = 'wall'
        self.width = self.image.get_rect()[2]
        self.height = self.image.get_rect()[3]
        self.type = type
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(tile_width * posx, tile_height * posy)


class Boss(pygame.sprite.Sprite):
    def __init__(self, columns, rows, posx, posy):
        super().__init__(enemy_group, all_sprites)
        self.frames = []
        self.type = 'enemy'
        self.hearts = 40
        self.dir = 3
        self.cut_sheet(boss_image, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(tile_width * posx + 15, tile_height * posy + 5)
        self.pause = False
        self.fire_rate = 0

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        for sprite in all_sprites:
            if sprite.type == 'wall':
                if pygame.sprite.collide_mask(self, sprite):
                    self.dir = -1 * self.dir

        if self.pause:
            self.fire_rate += 1
        if self.fire_rate == 40:
            self.pause = False
        if self.hearts <= 0:
            enemy_group.remove(self)
            all_sprites.remove(self)
        self.rect.x += self.dir
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        self.fire()

    def fire(self):
        if not self.pause:
            Bullet(3, 'down', self.rect.x + 100, self.rect.y + 84, 1000, self.type, scale=False, boss=True)
            self.pause = True
            self.fire_rate = 0


class Turret(pygame.sprite.Sprite):
    global player

    def __init__(self, posx, posy ):
        super().__init__(enemy_group, all_sprites)
        self.stand = True
        self.hearts = 8
        self.type = 'enemy'
        self.pause = False
        self.fire_rate = 0
        self.image = turret_image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(tile_width * posx + 15, tile_height * posy + 5)

    def update(self):
        if self.pause:
            self.fire_rate += 1
        if self.fire_rate == 60:
            self.pause = False
        if self.hearts <= 0:
            enemy_group.remove(self)
            all_sprites.remove(self)
        if player.rect.x < self.rect.x and self.rect.y <= player.rect.y <= self.rect.y + self.rect[3]:
            self.fire()

    def fire(self):
        if not self.pause:
            Bullet(3, 'left', self.rect.x, self.rect.y, 1000, self.type, scale=True)
            self.pause = True
            self.fire_rate = 0


class Player(pygame.sprite.Sprite):
    def __init__(self, columns, rows, posx, posy):
        super().__init__(player_group, all_sprites)
        self.frames = {}
        self.cut_sheet(player_image, columns, rows)
        self.cur_frame = 0
        self.stand = True
        self.type = 'player'
        self.hearts = 6
        self.last_direct = None
        self.cur_direct = None
        self.image = self.frames['down'][6]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(tile_width * posx + 15, tile_height * posy + 5)
        self.speed = 2
        self.bullet_speed = 3
        self.fire_rate = 20
        self.range = 200

    def cut_sheet(self, sheet, columns, rows):
        directions = ['down', 'left', 'right', 'up']
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            self.frames[directions[j]] = []
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames[directions[j]].append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))
                self.frames[directions[j]].append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))
                self.frames[directions[j]].append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))
                self.frames[directions[j]].append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))
                self.frames[directions[j]].append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        if not self.stand:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames[self.cur_direct])
            self.image = self.frames[self.cur_direct][self.cur_frame]
        else:
            self.image = self.frames['down'][6]

    def hurt(self):
        self.image = hurt_image

    def fire(self, dir):
        Bullet(self.bullet_speed, dir, player.rect.x, player.rect.y, self.range, self.type)


class Diamond(pygame.sprite.Sprite):
    global player

    def __init__(self, x, y):
        super().__init__(colect_group, all_sprites)
        self.image = diamond_image
        self.type = 'dim'
        self.hearts = 0
        self.rect = self.image.get_rect()
        self.rect.x = x * tile_width
        self.rect.y = y * tile_width
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        global dim
        if pygame.sprite.collide_mask(self, player):
            colect_group.remove(self)
            dim = True


class Fly(pygame.sprite.Sprite):
    global player

    def __init__(self, columns, rows, posx, posy):
        super().__init__(enemy_group, all_sprites)
        self.frames = []
        self.cut_sheet(fly_image, columns, rows)
        self.cur_frame = 0
        self.type = 'enemy'
        self.stand = True
        self.hearts = 3
        self.image = self.frames[self.cur_frame]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(tile_width * posx + 15, tile_height * posy + 5)
        self.speed = 1

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        if self.hearts <= 0:
            enemy_group.remove(self)
            all_sprites.remove(self)
        if self.cur_frame % 2 == 0:
            return
        if player.rect.x > self.rect.x:
            self.rect.x += 1
        if player.rect.x < self.rect.x:
            self.rect.x -= 1
        if player.rect.y > self.rect.y:
            self.rect.y += 1
        if player.rect.y < self.rect.y:
            self.rect.y -= 1
        for sprite in all_sprites:
            if sprite.type == 'wall' or sprite.type == 'enemy' and sprite != self:
                if pygame.sprite.collide_mask(self, sprite):
                    if self.rect.x > sprite.rect.x:
                        self.rect.x += 5
                    else:
                        self.rect.x -= 5
                    if self.rect.y > sprite.rect.y:
                        self.rect.y += 5
                    else:
                        self.rect.y -= 5


def pause():
    p = pygame.sprite.Group()
    sprite = pygame.sprite.Sprite(p)
    sprite.image = pause_image
    sprite.rect = sprite.image.get_rect()
    sprite.rect.x = 200
    sprite.rect.y = 200
    p.draw(screen)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == 13 or event.key == pygame.K_SPACE:
                    return  # начинаем игру
        pygame.display.flip()
        p.draw(screen)
        clock.tick(fps)


class Centre:
    def __init__(self, x, y):
        self.rect = pygame.Rect((x, y), (1, 1))

    def move_centre(self, dx, dy):
        self.x += dx
        self.y += dy


centre = Centre(width / 2, height / 2)
player = None
boss = None
colect_group = pygame.sprite.Group()
door_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
heart_group = pygame.sprite.Group()

level = load_level("levelex.txt")


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


camera = Camera()

running = True

while running:
    startScreen()
    room = Room(level)
    direction = None
    w, a, s, d = [False for i in range(4)]
    inv = False
    c = 0
    fire_pause = False
    dim = False
    fire_rate = 0
    while running:
        if fire_pause:
            fire_rate += 1
        if fire_rate >= player.fire_rate:
            fire_rate = 0
            fire_pause = False
        if c >= 60:
            inv = False
            c = 0
        if inv:
            c += 1
        if player.hearts <= 0:
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                collided_sprites = []
                for tile in all_sprites:
                    if pygame.sprite.collide_mask(player, tile):
                        if tile.type == 'wall':
                            if tile.rect.x < player.rect.x < tile.rect.x + tile_width - 1 and player.rect.x:
                                player.rect.x += 2
                            if player.rect.x + player_width - 1 > tile.rect.x > player.rect.x:
                                player.rect.x -= 2
                            if player.rect.y - tile.height - 1 < tile.rect.y < player.rect.y:
                                player.rect.y += 2
                            if tile.rect.y > player.rect.y > tile.rect.y - player_high - 1:
                                player.rect.y -= 2
                            collided_sprites.append(tile)
                if event.key == pygame.K_a:
                    player.stand = False
                    fl = True
                    for tile in collided_sprites:
                        if tile.rect.x < player.rect.x < tile.rect.x + tile_width - 1 and player.rect.x:
                            fl = False
                            w, a, s, d = [False for i in range(4)]
                            player.rect.x += 2

                    if fl:
                        a = True
                    if player.cur_direct != 'left':
                        player.last_direct = player.cur_direct
                    player.cur_direct = 'left'

                if event.key == pygame.K_d:
                    player.stand = False
                    fl = True
                    for tile in collided_sprites:

                        if player.rect.x + player_width - 1 > tile.rect.x > player.rect.x:
                            fl = False
                            w, a, s, d = [False for i in range(4)]
                            player.rect.x -= 2
                    if fl:
                        d = True
                    if player.cur_direct != 'right':
                        player.last_direct = player.cur_direct
                    player.cur_direct = 'right'
                if event.key == pygame.K_w:
                    player.stand = False
                    fl = True
                    for tile in collided_sprites:
                        if player.rect.y - tile.height - 1 < tile.rect.y < player.rect.y:
                            fl = False
                            w, a, s, d = [False for i in range(4)]
                            player.rect.y += 2
                    if fl:

                        w = True
                    if player.cur_direct != 'up':
                        player.last_direct = player.cur_direct
                    player.cur_direct = 'up'

                if event.key == pygame.K_s:
                    fl = True
                    player.stand = False
                    for tile in collided_sprites:
                        if tile.rect.y > player.rect.y > tile.rect.y - player_high - 1:
                            player.rect.y -= 2
                            fl = False
                            w, a, s, d = [False for i in range(4)]
                    if fl:
                        s = True
                    if player.cur_direct != 'down':
                        player.last_direct = player.cur_direct
                    player.cur_direct = 'down'

                if event.key == pygame.K_UP:
                    if not fire_pause:
                        player.fire('up')
                        fire_pause = True
                if event.key == pygame.K_DOWN:
                    if not fire_pause:
                        player.fire('down')
                        fire_pause = True
                if event.key == pygame.K_LEFT:
                    if not fire_pause:
                        player.fire('left')
                        fire_pause = True
                if event.key == pygame.K_RIGHT:
                    if not fire_pause:
                        player.fire('right')
                        fire_pause = True
                if event.key == pygame.K_ESCAPE:
                    pause()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    a = False
                    player.cur_direct = player.last_direct
                if event.key == pygame.K_d:
                    d = False
                    player.cur_direct = player.last_direct
                if event.key == pygame.K_w:
                    w = False
                    player.cur_direct = player.last_direct
                if event.key == pygame.K_s:
                    s = False
                    player.cur_direct = player.last_direct
                if (w, a, s, d) == (False, False, False, False,):
                    player.stand = True

        if w:
            player.rect.y -= player.speed
        if s:
            player.rect.y += player.speed
        if d:
            player.rect.x += player.speed
        if a:
            player.rect.x -= player.speed
        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)
        for sprite in enemy_group:
            if pygame.sprite.collide_mask(player, sprite):
                if not inv:
                    player.hearts -= 1
                    death_enemy = sprite
                    inv = True

        screen.fill(pygame.Color(0, 0, 0))
        for door in door_group:
            door.update()
        door_group.draw(screen)
        tiles_group.draw(screen)
        for item in colect_group:
            item.update()

        colect_group.draw(screen)
        player_group.draw(screen)
        for enemy in enemy_group:
            enemy.update()

        enemy_group.draw(screen)
        bullet_group.draw(screen)
        for i in range(player.hearts):
            Heart(i)
        heart_group.draw(screen)
        heart_group = pygame.sprite.Group()

        for bul in bullet_group:
            bul.update()
        player.update()
        if 0 < c < 30:
            player.hurt()

        pygame.display.flip()

        clock.tick(fps)
    if running:
        end_screen(death_enemy)
        all_sprites = pygame.sprite.Group()
        tiles_group = pygame.sprite.Group()
        player_group = pygame.sprite.Group()
        enemy_group = pygame.sprite.Group()
        bullet_group = pygame.sprite.Group()
        colect_group = pygame.sprite.Group()
        door_group = pygame.sprite.Group()

terminate()
