#!/usr/bin/env python
from __future__ import division
import io
import sys
import pygame
import gettext
import i18n
import ziptiled
import bitmapfont
import config
import resmngr
import scene_manager
import scene
import logo_scene
import menu_scene
import game_scene
import screen

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
    gettext.bindtextdomain('solstice', 'locale')
    gettext.textdomain('solstice')
    cfg = config.Configuration()
    pygame.init()
    scr = screen.Screen(cfg.screen_size, cfg, i18n._('Solstice'))
    rmngr = resmngr.ResourceManager('data.zip')
    logoscene = logo_scene.LogoScene(rmngr)
    menuscene = menu_scene.MenuScene(rmngr)
    gamescene = game_scene.GameScene(rmngr)
    scene_mngr = scene_manager.SceneManager(scr)
    scene_mngr.set(logoscene)
    scene_mngr.run()
    scene_mngr.set(menuscene)
    scene_mngr.run()
    sys.exit(0)

    level = ziptiled.TiledLoader('data.zip', 'level02.tmx')

    '''
    if cfg.music:
        pygame.mixer.music.load(music)
        pygame.mixer.music.set_volume(cfg.music_vol / 10)
        pygame.mixer.music.play(-1, 0.0)
    '''

    running = True
    FPS = 30
    clock = pygame.time.Clock()
    scroll_speed = [4, 4]
    view_port = [256, 144]
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

    half_view_port = (view_port[0]/2, view_port[1]/2)
    half_player = (player.w/2, player.h/2)

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_p]:
            if not check_right_collision(player, level):
                if (player.x % view_port[0]) >= half_view_port[0] - half_player[0]:

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
                if (player.x % view_port[0]) <= half_view_port[0] - half_player[0]:
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

        if keys[pygame.K_SPACE]:
            laser.play()


        if keys[pygame.K_a]:
            if not check_bottom_collision(player, level):
                if (player.y % view_port[1]) >= half_view_port[1] - half_player[1]:
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
                if (player.y % view_port[1]) <= half_view_port[0] - half_player[0]:
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

        render(scr.virt, level, cursor, view_port, player)
        scr.virt.blit(pnl_srf, (64, 80))
        pygame.transform.scale(scr.virt, cfg.screen_size, scr.display)
        pygame.display.update()

        milliseconds = clock.tick(FPS)
        playtime += milliseconds / 1000.0

    pygame.quit()
    return 0


def check_right_collision(player, level):

    calculated_x = int((player.absolute_x + player.w) / level.map.tilewidth)
    calculated_y = []
    calculated_y.insert(0, int(player.absolute_y / level.map.tilewidth))
    calculated_y.insert(1, int((player.absolute_y + ((player.h / 2) - 1)) / level.map.tilewidth))
    calculated_y.insert(2, int((player.absolute_y + (player.h - 1)) / level.map.tilewidth))

    for l in level.layers:
        if l.name == 'special':
            for a in calculated_y:
                if l.get_gid(calculated_x, a) == 520:
                    return True

    return False


def check_left_collision(player, level):

    calculated_x = int((player.absolute_x - 1) / level.map.tilewidth)
    calculated_y = []
    calculated_y.insert(0, int(player.absolute_y / level.map.tileheight))
    calculated_y.insert(1, int((player.absolute_y + ((player.h / 2) - 1)) / level.map.tileheight))
    calculated_y.insert(2, int((player.absolute_y + (player.h - 1)) / level.map.tileheight))

    for l in level.layers:
        if l.name == 'special':
            for a in calculated_y:
                if l.get_gid(calculated_x, a) == 520:
                    return True

    return False


def check_upper_collision(player, level):

    calculated_y = int((player.absolute_y - 1) / level.map.tileheight)
    calculated_x = []
    calculated_x.insert(0, int(player.absolute_x / level.map.tilewidth))
    calculated_x.insert(1, int((player.absolute_x + ((player.w / 2) - 1)) / level.map.tilewidth))
    calculated_x.insert(2, int((player.absolute_x + (player.w - 1)) / level.map.tilewidth))

    for l in level.layers:
        if l.name == 'special':
            for i in calculated_x:
                if l.get_gid(i, calculated_y) == 520:
                    return True

    return False


def check_bottom_collision(player, level):

    calculated_y = int((player.absolute_y + player.h) / level.map.tileheight)
    calculated_x = []
    calculated_x.insert(0, int(player.absolute_x / level.map.tilewidth))
    calculated_x.insert(1, int((player.absolute_x + ((player.w / 2) - 1)) / level.map.tilewidth))
    calculated_x.insert(2, int((player.absolute_x + (player.w - 1)) / level.map.tilewidth))

    for l in level.layers:
        if l.name == 'special':
            for i in calculated_x:
                if l.get_gid(i, calculated_y) == 520:
                    return True

    return False


if __name__ == '__main__':
    main()
