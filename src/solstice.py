#!/usr/bin/env python
from __future__ import division
import pygame
import gettext
import i18n
import config
import resmngr
import scene_manager
import scene
import logo_scene
import menu_scene
import game_scene
import screen

def main():
    gettext.bindtextdomain('solstice', 'locale')
    gettext.textdomain('solstice')
    cfg = config.Configuration()
    pygame.init()
    scr = screen.Screen(cfg.screen_size, cfg, i18n._('Solstice'))
    rmngr = resmngr.ResourceManager('data.zip')
    logoscene = logo_scene.LogoScene(rmngr)
    menuscene = menu_scene.MenuScene(rmngr)
    gamescene = game_scene.GameScene(rmngr)
    scene_mngr = scene_manager.SceneManager(scr)
    scene_mngr.set(logoscene)
    scene_mngr.run()
    scene_mngr.set(gamescene)
    scene_mngr.run()
    pygame.quit()
    return 0

if __name__ == '__main__':
    main()
