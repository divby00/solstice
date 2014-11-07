import pygame
import random
import math
import scene
import i18n


class Panel(object):

    def __init__(self, resourcemanager):
        self.panel_imgs = []
        panel = ['panel0', 'panel1', 'panel2',
                 'panel3', 'panel4', 'panel5',
                 'panel6', 'panel7', 'panel8']

        for p in xrange(0, len(panel)):
            self.panel_imgs.insert(p, resourcemanager.get(panel[p]))

    def get(self, size):
        assert(size[0] > 0)
        assert(size[1] > 0)
        surface = pygame.Surface(size).convert_alpha()
        surface.fill((0, 0, 0, 0))
        img = -1

        for a in xrange(0, size[1], 8):
            for i in xrange(0, size[0], 8):
                if a == 0 and i == 0:
                    img = 0
                if a == 0 and i > 0 and i < size[0] - 8:
                    img = 1
                if a == 0 and i == size[0] - 8:
                    img = 2
                if a > 0 and a < size[1] - 8 and i == 0:
                    img = 3
                if a > 0 and a < size[1] - 8 and i > 0 and i < size[0] - 8:
                    img = 4
                if a > 0 and a < size[1] - 8 and i == size[0] - 8:
                    img = 5
                if a == size[1] - 8 and i == 0:
                    img = 6
                if a == size[1] - 8 and i > 0 and i < size[0] - 8:
                    img = 7
                if a == size[1] - 8 and i == size[0] - 8:
                    img = 8

                surface.blit(self.panel_imgs[img], (i, a))

        return surface


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

    def __init__(self, resourcemanager, scene_speed=15):
        super(MenuScene, self).__init__(resourcemanager, scene_speed)
        self.menu = resourcemanager.get('menu')
        self.planet = resourcemanager.get('planet')
        self.title = resourcemanager.get('title')
        self.sun = resourcemanager.get('sun')
        self.plant = resourcemanager.get('plant')
        self.cursor = resourcemanager.get('cursor')
        self.music = resourcemanager.get('menu_song')
        self.__init_stars(resourcemanager)
        self.skip_text = self.font.get(i18n._('Press ESC to skip'), 256)
        self.text = self.font.get(i18n._('Press Return'), 256)
        self.intro_text = []
        self.intro_text.insert(0, self.font.get(i18n._('In a very near place...'), 164))
        self.intro_text.insert(1, self.font.get(i18n._('...a nuclear plant is going to blow!!!'), 164))
        self.menu_text = []
        self.menu_text_sel = []

        self.menu_text.insert(0, self.font.get(i18n._('Start'), 128))
        self.menu_text.insert(1, self.font.get(i18n._('Options'), 128))
        self.menu_text.insert(2, self.font.get(i18n._('Instructions'), 128))
        self.menu_text.insert(3, self.font.get(i18n._('Exit'), 128))

        self.menu_text_sel.insert(0, self.font_selected.get(i18n._('Start'), 128))
        self.menu_text_sel.insert(1, self.font_selected.get(i18n._('Options'), 128))
        self.menu_text_sel.insert(2, self.font_selected.get(i18n._('Instructions'), 128))
        self.menu_text_sel.insert(3, self.font_selected.get(i18n._('Exit'), 128))
        panel = Panel(resourcemanager)

        text_max_length = 0
        for t in self.menu_text:
            if t.get_width() > text_max_length:
                text_max_length = t.get_width()
        text_max_length += self.font.gl_width * 2
        panel_height = (len(self.menu_text) * 12) + 16
        self.panel = panel.get((text_max_length, panel_height))
        self.background = pygame.Surface((self.menu.get_width(), self.menu.get_height())).convert()
        self.background_x_position = 0
        self.title_anim = 0
        self.show_menu = False

    def run(self):
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(self.music)
            pygame.mixer.music.play(-1)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            self.title_anim = 12
            self.background_x_position = 196
            self.show_menu = True

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
            self.title_anim += 2
            if self.title_anim >= 12:
                self.title_anim = 12

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

        self.background.blit(self.planet, (325 - self.planet.get_width()/2, 0))
        self.background.blit(self.sun, (310, 84))
        self.background.blit(self.plant, (377, 125))

        if self.title_anim > 0:
            tmp_surface = pygame.Surface((self.title.get_width(), self.title_anim)).convert()
            tmp_surface.fill((0, 0, 0, 0))
            pygame.transform.scale(self.title, (self.title.get_width(), self.title_anim), tmp_surface)
            self.background.blit(tmp_surface, (325 - tmp_surface.get_width()/2, 22 - tmp_surface.get_height()/2))
            tmp_surface = None

        if self.show_menu:
            self.background.blit(self.panel, (325 - self.panel.get_width()/2, 70))
            y = 78

            for t in self.menu_text:
                self.background.blit(t, (282, y))
                y += 12

            self.background.blit(self.menu_text_sel[0], (282, 78))
            self.background.blit(self.cursor, (274, 78))

        scr.virt.blit(self.background, (0, 0), (self.background_x_position, 0,
                                                scr.WINDOW_SIZE[0],
                                                scr.WINDOW_SIZE[1]))
        if not self.show_menu:
            scr.virt.blit(self.skip_text, (128-self.skip_text.get_width()/2, 172))
        else:
            scr.virt.blit(self.text, (128-self.text.get_width()/2, 172))

        if self.background_x_position < 98:
            scr.virt.blit(self.intro_text[0], (128-self.intro_text[0].get_width()/2, 68))
        elif self.background_x_position >= 98 and self.background_x_position < 196:
            scr.virt.blit(self.intro_text[1], (128-self.intro_text[1].get_width()/2, 68))

    def __init_stars(self, resourcemanager):
        self.stars = []
        stars_imgs = ['star0', 'star1', 'star2',
                      'star3', 'star4', 'star5',
                      'star6', 'star7', 'star8',
                      'star9', 'star10', 'star11']

        self.star_sprites = []
        for s in xrange(0, len(stars_imgs)):
            self.star_sprites.insert(s, resourcemanager.get(stars_imgs[s]))

        for s in xrange(0, 300):
            self.stars.insert(s, Star(random.randint(0, self.menu.get_width()), random.randint(0, 145), random.randint(1, 4)))
