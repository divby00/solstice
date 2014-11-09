#!/usr/bin/env python
from __future__ import division
import sys
import gettext
import pygame
import i18n
import config
import resource_manager
import scene_manager
import scene
import logo_scene
import menu_scene
import game_scene
import screen


class Solstice(object):

    def __init__(self):
        self.cfg = config.Configuration()
        gettext.bindtextdomain('solstice', self.cfg.locale_path)
        gettext.textdomain('solstice')
        pygame.mixer.pre_init(22050, -16, 2, 4096)
        pygame.init()
        self.scr = screen.Screen(self.cfg, i18n._('Solstice'))
        self.resourcemanager = resource_manager.ResourceManager(self, 'data.zip')
        self.logoscene = logo_scene.LogoScene(self)
        self.menuscene = menu_scene.MenuScene(self)
        self.gamescene = game_scene.GameScene(self)
        self.scenemanager = scene_manager.SceneManager(self)
        self.scenemanager.set(self.logoscene)
        self.scenemanager.run()
        self.scenemanager.set(self.menuscene)
        self.scenemanager.run()
        self.scenemanager.set(self.gamescene)
        self.scenemanager.run()

    def exit(self, exit_code):
        self.cfg.save()
        pygame.quit()
        sys.exit(exit_code)


def main():
    solstice = Solstice()
    solstice.exit(0)

if __name__ == '__main__':
    main()
