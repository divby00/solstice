#-*- coding: utf-8 -*-
import sys
import pygame as pg


class DisplayInfo(object):

    def __init__(self, depth=0, flags=0):
        super(DisplayInfo, self).__init__()
        self.info = pg.display.Info()
        self.resolution = (self.info.current_w, self.info.current_h)
        self.windowed = self.info.wm
        self.modes = pg.display.list_modes(depth, flags)


class Display(object):

    supported_aspect_ratios = [
        '1.6', '1.25', '1.33', '1.77'
    ]

    virtual = None
    width = 0
    height = 0
    aspect_ratio = 0

    screen = None
    screen_width = 0
    screen_height = 0
    screen_aspect_ratio = 0

    def __init__(self):
        super(Display, self).__init__()

    def set_mode(self):
        init_display_info = DisplayInfo()
        flags = 0

        # Can go in windowed mode, remove the frame decoration
        # to emulate fullscreen
        if init_display_info.windowed == 1:
            flags = pg.NOFRAME
        # Can't set windowed mode, have to go for a fullscreen mode
        else:
            flags = pg.FULLSCREEN

        display_info = DisplayInfo(flags=flags)
        mode_set = False

        if display_info.modes != -1:
            if display_info.resolution in display_info.modes:
                self.screen = pg.display.set_mode(display_info.resolution, flags)
                mode_set = True
        else:
            self.screen = pg.display.set_mode(display_info.resolution, flags)
            mode_set = True

        if not mode_set:
            sys.exit(1)

        # Make virtual screen
        screen_size = self.screen.get_size()
        self.screen_aspect_ratio = str(float(screen_size[0]) / screen_size[1])[:4]
        self.virtual = pg.Surface(self.__get_resolution_with_aspect_ratio(), pg.SRCALPHA)
        self.virtual.fill((0, 0, 0, 0))

        # Set some useful variables
        virtual_size = self.virtual.get_size()
        self.aspect_ratio = str(float(virtual_size[0]) / virtual_size[1])[:4]
        self.width = self.virtual.get_width()
        self.height = self.virtual.get_height()
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()

    def __get_resolution_with_aspect_ratio(self):
        resolutions = {
            '1.6': (1280, 800),
            '1.77': (1366, 768),
            '1.33': (1024, 768),
            '1.25': (1280, 1024)
        }
        resolution = resolutions.get(self.screen_aspect_ratio)

        if not resolution:
            return (1024, 768)
        else:
            return resolution

    def draw(self, srfc, (x, y)):
        self.virtual.blit(srfc, (x, y))

    def flip(self):

        if self.aspect_ratio == self.screen_aspect_ratio:
            pg.transform.scale(self.virtual, (self.screen_width, self.screen_height), self.screen)
        else:
            src = pg.Surface(self.screen.get_size(), pg.SRCALPHA)
            src.fill((0, 0, 0, 0))
            w = src.get_width()
            h = src.get_height()
            vw = self.virtual.get_width()
            vh = self.virtual.get_height()
            x = (w / 2) - (vw / 2)
            y = (h / 2) - (vh / 2)
            src.blit(self.virtual, (x, y))
            self.screen.blit(src, (0, 0))

        pg.display.flip()
