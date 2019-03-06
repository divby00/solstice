import pygame
import random
from gettext import gettext as _

import control
import particles
import particles_manager
import scene
import screen


class Star(object):
    def __init__(self, x, y, star_type):
        self._x = x
        self._y = y
        self._star_type = star_type
        self._frame = 0
        self._frame_incrementer = random.triangular()
        if self._star_type in [0, 1, 3, 4]:
            self._frame = random.randint(0, 2)
            self._max_frame = 2
        else:
            self._frame = random.randint(0, 4)
            self._max_frame = 4

    '''
    Public methods
    '''

    @property
    def star_type(self):
        return self._star_type

    @property
    def frame_incrementer(self):
        return self._frame_incrementer

    @property
    def frame(self):
        return self._frame

    @frame.setter
    def frame(self, value):
        self._frame = value

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y


class Stars(object):
    def __init__(self, resource_manager, position, amount=200):
        self._star_sprites = [resource_manager.get('star' + str(index)) for index in xrange(0, 12)]
        self._stars = [Star(random.randint(0, position[0]), random.randint(0, position[1]),
                            random.randint(0, 5)) for i in xrange(amount)]

    '''
    Public methods
    '''

    def run(self):
        for star in self._stars:
            star.frame += star.frame_incrementer

            if star.star_type == 0:
                if star.frame >= 2:
                    star.frame = 0
            if star.star_type == 1:
                if star.frame >= 2:
                    star.frame = 0
            if star.star_type == 2:
                if star.frame >= 4:
                    star.frame = 0
            if star.star_type == 3:
                if star.frame >= 2:
                    star.frame = 0
            if star.star_type == 4:
                if star.frame >= 2:
                    star.frame = 0

    def render(self, surface):
        for star in self._stars:
            img = None
            if star.star_type == 0:
                img = self._star_sprites[int(0 + star.frame)]
            if star.star_type == 1:
                img = self._star_sprites[int(2 + star.frame)]
            if star.star_type == 2:
                img = self._star_sprites[int(4 + star.frame)]
            if star.star_type == 3:
                img = self._star_sprites[int(8 + star.frame)]
            if star.star_type == 4:
                img = self._star_sprites[int(10)]
            if img is not None:
                surface.blit(img, (star.x, star.y))


class Credits(object):
    def __init__(self, font, font_dither):
        self._credits_text = [
            _('2019 Love4Retro Games'),
            _('Solstice is an Equinox remake'),
            _('Program and graphics by:'),
            _('Jesus Chicharro'),
            _('Music by:'),
            _('Juhani Junkala'),
            _('This is Free Software'),
            _('We hope you enjoy it!'),
            _('Thank you Raffaele Cecco!'),
        ]
        self._font_dither = font_dither
        self._credits_sprites = [font.get(text, screen.Screen.WINDOW_SIZE[0])
                                 for text in self._credits_text]
        self._actual_text = 0
        self._credits_frame = 0
        self._y = 0

    '''
    Public methods
    '''

    def on_start(self):
        self._actual_text = 0
        self._credits_frame = 0
        self._y = screen.Screen.WINDOW_SIZE[1]

    def run(self):
        if self._credits_frame >= 100:
            self._actual_text += 1
            self._y = screen.Screen.WINDOW_SIZE[1]
            self._credits_frame = 0

            if self._actual_text == len(self._credits_text):
                self._actual_text = 0

        if self._credits_frame < 16:
            self._y -= 1

        if self._credits_frame > 84:
            self._y -= 1

        self._credits_frame += 1

    def render(self, surface):
        surface.blit(self._credits_sprites[self._actual_text],
                     (325 - self._credits_sprites[self._actual_text].get_width() / 2, self._y))

        for i in xrange(196, 196 + screen.Screen.WINDOW_SIZE[0], 8):
            surface.blit(self._font_dither,
                         (i, screen.Screen.WINDOW_SIZE[1] - self._font_dither.get_height()))


class IntroScene(scene.Scene):
    def __init__(self, context, name='intro', scene_speed=15):
        super(IntroScene, self).__init__(context, name, scene_speed)
        self._exit = context.exit
        self._screen = context.screen
        self._config = context.config
        self._sound_player = context.sound_player
        self._menu_image = context.resource_manager.get('menu')
        self._planet = context.resource_manager.get('planet')
        self._title_sprites = [context.resource_manager.get('title' + str(index)) for index in
                               xrange(0, 5)]
        self._sun = context.resource_manager.get('sun')
        self._plant = context.resource_manager.get('plant')
        self._font_dither = context.resource_manager.get('font_dither')
        self._sound_player.load_music('title')
        self._stars = Stars(context.resource_manager, (self._menu_image.get_width(), 145))
        self._skip_text = self._font_white.get(_('Press start to skip'), 256)
        self._intro_text = []
        self._intro_text.insert(0, self._font_white.get(_('In the near future...'), 256))
        self._intro_text.insert(1, self._font_white.get(_("...the world's most powerful nuclear plant is going to blow!!!"),
                                                        256))
        self._credits = Credits(self._font_blue, self._font_dither)
        self._background = pygame.Surface(
            (self._menu_image.get_width(), self._menu_image.get_height())).convert()
        self.get_menu()
        self._particles_manager = particles_manager.ParticlesManager()
        smoke = particles.SmokeParticles(context.resource_manager, 'smoke')
        self._particles_manager.register_particles(smoke)
        self._background_x_position = 0
        self._title_frame = 0
        self._title_fade = -1

    def _run_control_start(self):
        self._title_frame = 12
        self._background_x_position = 196

        if not self._menu_group.visible:
            self._credits._credits_frame = 0
            self._credits.text_y = screen.Screen.WINDOW_SIZE[1]
            self._credits.actual_text = 0
            self._menu_group.visible = True

    def _run_background_animation(self):
        # 196 is the sun position in the menu background image
        if self._background_x_position < 196:
            self._background_x_position += 2
        else:
            self._title_frame += 2
            if self._title_frame >= 12:
                self._title_frame = 12

                if self._title_fade == -1:
                    self._title_fade = 0

            if self._title_frame == 12 and self._title_fade > -1:
                self._title_fade += 1

                if self._title_fade >= 4:
                    self._title_fade = 4

    '''
    Public methods
    '''

    def on_start(self):
        self._background_x_position = 0
        self._title_frame = 0
        self._title_fade = -1
        self._credits.on_start()
        self._menu_group.visible = False
        self._sound_player.play_music()
        self._control.event_driven = True

    def on_quit(self):
        self._sound_player.stop_music()

    def run(self):
        self._menu_group.run()
        self._control.keyboard_event = self._keyboard_event

        if self._control.on(control.Control.START):
            self._run_control_start()

        self._stars.run()

        if self._menu_group.visible:
            self._credits.run()

        self._particles_manager.run()
        self._run_background_animation()

    def render(self, display):
        self._background.blit(self._menu_image, (0, 0))
        self._stars.render(self._background)
        self._background.blit(self._planet, (325 - self._planet.get_width() / 2, 0))
        self._background.blit(self._sun, (310, 84))
        self._particles_manager.render(self._background)
        self._background.blit(self._plant, (377, 125))

        if 0 < self._title_frame < 12:
            tmp_surface = pygame.Surface((self._title_sprites[0].get_width(),
                                          self._title_frame)).convert_alpha()
            tmp_surface.fill((0, 0, 0, 0))
            pygame.transform.scale(self._title_sprites[0],
                                   (self._title_sprites[0].get_width(), self._title_frame),
                                   tmp_surface)
            self._background.blit(tmp_surface,
                                  (325 - tmp_surface.get_width() / 2,
                                   22 - tmp_surface.get_height() / 2))

        if self._title_frame == 12:
            self._background.blit(self._title_sprites[self._title_fade],
                                  (325 - self._title_sprites[self._title_fade].get_width() / 2,
                                   22 - self._title_sprites[self._title_fade].get_height() / 2))

        if self._menu_group.visible:
            self._menu_group.render(self._background, (325, 70))
            self._credits.render(self._background)

        display.virt.blit(self._background, (0, 0),
                          (self._background_x_position, 0, display.WINDOW_SIZE[0],
                           display.WINDOW_SIZE[1]))

        if self._background_x_position < 98:
            display.virt.blit(self._intro_text[0], (128 - self._intro_text[0].get_width() / 2, 68))
        elif self._background_x_position in list(xrange(98, 196)):
            display.virt.blit(self._intro_text[1], (128 - self._intro_text[1].get_width() / 2, 68))
        if not self._menu_group.visible:
            display.virt.blit(self._skip_text, (128 - self._skip_text.get_width() / 2, 176))
