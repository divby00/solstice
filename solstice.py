#!/usr/bin/env python
from __future__ import division
import io
import pygame
from pygame import gfxdraw
import ziptiled
import bitmapfont
import config
import resmngr


class Player(object):

    def __init__(self):
        pass


def render(surface, level, cursor, view_port, player):
    posx = posy = 0

    #Draw background
    backx = 0
    backy = 0
    backw = level.background.get_width()
    backh = level.background.get_height()

    for y in xrange(-1, int(192 / backh)):
        for x in xrange(-1, int(256 / backw)):
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
    '''
    pygame.draw.line(surface, (255,255,255), (512, 0), (512, 768), 1)
    pygame.draw.line(surface, (255,255,255), (0, 288), (1024, 288), 1)
    '''
    surface.blit(level.marcador, (0, view_port[1]))


def main():
    cfg = config.Configuration()
    pygame.init()
    graphics_params = pygame.DOUBLEBUF

    if cfg.fullscreen:
        graphics_params |= pygame.FULLSCREEN
        
    display = pygame.display.set_mode(cfg.screen_size, graphics_params)
    pygame.display.set_caption('Solstice')
    pygame.mouse.set_visible(False)
    display_info = pygame.display.Info()
    virt = pygame.Surface((256, 192), 0)
    pygame.event.set_allowed([pygame.QUIT])

    #Resource loading...
    rmngr = resmngr.ResourceManager('data.zip')
    logo = rmngr.get('logo')
    menu = rmngr.get('menu')
    music = rmngr.get('menu_song')
    font = rmngr.get('font')
    #Resource loading...

    clock = pygame.time.Clock()
    level = ziptiled.TiledLoader('data.zip', 'level02.tmx')

    if cfg.music:
        pygame.mixer.music.load(music)
        pygame.mixer.music.set_volume(cfg.music_vol / 10)
        pygame.mixer.music.play(-1, 0.0)

    running = True
    dither_anim = 6
    FPS = 30

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        virt.blit(logo, (128-(logo.get_width()/2), 96-(logo.get_height()/2)))

        for a in xrange(0, 192, 8):
            for i in xrange(0, 256, 8):
                virt.blit(level.dither[dither_anim], (i, a))

        if dither_anim > 0:
            dither_anim -= 1

        pygame.transform.scale(virt, cfg.screen_size, display)
        pygame.display.update()
        clock.tick(FPS)

        if dither_anim == 0:
            running = False
            virt.blit(logo, (128-(logo.get_width()/2), 96-(logo.get_height()/2)))
            pygame.transform.scale(virt, cfg.screen_size, display)
            pygame.display.update()
            pygame.time.delay(1500)

    dither_anim = 0
    running = True

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        virt.blit(logo, (128-(logo.get_width()/2), 96-(logo.get_height()/2)))

        for a in xrange(0, 192, 8):
            for i in xrange(0, 256, 8):
                virt.blit(level.dither[dither_anim], (i, a))

        if dither_anim < 7:
            dither_anim += 1

        pygame.transform.scale(virt, cfg.screen_size, display)
        pygame.display.update()
        clock.tick(FPS)

        if dither_anim == 7:
            running = False
            pygame.transform.scale(virt, cfg.screen_size, display)
            pygame.display.update()

    scroll_speed = [4, 4]
    view_port = [256, 144]
    running = True
    accumulator = 0

    player = Player()
    player.w = 16
    player.h = 16
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
    playtime = 0.0

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_p]:
            if not check_right_collision(player, level):
                if (player.x % view_port[0]) >= (view_port[0]/2) - (player.w / 2):
                    if cursor[0] < level.map.width_pixels - view_port[0]:
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
                    if cursor[1] < level.map.height_pixels - view_port[1] + (192/4):
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
        pygame.transform.scale(virt, cfg.screen_size, display)
        pygame.display.update()
        milliseconds = clock.tick(FPS)
        playtime += milliseconds / 1000.0

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
