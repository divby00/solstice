import pygame
from gettext import gettext as _

import config
import menu


class Scene(object):
    def __init__(self, context, name, scene_speed=40):
        self._name = name
        self._exit = context.exit
        self._scene_speed = scene_speed
        self._scene_manager = None
        self._scene_data = None
        self._screen = None
        self._keyboard_event = None
        self._joystick_event = None
        self._running = False
        self._menu_group = None
        self._config = context.config
        self._control = context.control
        self._font_white = context.resource_manager.get('font_white')
        self._font_blue = context.resource_manager.get('font_blue')
        self._font_yellow = context.resource_manager.get('font_yellow')
        self._sound_player = context.sound_player
        self._sound_player.load_sample(['blip', 'accept', 'cancel'])
        panel = [
            'panel0', 'panel1', 'panel2', 'panel3', 'panel4', 'panel5',
            'panel6', 'panel7', 'panel8', 'cursor', 'font_dither'
        ]
        panel_sprites = [context.resource_manager.get(panel[index])
                         for index, value in enumerate(panel)]
        self._menu_context = (panel_sprites, (self._font_white, self._font_blue, self._font_yellow),
                              self._sound_player, self._control)

    '''
    Private methods
    '''

    def _sound_volume_selected(self):
        self._config.parser.set(config.Configuration.SECTION[2],
                                config.Configuration.OPT_SOUND_VOL,
                                self._menu_group.selected_menu.selected_option + 1)
        self._config.sound_vol = self._menu_group.selected_menu.selected_option + 1

    def _music_volume_selected(self):
        self._config.parser.set(config.Configuration.SECTION[2],
                                config.Configuration.OPT_MUSIC_VOL,
                                self.menu_group.selected_menu.selected_option + 1)
        self._config.music_vol = self.menu_group.selected_menu.selected_option + 1

    def _sound_active_selected(self):
        self._config.parser.set(config.Configuration.SECTION[2],
                                config.Configuration.OPT_SOUND,
                                False)
        self._config.sound = False
        option = self.menu_group.selected_menu.selected_option

        if option == 0:
            self._config.parser.set(config.Configuration.SECTION[2],
                                    config.Configuration.OPT_SOUND, True)
            self._config.sound = True

    def _music_active_selected(self):
        self._config.parser.set(config.Configuration.SECTION[2],
                                config.Configuration.OPT_MUSIC, False)
        self._config.music = False
        option = self.menu_group.selected_menu.selected_option

        if option == 0:
            self._config.parser.set(config.Configuration.SECTION[2],
                                    config.Configuration.OPT_MUSIC, True)
            self._config.music = True

    def _fullscreen_mode_selected(self):
        option = self._menu_group.selected_menu.selected_option

        if option == 0:
            self._screen.toggle_fullscreen(True)
            self._config.parser.set(config.Configuration.SECTION[1],
                                    config.Configuration.OPT_FULLSCREEN, True)
            self._config.full_screen = True
        else:
            self._screen.toggle_fullscreen(False)
            self._config.parser.set(config.Configuration.SECTION[1],
                                    config.Configuration.OPT_FULLSCREEN, False)
            self._config.full_screen = False

    '''
    Public methods
    '''

    def on_start(self):
        raise NotImplementedError('Implement this method')

    def render(self, scr):
        raise NotImplementedError('Implement this method')

    def run(self):
        raise NotImplementedError('Implement this method')

    def get_menu(self):
        music_volume_options = [
            menu.MenuItem('music_vol_1_item', _('1'), self._music_volume_selected, None),
            menu.MenuItem('music_vol_2_item', _('2'), self._music_volume_selected, None),
            menu.MenuItem('music_vol_3_item', _('3'), self._music_volume_selected, None),
            menu.MenuItem('music_vol_4_item', _('4'), self._music_volume_selected, None),
            menu.MenuItem('music_vol_5_item', _('5'), self._music_volume_selected, None)
        ]
        music_active_options = [
            menu.MenuItem('music_active_on_item', _('music on'), self._music_active_selected, None),
            menu.MenuItem('music_active_off_item', _('music off'), self._music_active_selected,
                          None)
        ]
        sound_volume_options = [
            menu.MenuItem('sound_vol_1_item', _('1'), self._sound_volume_selected, None),
            menu.MenuItem('sound_vol_2_item', _('2'), self._sound_volume_selected, None),
            menu.MenuItem('sound_vol_3_item', _('3'), self._sound_volume_selected, None),
            menu.MenuItem('sound_vol_4_item', _('4'), self._sound_volume_selected, None),
            menu.MenuItem('sound_vol_5_item', _('5'), self._sound_volume_selected, None)
        ]
        sound_active_options = [
            menu.MenuItem('sound_active_on_item', _('sound effects on'),
                          self._sound_active_selected,
                          None),
            menu.MenuItem('sound_active_off_item', _('sound effects off'),
                          self._sound_active_selected, None)
        ]
        sound_options = [
            menu.MenuItem('sound_active_item', _('sound active'), None, 'sound_active_menu'),
            menu.MenuItem('sound_volume_item', _('sound volume'), None, 'sound_volume_menu'),
            menu.MenuItem('music_active_item', _('music active'), None, 'music_active_menu'),
            menu.MenuItem('music_volume_item', _('music volume'), None, 'music_volume_menu')
        ]
        control_options = [
            menu.MenuItem('control_type_item', _('control type'), None, None),
            menu.MenuItem('define_keys_item', _('define keys'), None, None)
        ]
        graphics_options = [
            menu.MenuItem('fullscreen_item', _('fullscreen'), self._fullscreen_mode_selected, None),
            menu.MenuItem('window_item', _('windowed'), self._fullscreen_mode_selected, None)
        ]
        options_options = [
            menu.MenuItem('graphics_item', _('graphics'), None, 'graphics_menu'),
            menu.MenuItem('sound_item', _('sound'), None, 'sound_menu'),
            menu.MenuItem('control_item', _('control'), None, 'control_menu')
        ]
        main_options = [
            menu.MenuItem('start_item', _('start'), self.enter_game, None),
            menu.MenuItem('options_item', _('options'), None, 'options_menu'),
            menu.MenuItem('exit_item', _('exit'), self.quit_game, None)
        ]

        main_menu = menu.Menu('main_menu', main_options)
        graphics_menu = menu.Menu('graphics_menu', graphics_options, 'options_menu')
        sound_menu = menu.Menu('sound_menu', sound_options, 'options_menu')
        sound_active_menu = menu.Menu('sound_active_menu', sound_active_options, 'sound_menu')
        music_active_menu = menu.Menu('music_active_menu', music_active_options, 'sound_menu')
        sound_volume_menu = menu.Menu('sound_volume_menu', sound_volume_options, 'sound_menu')
        music_volume_menu = menu.Menu('music_volume_menu', music_volume_options, 'sound_menu')
        control_menu = menu.Menu('control_menu', control_options, 'options_menu')
        options_menu = menu.Menu('options_menu', options_options, 'main_menu')

        menu_list = [
            main_menu, options_menu, graphics_menu,
            sound_menu, sound_active_menu, sound_volume_menu,
            music_active_menu, music_volume_menu, control_menu
        ]

        self._menu_group = menu.MenuGroup(menu_list, 'main_menu', self._menu_context)

    def enter_elevator(self, player):
        self._scene_manager.set('elevator', player)
        self._menu_group.visible = False
        self._control.event_driven = True

    def enter_game(self):
        if self._name == 'intro':
            pygame.mixer.music.stop()
            self._scene_manager.set('game')
        else:
            self._menu_group.visible = False
            self._control.event_driven = False

    def quit_game(self):
        if self._name == 'intro':
            self._exit(0)
        else:
            self._scene_manager.set('intro')

    @property
    def scene_speed(self):
        return self._scene_speed

    @property
    def scene_data(self):
        return self._scene_data

    @scene_data.setter
    def scene_data(self, value):
        self._scene_data = value

    @property
    def scene_manager(self):
        return self._scene_manager

    @scene_manager.setter
    def scene_manager(self, value):
        self._scene_manager = value

    @property
    def keyboard_event(self):
        return self._keyboard_event

    @keyboard_event.setter
    def keyboard_event(self, value):
        self._keyboard_event = value

    @property
    def joystick_event(self):
        return self._joystick_event

    @joystick_event.setter
    def joystick_event(self, value):
        self._joystick_event = value

    @property
    def menu_group(self):
        return self._menu_group

    @property
    def font_white(self):
        return self._font_white

    @property
    def screen(self):
        return self._screen
