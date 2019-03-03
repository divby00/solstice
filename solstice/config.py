import ConfigParser
import os
from gettext import gettext as _


class ConfigurationError(Exception):
    def __init__(self, value):
        super(ConfigurationError, self).__init__()
        self.value = value

    def __str__(self):
        return self.value


class Configuration(object):
    OPT_DATA_PATH = 'data path'
    OPT_LOCALE_PATH = 'locale path'
    OPT_SCREEN_WIDTH = 'screen width'
    OPT_SCREEN_HEIGHT = 'screen height'
    OPT_FULLSCREEN = 'fullscreen'
    OPT_SOUND = 'sound'
    OPT_MUSIC = 'music'
    OPT_SOUND_VOL = 'sound volume'
    OPT_MUSIC_VOL = 'music volume'
    OPT_CONTROL_TYPE = 'type'
    OPT_KEY_UP = 'key up'
    OPT_KEY_DOWN = 'key down'
    OPT_KEY_LEFT = 'key left'
    OPT_KEY_RIGHT = 'key right'
    OPT_KEY_ACTION_1 = 'key action 1'
    OPT_KEY_ACTION_2 = 'key action 2'
    OPT_KEY_START = 'key start'
    OPT_VERTICAL_AXIS = 'vertical axis'
    OPT_HORIZONTAL_AXIS = 'horizontal axis'
    OPT_AXIS_UP = 'axis up'
    OPT_AXIS_DOWN = 'axis down'
    OPT_AXIS_LEFT = 'axis left'
    OPT_AXIS_RIGHT = 'axis right'
    OPT_BUTTON_ACTION_1 = 'joy button action 1'
    OPT_BUTTON_ACTION_2 = 'joy button action 2'

    # Default values
    DATA_PATH = './'
    LOCALE_PATH = 'locale'
    SECTION = ['Paths', 'Graphics', 'Sound', 'Control']
    SCREEN_SIZE = [1024, 768]
    FULLSCREEN = False
    SOUND = True
    MUSIC = True
    SOUND_VOLUME = 5
    MUSIC_VOLUME = 5
    CFGFILE_NAME = 'solstice.cfg'
    CONTROL_TYPE = 'autodetect'
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

    def __init__(self):
        self._parser = ConfigParser.ConfigParser()
        self._full_screen = Configuration.FULLSCREEN
        self._sound = Configuration.SOUND
        self._music = Configuration.MUSIC
        self._sound_vol = Configuration.SOUND_VOLUME
        self._music_vol = Configuration.MUSIC_VOLUME
        self._control_type = Configuration.CONTROL_TYPE
        self._key_up = Configuration.KEY_UP
        self._key_down = Configuration.KEY_DOWN
        self._key_left = Configuration.KEY_LEFT
        self._key_right = Configuration.KEY_RIGHT
        self._key_act1 = Configuration.KEY_ACTION_1
        self._key_act2 = Configuration.KEY_ACTION_2
        self._key_start = Configuration.KEY_START
        self._vertical_axis = Configuration.VERTICAL_AXIS
        self._horizontal_axis = Configuration.HORIZONTAL_AXIS
        self._axis_up = Configuration.AXIS_UP
        self._axis_down = Configuration.AXIS_DOWN
        self._axis_left = Configuration.AXIS_LEFT
        self._axis_right = Configuration.AXIS_RIGHT
        self._button_act1 = Configuration.BUTTON_ACTION_1
        self._button_act2 = Configuration.BUTTON_ACTION_2

        try:
            parsed_file = self._parser.read([Configuration.CFGFILE_NAME])

            if len(parsed_file) > 0:
                self._data_path = self._parser.get(Configuration.SECTION[0],
                                                   Configuration.OPT_DATA_PATH)
                self._check_correct_values(Configuration.OPT_DATA_PATH, self.data_path)
                self._locale_path = self._parser.get(Configuration.SECTION[0],
                                                     Configuration.OPT_LOCALE_PATH)
                w = self._parser.getint(Configuration.SECTION[1], Configuration.OPT_SCREEN_WIDTH)
                self._check_correct_values(Configuration.OPT_SCREEN_WIDTH, w)
                h = self._parser.getint(Configuration.SECTION[1], Configuration.OPT_SCREEN_HEIGHT)
                self._check_correct_values(Configuration.OPT_SCREEN_HEIGHT, h)
                self._full_screen = self._parser.getboolean(Configuration.SECTION[1],
                                                            Configuration.OPT_FULLSCREEN)
                self._sound = self._parser.getboolean(Configuration.SECTION[2],
                                                      Configuration.OPT_SOUND)
                self._music = self._parser.getboolean(Configuration.SECTION[2],
                                                      Configuration.OPT_MUSIC)
                self._sound_vol = self._parser.getint(Configuration.SECTION[2],
                                                      Configuration.OPT_SOUND_VOL)
                self._check_correct_values(Configuration.OPT_SOUND_VOL, self._sound_vol)
                self._music_vol = self._parser.getint(Configuration.SECTION[2],
                                                      Configuration.OPT_MUSIC_VOL)
                self._check_correct_values(Configuration.OPT_MUSIC_VOL, self._music_vol)
                self._screen_size = (w, h)
                self._control_type = self._parser.get(Configuration.SECTION[3],
                                                      Configuration.OPT_CONTROL_TYPE)
                self._check_correct_values(Configuration.OPT_CONTROL_TYPE, self._control_type)
                self._key_up = self._parser.getint(Configuration.SECTION[3],
                                                   Configuration.OPT_KEY_UP)
                self._key_down = self._parser.getint(Configuration.SECTION[3],
                                                     Configuration.OPT_KEY_DOWN)
                self._key_left = self._parser.getint(Configuration.SECTION[3],
                                                     Configuration.OPT_KEY_LEFT)
                self._key_right = self._parser.getint(Configuration.SECTION[3],
                                                      Configuration.OPT_KEY_RIGHT)
                self._key_act1 = self._parser.getint(Configuration.SECTION[3],
                                                     Configuration.OPT_KEY_ACTION_1)
                self._key_act2 = self._parser.getint(Configuration.SECTION[3],
                                                     Configuration.OPT_KEY_ACTION_2)
                self._key_start = self._parser.getint(Configuration.SECTION[3],
                                                      Configuration.OPT_KEY_START)
                self._vertical_axis = self._parser.getint(Configuration.SECTION[3],
                                                     Configuration.OPT_VERTICAL_AXIS)
                self._horizontal_axis = self._parser.getint(Configuration.SECTION[3],
                                                     Configuration.OPT_HORIZONTAL_AXIS)
                self._axis_up = self._parser.getint(Configuration.SECTION[3],
                                                     Configuration.OPT_AXIS_UP)
                self._axis_down = self._parser.getint(Configuration.SECTION[3],
                                                     Configuration.OPT_AXIS_DOWN)
                self._axis_left = self._parser.getint(Configuration.SECTION[3],
                                                     Configuration.OPT_AXIS_LEFT)
                self._axis_right = self._parser.getint(Configuration.SECTION[3],
                                                     Configuration.OPT_AXIS_RIGHT)
                self._button_act1 = self._parser.getint(Configuration.SECTION[3],
                                                     Configuration.OPT_BUTTON_ACTION_1)
                self._button_act2 = self._parser.getint(Configuration.SECTION[3],
                                                     Configuration.OPT_BUTTON_ACTION_2)
            else:
                self._default_values_set()
        except ConfigurationError as e:
            print(e.value)
            self._default_values_set()
        except Exception:
            self._default_values_set()

    '''
    Private methods
    '''

    def _default_values_set(self):
        for section in Configuration.SECTION:
            if not self._parser.has_section(section):
                self._parser.add_section(section)

        self._paths_section_set()
        self._graphics_section_set()
        self._sound_section_set()
        self._control_section_set()
        self.save()
        self._data_path = Configuration.DATA_PATH
        self._locale_path = Configuration.LOCALE_PATH
        self._screen_size = (Configuration.SCREEN_SIZE[0],
                             Configuration.SCREEN_SIZE[1])
        self._full_screen = Configuration.FULLSCREEN
        self._sound = Configuration.SOUND
        self._music = Configuration.MUSIC
        self._sound_vol = Configuration.SOUND_VOLUME
        self._music_vol = Configuration.MUSIC_VOLUME
        self._control_type = Configuration.CONTROL_TYPE
        self._key_up = Configuration.KEY_UP
        self._key_down = Configuration.KEY_DOWN
        self._key_left = Configuration.KEY_LEFT
        self._key_right = Configuration.KEY_RIGHT
        self._key_act1 = Configuration.KEY_ACTION_1
        self._key_act2 = Configuration.KEY_ACTION_2
        self._key_start = Configuration.KEY_START
        self._vertical_axis = Configuration.VERTICAL_AXIS
        self._horizontal_axis = Configuration.HORIZONTAL_AXIS
        self._axis_up = Configuration.AXIS_UP
        self._axis_down = Configuration.AXIS_DOWN
        self._axis_left = Configuration.AXIS_LEFT
        self._axis_right = Configuration.AXIS_RIGHT
        self._button_act1 = Configuration.BUTTON_ACTION_1
        self._button_act2 = Configuration.BUTTON_ACTION_2

    def _paths_section_set(self):
        self._parser.set(Configuration.SECTION[0],
                         Configuration.OPT_DATA_PATH,
                         Configuration.DATA_PATH)
        self._parser.set(Configuration.SECTION[0],
                         Configuration.OPT_LOCALE_PATH,
                         Configuration.LOCALE_PATH)

    def _graphics_section_set(self):
        self._parser.set(Configuration.SECTION[1],
                         Configuration.OPT_SCREEN_WIDTH,
                         Configuration.SCREEN_SIZE[0])
        self._parser.set(Configuration.SECTION[1],
                         Configuration.OPT_SCREEN_HEIGHT,
                         Configuration.SCREEN_SIZE[1])
        self._parser.set(Configuration.SECTION[1],
                         Configuration.OPT_FULLSCREEN,
                         Configuration.FULLSCREEN)

    def _sound_section_set(self):
        self._parser.set(Configuration.SECTION[2],
                         Configuration.OPT_SOUND,
                         Configuration.SOUND)
        self._parser.set(Configuration.SECTION[2],
                         Configuration.OPT_MUSIC,
                         Configuration.MUSIC)
        self._parser.set(Configuration.SECTION[2],
                         Configuration.OPT_SOUND_VOL,
                         Configuration.SOUND_VOLUME)
        self._parser.set(Configuration.SECTION[2],
                         Configuration.OPT_MUSIC_VOL,
                         Configuration.MUSIC_VOLUME)

    def _control_section_set(self):
        self._parser.set(Configuration.SECTION[3],
                         Configuration.OPT_CONTROL_TYPE,
                         Configuration.CONTROL_TYPE),
        self._parser.set(Configuration.SECTION[3],
                         Configuration.OPT_KEY_UP,
                         Configuration.KEY_UP),
        self._parser.set(Configuration.SECTION[3],
                         Configuration.OPT_KEY_DOWN,
                         Configuration.KEY_DOWN),
        self._parser.set(Configuration.SECTION[3],
                         Configuration.OPT_KEY_LEFT,
                         Configuration.KEY_LEFT),
        self._parser.set(Configuration.SECTION[3],
                         Configuration.OPT_KEY_RIGHT,
                         Configuration.KEY_RIGHT),
        self._parser.set(Configuration.SECTION[3],
                         Configuration.OPT_KEY_ACTION_1,
                         Configuration.KEY_ACTION_1),
        self._parser.set(Configuration.SECTION[3],
                         Configuration.OPT_KEY_ACTION_2,
                         Configuration.KEY_ACTION_2)
        self._parser.set(Configuration.SECTION[3],
                         Configuration.OPT_KEY_START,
                         Configuration.KEY_START)
        self._parser.set(Configuration.SECTION[3],
                         Configuration.OPT_VERTICAL_AXIS,
                         Configuration.VERTICAL_AXIS),
        self._parser.set(Configuration.SECTION[3],
                         Configuration.OPT_HORIZONTAL_AXIS,
                         Configuration.HORIZONTAL_AXIS),
        self._parser.set(Configuration.SECTION[3],
                         Configuration.OPT_AXIS_UP,
                         Configuration.AXIS_UP),
        self._parser.set(Configuration.SECTION[3],
                         Configuration.OPT_AXIS_DOWN,
                         Configuration.AXIS_DOWN),
        self._parser.set(Configuration.SECTION[3],
                         Configuration.OPT_AXIS_LEFT,
                         Configuration.AXIS_LEFT),
        self._parser.set(Configuration.SECTION[3],
                         Configuration.OPT_AXIS_RIGHT,
                         Configuration.AXIS_RIGHT),
        self._parser.set(Configuration.SECTION[3],
                         Configuration.OPT_BUTTON_ACTION_1,
                         Configuration.BUTTON_ACTION_1),
        self._parser.set(Configuration.SECTION[3],
                         Configuration.OPT_BUTTON_ACTION_2,
                         Configuration.BUTTON_ACTION_2)

    @staticmethod
    def _check_correct_values(option, read_value):

        if option == Configuration.OPT_DATA_PATH:
            file_path = ''.join([read_value, 'data.zip'])
            if not os.path.isfile(file_path):
                raise ConfigurationError(
                    _('Unable to find the data file in the directory pointed at config. file.'))
        elif option == Configuration.OPT_SOUND_VOL:
            if read_value not in list(xrange(Configuration.SOUND_VOLUME + 1)):
                raise ConfigurationError(_('Sound volume must be between 0 (min) and 5 (max).'))
        elif option == Configuration.OPT_MUSIC_VOL:
            if read_value not in list(xrange(Configuration.MUSIC_VOLUME + 1)):
                raise ConfigurationError(_('Music volume must be between 0 (min) and 5 (max).'))
        elif option == Configuration.OPT_CONTROL_TYPE:
            if read_value not in ['keyboard', 'joystick', 'autodetect']:
                raise ConfigurationError(_('Control must be keyboard, joystick or autodetect.'))
        elif option == Configuration.OPT_SCREEN_WIDTH:
            if read_value < 1:
                raise ConfigurationError(_('Screen width must be greater than 1.'))
        elif option == Configuration.OPT_SCREEN_HEIGHT:
            if read_value < 1:
                raise ConfigurationError(_('Screen height must be greater than 1.'))

    '''
    Public methods
    '''

    def save(self):
        with open(Configuration.CFGFILE_NAME, 'wb') as config_file:
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
