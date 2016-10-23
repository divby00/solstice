#!/usr/bin/env python
from __future__ import division
import gettext
from gettext import gettext as _
import os
import platform
import sys
'''
Everything works correctly with pygame_sdl2 except sound
import pygame_sdl2
pygame_sdl2.import_as_pygame()
'''
import pygame
import config
import control
import resource_manager
import scene_manager
import logo_scene
import intro_scene
import game_scene
import game_over_scene
import screen
import sound_player


class Solstice(object):
    def __init__(self):
        self.__platform_specific_inits()
        self.cfg = config.Configuration()
        gettext.bindtextdomain('solstice', self.cfg.locale_path)
        gettext.textdomain('solstice')

        '''
        if self.cfg.sound or self.cfg.music:
            pygame.mixer.pre_init(22050, -16, 2, 1024)
        '''

        pygame.init()
        if self.cfg.sound or self.cfg.music:
            pygame.mixer.pre_init(22050, -16, 2, 2048)
        self.scr = screen.Screen(self.cfg, _('Solstice'))
        self.control = control.Control(self)
        self.resourcemanager = resource_manager.ResourceManager(self,
                                                                'data.zip')
        self.sound_player = sound_player.SoundPlayer(self)
        self.scenes = {
            'logo': logo_scene.LogoScene(self),
            'intro': intro_scene.IntroScene(self),
            'game': game_scene.GameScene(self),
            'gameover': game_over_scene.GameOverScene(self)
        }

        self.scenemanager = scene_manager.SceneManager(self, 'logo')
        self.scenemanager.run()

    def exit(self, exit_code):
        self.cfg.save()
        pygame.quit()
        sys.exit(exit_code)

    @staticmethod
    def __platform_specific_inits():
        if platform.system() == 'Windows':
            os.environ['SDL_AUDIODRIVER'] = 'dsound'

        os.environ['SDL_VIDEO_CENTERED'] = '1'


def main():
    solstice = Solstice()
    solstice.exit(0)


if __name__ == '__main__':
    main()
