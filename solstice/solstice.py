#!/usr/bin/env python
from __future__ import division

import gettext
import os
import platform
import sys
from gettext import gettext as _

'''
Everything works correctly with pygame_sdl2 except sound
import pygame_sdl2
pygame_sdl2.import_as_pygame()
'''
import pygame
import config as config
import control as control
import resource_manager as resource_manager
import scene_manager as scene_manager
import logo_scene as logo_scene
import elevator_scene as elevator_scene
import intro_scene as intro_scene
import game_scene as game_scene
import screen as screen
import sound_player as sound_player


class Solstice(object):
    def __init__(self):
        Solstice._platform_specific_init()
        self._config = config.Configuration()
        self._translations_init()
        self._pygame_init()
        self._screen = screen.Screen(self._config, _('Solstice'))
        self._control = control.Control(self)
        # TODO: Change data file name (don't use .zip extension)
        self._resource_manager = resource_manager.ResourceManager(self, 'data.zip')
        self._sound_player = sound_player.SoundPlayer(self)
        self._scenes = {
            'logo': logo_scene.LogoScene(self),
            'intro': intro_scene.IntroScene(self),
            'game': game_scene.GameScene(self),
            'elevator': elevator_scene.ElevatorScene(self)
        }
        '''
            'game_over': game_over_scene.GameOverScene(self),
        '''
        # The first parameter in this function call is the game 'context'
        self._scene_manager = scene_manager.SceneManager(self, 'game')

    '''
    Private methods
    '''

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

    @staticmethod
    def _platform_specific_init():
        if platform.system() == 'Windows':
            os.environ['SDL_AUDIODRIVER'] = 'dsound'

    '''
    Public methods
    '''

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
