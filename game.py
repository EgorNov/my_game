import os
import sys

import pygame

pygame.init()

pygame.key.set_repeat(200, 10)
fps = 60

width = 400
height = 300
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()


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
                 "Если в правилах несколько строк,",
                 "приходится выводить их построчно"]

    screen.fill(pygame.Color('blue'))
    font = pygame.font.Font(None, 30)
    textCoord = 50
    for i in range(len(introText)):
        stringRendered = font.render(introText[i], 1, pygame.Color('white'))
        introRect = stringRendered.get_rect()
        textCoord += 10
        introRect.top = textCoord
        introRect.x = 10
        textCoord += introRect.height
        screen.blit(stringRendered, introRect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(fps)


startScreen()


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
    for i in range(len(level_map)):
        if len(level_map[i]) < maxWidth:
            level_map[i] += '.' * (maxWidth - len(level_map[i]))
    return level_map


def terminate():
    pygame.quit()
    sys.exit()


tile_images = {'wall': load_image('box.png'), 'empty': load_image('grass.png')}
player_image = load_image('player.png', colorkey=-1)
fly_image = load_image('fly.png', colorkey=-1)

tile_width = 50
tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, type, posx, posy):
        super().__init__(tiles_group, all_sprites)
        self.type = type
        self.image = tile_images[type]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(tile_width * posx, tile_height * posy)


class Player(pygame.sprite.Sprite):
    def __init__(self, columns, rows, posx, posy):
        super().__init__(player_group, all_sprites)
        self.frames = {}
        self.cut_sheet(player_image, columns, rows)
        self.cur_frame = 0
        self.stand = True
        self.hurts = 6
        self.image = self.frames['down'][6]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(tile_width * posx + 15, tile_height * posy + 5)
        self.speed = 2

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

    def update(self, direction):
        if not self.stand:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames[direction])
            self.image = self.frames[direction][self.cur_frame]
        else:
            self.image = self.frames['down'][6]



class Fly(pygame.sprite.Sprite):
    global player

    def __init__(self, columns, rows, posx, posy):
        super().__init__(enemy_group, all_sprites)
        self.frames = []
        self.cut_sheet(fly_image, columns, rows)
        self.cur_frame = 0
        self.stand = True
        self.hurts = 3
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

class Centre:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move_centre(self, dx, dy):
        self.x += dx
        self.y += dy


centre = Centre(width/2, height/2)
player = None

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()


def generate_level(level):
    global player
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                player = Player(3, 4, x, y,)
            elif level[y][x] == '*':
                Tile('empty', x, y)
                Fly(2, 1, x, y,)


level = load_level("levelex.txt")
generate_level(level)


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
direction = None
w, a, s, d = [False for i in range(4)]
inv = False
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            collided_sprites = []
            for sprite in tiles_group:
                if pygame.sprite.collide_mask(player, sprite):
                    if sprite.type == 'wall':
                        collided_sprites.append(sprite)
            if event.key == pygame.K_a:
                player.stand = False
                fl = True
                for tile in collided_sprites:
                    if player.rect.x < tile.rect.x + 49 and player.rect.x > tile.rect.x:
                        fl = False
                        a = False

                if fl:
                    a = True
                direction = 'left'

            if event.key == pygame.K_d:
                player.stand = False
                fl = True
                for tile in collided_sprites:
                    if player.rect.x + 34 > tile.rect.x and player.rect.x < tile.rect.x:
                        fl = False
                        d = False
                if fl:
                    d = True
                direction = 'right'
            if event.key == pygame.K_w:
                player.stand = False
                fl = True
                for tile in collided_sprites:
                    if player.rect.y - tile_height - 1 < tile.rect.y and player.rect.y > tile.rect.y:
                        fl = False
                        w = False
                if fl:
                    w = True
                direction = 'up'

            if event.key == pygame.K_s:
                fl = True
                player.stand = True
                for tile in collided_sprites:
                    if player.rect.y > tile.rect.y - 34 and player.rect.y < tile.rect.y:
                        fl = False
                        s = False
                if fl:
                    s = True
                direction = 'down'
                player.stand = False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                a = False
                player.stand = True
            if event.key == pygame.K_d:
                d = False
                player.stand = True
            if event.key == pygame.K_w:
                w = False
                player.stand = True
            if event.key == pygame.K_s:
                s = False
                player.stand = True
    # camera.update()
    if w:
        player.rect.y -= player.speed
    if s:
        player.rect.y += player.speed
    if d:
        player.rect.x += player.speed
    if a:
        player.rect.x -= player.speed
    for sprite in all_sprites:
        camera.apply(sprite)
    for sprite in enemy_group and not inv:
        if pygame.sprite.collide_mask(player, sprite):
            player.hurts -= 1
            print(player.hurts)

    screen.fill(pygame.Color(0, 0, 0))
    tiles_group.draw(screen)
    player_group.draw(screen)
    for enemy in enemy_group:
        enemy.update()
    enemy_group.draw(screen)
    player.update(direction)

    pygame.display.flip()

    clock.tick(fps)

terminate()
