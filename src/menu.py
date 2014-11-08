import pygame


class Panel(object):

    def __init__(self, panel_imgs, size):
        assert(size[0] > 0 and size[1] > 0)
        assert(panel_imgs is not None)
        self.panel_imgs = panel_imgs
        self.size = size
        self.surface = pygame.Surface(size).convert_alpha()


class Menu(object):

    def __init__(self, panel_imgs, fonts, options, default_option=0, parent_menu=None):
        assert(options is not None)
        assert(len(options) > 0)
        self.options = options
        self.panel_imgs = panel_imgs
        self.selected_option = default_option
        option_max_length = 0

        for o in self.options:
            if len(o) > option_max_length:
                option_max_length = len(o)

        option_max_length *= fonts[0].gl_width
        option_max_length += fonts[0].gl_width * 3
        panel_height = (len(self.options) * fonts[0].gl_height) + (fonts[0].gl_height * 2)
        self.panel = Panel(panel_imgs, (option_max_length, panel_height))
        self.options_images = []
        self.sel_options_images = []

        for i in xrange(0, len(self.options)):
            self.options_images.insert(i, fonts[0].get(self.options[i], 256))
            self.sel_options_images.insert(i, fonts[1].get(self.options[i], 256))

    def render(self, surface, position):
        assert(position[0] > 0 and position[1] > 0)

        self.panel.surface.fill((0, 0, 0, 0))
        img = -1

        for a in xrange(0, self.panel.size[1], 8):
            for i in xrange(0, self.panel.size[0], 8):
                if a == 0 and i == 0:
                    img = 0
                if a == 0 and i > 0 and i < self.panel.size[0] - 8:
                    img = 1
                if a == 0 and i == self.panel.size[0] - 8:
                    img = 2
                if a > 0 and a < self.panel.size[1] - 8 and i == 0:
                    img = 3
                if a > 0 and a < self.panel.size[1] - 8 and i > 0 and i < self.panel.size[0] - 8:
                    img = 4
                if a > 0 and a < self.panel.size[1] - 8 and i == self.panel.size[0] - 8:
                    img = 5
                if a == self.panel.size[1] - 8 and i == 0:
                    img = 6
                if a == self.panel.size[1] - 8 and i > 0 and i < self.panel.size[0] - 8:
                    img = 7
                if a == self.panel.size[1] - 8 and i == self.panel.size[0] - 8:
                    img = 8

                self.panel.surface.blit(self.panel_imgs[img], (i, a))

        y = 8

        for o in self.options_images:
            self.panel.surface.blit(o, (16, y))
            y += 8

        self.panel.surface.blit(self.sel_options_images[self.selected_option], (16, (self.selected_option * 8) + 8))
        self.panel.surface.blit(self.panel_imgs[9], (8, (self.selected_option * 8) + 8))
        surface.blit(self.panel.surface, position)
