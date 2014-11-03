import pygame


class Screen(object):

    WINDOW_SIZE = (256, 192)

    def __init__(self, cfg, caption):
        graphics_params = pygame.DOUBLEBUF

        if cfg.fullscreen:
            graphics_params |= pygame.FULLSCREEN

        self.screen_size = cfg.screen_size
        self.icon = pygame.image.load("solstice.png")
        pygame.display.set_icon(self.icon)
        self.display = pygame.display.set_mode(self.screen_size,
                                               graphics_params)
        self.display_info = pygame.display.Info()
        self.virt = pygame.Surface(Screen.WINDOW_SIZE, 0).convert()
        pygame.display.set_caption(caption)
        pygame.mouse.set_visible(False)
        pygame.event.set_allowed([pygame.QUIT])
