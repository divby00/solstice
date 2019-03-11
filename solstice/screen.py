from __future__ import division

import pygame
from gettext import gettext as _
from config import Entries, DefaultValues


class IconNotFoundError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value


class Screen(object):
    WINDOW_SIZE = [256, 192]

    def __init__(self, configuration, caption):
        self._configuration = configuration
        self._caption = caption
        self._icon = None
        self._full_screen = None
        self._screen_size = self._configuration.screen_size
        self._last_resize_size = self._screen_size
        native_info = pygame.display.Info()
        self._native_w = native_info.current_w
        self._native_h = native_info.current_h
        self._design_w = Screen.WINDOW_SIZE[0]
        self._design_h = Screen.WINDOW_SIZE[1]
        self._scaling_resolution = None
        self._final_offset = None

        width_fits = self._check_width_fits_screen()
        if not width_fits:
            height_fits = self._check_height_fits_screen()
            if not height_fits:
                # TODO Throw exception here
                print('This should never happen')
                exit(-1)

        graphic_parameters = self._get_graphics_parameters()
        self._set_icon()

        if self._full_screen:
            self._display = pygame.display.set_mode((self._native_w, self._native_h), graphic_parameters)
        else:
            self._final_offset = 0, 0
            self._scaling_resolution = self._screen_size
            self._display = pygame.display.set_mode((self._screen_size[0], self._screen_size[1]), graphic_parameters)
        self._virtual_screen = pygame.Surface(Screen.WINDOW_SIZE, 0).convert()
        self._scaled_virtual = pygame.Surface(self._scaling_resolution, 0).convert()
        pygame.display.set_caption(self._caption)
        pygame.mouse.set_visible(False)
        pygame.event.set_allowed([pygame.QUIT])

    def _set_icon(self):
        try:
            self._icon = pygame.image.load("solstice.png")
            pygame.display.set_icon(self._icon)
        except Exception:
            self._icon = None
            print(_('Unable to find the file solstice.png needed for the loading screen.'))

    def _get_graphics_parameters(self):
        graphics_params = pygame.DOUBLEBUF
        if self._configuration.full_screen:
            graphics_params |= pygame.FULLSCREEN
            self._full_screen = True
        else:
            graphics_params |= pygame.RESIZABLE
            self._full_screen = False
        return graphics_params

    def _check_width_fits_screen(self):
        x = int((self._design_w * self._native_h) / self._design_h)
        if x <= self._native_w:
            self._scaling_resolution = x, self._native_h
            self._final_offset = self._get_horizontal_offset()
            return True
        return False

    def _check_height_fits_screen(self):
        y = int((self._design_h * self._native_w) / self._design_w)
        if y <= self._native_h:
            self._scaling_resolution = self._native_w, y
            self._final_offset = self._get_vertical_offset()
            return True
        return False

    def _get_horizontal_offset(self):
        return ((self._native_w - self._scaling_resolution[0]) / 2), 0

    def _get_vertical_offset(self):
        return 0, ((self._native_h - self._scaling_resolution[1]) / 2)

    def toggle_fullscreen(self, full_screen):
        self._full_screen = full_screen
        if self._full_screen:
            graphics_params = pygame.DOUBLEBUF | pygame.FULLSCREEN
            self._scaling_resolution = None
            self._final_offset = None
            self._last_resize_size = self._screen_size

            width_fits = self._check_width_fits_screen()
            if not width_fits:
                height_fits = self._check_height_fits_screen()
                if not height_fits:
                    # TODO Throw exception here
                    print('This should never happen')
                    exit(-1)

            self._display = pygame.display.set_mode((self._native_w, self._native_h), graphics_params)
            self._virtual_screen = pygame.Surface(Screen.WINDOW_SIZE, 0).convert()
            self._scaled_virtual = pygame.Surface(self._scaling_resolution, 0).convert()
        else:
            graphics_params = pygame.DOUBLEBUF
            self._final_offset = 0, 0
            self._scaling_resolution = self._last_resize_size
            self._display = pygame.display.set_mode((self._last_resize_size[0], self._last_resize_size[1]), graphics_params)
            self._virtual_screen = pygame.Surface(Screen.WINDOW_SIZE, 0).convert()
            self._scaled_virtual = pygame.Surface(self._scaling_resolution, 0).convert()
            pygame.display.set_caption(self._caption)
            pygame.mouse.set_visible(False)
            pygame.event.set_allowed([pygame.QUIT])
            self._configuration.parser.set(DefaultValues.SECTION.value[1], Entries.SCREEN_WIDTH.value,
                                           self._scaling_resolution[0])
            self._configuration.parser.set(DefaultValues.SECTION.value[1], Entries.SCREEN_HEIGHT.value,
                                           self._scaling_resolution[1])

    def resize_window(self, resize_event):
        graphics_params = pygame.DOUBLEBUF | pygame.RESIZABLE
        self._final_offset = 0, 0
        self._screen_size = resize_event.size
        self._last_resize_size = self._screen_size
        self._scaling_resolution = self._screen_size
        self._display = pygame.display.set_mode((self._screen_size[0], self._screen_size[1]),
                                                graphics_params)
        self._virtual_screen = pygame.Surface(Screen.WINDOW_SIZE, 0).convert()
        self._scaled_virtual = pygame.Surface(self._scaling_resolution, 0).convert()
        pygame.mouse.set_visible(False)
        pygame.event.set_allowed([pygame.QUIT])

    @property
    def virtual_screen(self):
        return self._virtual_screen

    @property
    def icon(self):
        return self._icon

    @property
    def scaling_resolution(self):
        return self._scaling_resolution

    @property
    def scaled_virtual(self):
        return self._scaled_virtual

    @property
    def display(self):
        return self._display

    @property
    def final_offset(self):
        return self._final_offset
