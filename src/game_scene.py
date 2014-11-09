import pygame
import scene
import player


class GameScene(scene.Scene):

    def __init__(self, context, scene_speed=30):
        super(GameScene, self).__init__(context, scene_speed)
        self.marcador = context.resourcemanager.get('marcador')
        self.level01 = context.resourcemanager.get('level01')
        self.level02 = context.resourcemanager.get('level02')
        self.current_level = self.level01
        self.player = player.Player(context.resourcemanager, self.current_level)

        ''' Scroll related variables '''
        self.scroll_speed = [4, 4]
        self.view_port = [256, 144]
        self.cursor = [0, 0]
        self.cursor[0] = self.player.x - (self.view_port[0] / 2) + (self.player.w / 2)
        self.cursor[1] = self.player.y - (self.view_port[1] / 2) + (self.player.h / 2)

        if self.cursor[0] < 0:
            self.cursor[0] = 0

        if self.cursor[1] < 0:
            self.cursor[1] = 0

        self.player.y = self.view_port[1] / 2 - (self.player.h / 2)
        self.half_view_port = (self.view_port[0]/2, self.view_port[1]/2)
        self.half_player = (self.player.w/2, self.player.h/2)
        self.song = context.resourcemanager.get('level01_song')
        self.laser = context.resourcemanager.get('laser')
        self.music = pygame.mixer.Sound(self.song)
        self.playing = False

    def run(self):

        if not self.playing:
            self.playing = True
            self.music.play(-1)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_p]:
            if not check_right_collision(self.player, self.current_level):
                if (self.player.x % self.view_port[0]) >= self.half_view_port[0] - self.half_player[0]:

                    if self.cursor[0] < self.current_level.map.width_pixels - self.view_port[0]:
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

        if keys[pygame.K_o]:
            if not check_left_collision(self.player, self.current_level):
                if (self.player.x % self.view_port[0]) <= self.half_view_port[0] - self.half_player[0]:
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

        if keys[pygame.K_a]:
            if not check_bottom_collision(self.player, self.current_level):
                if (self.player.y % self.view_port[1]) >= self.half_view_port[1] - self.half_player[1]:
                    if self.cursor[1] < self.current_level.map.height_pixels - self.view_port[1] + (192/4):
                        self.cursor[1] += self.scroll_speed[1]
                        self.player.absolute_y += self.scroll_speed[1]
                    else:
                        self.player.y += self.scroll_speed[1]
                        self.player.absolute_y += self.scroll_speed[1]
                else:
                    self.player.y += self.scroll_speed[1]
                    self.player.absolute_y += self.scroll_speed[1]

        if keys[pygame.K_q]:
            if not check_upper_collision(self.player, self.current_level):
                if (self.player.y % self.view_port[1]) <= self.half_view_port[0] - self.half_player[0]:
                    if self.cursor[1] > 0:
                        self.cursor[1] -= self.scroll_speed[1]
                        self.player.absolute_y -= self.scroll_speed[1]
                    else:
                        self.player.y -= self.scroll_speed[1]
                        self.player.absolute_y -= self.scroll_speed[1]
                else:
                    self.player.y -= self.scroll_speed[1]
                    self.player.absolute_y -= self.scroll_speed[1]

        if keys[pygame.K_SPACE]:
            self.laser.play()

        if keys[pygame.K_ESCAPE]:
            self.running = False

        self.player.animation += self.player.direction

        if self.player.animation == 15:
            self.player.animation = 0
        if self.player.animation < 0:
            self.player.animation = 14

    def render(self, scr):
        posx = posy = 0

        #Draw background
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

                if l.name == 'backpatterns':
                    posy = posx = 0

                    for y in xrange(int(offset_tiles[1]), int(offset_tiles[1]) + int((self.view_port[1]/self.current_level.map.tileheight)+1)):
                        for x in xrange(int(offset_tiles[0]), int(offset_tiles[0]) + int((self.view_port[0]/self.current_level.map.tilewidth)+1)):
                            gid = l.get_gid(x, y)

                            if gid > 0:
                                scr.virt.blit(self.current_level.tiles[gid-1].srfc,
                                              (posx - offset_pixels[0],
                                               posy - offset_pixels[1]),
                                              (0, 0, l.size[0], l.size[1]))

                            posx += self.current_level.tiles[gid - 1].size[0]

                        posx = 0
                        posy += self.current_level.tiles[gid-1].size[1]

                scr.virt.blit(self.player.sprites[self.player.animation],
                             (self.player.x % self.view_port[0], self.player.y % self.view_port[1]))

                if l.name == 'forepatterns':
                    posy = posx = 0

                    for y in xrange(int(offset_tiles[1]), int(offset_tiles[1]) + int((self.view_port[1]/self.current_level.map.tileheight)+1)):
                        for x in xrange(int(offset_tiles[0]), int(offset_tiles[0]) + int((self.view_port[0]/self.current_level.map.tilewidth)+1)):
                            gid = l.get_gid(x, y)

                            if gid > 0:
                                scr.virt.blit(self.current_level.tiles[gid-1].srfc,
                                             (posx - offset_pixels[0],
                                              posy - offset_pixels[1]),
                                             (0, 0, l.size[0], l.size[1]))

                            posx += self.current_level.tiles[gid-1].size[0]

                        posx = 0
                        posy += self.current_level.tiles[gid-1].size[1]

        scr.virt.blit(self.marcador, (0, self.view_port[1]))


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
