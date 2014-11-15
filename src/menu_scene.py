import math
import random
import pygame
import scene
import menu
import screen
import control
from gettext import gettext as _


class Star(object):

    def __init__(self, x, y, star_type):
        self.x = x
        self.y = y
        self.star_type = star_type
        self.frame_incrementor = random.triangular()

        if self.star_type in [0, 1, 3, 4]:
            self.frame = random.randint(0, 2)
            self.maxframe = 2
        else:
            self.frame = random.randint(0, 4)
            self.maxframe = 4


class Stars(object):

    def __init__(self, resourcemanager, position, amount=200):
        self.stars = []
        stars_imgs = ['star0', 'star1', 'star2',
                      'star3', 'star4', 'star5',
                      'star6', 'star7', 'star8',
                      'star9', 'star10', 'star11']

        self.star_sprites = []
        for s in xrange(0, len(stars_imgs)):
            self.star_sprites.insert(s, resourcemanager.get(stars_imgs[s]))

        for s in xrange(0, amount):
            x = random.randint(0, position[0])
            y = random.randint(0, position[1])
            self.stars.insert(s, Star(x, y, random.randint(0, 5)))

    def run(self):
        for s in self.stars:
            s.frame += s.frame_incrementor

            if s.star_type == 0:
                if s.frame >= 2:
                    s.frame = 0
            if s.star_type == 1:
                if s.frame >= 2:
                    s.frame = 0
            if s.star_type == 2:
                if s.frame >= 4:
                    s.frame = 0
            if s.star_type == 3:
                if s.frame >= 2:
                    s.frame = 0
            if s.star_type == 4:
                if s.frame >= 2:
                    s.frame = 0

    def render(self, surface):
        for s in self.stars:
            img = None
            if s.star_type == 0:
                img = self.star_sprites[int(0 + s.frame)]
            if s.star_type == 1:
                img = self.star_sprites[int(2 + s.frame)]
            if s.star_type == 2:
                img = self.star_sprites[int(4 + s.frame)]
            if s.star_type == 3:
                img = self.star_sprites[int(8 + s.frame)]
            if s.star_type == 4:
                img = self.star_sprites[int(10 + s.frame)]
            if img is not None:
                surface.blit(img, (s.x, s.y))


class Credits(object):

    def __init__(self, font, font_dither):
        self.credits_text = [
            _('2015 Love4Retro Games'),
            _('Solstice is an Equinox remake'),
            _('Program and graphics by:'),
            _('Jesus Chicharro'),
            _('Music by:'),
            _('Daniel Galan'),
            _('This is Free Software'),
            _('Hope you enjoy this game...'),
            _('...and long life to EGA!!!')
        ]
        self.actual_text = 0
        self.credits_anim = 0
        self.text_y = screen.Screen.WINDOW_SIZE[1]
        self.credits_imgs = []
        self.font_dither = font_dither

        for i in xrange(0, len(self.credits_text)):
            self.credits_imgs.insert(i, font.get(self.credits_text[i],
                                                 screen.Screen.WINDOW_SIZE[0]))

    def run(self):
        if self.credits_anim >= 100:
            self.actual_text += 1
            self.text_y = screen.Screen.WINDOW_SIZE[1]
            self.credits_anim = 0

            if self.actual_text == len(self.credits_text):
                self.actual_text = 0

        if self.credits_anim < 16:
            self.text_y -= 1

        if self.credits_anim > 84:
            self.text_y -= 1

        self.credits_anim += 1

    def render(self, surface):
        surface.blit(self.credits_imgs[self.actual_text],
                     (325 - self.credits_imgs[self.actual_text].get_width()/2,
                      self.text_y))

        for i in xrange(196, 196 + screen.Screen.WINDOW_SIZE[0], 8):
            surface.blit(self.font_dither,
                         (i, screen.Screen.WINDOW_SIZE[1] -
                          self.font_dither.get_height()))


class MenuScene(scene.Scene):

    def __init__(self, context, scene_speed=15):
        super(MenuScene, self).__init__(context, scene_speed)
        self.exit = context.exit
        self.menu = context.resourcemanager.get('menu')
        self.planet = context.resourcemanager.get('planet')
        title = ['title0', 'title1', 'title2', 'title3', 'title4']
        self.title_imgs = []

        for i in xrange(0, len(title)):
            self.title_imgs.insert(i, context.resourcemanager.get(title[i]))

        self.sun = context.resourcemanager.get('sun')
        self.plant = context.resourcemanager.get('plant')
        self.font_dither = context.resourcemanager.get('font_dither')
        self.music = context.resourcemanager.get('menu_song')
        self.stars = Stars(context.resourcemanager,
                           (self.menu.get_width(), 145))
        self.skip_text = self.font.get(_('Press action 2 to skip'), 256)
        self.intro_text = []
        self.intro_text.insert(
            0, self.font.get(_('In a very near place...'), 256))
        self.intro_text.insert(
            1, self.font.get(_('...a nuclear plant is going to blow!!!'), 256))
        self.credits = Credits(self.font, self.font_dither)
        self.background = pygame.Surface(
            (self.menu.get_width(), self.menu.get_height())).convert()
        self.background_x_position = 0
        self.title_anim = 0
        self.title_fade = -1
        self.show_menu = False
        fonts = (self.font, self.font_selected)
        menu_main_options = [_('start'), _('options'), _('instructions'), _('exit')]
        menu_options_options = [_('graphics'), _('sound'), _('control')]
        menu_graphics_options = [_('resolution'), _('fullscreen')]
        menu_resolution_options = [_('256x192'), _('512x384'), _('1024x768')]
        menu_fullscreen_options = [_('on'), _('off')]
        menu_sound_options = [_('sound effects'), _('sound effects volume'),
                              _('music'), _('music volume')]
        menu_effects_options = [_('on'), _('off')]
        menu_effects_vol_options = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        menu_music_options = [_('on'), _('off')]
        menu_music_vol_options = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        main_menu = menu.Menu('main', menu_main_options)
        options_menu = menu.Menu('options', menu_options_options, main_menu)
        graphics_menu = menu.Menu('graphics', menu_graphics_options, options_menu)
        sounds_menu = menu.Menu('sounds', menu_sound_options, options_menu)
        menu_list = [main_menu, options_menu, graphics_menu, sounds_menu]
        self.menu_group = menu.MenuGroup(menu_list, self.menu_context)

    def run(self):
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(self.music)
            pygame.mixer.music.play(-1)

        self.menu_group.run()

        if self.control.on(control.Control.ACTION2):
            self.title_anim = 12
            self.background_x_position = 196

            if not self.menu_group.visible:
                self.credits.credits_anim = 0
                self.credits.text_y = screen.Screen.WINDOW_SIZE[1]
                self.credits.actual_text = 0
                self.menu_group.visible = True

        if self.menu_group.visible:
            if self.menu_group.accept:

                menu = self.menu_group.menu_list[self.menu_group.selected_menu]

                if menu.name == 'main':
                    if menu.selected_option == 0:
                        pygame.mixer.music.stop()
                        self.running = False

                    if menu.selected_option == 1:
                        self.menu_group.selected_menu = 1

                    if menu.selected_option == 3:
                        pygame.time.delay(1000)
                        self.exit(0)

                if menu.name == 'options':
                    if menu.selected_option == 0:
                        self.menu_group.selected_menu = 2
                    if menu.selected_option == 1:
                        self.menu_group.selected_menu = 3


        self.stars.run()

        if self.menu_group.visible:
            self.credits.run()

        # 196 is the sun position in the menu background image
        if self.background_x_position < 196:
            self.background_x_position += 2
        else:
            self.title_anim += 2
            if self.title_anim >= 12:
                self.title_anim = 12

                if self.title_fade == -1:
                    self.title_fade = 0

            if self.title_anim == 12 and self.title_fade > -1:
                self.title_fade += 1

                if self.title_fade >= 4:
                    self.title_fade = 4

    def render(self, scr):

        self.background.blit(self.menu, (0, 0))
        self.stars.render(self.background)
        self.background.blit(self.planet, (325 - self.planet.get_width()/2, 0))
        self.background.blit(self.sun, (310, 84))
        self.background.blit(self.plant, (377, 125))

        if self.title_anim > 0 and self.title_anim < 12:
            tmp_surface = pygame.Surface((self.title_imgs[0].get_width(),
                                         self.title_anim)).convert()
            tmp_surface.fill((0, 0, 0, 0))
            pygame.transform.scale(self.title_imgs[0],
                                   (self.title_imgs[0].get_width(),
                                    self.title_anim),
                                   tmp_surface)
            self.background.blit(tmp_surface,
                                 (325 - tmp_surface.get_width()/2,
                                  22 - tmp_surface.get_height()/2))
            tmp_surface = None

        if self.title_anim == 12:
            self.background.blit(
                self.title_imgs[self.title_fade],
                (325 - self.title_imgs[self.title_fade].get_width()/2,
                 22 - self.title_imgs[self.title_fade].get_height()/2))

        if self.menu_group.visible:
            self.menu_group.render(self.background, (325, 70))
            self.credits.render(self.background)

        scr.virt.blit(self.background, (0, 0), (self.background_x_position, 0,
                                                scr.WINDOW_SIZE[0],
                                                scr.WINDOW_SIZE[1]))
        if not self.menu_group.visible:
            scr.virt.blit(self.skip_text,
                         (128 - self.skip_text.get_width()/2, 176))
        if self.background_x_position < 98:
            scr.virt.blit(self.intro_text[0],
                         (128-self.intro_text[0].get_width()/2, 68))
        elif self.background_x_position in list(xrange(98, 196)):
            scr.virt.blit(self.intro_text[1],
                         (128-self.intro_text[1].get_width()/2, 68))
