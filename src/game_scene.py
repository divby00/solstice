from gettext import gettext as _
import control
import menu
import player
import pygame
import scene


class GameScene(scene.Scene):

    def __init__(self, context, name, scene_speed=25):
        super(GameScene, self).__init__(context, name, scene_speed)
        self.screen = context.scr
        self.marcador = context.resourcemanager.get('marcador')
        self.level01 = context.resourcemanager.get('level01')
        self.level02 = context.resourcemanager.get('level02')
        self.player = player.Player(context.resourcemanager,
                                    self.level01)
        self.laser = context.resourcemanager.get('laser')
        self.song = context.resourcemanager.get('level01_song')
        self.music = self.song
        self.get_menu()

    def on_start(self):
        self.player.on_start()
        self.scroll_speed = [4, 4]
        self.view_port = [256, 144]
        self.cursor = [0, 0]
        self.cursor[0] = self.player.x - (self.view_port[0] / 2) + \
            (self.player.w / 2)
        self.cursor[1] = self.player.y - (self.view_port[1] / 2) + \
            (self.player.h / 2)

        if self.cursor[0] < 0:
            self.cursor[0] = 0

        if self.cursor[1] < 0:
            self.cursor[1] = 0

        self.player.y = self.view_port[1] / 2 - (self.player.h / 2)
        self.half_view_port = (self.view_port[0]/2, self.view_port[1]/2)
        self.half_player = (self.player.w/2, self.player.h/2)
        self.menu_group.visible = False
        self.current_level = self.level01
        self.music.play(-1)

    def on_quit(self):
        self.music.stop()

    def run(self):
        if self.menu_group.visible:
            self.menu_group.run()
        else:
            half = [self.half_view_port[0] - self.half_player[0],
                    self.half_view_port[1] - self.half_player[1]]

            map_size = [self.current_level.map.width_pixels - self.view_port[0],
                        self.current_level.map.height_pixels -
                        self.view_port[1] + (192/4)]

            if self.control.on(control.Control.RIGHT):
                if not check_right_collision(self.player, self.current_level):
                    if (self.player.x % self.view_port[0]) >= half[0]:
                        if self.cursor[0] < map_size[0]:
                            self.player.direction = 1
                            self.cursor[0] += self.scroll_speed[0]
                            self.player.absolute_x += self.scroll_speed[0]
                        else:
                            self.player.direction = 1
                            self.player.x += self.scroll_speed[0]
                            self.player.absolute_x += self.scroll_speed[0]
                    else:
                        self.player.direction = 1
                        self.player.x += self.scroll_speed[0]
                        self.player.absolute_x += self.scroll_speed[0]

            if self.control.on(control.Control.LEFT):
                if not check_left_collision(self.player, self.current_level):
                    if (self.player.x % self.view_port[0]) <= half[0]:
                        if self.cursor[0] > 0:
                            self.player.direction = -1
                            self.cursor[0] -= self.scroll_speed[0]
                            self.player.absolute_x -= self.scroll_speed[0]
                        else:
                            self.player.direction = -1
                            self.player.x -= self.scroll_speed[0]
                            self.player.absolute_x -= self.scroll_speed[0]
                    else:
                        self.player.direction = -1
                        self.player.x -= self.scroll_speed[0]
                        self.player.absolute_x -= self.scroll_speed[0]

            if self.control.on(control.Control.DOWN):
                if not check_bottom_collision(self.player, self.current_level):
                    if (self.player.y % self.view_port[1]) >= half[1]:
                        if self.cursor[1] < map_size[1]:
                            self.cursor[1] += self.scroll_speed[1]
                            self.player.absolute_y += self.scroll_speed[1]
                        else:
                            self.player.y += self.scroll_speed[1]
                            self.player.absolute_y += self.scroll_speed[1]
                    else:
                        self.player.y += self.scroll_speed[1]
                        self.player.absolute_y += self.scroll_speed[1]

            if self.control.on(control.Control.UP):
                if not check_upper_collision(self.player, self.current_level):
                    if (self.player.y % self.view_port[1]) <= half[1]:
                        if self.cursor[1] > 0:
                            self.cursor[1] -= self.scroll_speed[1]
                            self.player.absolute_y -= self.scroll_speed[1]
                        else:
                            self.player.y -= self.scroll_speed[1]
                            self.player.absolute_y -= self.scroll_speed[1]
                    else:
                        self.player.y -= self.scroll_speed[1]
                        self.player.absolute_y -= self.scroll_speed[1]

            '''
            if self.control.on('action1'):
                self.laser.play()
            '''

            if self.control.on(control.Control.ACTION2):
                self.menu_group.visible = True

        self.player.animation += self.player.direction

        if self.player.animation == 15:
            self.player.animation = 0
        if self.player.animation < 0:
            self.player.animation = 14

    def render(self, scr):
        posx = posy = 0
        backx = 0
        backy = 0
        backw = self.current_level.background.get_width()
        backh = self.current_level.background.get_height()

        for y in xrange(-1, int(192 / backh)):
            for x in xrange(-1, int(256 / backw)):
                backx = backw - (self.cursor[0] % backw)
                backy = backh - (self.cursor[1] % backh)
                scr.virt.blit(self.current_level.background,
                              (backx + (x * backw), backy + (y * backh)))

        offset_pixels = (self.cursor[0] % self.current_level.map.tilewidth,
                         self.cursor[1] % self.current_level.map.tileheight)
        offset_tiles = (self.cursor[0] / self.current_level.map.tilewidth,
                        self.cursor[1] / self.current_level.map.tileheight)
        aux = False

        for l in self.current_level.layers:

            if l.visible:

                range_limit_y = int(offset_tiles[1]) + \
                    int((self.view_port[1] /
                         self.current_level.map.tileheight)+1)

                range_limit_x = int(offset_tiles[0]) + \
                    int((self.view_port[0] /
                         self.current_level.map.tilewidth)+1)

                if l.name == 'backpatterns':
                    posy = posx = 0

                    for y in xrange(int(offset_tiles[1]), range_limit_y):
                        for x in xrange(int(offset_tiles[0]), range_limit_x):
                            gid = l.get_gid(x, y)

                            if gid > 0:
                                scr.virt.blit(
                                    self.current_level.tiles[gid-1].srfc,
                                    (posx - offset_pixels[0],
                                     posy - offset_pixels[1]),
                                    (0, 0, l.size[0], l.size[1]))

                            posx += self.current_level.tiles[gid - 1].size[0]

                        posx = 0
                        posy += self.current_level.tiles[gid-1].size[1]

                scr.virt.blit(self.player.sprites[self.player.animation],
                              (self.player.x % self.view_port[0],
                               self.player.y % self.view_port[1]))

                if l.name == 'forepatterns':
                    posy = posx = 0

                    for y in xrange(int(offset_tiles[1]), range_limit_y):
                        for x in xrange(int(offset_tiles[0]), range_limit_x):
                            gid = l.get_gid(x, y)

                            if gid > 0:
                                scr.virt.blit(
                                    self.current_level.tiles[gid-1].srfc,
                                    (posx - offset_pixels[0],
                                     posy - offset_pixels[1]),
                                    (0, 0, l.size[0], l.size[1]))

                            posx += self.current_level.tiles[gid-1].size[0]

                        posx = 0
                        posy += self.current_level.tiles[gid-1].size[1]

        if self.menu_group.visible:
            self.menu_group.render(scr.virt, (128, 70))

        scr.virt.blit(self.marcador, (0, self.view_port[1]))


def check_right_collision(player, level):

    calculated_x = int((player.absolute_x + player.w) / level.map.tilewidth)
    calculated_y = []
    calculated_y.insert(0, int(player.absolute_y / level.map.tilewidth))
    calculated_y.insert(1, int((player.absolute_y + ((player.h / 2) - 1)) /
                               level.map.tilewidth))
    calculated_y.insert(2, int((player.absolute_y + (player.h - 1)) /
                               level.map.tilewidth))

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
    calculated_y.insert(1, int((player.absolute_y + ((player.h / 2) - 1)) /
                               level.map.tileheight))
    calculated_y.insert(2, int((player.absolute_y + (player.h - 1)) /
                               level.map.tileheight))

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
    calculated_x.insert(1, int((player.absolute_x + ((player.w / 2) - 1)) /
                               level.map.tilewidth))
    calculated_x.insert(2, int((player.absolute_x + (player.w - 1)) /
                               level.map.tilewidth))

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
    calculated_x.insert(1, int((player.absolute_x + ((player.w / 2) - 1)) /
                               level.map.tilewidth))
    calculated_x.insert(2, int((player.absolute_x + (player.w - 1)) /
                               level.map.tilewidth))

    for l in level.layers:
        if l.name == 'special':
            for i in calculated_x:
                if l.get_gid(i, calculated_y) == 520:
                    return True

    return False
