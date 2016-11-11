from __future__ import division
import pygame
from gettext import gettext as _


class IconNotFoundError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value


class Screen(object):
    WINDOW_SIZE = [256, 192]

    def __init__(self, cfg, caption):
        graphics_params = pygame.DOUBLEBUF
        self.caption = caption

        if cfg.fullscreen:
            graphics_params |= pygame.FULLSCREEN
            self.fullscreen = True
        else:
            self.fullscreen = False

        self.screen_size = cfg.screen_size

        try:
            self.icon = pygame.image.load("solstice.png")
            pygame.display.set_icon(self.icon)
        except:
            self.icon = None
            print(_('Unable to find the file solstice.png needed for the loading screen.'))

        native_info = pygame.display.Info()
        self.native_w = native_info.current_w
        self.native_h = native_info.current_h
        self.design_w = self.screen_size[0]
        self.design_h = self.screen_size[1]
        self.scaling_resolution = None
        self.final_offset = None

        width_fits = self.check_width_fits_screen()
        if not width_fits:
            height_fits = self.check_height_fits_screen()
            if not height_fits:
                # TODO Throw exception here
                print('This should never happen')
                exit(-1)

        graphics_params = 0
        graphics_params = pygame.FULLSCREEN
        self.display = pygame.display.set_mode((self.native_w, self.native_h),
                                               graphics_params)
        self.display_info = pygame.display.Info()
        self.virt = pygame.Surface(Screen.WINDOW_SIZE, 0).convert()
        self.scaled_virt = pygame.Surface(self.scaling_resolution, 0).convert()
        pygame.display.set_caption(caption)
        pygame.mouse.set_visible(False)
        pygame.event.set_allowed([pygame.QUIT])

    def check_width_fits_screen(self):
        x = int((self.design_w * self.native_h) / self.design_h)
        if x <= self.native_w:
            self.scaling_resolution = x, self.native_h
            self.final_offset = self.get_horizontal_offset()
            return True

        return False

    def check_height_fits_screen(self):
        y = int((self.design_h * self.native_w) / self.design_w)
        if y <= self.native_h:
            self.scaling_resolution = self.native_w, y
            self.final_offset = self.get_vertical_offset()
            return True

        return False

    def get_horizontal_offset(self):
        return ((self.native_w - self.scaling_resolution[0]) / 2), 0

    def get_vertical_offset(self):
        return 0, ((self.native_h - self.scaling_resolution[1]) / 2)

    def toggle_fullscreen(self, fullscreen):

        self.fullscreen = False
        graphics_params = pygame.DOUBLEBUF

        if fullscreen:
            graphics_params |= pygame.FULLSCREEN
            self.fullscreen = True

        self.display = pygame.display.set_mode(self.screen_size,
                                               graphics_params)
        self.display_info = pygame.display.Info()
        self.virt = pygame.Surface(Screen.WINDOW_SIZE, 0).convert()
        pygame.display.set_caption(self.caption)
        pygame.mouse.set_visible(False)
        pygame.event.set_allowed([pygame.QUIT])

    def change_resolution(self, resolution_index):

        resolutions = [
            (256, 192),
            (512, 384),
            (1024, 768)
        ]

        self.screen_size = resolutions[resolution_index]
        graphics_params = pygame.DOUBLEBUF

        if self.fullscreen:
            graphics_params |= pygame.FULLSCREEN

        self.display = pygame.display.set_mode(self.screen_size,
                                               graphics_params)
        self.display_info = pygame.display.Info()
        self.virt = pygame.Surface(Screen.WINDOW_SIZE, 0).convert()
        pygame.display.set_caption(self.caption)
        pygame.mouse.set_visible(False)
        pygame.event.set_allowed([pygame.QUIT])
        return resolutions[resolution_index]
