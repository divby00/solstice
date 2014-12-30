import pygame
import control
import player
import scene
import particles_manager
import particles
import scroll


class GameScene(scene.Scene):

    def __init__(self, context, name='game', scene_speed=25):
        super(GameScene, self).__init__(context, name, scene_speed)
        self.screen = context.scr
        self.marcador = context.resourcemanager.get('marcador')
        self.level01 = context.resourcemanager.get('level01')
        # self.level02 = context.resourcemanager.get('level02')
        self.scrollobj = None
        self.particlesmanager = particles_manager.ParticlesManager()
        beam_particles = particles.BeamParticles(context, 'hit')
        self.particlesmanager.register_particles(beam_particles)
        context.particlesmanager = self.particlesmanager
        self.player = player.Player(context, self.level01)
        self.animations = context.resourcemanager.animations
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

        self.half_view_port = (self.view_port[0] / 2, self.view_port[1] / 2)
        self.half_player = (self.player.w / 2, self.player.h / 2)
        self.menu_group.visible = False
        self.current_level = self.level01
        self.scrollobj = scroll.Scroll(self.current_level, self.player)
        self.map_size = [self.current_level.map.width_pixels - self.view_port[0],
                         self.current_level.map.height_pixels - self.view_port[1] + (192 / 4)]
        self.half = [self.half_view_port[0] - self.half_player[0],
                     self.half_view_port[1] - self.half_player[1]]

        self.music.play(-1)

    def on_quit(self):
        self.music.stop()

    def run2(self):
        if self.menu_group.visible:
            self.menu_group.run()
        else:
            if self.control.on(control.Control.RIGHT):
                if not self.player.check_right_collision(self.current_level):
                    if (self.player.x % self.view_port[0]) >= self.half[0]:
                        if self.cursor[0] < self.map_size[0]:
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
                if not self.player.check_left_collision(self.current_level):
                    if (self.player.x % self.view_port[0]) <= self.half[0]:
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
                if not self.player.check_bottom_collision(self.current_level):
                    if (self.player.y % self.view_port[1]) >= self.half[1]:
                        if self.cursor[1] < self.map_size[1]:
                            self.cursor[1] += self.scroll_speed[1]
                            self.player.absolute_y += self.scroll_speed[1]
                        else:
                            self.player.y += self.scroll_speed[1]
                            self.player.absolute_y += self.scroll_speed[1]
                    else:
                        self.player.y += self.scroll_speed[1]
                        self.player.absolute_y += self.scroll_speed[1]

            if self.control.on(control.Control.UP):
                if not self.player.check_upper_collision(self.current_level):
                    if (self.player.y % self.view_port[1]) <= self.half[1]:
                        if self.cursor[1] > 0:
                            self.cursor[1] -= self.scroll_speed[1]
                            self.player.absolute_y -= self.scroll_speed[1]
                        else:
                            self.player.y -= self.scroll_speed[1]
                            self.player.absolute_y -= self.scroll_speed[1]
                    else:
                        self.player.y -= self.scroll_speed[1]
                        self.player.absolute_y -= self.scroll_speed[1]

            if self.control.on('action1'):
                self.laser.play()
                self.player.firing = True

            if self.control.on(control.Control.ACTION2):
                self.menu_group.visible = True

            self.particlesmanager.run()

        self.player.run()

    def run(self):
        if self.menu_group.visible:
            self.menu_group.run()
        else:
            if self.control.on(control.Control.RIGHT):
                self.player.x += 4
            if self.control.on(control.Control.LEFT):
                self.player.x -= 4
            if self.control.on(control.Control.UP):
                self.player.y -= 4
            if self.control.on(control.Control.DOWN):
                self.player.y += 4

            if self.control.on(control.Control.ACTION2):
                self.menu_group.visible = True

        self.player.run()

    def render(self, scr):
        
        scr.virt.blit(self.scrollobj.get_frame(), (0, 0))

        if self.menu_group.visible:
            self.menu_group.render(scr.virt, (128, 70))

        scr.virt.blit(self.marcador, (0, self.view_port[1]))

    def render2(self, scr):
        posx = posy = 0
        backx = 0
        backy = 0
        backw = self.current_level.back.get_width()
        backh = self.current_level.back.get_height()

        for y in xrange(-1, int(192 / backh)):
            for x in xrange(-1, int(256 / backw)):
                backx = backw - (self.cursor[0] % backw)
                backy = backh - (self.cursor[1] % backh)
                scr.virt.blit(self.current_level.back,
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
                                     self.current_level.map.tileheight) + 1)

                range_limit_x = int(offset_tiles[0]) + \
                                int((self.view_port[0] /
                                     self.current_level.map.tilewidth) + 1)

                if l.name == 'backpatterns':
                    posy = posx = 0

                    for y in xrange(int(offset_tiles[1]), range_limit_y):
                        for x in xrange(int(offset_tiles[0]), range_limit_x):
                            gid = l.get_gid(x, y)

                            if gid > 0:
                                if gid in self.current_level.animated_tiles.keys():
                                    nombre = self.current_level.animated_tiles.get(gid)
                                    anim = self.animations.get(nombre)
                                    img = anim.images.get(str(anim.frames[anim.active_frame].id))
                                    scr.virt.blit( img, (posx - offset_pixels[0], posy - offset_pixels[1]))
                                    if anim.active_frame < 6:
                                        anim.active_frame += 1
                                    else:
                                        anim.active_frame = 0
                                else:
                                    scr.virt.blit(
                                        self.current_level.tiles[gid - 1].srfc,
                                        (posx - offset_pixels[0],
                                         posy - offset_pixels[1]),
                                        (0, 0, l.size[0], l.size[1]))

                            posx += self.current_level.tiles[gid - 1].size[0]

                        posx = 0
                        posy += self.current_level.tiles[gid - 1].size[1]

                self.player.render()

                if l.name == 'forepatterns':
                    posy = posx = 0

                    for y in xrange(int(offset_tiles[1]), range_limit_y):
                        for x in xrange(int(offset_tiles[0]), range_limit_x):
                            gid = l.get_gid(x, y)

                            if gid > 0:
                                scr.virt.blit(
                                    self.current_level.tiles[gid - 1].srfc,
                                    (posx - offset_pixels[0],
                                     posy - offset_pixels[1]),
                                    (0, 0, l.size[0], l.size[1]))

                            posx += self.current_level.tiles[gid - 1].size[0]

                        posx = 0
                        posy += self.current_level.tiles[gid - 1].size[1]

                self.particlesmanager.render(scr.virt)

        if self.menu_group.visible:
            self.menu_group.render(scr.virt, (128, 70))

        scr.virt.blit(self.marcador, (0, self.view_port[1]))
