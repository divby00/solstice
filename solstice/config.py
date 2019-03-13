# -*- coding: utf-8 -*-

import os
from enum import IntEnum, Enum
from gettext import gettext as _
from ConfigParser import ConfigParser


class ConfigurationError(Exception):

    def __init__(self, value):
        super(ConfigurationError, self).__init__()
        self.value = value


class Entries(Enum):
    DATA_PATH = 'data path'
    LOCALE_PATH = 'locale path'
    SCREEN_WIDTH = 'screen width'
    SCREEN_HEIGHT = 'screen height'
    FULLSCREEN = 'fullscreen'
    SOUND = 'sound'
    MUSIC = 'music'
    SOUND_VOL = 'sound volume'
    MUSIC_VOL = 'music volume'
    CONTROL_TYPE = 'type'
    KEY_UP = 'key up'
    KEY_DOWN = 'key down'
    KEY_LEFT = 'key left'
    KEY_RIGHT = 'key right'
    KEY_ACTION_1 = 'key action 1'
    KEY_ACTION_2 = 'key action 2'
    KEY_START = 'key start'
    VERTICAL_AXIS = 'vertical axis'
    HORIZONTAL_AXIS = 'horizontal axis'
    AXIS_UP = 'axis up'
    AXIS_DOWN = 'axis down'
    AXIS_LEFT = 'axis left'
    AXIS_RIGHT = 'axis right'
    BUTTON_ACTION_1 = 'joy button action 1'
    BUTTON_ACTION_2 = 'joy button action 2'


class DefaultIntValues(IntEnum):
    SOUND_VOLUME = 5
    MUSIC_VOLUME = 5
    KEY_UP = 119
    KEY_DOWN = 115
    KEY_LEFT = 97
    KEY_RIGHT = 100
    KEY_ACTION_1 = 117
    KEY_ACTION_2 = 105
    KEY_START = 13
    VERTICAL_AXIS = 1
    HORIZONTAL_AXIS = 0
    AXIS_UP = -1
    AXIS_DOWN = 1
    AXIS_RIGHT = 1
    AXIS_LEFT = -1
    BUTTON_ACTION_1 = 1
    BUTTON_ACTION_2 = 2


class DefaultValues(Enum):
    DATA_PATH = './'
    LOCALE_PATH = 'locale'
    SECTION = ['Paths', 'Graphics', 'Sound', 'Control']
    SCREEN_SIZE = [1024, 768]
    CFGFILE_NAME = 'solstice.cfg'
    CONTROL_TYPE = 'autodetect'
    FULLSCREEN = False
    SOUND = True
    MUSIC = True


class Configuration(object):

    @staticmethod
    def _check_correct_values(option, read_value):

        if option == Entries.DATA_PATH:
            file_path = ''.join([read_value, 'data.zip'])
            if not os.path.isfile(file_path):
                raise ConfigurationError(_('Unable to find the data file in the directory pointed at config. file.'))
        elif option == Entries.SOUND_VOL:
            if read_value not in list(range(DefaultIntValues.SOUND_VOLUME + 1)):
                raise ConfigurationError(_('Sound volume must be between 0 (min) and 5 (max).'))
        elif option == Entries.MUSIC_VOL:
            if read_value not in list(range(DefaultIntValues.MUSIC_VOLUME + 1)):
                raise ConfigurationError(_('Music volume must be between 0 (min) and 5 (max).'))
        elif option == Entries.CONTROL_TYPE:
            if read_value not in ['keyboard', 'joystick', 'autodetect']:
                raise ConfigurationError(_('Control must be keyboard, joystick or autodetect.'))
        elif option == Entries.SCREEN_WIDTH:
            if read_value < 1:
                raise ConfigurationError(_('Screen width must be greater than 1.'))
        elif option == Entries.SCREEN_HEIGHT:
            if read_value < 1:
                raise ConfigurationError(_('Screen height must be greater than 1.'))

    def __init__(self):
        self._parser = ConfigParser()
        self._control_type = DefaultValues.CONTROL_TYPE
        self._full_screen = DefaultValues.FULLSCREEN
        self._sound = DefaultValues.SOUND
        self._music = DefaultValues.MUSIC
        self._sound_vol = DefaultIntValues.SOUND_VOLUME
        self._music_vol = DefaultIntValues.MUSIC_VOLUME
        self._key_up = DefaultIntValues.KEY_UP
        self._key_down = DefaultIntValues.KEY_DOWN
        self._key_left = DefaultIntValues.KEY_LEFT
        self._key_right = DefaultIntValues.KEY_RIGHT
        self._key_act1 = DefaultIntValues.KEY_ACTION_1
        self._key_act2 = DefaultIntValues.KEY_ACTION_2
        self._key_start = DefaultIntValues.KEY_START
        self._vertical_axis = DefaultIntValues.VERTICAL_AXIS
        self._horizontal_axis = DefaultIntValues.HORIZONTAL_AXIS
        self._axis_up = DefaultIntValues.AXIS_UP
        self._axis_down = DefaultIntValues.AXIS_DOWN
        self._axis_left = DefaultIntValues.AXIS_LEFT
        self._axis_right = DefaultIntValues.AXIS_RIGHT
        self._button_act1 = DefaultIntValues.BUTTON_ACTION_1
        self._button_act2 = DefaultIntValues.BUTTON_ACTION_2

        try:
            parsed_file = self._parser.read(DefaultValues.CFGFILE_NAME.value)

            if len(parsed_file) > 0:
                self._data_path = self._parser.get(DefaultValues.SECTION.value[0], Entries.DATA_PATH.value)
                self._check_correct_values(Entries.DATA_PATH, self.data_path)
                self._locale_path = self._parser.get(DefaultValues.SECTION.value[0], Entries.LOCALE_PATH.value)
                w = self._parser.getint(DefaultValues.SECTION.value[1], Entries.SCREEN_WIDTH.value)
                self._check_correct_values(Entries.SCREEN_WIDTH, w)
                h = self._parser.getint(DefaultValues.SECTION.value[1], Entries.SCREEN_HEIGHT.value)
                self._check_correct_values(Entries.SCREEN_HEIGHT, h)
                self._full_screen = self._parser.getboolean(DefaultValues.SECTION.value[1], Entries.FULLSCREEN.value)
                self._sound = self._parser.getboolean(DefaultValues.SECTION.value[2], Entries.SOUND.value)
                self._music = self._parser.getboolean(DefaultValues.SECTION.value[2], Entries.MUSIC.value)
                self._sound_vol = self._parser.getint(DefaultValues.SECTION.value[2], Entries.SOUND_VOL.value)
                self._check_correct_values(Entries.SOUND_VOL, self._sound_vol)
                self._music_vol = self._parser.getint(DefaultValues.SECTION.value[2], Entries.MUSIC_VOL.value)
                self._check_correct_values(Entries.MUSIC_VOL, self._music_vol)
                self._screen_size = (w, h)
                self._control_type = self._parser.get(DefaultValues.SECTION.value[3], Entries.CONTROL_TYPE.value)
                self._check_correct_values(Entries.CONTROL_TYPE, self._control_type)
                self._key_up = self._parser.getint(DefaultValues.SECTION.value[3], Entries.KEY_UP.value)
                self._key_down = self._parser.getint(DefaultValues.SECTION.value[3], Entries.KEY_DOWN.value)
                self._key_left = self._parser.getint(DefaultValues.SECTION.value[3], Entries.KEY_LEFT.value)
                self._key_right = self._parser.getint(DefaultValues.SECTION.value[3], Entries.KEY_RIGHT.value)
                self._key_act1 = self._parser.getint(DefaultValues.SECTION.value[3], Entries.KEY_ACTION_1.value)
                self._key_act2 = self._parser.getint(DefaultValues.SECTION.value[3], Entries.KEY_ACTION_2.value)
                self._key_start = self._parser.getint(DefaultValues.SECTION.value[3], Entries.KEY_START.value)
                self._vertical_axis = self._parser.getint(DefaultValues.SECTION.value[3], Entries.VERTICAL_AXIS.value)
                self._horizontal_axis = self._parser.getint(DefaultValues.SECTION.value[3], Entries.HORIZONTAL_AXIS.value)
                self._axis_up = self._parser.getint(DefaultValues.SECTION.value[3], Entries.AXIS_UP.value)
                self._axis_down = self._parser.getint(DefaultValues.SECTION.value[3], Entries.AXIS_DOWN.value)
                self._axis_left = self._parser.getint(DefaultValues.SECTION.value[3], Entries.AXIS_LEFT.value)
                self._axis_right = self._parser.getint(DefaultValues.SECTION.value[3], Entries.AXIS_RIGHT.value)
                self._button_act1 = self._parser.getint(DefaultValues.SECTION.value[3], Entries.BUTTON_ACTION_1.value)
                self._button_act2 = self._parser.getint(DefaultValues.SECTION.value[3], Entries.BUTTON_ACTION_2.value)
            else:
                self._default_values_set()
        except ConfigurationError as e:
            print(e.value)
            self._default_values_set()
        except Exception:
            self._default_values_set()

    def _default_values_set(self):
        for section in DefaultValues.SECTION.value:
            if not self._parser.has_section(section):
                self._parser.add_section(section)

        self._paths_section_set()
        self._graphics_section_set()
        self._sound_section_set()
        self._control_section_set()
        self.save()
        self._data_path = DefaultValues.DATA_PATH.value
        self._locale_path = DefaultValues.LOCALE_PATH.value
        self._screen_size = (DefaultValues.SCREEN_SIZE.value[0], DefaultValues.SCREEN_SIZE.value[1])
        self._full_screen = DefaultValues.FULLSCREEN
        self._sound = DefaultValues.SOUND
        self._music = DefaultValues.MUSIC
        self._sound_vol = DefaultIntValues.SOUND_VOLUME
        self._music_vol = DefaultIntValues.MUSIC_VOLUME
        self._control_type = DefaultValues.CONTROL_TYPE.value
        self._key_up = DefaultIntValues.KEY_UP
        self._key_down = DefaultIntValues.KEY_DOWN
        self._key_left = DefaultIntValues.KEY_LEFT
        self._key_right = DefaultIntValues.KEY_RIGHT
        self._key_act1 = DefaultIntValues.KEY_ACTION_1
        self._key_act2 = DefaultIntValues.KEY_ACTION_2
        self._key_start = DefaultIntValues.KEY_START
        self._vertical_axis = DefaultIntValues.VERTICAL_AXIS
        self._horizontal_axis = DefaultIntValues.HORIZONTAL_AXIS
        self._axis_up = DefaultIntValues.AXIS_UP
        self._axis_down = DefaultIntValues.AXIS_DOWN
        self._axis_left = DefaultIntValues.AXIS_LEFT
        self._axis_right = DefaultIntValues.AXIS_RIGHT
        self._button_act1 = DefaultIntValues.BUTTON_ACTION_1
        self._button_act2 = DefaultIntValues.BUTTON_ACTION_2

    def _paths_section_set(self):
        self._parser.set(DefaultValues.SECTION.value[0], Entries.DATA_PATH.value, DefaultValues.DATA_PATH.value)
        self._parser.set(DefaultValues.SECTION.value[0], Entries.LOCALE_PATH.value, DefaultValues.LOCALE_PATH.value)

    def _graphics_section_set(self):
        self._parser.set(DefaultValues.SECTION.value[1], Entries.SCREEN_WIDTH.value, DefaultValues.SCREEN_SIZE.value[0])
        self._parser.set(DefaultValues.SECTION.value[1], Entries.SCREEN_HEIGHT.value,
                         DefaultValues.SCREEN_SIZE.value[1])
        self._parser.set(DefaultValues.SECTION.value[1], Entries.FULLSCREEN.value, DefaultValues.FULLSCREEN.value)

    def _sound_section_set(self):
        self._parser.set(DefaultValues.SECTION.value[2], Entries.SOUND.value, DefaultValues.SOUND.value)
        self._parser.set(DefaultValues.SECTION.value[2], Entries.MUSIC.value, DefaultValues.MUSIC.value)
        self._parser.set(DefaultValues.SECTION.value[2], Entries.SOUND_VOL.value, DefaultIntValues.SOUND_VOLUME.value)
        self._parser.set(DefaultValues.SECTION.value[2], Entries.MUSIC_VOL.value, DefaultIntValues.MUSIC_VOLUME.value)

    def _control_section_set(self):
        self._parser.set(DefaultValues.SECTION.value[3], Entries.CONTROL_TYPE.value, DefaultValues.CONTROL_TYPE.value),
        self._parser.set(DefaultValues.SECTION.value[3], Entries.KEY_UP.value, DefaultIntValues.KEY_UP.value),
        self._parser.set(DefaultValues.SECTION.value[3], Entries.KEY_DOWN.value, DefaultIntValues.KEY_DOWN.value),
        self._parser.set(DefaultValues.SECTION.value[3], Entries.KEY_LEFT.value, DefaultIntValues.KEY_LEFT.value),
        self._parser.set(DefaultValues.SECTION.value[3], Entries.KEY_RIGHT.value, DefaultIntValues.KEY_RIGHT.value),
        self._parser.set(DefaultValues.SECTION.value[3], Entries.KEY_ACTION_1.value,
                         DefaultIntValues.KEY_ACTION_1.value),
        self._parser.set(DefaultValues.SECTION.value[3], Entries.KEY_ACTION_2.value,
                         DefaultIntValues.KEY_ACTION_2.value)
        self._parser.set(DefaultValues.SECTION.value[3], Entries.KEY_START.value, DefaultIntValues.KEY_START.value)
        self._parser.set(DefaultValues.SECTION.value[3], Entries.VERTICAL_AXIS.value,
                         DefaultIntValues.VERTICAL_AXIS.value),
        self._parser.set(DefaultValues.SECTION.value[3], Entries.HORIZONTAL_AXIS.value,
                         DefaultIntValues.HORIZONTAL_AXIS.value),
        self._parser.set(DefaultValues.SECTION.value[3], Entries.AXIS_UP.value, DefaultIntValues.AXIS_UP.value),
        self._parser.set(DefaultValues.SECTION.value[3], Entries.AXIS_DOWN.value, DefaultIntValues.AXIS_DOWN.value),
        self._parser.set(DefaultValues.SECTION.value[3], Entries.AXIS_LEFT.value, DefaultIntValues.AXIS_LEFT.value),
        self._parser.set(DefaultValues.SECTION.value[3], Entries.AXIS_RIGHT.value, DefaultIntValues.AXIS_RIGHT.value),
        self._parser.set(DefaultValues.SECTION.value[3], Entries.BUTTON_ACTION_1.value,
                         DefaultIntValues.BUTTON_ACTION_1.value),
        self._parser.set(DefaultValues.SECTION.value[3], Entries.BUTTON_ACTION_2.value,
                         DefaultIntValues.BUTTON_ACTION_2.value)

    def save(self):
        with open(DefaultValues.CFGFILE_NAME.value, 'wb') as config_file:
            self._parser.write(config_file)

    @property
    def data_path(self):
        return self._data_path

    @property
    def locale_path(self):
        return self._locale_path

    @property
    def music(self):
        return self._music

    @music.setter
    def music(self, value):
        self._music = value

    @property
    def sound(self):
        return self._sound

    @sound.setter
    def sound(self, value):
        self._sound = value

    @property
    def screen_size(self):
        return self._screen_size

    @property
    def control_type(self):
        return self._control_type

    @property
    def key_up(self):
        return self._key_up

    @property
    def key_down(self):
        return self._key_down

    @property
    def key_left(self):
        return self._key_left

    @property
    def key_right(self):
        return self._key_right

    @property
    def key_act1(self):
        return self._key_act1

    @property
    def key_act2(self):
        return self._key_act2

    @property
    def key_start(self):
        return self._key_start

    @property
    def axis_up(self):
        return self._axis_up

    @property
    def axis_down(self):
        return self._axis_down

    @property
    def axis_left(self):
        return self._axis_left

    @property
    def axis_right(self):
        return self._axis_right

    @property
    def vertical_axis(self):
        return self._vertical_axis

    @property
    def horizontal_axis(self):
        return self._horizontal_axis

    @property
    def button_act1(self):
        return self._button_act1

    @property
    def button_act2(self):
        return self._button_act2

    @property
    def parser(self):
        return self._parser

    @property
    def full_screen(self):
        return self._full_screen

    @full_screen.setter
    def full_screen(self, value):
        self._full_screen = value
