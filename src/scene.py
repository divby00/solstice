from gettext import gettext as _
import pygame

import menu
import config


class Scene(object):
    def __init__(self, context, name, scene_speed=40):
        self.name = name
        self.exit = context.exit
        self.scene_speed = scene_speed
        self.scenemanager = None
        self.screen = None
        self._keyboard_event = None
        self.running = False
        self.cfg = context.cfg
        self.control = context.control
        self.font_white = context.resourcemanager.get('font_white')
        self.font_blue = context.resourcemanager.get('font_blue')
        self.font_yellow = context.resourcemanager.get('font_yellow')
        self.sound_player = context.sound_player
        self.sound_player.load_sample(['blip', 'accept', 'cancel'])
        '''
        self.blip = context.resourcemanager.get('blip')
        self.accept = context.resourcemanager.get('accept')
        self.cancel = context.resourcemanager.get('cancel')
        '''
        self.panel_imgs = []
        panel = ['panel0', 'panel1', 'panel2',
                 'panel3', 'panel4', 'panel5',
                 'panel6', 'panel7', 'panel8',
                 'cursor', 'font_dither']

        for p in xrange(0, len(panel)):
            self.panel_imgs.insert(p, context.resourcemanager.get(panel[p]))

        self.menu_context = (self.panel_imgs,
                             (self.font_white, self.font_blue, self.font_yellow),
                             self.sound_player,
                             self.control)

    @property
    def keyboard_event(self):
        return self._keyboard_event

    @keyboard_event.setter
    def keyboard_event(self, value):
        self._keyboard_event = value

    def on_start(self):
        raise NotImplementedError('Implement this method')

    def render(self, scr):
        raise NotImplementedError('Implement this method')

    def run(self):
        raise NotImplementedError('Implement this method')

    def get_menu(self):
        music_volume_options = [
            menu.MenuItem('music_vol_1_item', _('1'),
                          self.music_vol_selected, None),
            menu.MenuItem('music_vol_2_item', _('2'),
                          self.music_vol_selected, None),
            menu.MenuItem('music_vol_3_item', _('3'),
                          self.music_vol_selected, None),
            menu.MenuItem('music_vol_4_item', _('4'),
                          self.music_vol_selected, None),
            menu.MenuItem('music_vol_5_item', _('5'),
                          self.music_vol_selected, None)
        ]
        music_active_options = [
            menu.MenuItem('music_active_on_item', _('music on'),
                          self.music_active_selected, None),
            menu.MenuItem('music_active_off_item', _('music off'),
                          self.music_active_selected, None)
        ]
        sound_volume_options = [
            menu.MenuItem('sound_vol_1_item', _('1'),
                          self.sound_vol_selected, None),
            menu.MenuItem('sound_vol_2_item', _('2'),
                          self.sound_vol_selected, None),
            menu.MenuItem('sound_vol_3_item', _('3'),
                          self.sound_vol_selected, None),
            menu.MenuItem('sound_vol_4_item', _('4'),
                          self.sound_vol_selected, None),
            menu.MenuItem('sound_vol_5_item', _('5'),
                          self.sound_vol_selected, None)
        ]
        sound_active_options = [
            menu.MenuItem('sound_active_on_item', _('sound effects on'),
                          self.sound_active_selected, None),
            menu.MenuItem('sound_active_off_item', _('sound effects off'),
                          self.sound_active_selected, None)
        ]
        sound_options = [
            menu.MenuItem('sound_active_item', _('sound active'),
                          None, 'sound_active_menu'),
            menu.MenuItem('sound_volume_item', _('sound volume'),
                          None, 'sound_volume_menu'),
            menu.MenuItem('music_active_item', _('music active'),
                          None, 'music_active_menu'),
            menu.MenuItem('music_volume_item', _('music volume'),
                          None, 'music_volume_menu')
        ]
        control_options = [
            menu.MenuItem('control_type_item', _('control type'),
                          None, None),
            menu.MenuItem('define_keys_item', _('define keys'),
                          None, None)
        ]
        fullscreen_options = [
            menu.MenuItem('fullscreen_item', _('fullscreen'),
                          self.fullscreen_mode_selected, None),
            menu.MenuItem('window_item', _('windowed'),
                          self.fullscreen_mode_selected, None)
        ]
        resolution_options = [
            menu.MenuItem('small_item', _('256 x 192'), self.resolution_selected, None),
            menu.MenuItem('medium_item', _('512 x 384'), self.resolution_selected, None),
            menu.MenuItem('large_item', _('1024 x 768'), self.resolution_selected, None)
        ]
        graphics_options = [
            menu.MenuItem('resolution_item', _('resolution'),
                          None, 'resolution_menu'),
            menu.MenuItem('fullscreen_item', _('fullscreen'),
                          None, 'fullscreen_menu')
        ]
        options_options = [
            menu.MenuItem('graphics_item', _('graphics'),
                          None, 'graphics_menu'),
            menu.MenuItem('sound_item', _('sound'), None, 'sound_menu'),
            menu.MenuItem('control_item', _('control'), None, 'control_menu')
        ]
        main_options = [
            menu.MenuItem('start_item', _('start'), self.enter_game, None),
            menu.MenuItem('options_item', _('options'), None, 'options_menu'),
            menu.MenuItem('exit_item', _('exit'), self.quit_game, None)
        ]

        main_menu = menu.Menu('main_menu', main_options)
        graphics_menu = menu.Menu('graphics_menu',
                                  graphics_options,
                                  'options_menu')
        fullscreen_menu = menu.Menu('fullscreen_menu',
                                    fullscreen_options,
                                    'graphics_menu')
        resolution_menu = menu.Menu('resolution_menu',
                                    resolution_options,
                                    'graphics_menu')
        sound_menu = menu.Menu('sound_menu',
                               sound_options,
                               'options_menu')
        sound_active_menu = menu.Menu('sound_active_menu',
                                      sound_active_options,
                                      'sound_menu')
        music_active_menu = menu.Menu('music_active_menu',
                                      music_active_options,
                                      'sound_menu')
        sound_volume_menu = menu.Menu('sound_volume_menu',
                                      sound_volume_options,
                                      'sound_menu')
        music_volume_menu = menu.Menu('music_volume_menu',
                                      music_volume_options,
                                      'sound_menu')
        control_menu = menu.Menu('control_menu',
                                 control_options,
                                 'options_menu')
        options_menu = menu.Menu('options_menu',
                                 options_options,
                                 'main_menu')

        menu_list = [
            main_menu, options_menu, graphics_menu,
            sound_menu, sound_active_menu, sound_volume_menu,
            music_active_menu, music_volume_menu, control_menu,
            resolution_menu, fullscreen_menu
        ]

        self.menu_group = menu.MenuGroup(menu_list,
                                         'main_menu',
                                         self.menu_context)

    def enter_game(self):
        if self.name == 'intro':
            pygame.mixer.music.stop()
            self.scenemanager.set('game')
        else:
            self.menu_group.visible = False
            self.control.event_driven = False

    def quit_game(self):
        if self.name == 'intro':
            self.exit(0)
        else:
            self.scenemanager.set('intro')

    def sound_vol_selected(self):
        self.cfg.parser.set(config.Configuration.SECTION[2],
                            config.Configuration.OPT_SOUND_VOL,
                            self.menu_group.selected_menu.selected_option + 1)
        self.cfg.sound_vol = self.menu_group.selected_menu.selected_option + 1

    def music_vol_selected(self):
        self.cfg.parser.set(config.Configuration.SECTION[2],
                            config.Configuration.OPT_MUSIC_VOL,
                            self.menu_group.selected_menu.selected_option + 1)
        self.cfg.music_vol = self.menu_group.selected_menu.selected_option + 1

    def sound_active_selected(self):
        self.cfg.parser.set(config.Configuration.SECTION[2],
                            config.Configuration.OPT_SOUND,
                            False)
        self.cfg.sound = False
        option = self.menu_group.selected_menu.selected_option

        if option == 0:
            self.cfg.parser.set(config.Configuration.SECTION[2],
                                config.Configuration.OPT_SOUND,
                                True)
            self.cfg.sound = True

    def music_active_selected(self):
        self.cfg.parser.set(config.Configuration.SECTION[2],
                            config.Configuration.OPT_MUSIC,
                            False)
        self.cfg.music = False
        option = self.menu_group.selected_menu.selected_option

        if option == 0:
            self.cfg.parser.set(config.Configuration.SECTION[2],
                                config.Configuration.OPT_MUSIC,
                                True)
            self.cfg.music = True

    def fullscreen_mode_selected(self):
        option = self.menu_group.selected_menu.selected_option

        if option == 0:
            self.screen.toggle_fullscreen(True)
            self.cfg.parser.set(config.Configuration.SECTION[1],
                                config.Configuration.OPT_FULLSCREEN,
                                True)
            self.cfg.fullscreen = True
        else:
            self.screen.toggle_fullscreen(False)
            self.cfg.parser.set(config.Configuration.SECTION[1],
                                config.Configuration.OPT_FULLSCREEN,
                                False)
            self.cfg.fullscreen = False

    def resolution_selected(self):
        option = self.menu_group.selected_menu.selected_option
        new_resolution = self.screen.change_resolution(option)
        self.cfg.parser.set(config.Configuration.SECTION[1],
                            config.Configuration.OPT_SCREEN_WIDTH,
                            new_resolution[0])
        self.cfg.parser.set(config.Configuration.SECTION[1],
                            config.Configuration.OPT_SCREEN_HEIGHT,
                            new_resolution[1])
