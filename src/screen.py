import pygame


class Screen(object):

    WINDOW_SIZE = (256, 192)

    def __init__(self, screen_size, cfg, caption):
        graphics_params = pygame.DOUBLEBUF

        if cfg.fullscreen:
            graphics_params |= pygame.FULLSCREEN

        self.screen_size = screen_size
        self.display = pygame.display.set_mode(screen_size, graphics_params)
        self.display_info = pygame.display.Info()
        self.virt = pygame.Surface(Screen.WINDOW_SIZE, 0)
        pygame.display.set_caption(caption)
        pygame.mouse.set_visible(False)
        pygame.event.set_allowed([pygame.QUIT])
