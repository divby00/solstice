import pygame

import control


class MenuItem(object):
    def __init__(self, name, text, function, next_menu):
        self._name = name
        self._text = text
        self._function = function
        self._next_menu = next_menu

    '''
    Public methods
    '''

    @property
    def text(self):
        return self._text

    @property
    def function(self):
        return self._function

    @property
    def next_menu(self):
        return self._next_menu


class Menu(object):
    def __init__(self, name, items, parent_menu_name=None):
        self._name = name
        self._parent_menu_name = parent_menu_name
        self._items = items
        self._selected_option = 0
        self._panel = None

    '''
    Private methods
    '''

    def __str__(self):
        return self._name

    def __repr__(self):
        return self._name

    '''
    Public methods
    '''

    @property
    def name(self):
        return self._name

    @property
    def items(self):
        return self._items

    @property
    def selected_option(self):
        return self._selected_option

    @selected_option.setter
    def selected_option(self, value):
        self._selected_option = value

    @property
    def parent_menu_name(self):
        return self._parent_menu_name


class Panel(object):
    def __init__(self, panel_sprites, size):
        self._panel_sprites = panel_sprites
        self._surface = pygame.Surface(size).convert_alpha()
        self._surface.fill((0, 0, 0, 0))
        img = -1

        for a in xrange(0, size[1], 8):
            for i in xrange(0, size[0], 8):
                if a == 0 and i == 0:
                    img = 0
                if a == 0 and 0 < i < size[0] - 8:
                    img = 1
                if a == 0 and i == size[0] - 8:
                    img = 2
                if size[1] - 8 > a > 0 == i:
                    img = 3
                if 0 < a < size[1] - 8 and 0 < i < size[0] - 8:
                    img = 4
                if 0 < a < size[1] - 8 and i == size[0] - 8:
                    img = 5
                if a == size[1] - 8 and i == 0:
                    img = 6
                if a == size[1] - 8 and 0 < i < size[0] - 8:
                    img = 7
                if a == size[1] - 8 and i == size[0] - 8:
                    img = 8

                self._surface.blit(self._panel_sprites[img], (i, a))

    '''
    Public methods
    '''

    @property
    def surface(self):
        return self._surface


class MenuGroup(object):
    def __init__(self, menu_list, first_menu, menu_context):
        self._menu_list = menu_list
        self._panel_sprites = menu_context[0]
        self._sound_player = menu_context[2]
        self._control = menu_context[3]
        self._visible = False
        self._accept = False
        self._cancel = False
        self._selected_menu = self._get_menu(first_menu)
        self._selected_option = 0
        self._previous_menu = None
        fonts = menu_context[1]

        for menu in self._menu_list:
            option_max_length = 0

            for o in menu.items:
                if len(o.text) > option_max_length:
                    option_max_length = len(o.text)

            option_max_length *= fonts[0].glyph_width
            option_max_length += fonts[0].glyph_width * 3
            panel_height = (len(menu.items) * fonts[0].glyph_height) + (fonts[0].glyph_height * 2)
            menu.panel = Panel(self._panel_sprites, (option_max_length, panel_height))
            menu.options_images = []
            menu.sel_options_images = []
            menu.prev_options_images = []

            for i in xrange(0, len(menu.items)):
                menu.options_images.insert(i, fonts[0].get(menu.items[i].text, 256))
                menu.sel_options_images.insert(i, fonts[1].get(menu.items[i].text, 256))
                menu.prev_options_images.insert(i, fonts[2].get(menu.items[i].text, 256))

    '''
    Private methods
    '''

    def _get_menu(self, menu_name):
        for menu in self._menu_list:
            if menu.name == menu_name:
                return menu
        return None

    '''
    Public methods
    '''

    def run(self):
        self._accept = False
        self._cancel = False

        if self._visible:
            menu = self._selected_menu

            if self._control.on(control.Control.UP):
                menu.selected_option -= 1
                self._sound_player.play_sample('blip')

                if menu.selected_option == -1:
                    menu.selected_option = len(menu.items) - 1

            if self._control.on(control.Control.DOWN):
                menu.selected_option += 1
                self._sound_player.play_sample('blip')

                if menu.selected_option == len(menu.items):
                    menu.selected_option = 0

            if self._control.on(control.Control.ACTION1):
                self._accept = True
                self._sound_player.play_sample('accept')
                item = menu.items[menu.selected_option]

                if item.function is not None:
                    item.function()

                if item.next_menu is not None:
                    self._previous_menu = self._selected_menu
                    self._selected_menu = self._get_menu(item.next_menu)
                    self._selected_option = self._selected_menu.selected_option
                else:
                    self._selected_option = self._selected_menu.selected_option

            if self._control.on(control.Control.ACTION2):
                self._sound_player.play_sample('cancel')
                parent = self._get_menu(menu.parent_menu_name)

                if parent:
                    self._selected_menu = parent
                    self._previous_menu = self._get_menu(parent.parent_menu_name)
                    self._selected_option = self._selected_menu.selected_option

                self._cancel = True

    def render(self, surface, position):
        menu = self._selected_menu
        calculated_position = position[0] - menu.panel.surface.get_width() / 2, position[1]
        surface.blit(menu.panel.surface, calculated_position)

        y = 8
        for option_image in menu.options_images:
            surface.blit(option_image, (16 + calculated_position[0], y + calculated_position[1]))
            y += 8

        pygame.draw.rect(surface, (0, 0, 0), (
            calculated_position[0] + 4, (menu.selected_option * 8) + 7 + calculated_position[1],
            menu.panel.surface.get_width() - 7, 9), 0)
        surface.blit(menu.options_images[menu.selected_option], (
            16 + calculated_position[0], (menu.selected_option * 8) + 8 + calculated_position[1]))
        surface.blit(menu.sel_options_images[self._selected_option], (
            16 + calculated_position[0], (self._selected_option * 8) + 8 + calculated_position[1]))
        surface.blit(self._panel_sprites[9], (
            8 + calculated_position[0], (menu.selected_option * 8) + 8 + calculated_position[1]))

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, value):
        self._visible = value

    @property
    def selected_menu(self):
        return self._selected_menu
