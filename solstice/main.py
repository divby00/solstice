#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division

import gettext
import os
import platform
import sys
from gettext import gettext as _

import pygame

from config import Configuration
from control import Control
from elevator_scene import ElevatorScene
from game_scene import GameScene
from intro_scene import IntroScene
from logo_scene import LogoScene
from resource_manager import ResourceManager
from scene_manager import SceneManager
from screen import Screen
from sound_player import SoundPlayer


class Solstice(object):

    @staticmethod
    def _platform_specific_init():
        if platform.system() == 'Windows':
            os.environ['SDL_AUDIODRIVER'] = 'dsound'

    def __init__(self):
        Solstice._platform_specific_init()
        self._config = Configuration()
        self._translations_init()
        self._pygame_init()
        self._screen = Screen(self._config, _('Solstice'))
        self._control = Control(self)
        # TODO: Change data file name (don't use .zip extension)
        self._resource_manager = ResourceManager(self, 'data.zip')
        self._sound_player = SoundPlayer(self)
        self._scenes = {
            'logo': LogoScene(self),
            'intro': IntroScene(self),
            'game': GameScene(self),
            'elevator': ElevatorScene(self)
        }
        # The first parameter is the game 'context'
        self._scene_manager = SceneManager(self, 'logo')

    def _translations_init(self):
        gettext.bindtextdomain('solstice', self._config.locale_path)
        gettext.textdomain('solstice')

    def _sound_preinit(self):
        if self._config.sound or self._config.music:
            pygame.mixer.pre_init(22050, -16, 2, 1024)

    def _pygame_init(self):
        self._sound_preinit()
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()

    def run(self):
        self._scene_manager.run()

    def exit(self, exit_code):
        self._config.save()
        pygame.quit()
        sys.exit(exit_code)

    @property
    def config(self):
        return self._config

    @property
    def screen(self):
        return self._screen

    @property
    def resource_manager(self):
        return self._resource_manager

    @property
    def control(self):
        return self._control

    @property
    def sound_player(self):
        return self._sound_player

    @property
    def scenes(self):
        return self._scenes

    @property
    def scene_manager(self):
        return self._scene_manager


# Entry point
def main():
    solstice = Solstice()
    solstice.run()
    solstice.exit(0)


if __name__ == '__main__':
    main()
