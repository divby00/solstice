import pygame
import random
import math
import scene
import i18n


class Star(object):

    def __init__(self, x, y, star_type):
        self.x = x
        self.y = y
        self.star_type = star_type
        self.frame_incrementor = random.triangular()

        if self.star_type in [0, 1]:
            self.frame = random.randint(0, 3)
            self.maxframe = 4
        else:
            self.frame = random.randint(0, 1)
            self.maxframe = 2


class MenuScene(scene.Scene):

    def __init__(self, resourcemanager, scene_speed=30):
        super(MenuScene, self).__init__(resourcemanager, scene_speed)
        self.menu = resourcemanager.get('menu')
        self.background = pygame.Surface((self.menu.get_width(),
                                         self.menu.get_height())).convert()
        self.background_x_position = 0
        self.title_anim = 0
        self.panel = []
        panel = ['panel0', 'panel1', 'panel2',
                 'panel3', 'panel4', 'panel5',
                 'panel6', 'panel7', 'panel8']

        for p in xrange(0, len(panel)):
            self.panel.insert(p, resourcemanager.get(panel[p]))

        self.planet = resourcemanager.get('planet')
        self.title = resourcemanager.get('title')

        self.__init_stars(resourcemanager)
        self.text = self.font.get(i18n._('Press Return'), 256)
        self.intro_text = []
        self.intro_text.insert(0,
                               self.font.get(i18n._('In a very near place...'),
                                             256))
        self.intro_text.insert(1,
                               self.font.get(i18n._('...a nuclear plant is \
                                                    going to blow!!!'), 256))
        self.pnl_srf = pygame.Surface((128, 80))
        self.pnl_srf = self.pnl_srf.convert_alpha()
        self.pnl_srf.fill((0, 0, 0, 0))
        img = -1

        self.music = resourcemanager.get('menu_song')

        for a in xrange(0, 80, 8):
            for i in xrange(0, 128, 8):
                if a == 0 and i == 0:
                    img = 0
                if a == 0 and i > 0 and i < 120:
                    img = 1
                if a == 0 and i == 120:
                    img = 2
                if a > 0 and a < 72 and i == 0:
                    img = 3
                if a > 0 and a < 72 and i > 0 and i < 120:
                    img = 4
                if a > 0 and a < 72 and i == 120:
                    img = 5
                if a == 72 and i == 0:
                    img = 6
                if a == 72 and i > 0 and i < 120:
                    img = 7
                if a == 72 and i == 120:
                    img = 8

                self.pnl_srf.blit(self.panel[img], (i, a))
                self.pnl_srf.blit(self.text, (32, 16))

    def run(self):
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(self.music)
            pygame.mixer.music.play(-1)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RETURN]:
            pygame.mixer.music.stop()
            self.running = False

        for s in self.stars:
            s.frame += s.frame_incrementor

            if s.star_type == 0:
                if s.frame >= 4:
                    s.frame = 0
            if s.star_type == 1:
                if s.frame >= 4:
                    s.frame = 0
            if s.star_type == 2:
                if s.frame >= 2:
                    s.frame = 0
            if s.star_type == 3:
                if s.frame >= 2:
                    s.frame = 0

        # 196 is the sun position in the menu background image
        if self.background_x_position < 196:
            self.background_x_position += 2
        else:
            self.title_anim = 1

    def render(self, scr):

        self.background.blit(self.menu, (0, 0))

        for s in self.stars:
            img = None
            if s.star_type == 0:
                img = self.star_sprites[int(0 + s.frame)]
            if s.star_type == 1:
                img = self.star_sprites[int(4 + s.frame)]
            if s.star_type == 2:
                img = self.star_sprites[int(8 + s.frame)]
            if s.star_type == 3:
                img = self.star_sprites[int(10 + s.frame)]
            if img is not None:
                self.background.blit(img, (s.x, s.y))

        self.background.blit(self.planet, (278, 0))

        if self.title_anim > 0:
            self.background.blit(self.title, (298, 16))

        scr.virt.blit(self.background, (0, 0), (self.background_x_position, 0,
                                                scr.WINDOW_SIZE[0],
                                                scr.WINDOW_SIZE[1]))
        scr.virt.blit(self.text, (128-self.text.get_width()/2, 172))

        if self.background_x_position < 98:
            scr.virt.blit(self.intro_text[0],
                         (128-self.intro_text[0].get_width()/2, 68))
        elif self.background_x_position >= 98 and self.background_x_position < 196:
            scr.virt.blit(self.intro_text[1], 
                         (128-self.intro_text[1].get_width()/2, 68))

    def __init_stars(self, resourcemanager):
        self.stars = []
        stars_imgs = ['star0', 'star1', 'star2',
                      'star3', 'star4', 'star5',
                      'star6', 'star7', 'star8',
                      'star9', 'star10', 'star11']

        self.star_sprites = []
        for s in xrange(0, len(stars_imgs)):
            self.star_sprites.insert(s, resourcemanager.get(stars_imgs[s]))

        for s in xrange(0, 30):
            self.stars.insert(s, Star(random.randint(0, self.menu.get_width()), random.randint(0, 75), 1))
