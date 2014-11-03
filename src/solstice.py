#!/usr/bin/env python
from __future__ import division
import pygame
import gettext
import i18n
import config
import resource_manager
import scene_manager
import scene
import logo_scene
import menu_scene
import game_scene
import screen


def main():
    cfg = config.Configuration()
    gettext.bindtextdomain('solstice', cfg.locale_path)
    gettext.textdomain('solstice')
    pygame.init()
    scr = screen.Screen(cfg, i18n._('Solstice'))
    pygame.mixer.pre_init(44100,-16,2, 1024 * 3)
    resourcemanager = resource_manager.ResourceManager(scr, cfg, 'data.zip')
    logoscene = logo_scene.LogoScene(resourcemanager)
    menuscene = menu_scene.MenuScene(resourcemanager)
    gamescene = game_scene.GameScene(resourcemanager)
    scenemanager = scene_manager.SceneManager(scr)
    scenemanager.set(logoscene)
    scenemanager.run()
    scenemanager.set(menuscene)
    scenemanager.run()
    scenemanager.set(gamescene)
    scenemanager.run()
    cfg.save()
    pygame.quit()
    return 0

if __name__ == '__main__':
    main()
