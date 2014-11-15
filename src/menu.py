import pygame
import control


class Panel(object):

    def __init__(self, panel_imgs, size):
        assert(size[0] > 0 and size[1] > 0)
        assert(panel_imgs is not None)
        self.panel_imgs = panel_imgs
        self.size = size
        self.surface = pygame.Surface(size).convert_alpha()
        self.surface.fill((0, 0, 0, 0))
        img = -1

        for a in xrange(0, self.size[1], 8):
            for i in xrange(0, self.size[0], 8):
                if a == 0 and i == 0:
                    img = 0
                if a == 0 and i > 0 and i < self.size[0] - 8:
                    img = 1
                if a == 0 and i == self.size[0] - 8:
                    img = 2
                if a > 0 and a < self.size[1] - 8 and i == 0:
                    img = 3
                if a > 0 and a < self.size[1] - 8 and i > 0 and i < self.size[0] - 8:
                    img = 4
                if a > 0 and a < self.size[1] - 8 and i == self.size[0] - 8:
                    img = 5
                if a == self.size[1] - 8 and i == 0:
                    img = 6
                if a == self.size[1] - 8 and i > 0 and i < self.size[0] - 8:
                    img = 7
                if a == self.size[1] - 8 and i == self.size[0] - 8:
                    img = 8

                self.surface.blit(self.panel_imgs[img], (i, a))


class Menu(object):

    def __init__(self, name, options, parent_menu=None):
        assert(options is not None)
        assert(len(options) > 0)
        self.name = name
        self.parent_menu = parent_menu
        self.options = options
        self.selected_option = 0
        self.panel = None


class MenuGroup(object):

    def __init__(self, menu_list, menu_context):
        assert(len(menu_list) > 0)
        self.menu_list = menu_list
        self.panel_imgs = menu_context[0]
        self.fonts = menu_context[1]
        self.sounds = menu_context[2]
        self.control = menu_context[3]
        self.visible = False
        self.accept = False
        self.cancel = False
        self.selected_menu = 0

        for m in self.menu_list:
            option_max_length = 0

            for o in m.options:
                if len(o) > option_max_length:
                    option_max_length = len(o)

            option_max_length *= self.fonts[0].gl_width
            option_max_length += self.fonts[0].gl_width * 3
            panel_height = (len(m.options) * self.fonts[0].gl_height) + (self.fonts[0].gl_height * 2)
            m.panel = Panel(self.panel_imgs, (option_max_length, panel_height))
            m.options_images = []
            m.sel_options_images = []

            for i in xrange(0, len(m.options)):
                m.options_images.insert(i, self.fonts[0].get(m.options[i], 256))
                m.sel_options_images.insert(i, self.fonts[1].get(m.options[i], 256))

    def run(self):

        self.accept = False
        self.cancel = False

        if self.visible:

            if self.control.on(control.Control.UP):
                menu = self.menu_list[self.selected_menu]
                menu.selected_option -= 1

                if menu.selected_option == -1:
                    menu.selected_option = len(menu.options)-1

            if self.control.on(control.Control.DOWN):
                menu = self.menu_list[self.selected_menu]
                menu.selected_option += 1

                if menu.selected_option == len(menu.options):
                    menu.selected_option = 0

            if self.control.on(control.Control.ACTION1):
                self.accept = True

            if self.control.on(control.Control.ACTION2):
                if self.selected_menu > 0:
                    self.selected_menu-=1
                self.cancel = True

    def render(self, surface, position):
        menu = self.menu_list[self.selected_menu]
        pos = position[0] - menu.panel.surface.get_width()/2, position[1]
        surface.blit(menu.panel.surface, pos)

        y = 8
        for o in menu.options_images:
            surface.blit(o, (16 + pos[0], y + pos[1]))
            y += 8

        surface.blit(menu.sel_options_images[menu.selected_option], (16 + pos[0], (menu.selected_option * 8) + 8 + pos[1]))
        surface.blit(self.panel_imgs[9], (8 + pos[0], (menu.selected_option * 8) + 8 + pos[1]))
