#!/usr/bin/env python
from __future__ import division
import sys
import io
import zipfile
import pygame
from pygame import gfxdraw
import xml.etree.ElementTree as ElementTree

import bitmapfont


class Player(object):

    def __init__(self):
        pass


class Tileset(object):

    def __init__(self, name, w, h, tilew, tileh, src, firstgid):
        self.name = name
        self.w = w
        self.h = h
        self.tilew = tilew
        self.tileh = tileh
        self.src = src
        self.firstgid = firstgid
        self.img = None

    def __cmp__(self, other):
        return cmp(self.firstgid, other.firstgid)


class Tile(object):

    def __init__(self, srfc, size):
        self.srfc = srfc
        self.size = size


class Map(object):

    def __init__(self, width, height, tilewidth, tileheight):
        self.width = width
        self.height = height
        self.tilewidth = tilewidth
        self.tileheight = tileheight
        self.width_pixels = width * tilewidth
        self.height_pixels = height * tileheight


class Layer(object):

    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.data = []
        self.zindex = None
        self.visible = False
        self.animated_tiles = []

    def get_gid(self, x, y):

        if x < 0 or y < 0:
            return 0

        if (y * self.size[0]) + x >= (self.size[0] * self.size[1]):
            return 0

        return self.data[(y * self.size[0]) + x]

    def __cmp__(self, other):
        return cmp(self.zindex, other.zindex)


class ZippedTiledLoader(object):

    def __init__(self, filename, tmxfile):
        self.zf = zipfile.ZipFile(filename)
        self.tiles = []
        self.layers = []
        self.background = None
        self.map = None
        self.marcador = None
        self.__load(tmxfile)

    def __load(self, tmxfile):
        xml = self.zf.read('levels/' + tmxfile)

        source = None
        imgwidth = 0
        imgheight = 0
        tilewidth = 0
        tileheight = 0
        firstgid = 0
        name = None
        tilesets = []
        root = ElementTree.fromstring(xml)

        #Read basic map info
        self.map = Map(int(root.get('width')), int(root.get('height')),
                       int(root.get('tilewidth')), int(root.get('tileheight')))

        #Read tileset info
        animated_tiles = []

        for tileset in root.findall('tileset'):
            tilewidth = int(tileset.get('tilewidth'))
            tileheight = int(tileset.get('tileheight'))
            firstgid = int(tileset.get('firstgid'))
            name = tileset.get('name')

            for image in tileset.findall('image'):
                source = image.get('source')
                imgwidth = int(image.get('width'))
                imgheight = int(image.get('height'))

            for tile in tileset.findall('tile'):
                tileid = int(tile.get('id'))

                for properties in tile.findall('properties'):
                    for property in properties:
                        name = property.get('name')

                        if name == 'animated':
                            if property.get('value') == 'True':
                                animated_tiles.append(tileid)

            tilesets.append(Tileset(name, imgwidth, imgheight, tilewidth,
                                    tileheight, source, firstgid))

        tilesets.sort(key=lambda obj: obj.firstgid)

        #Read background info
        source = None

        for imagelayer in root.findall('imagelayer'):
            for image in imagelayer.findall('image'):
                source = image.get('source')

        if source is not None:
            img_data = self.zf.read('gfx/' + source)
            byte_data = io.BytesIO(img_data)

            if byte_data is not None:
                self.background = pygame.image.load(byte_data)

        #Read layer info
        layerwidth = layerheight = layername = gid = None

        for layer in root.findall('layer'):
            layerwidth = int(layer.get('width'))
            layerheight = int(layer.get('height'))
            layername = layer.get('name')
            l = Layer(layername, (layerwidth, layerheight))

            for properties in layer.findall('properties'):
                for property in properties.findall('property'):
                    prop = property.get('name')

                    if prop == 'zindex':
                        l.zindex = int(property.get('value'))

                    if prop == 'visible':
                        l.visible = (property.get('value') == 'True')

            for data in layer.findall('data'):
                for tile in data.findall('tile'):
                    gid = int(tile.get('gid'))

                    if gid in animated_tiles:
                        l.animated_tiles.append(gid)

                    l.data.append(gid)

            self.layers.append(l)

        self.layers.sort(key=lambda obj: obj.zindex)

        # Get beginning point
        for l in self.layers:

            if l.name == 'special':
                for a in xrange(0, l.size[1]):
                    for i in xrange(0, l.size[0]):

                        if l.get_gid(i, a) == 521:
                            self.start_point = (i, a)

        # Load tiles sprites
        img_count = 0
        blank = pygame.Color(0, 0, 0, 0)

        for t in tilesets:
            img_data = self.zf.read('gfx/' + t.src)
            byte_data = io.BytesIO(img_data)

            if byte_data is not None:
                t.img = pygame.image.load(byte_data)
                t.img = t.img.convert_alpha()

            if t.img is not None:

                for y in xrange(0, t.h, t.tileh):

                    for x in xrange(0, t.w, t.tilew):
                        srfc = pygame.Surface((t.tilew, t.tileh))
                        srfc = srfc.convert_alpha()

                        if srfc is not None:
                            srfc.fill(blank)
                            srfc.blit(t.img,
                                      (0, 0),
                                      (x, y, t.tilew, t.tileh),
                                      0)

                        self.tiles.append(Tile(srfc, (t.tilew, t.tileh)))
                        img_count += 1

        # TODO: Remove this
        img_data = self.zf.read('gfx/marcador.png')
        byte_data = io.BytesIO(img_data)

        if byte_data is not None:
            self.marcador = pygame.image.load(byte_data)

        img_data = self.zf.read('gfx/equinox.png')
        byte_data = io.BytesIO(img_data)

        if byte_data is not None:
            temp = pygame.image.load(byte_data)
            self.equinox = []
            self.animation = 0
            self.direction = 1

            for i in xrange(0, 1024, 64):
                srfc = pygame.Surface((64, 64))
                srfc = srfc.convert_alpha()
                srfc.fill(blank)
                srfc.blit(temp, (0, 0), (i, 0, i+64, 64))
                self.equinox.append(srfc)

        img_data = self.zf.read('gfx/tree.png')
        byte_data = io.BytesIO(img_data)

        if byte_data is not None:
            temp = pygame.image.load(byte_data)
            self.tree = []
            self.tanimation = 0

            for i in xrange(0, 1152, 192):
                srfc = pygame.Surface((192, 192))
                srfc = srfc.convert_alpha()
                srfc.fill(blank)
                srfc.blit(temp, (0, 0), (i, 0, i+192, 192))
                self.tree.append(srfc)
        # Fin TODO

        self.zf.close()

    def get_gid(self, x, y, name):
        for l in self.layers:
            if l.name == name:
                return l.get_gid(x, y)
        return 0


def render(surface, level, cursor, view_port, player):
    posx = posy = 0

    #Draw background
    backx = 0
    backy = 0
    backw = level.background.get_width()
    backh = level.background.get_height()

    for y in xrange(-1, int(768 / backh)):
        for x in xrange(-1, int(1024 / backw)):
            backx = backw - (cursor[0] % backw)
            backy = backh - (cursor[1] % backh)
            surface.blit(level.background,
                         (backx + (x * backw), backy + (y * backh)))

    offset_pixels = (cursor[0] % level.map.tilewidth,
                     cursor[1] % level.map.tileheight)
    offset_tiles = (cursor[0] / level.map.tilewidth,
                    cursor[1] / level.map.tileheight)
    aux = False

    for l in level.layers:

        if l.visible:

            if l.name == 'backpatterns':
                posy = posx = 0

                for y in xrange(int(offset_tiles[1]), int(offset_tiles[1]) + int((view_port[1]/level.map.tileheight)+1)):
                    for x in xrange(int(offset_tiles[0]), int(offset_tiles[0]) + int((view_port[0]/level.map.tilewidth)+1)):
                        gid = l.get_gid(x, y)

                        if gid > 0:
                            surface.blit(level.tiles[gid-1].srfc,
                                        (posx - offset_pixels[0],
                                         posy - offset_pixels[1]),
                                        (0, 0, l.size[0], l.size[1]))

                        posx += level.tiles[gid - 1].size[0]

                    posx = 0
                    posy += level.tiles[gid-1].size[1]

            surface.blit(level.equinox[level.animation],
                        (player.x % view_port[0], player.y % view_port[1]))

            if l.name == 'forepatterns':
                posy = posx = 0

                for y in xrange(int(offset_tiles[1]), int(offset_tiles[1]) + int((view_port[1]/level.map.tileheight)+1)):
                    for x in xrange(int(offset_tiles[0]), int(offset_tiles[0]) + int((view_port[0]/level.map.tilewidth)+1)):
                        gid = l.get_gid(x, y)

                        if gid > 0:
                            surface.blit(level.tiles[gid-1].srfc,
                                        (posx - offset_pixels[0],
                                         posy - offset_pixels[1]),
                                        (0, 0, l.size[0], l.size[1]))

                        posx += level.tiles[gid-1].size[0]

                    posx = 0
                    posy += level.tiles[gid-1].size[1]

    '''
    for l in level.layers:

        if l.name == 'special':
            posy = posx = 0

            for y in xrange(int(offset_tiles[1]), int(offset_tiles[1]) + int((view_port[1]/level.map.tileheight)+1)):
                for x in xrange(int(offset_tiles[0]), int(offset_tiles[0]) + int((view_port[0]/level.map.tilewidth)+1)):
                    gid = l.get_gid(x, y)

                    if gid > 0:
                        pygame.draw.rect(surface, (120,0,0), ((posx - offset_pixels[0])+4, (posy - offset_pixels[1])+4, 24, 24), 0)

                    posx += 32

                posx = 0
                posy += 32
    '''

    level.animation += level.direction

    if level.animation == 16:
        level.animation = 0

    if level.animation < 0:
        level.animation = 15

    pygame.draw.line(surface, (255,255,255), (512, 0), (512, 768), 1)
    pygame.draw.line(surface, (255,255,255), (0, 288), (1024, 288), 1)
    surface.blit(level.marcador, (0, view_port[1]))


def main():
    pygame.init()
    pygame.display.set_mode((1024, 768))
    pygame.display.set_caption('Solstice, Equinox remake')
    display_info = pygame.display.Info()
    display = pygame.display.set_mode((display_info.current_w,
                                      display_info.current_h),
                                      pygame.DOUBLEBUF)
    virt = pygame.Surface((display_info.current_w, display_info.current_h), 0)
    pygame.event.set_allowed([pygame.QUIT])
    level = ZippedTiledLoader('data.zip', 'level01.tmx')
    font = bitmapfont.BitmapFont('data.zip', 'font_white.png')
    texto = font.get(', SOLSTICE ,')
    scroll_speed = [16, 16]
    # OJO!!! 192. Altura del marcador.
    view_port = [display_info.current_w, display_info.current_h - 192]
    running = True
    accumulator = 0

    player = Player()
    player.w = 64
    player.h = 64
    player.x = level.start_point[0] * level.map.tilewidth
    player.y = level.start_point[1] * level.map.tileheight
    player.absolute_x = player.x
    player.absolute_y = player.y

    cursor = [0, 0]
    cursor[0] = player.x - (view_port[0] / 2) + (player.w / 2)
    cursor[1] = player.y - (view_port[1] / 2) + (player.h / 2)

    if cursor[0] < 0:
        cursor[0] = 0

    if cursor[1] < 0:
        cursor[1] = 0

    player.y = view_port[1] / 2 - (player.h / 2)

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_p]:
            if not check_right_collision(player, level):
                if (player.x % view_port[0]) >= (view_port[0]/2) - (player.w / 2):
                    if cursor[0] < level.map.width_pixels - display_info.current_w:
                        level.direction = 1
                        cursor[0] += scroll_speed[0]
                        player.absolute_x += scroll_speed[0]
                    else:
                        player.x += scroll_speed[0]
                        player.absolute_x += scroll_speed[0]
                else:
                    player.x += scroll_speed[0]
                    player.absolute_x += scroll_speed[0]

        if keys[pygame.K_o]:
            if not check_left_collision(player, level):
                if (player.x % view_port[0]) <= (view_port[0]/2) - (player.w / 2):
                    if cursor[0] > 0:
                        level.direction = -1
                        cursor[0] -= scroll_speed[0]
                        player.absolute_x -= scroll_speed[0]
                    else:
                        player.x -= scroll_speed[0]
                        player.absolute_x -= scroll_speed[0]
                else:
                    player.x -= scroll_speed[0]
                    player.absolute_x -= scroll_speed[0]

        if keys[pygame.K_a]:
            if not check_bottom_collision(player, level):
                if (player.y % view_port[1]) >= (view_port[1]/2) - (player.h / 2):
                    if cursor[1] < level.map.height_pixels - display_info.current_h + 192:
                        cursor[1] += scroll_speed[1]
                        player.absolute_y += scroll_speed[1]
                    else:
                        player.y += scroll_speed[1]
                        player.absolute_y += scroll_speed[1]
                else:
                    player.y += scroll_speed[1]
                    player.absolute_y += scroll_speed[1]

        if keys[pygame.K_q]:
            if not check_upper_collision(player, level):
                if (player.y % view_port[1]) <= (view_port[1]/2) - (player.h / 2):
                    if cursor[1] > 0:
                        cursor[1] -= scroll_speed[1]
                        player.absolute_y -= scroll_speed[1]
                    else:
                        player.y -= scroll_speed[1]
                        player.absolute_y -= scroll_speed[1]
                else:
                    player.y -= scroll_speed[1]
                    player.absolute_y -= scroll_speed[1]

        if keys[pygame.K_ESCAPE]:
            running = False

        render(virt, level, cursor, view_port, player)
        virt.blit(texto, (512 - (texto.get_width()/2), 32))
        display.blit(virt, (0, 0))
        pygame.display.flip()
        #pygame.time.delay(20)

    pygame.quit()
    return 0


def check_right_collision(player, level):

    for l in level.layers:

        if l.name == 'special':
            x = int((player.absolute_x + player.w) / level.map.tilewidth)
            y = []
            y.append(int(player.absolute_y / level.map.tilewidth))
            y.append(int((player.absolute_y + ((player.h / 2) - 1)) / level.map.tilewidth))
            y.append(int((player.absolute_y + (player.h - 1)) / level.map.tilewidth))

            for a in y:
                if l.get_gid(x, a) == 520:
                    return True

    return False


def check_left_collision(player, level):

    for l in level.layers:

        if l.name == 'special':
            x = int((player.absolute_x - 1) / level.map.tilewidth)
            y = []
            y.append(int(player.absolute_y / level.map.tileheight))
            y.append(int((player.absolute_y + ((player.h / 2) - 1)) / level.map.tileheight))
            y.append(int((player.absolute_y + (player.h - 1)) / level.map.tileheight))

            for a in y:
                if l.get_gid(x, a) == 520:
                    return True

    return False


def check_upper_collision(player, level):

    for l in level.layers:

        if l.name == 'special':
            x = []
            y = int((player.absolute_y - 1) / level.map.tileheight)
            x.append(int(player.absolute_x / level.map.tilewidth))
            x.append(int((player.absolute_x + ((player.w / 2) - 1)) / level.map.tilewidth))
            x.append(int((player.absolute_x + (player.w - 1)) / level.map.tilewidth))

            for i in x:
                if l.get_gid(i, y) == 520:
                    return True

    return False


def check_bottom_collision(player, level):

    for l in level.layers:

        if l.name == 'special':
            x = []
            y = int((player.absolute_y + player.h) / level.map.tileheight)
            x.append(int(player.absolute_x / level.map.tilewidth))
            x.append(int((player.absolute_x + ((player.w / 2) - 1)) / level.map.tilewidth))
            x.append(int((player.absolute_x + (player.w - 1)) / level.map.tilewidth))

            for i in x:
                if l.get_gid(i, y) == 520:
                    return True

    return False


if __name__ == '__main__':
    main()
