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

        self.screen_size = cfg.screen_size

        try:
            self.icon = pygame.image.load("solstice.png")
            pygame.display.set_icon(self.icon)
        except:
            self.icon = None
            print(_('Unable to find the file solstice.png needed for the loading screen.'))

        self.display = pygame.display.set_mode(self.screen_size,
                                               graphics_params)
        self.display_info = pygame.display.Info()
        self.virt = pygame.Surface(Screen.WINDOW_SIZE, 0).convert()
        pygame.display.set_caption(caption)
        pygame.mouse.set_visible(False)
        pygame.event.set_allowed([pygame.QUIT])

    def toggle_fullscreen(self, fullscreen):

        graphics_params = pygame.DOUBLEBUF

        if fullscreen:
            graphics_params |= pygame.FULLSCREEN

        self.display = pygame.display.set_mode(self.screen_size,
                                               graphics_params)
        self.display_info = pygame.display.Info()
        self.virt = pygame.Surface(Screen.WINDOW_SIZE, 0).convert()
        pygame.display.set_caption(self.caption)
        pygame.mouse.set_visible(False)
        pygame.event.set_allowed([pygame.QUIT])

    def change_resolution(self, resolution):

        graphics_params = pygame.DOUBLEBUF

        if fullscreen:
            graphics_params |= pygame.FULLSCREEN

        self.display = pygame.display.set_mode(self.screen_size,
                                               graphics_params)
        self.display_info = pygame.display.Info()
        self.virt = pygame.Surface(Screen.WINDOW_SIZE, 0).convert()
        pygame.display.set_caption(self.caption)
        pygame.mouse.set_visible(False)
        pygame.event.set_allowed([pygame.QUIT])
