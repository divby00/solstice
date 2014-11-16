import pygame
import control
from gettext import gettext as _


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


class MenuItem(object):

    def __init__(self, name, text, function, next_menu):
        self.name = name
        self.text = text
        self.function = function
        self.next_menu = next_menu


class Menu(object):

    def __init__(self, name, items, parent_menu_name=None):
        assert(items is not None)
        assert(len(items) > 0)
        self.name = name
        self.parent_menu_name = parent_menu_name
        self.items =items
        self.selected_option = 0
        self.panel = None

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class MenuGroup(object):

    def __init__(self, menu_list, first_menu, menu_context):
        assert(len(menu_list) > 0)
        self.menu_list = menu_list
        self.panel_imgs = menu_context[0]
        self.fonts = menu_context[1]
        self.sounds = menu_context[2]
        self.control = menu_context[3]
        self.visible = False
        self.accept = False
        self.cancel = False
        self.selected_menu = self.__get_menu(first_menu)
        self.previous_menu = None

        for m in self.menu_list:
            option_max_length = 0

            for o in m.items:
                if len(o.text) > option_max_length:
                    option_max_length = len(o.text)

            option_max_length *= self.fonts[0].gl_width
            option_max_length += self.fonts[0].gl_width * 3
            panel_height = (len(m.items) * self.fonts[0].gl_height) + (self.fonts[0].gl_height * 2)
            m.panel = Panel(self.panel_imgs, (option_max_length, panel_height))
            m.options_images = []
            m.sel_options_images = []

            for i in xrange(0, len(m.items)):
                m.options_images.insert(i, self.fonts[0].get(m.items[i].text, 256))
                m.sel_options_images.insert(i, self.fonts[1].get(m.items[i].text, 256))

    def run(self):

        self.accept = False
        self.cancel = False

        if self.visible:
            menu = self.selected_menu

            if self.control.on(control.Control.UP):
                menu.selected_option -= 1
                self.sounds[0].play()

                if menu.selected_option == -1:
                    menu.selected_option = len(menu.items)-1

            if self.control.on(control.Control.DOWN):
                menu.selected_option += 1
                self.sounds[0].play()

                if menu.selected_option == len(menu.items):
                    menu.selected_option = 0

            if self.control.on(control.Control.ACTION1):
                self.accept = True
                self.sounds[1].play()
                item = menu.items[menu.selected_option]

                if item.function is not None:
                    item.function()

                if item.next_menu is not None:
                    self.previous_menu = self.selected_menu
                    self.selected_menu = self.__get_menu(item.next_menu)

            if self.control.on(control.Control.ACTION2):
                self.sounds[2].play()
                parent = self.__get_menu(menu.parent_menu_name)

                if parent:
                    self.selected_menu = parent
                    self.previous_menu = self.__get_menu(parent.parent_menu_name)
                self.cancel = True

    def render(self, surface, position):
        menu = self.selected_menu
        pos = position[0] - menu.panel.surface.get_width()/2, position[1]
        surface.blit(menu.panel.surface, pos)

        y = 8
        for o in menu.options_images:
            surface.blit(o, (16 + pos[0], y + pos[1]))
            y += 8

        surface.blit(menu.sel_options_images[menu.selected_option], (16 + pos[0], (menu.selected_option * 8) + 8 + pos[1]))
        surface.blit(self.panel_imgs[9], (8 + pos[0], (menu.selected_option * 8) + 8 + pos[1]))

    def __get_menu(self, menu_name):
        for m in self.menu_list:
            if m.name == menu_name:
                return m
        return None
